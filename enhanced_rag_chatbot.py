# This file contains the enhanced RAG chatbot system.

from shared_functions import * # Import all functions from our shared module
from typing import List, Dict, Any
import json
import sys # For sys.exit()
import os # To access environment variables like OPENAI_API_KEY

# --- OpenAI API Configuration ---
# IMPORTANT: Ensure your OPENAI_API_KEY is set as a Colab Secret.
# Access it via os.environ.get("OPENAI_API_KEY").
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Initialize the OpenAI client
try:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not found. Please set it in Colab Secrets.")
    client_openai = OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    print(f"❌ Error initializing OpenAI client: {e}")
    print("Please ensure your OPENAI_API_KEY is correctly set in Colab Secrets.")
    sys.exit(1)

# Global variable
food_items = []

# --- Helper Functions (will be defined below, before main) ---
# These will include:
# - prepare_context_for_llm
# - generate_llm_rag_response
# - generate_fallback_response
# - generate_llm_comparison
# - generate_simple_comparison
# - show_enhanced_rag_help
# - handle_enhanced_comparison_mode
# - handle_enhanced_rag_query
# - enhanced_rag_food_chatbot
# - main
# This part of the file contains the core logic for the RAG chatbot.

# --- Context Preparation Function ---
def prepare_context_for_llm(query: str, search_results: List[Dict]) -> str:
    """Prepare structured context from search results for LLM"""
    if not search_results:
        return "No relevant food items found in the database."

    context_parts = []
    context_parts.append("Based on the user's query, here are the most relevant food options from our database:")
    context_parts.append("")

    for i, result in enumerate(search_results[:3], 1): # Limit to top 3 for conciseness
        food_context = []
        food_context.append(f"Option {i}: {result['food_name']}")
        food_context.append(f"  - Description: {result['food_description']}")
        food_context.append(f"  - Cuisine: {result['cuisine_type']}")
        food_context.append(f"  - Calories: {result['food_calories_per_serving']} per serving")

        if result.get('food_ingredients'):
            ingredients = result['food_ingredients']
            if isinstance(ingredients, list):
                food_context.append(f"  - Key ingredients: {', '.join(ingredients[:5])}") # Limit ingredients
            else:
                food_context.append(f"  - Key ingredients: {ingredients}")

        if result.get('food_health_benefits'):
            food_context.append(f"  - Health benefits: {result['food_health_benefits']}")

        if result.get('cooking_method'):
            food_context.append(f"  - Cooking method: {result['cooking_method']}")

        if result.get('taste_profile'):
            food_context.append(f"  - Taste profile: {result['taste_profile']}")

        food_context.append(f"  - Similarity score: {result['similarity_score']*100:.1f}%")
        food_context.append("")

        context_parts.extend(food_context)

    return "\n".join(context_parts)

# --- Fallback Response Function ---
def generate_fallback_response(query: str, search_results: List[Dict]) -> str:
    """Generate fallback response when LLM fails or provides insufficient response"""
    if not search_results:
        return "I couldn't find any food items matching your request. Try describing what you're in the mood for with different words!"

    top_result = search_results[0]
    response_parts = []

    response_parts.append(f"Based on your request for '{query}', I'd recommend {top_result['food_name']}.")
    response_parts.append(f"It's a {top_result['cuisine_type']} dish with {top_result['food_calories_per_serving']} calories per serving.")

    if len(search_results) > 1:
        second_choice = search_results[1]
        response_parts.append(f"Another great option would be {second_choice['food_name']}.")

    return " ".join(response_parts)

# --- LLM Response Generation Function ---
def generate_llm_rag_response(query: str, search_results: List[Dict]) -> str:
    """Generate response using OpenAI with retrieved context"""
    try:
        # Prepare context from search results
        context = prepare_context_for_llm(query, search_results)

        # Build the prompt for the LLM
        prompt = f'''You are a helpful food recommendation assistant. A user is asking for food recommendations, and I've retrieved relevant options from a food database.

User Query: "{query}"

Retrieved Food Information:
{context}

Please provide a helpful, short response that:
1. Acknowledges the user's request
2. Recommends 2-3 specific food items from the retrieved options
3. Explains why these recommendations match their request
4. Includes relevant details like cuisine type, calories, or health benefits
5. Uses a friendly, conversational tone
6. Keeps the response concise but informative

Response:'''
        # Use the global client_openai object initialized in the first part of the file
        completion = client_openai.chat.completions.create(
            model="gpt-3.5-turbo", # Or "gpt-4" if you have access and prefer
            messages=[
                {"role": "system", "content": "You are a helpful food recommendation assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.7 # Adjust for creativity vs. consistency
        )

        generated_response = completion.choices[0].message.content
        response_text = generated_response.strip()

        # If response is too short, provide a fallback
        if len(response_text) < 50:
            return generate_fallback_response(query, search_results)

        return response_text

    except Exception as e:
        print(f"❌ LLM Error during RAG response generation: {e}")
        return generate_fallback_response(query, search_results)

# --- Simple Comparison Fallback Function ---
def generate_simple_comparison(query1: str, query2: str, results1: List[Dict], results2: List[Dict]) -> str:
    """Simple comparison fallback when LLM fails for comparison"""
    if not results1 and not results2:
        return "No results found for either query."
    if not results1:
        return f"Found results for '{query2}' but none for '{query1}'."
    if not results2:
        return f"Found results for '{query1}' but none for '{query2}'."

    rec1 = results1[0]['food_name'] if results1 else "no specific recommendation"
    rec2 = results2[0]['food_name'] if results2 else "no specific recommendation"

    return f"For '{query1}', I recommend {rec1}. For '{query2}', {rec2} would be perfect."

# --- LLM Comparison Generation Function ---
def generate_llm_comparison(query1: str, query2: str, results1: List[Dict], results2: List[Dict]) -> str:
    """Generate AI-powered comparison between two queries using OpenAI"""
    try:
        context1 = prepare_context_for_llm(query1, results1[:3])
        context2 = prepare_context_for_llm(query2, results2[:3])

        comparison_prompt = f'''You are analyzing and comparing two different food preference queries. Please provide a thoughtful comparison.

Query 1: "{query1}"
Top Results for Query 1:
{context1}

Query 2: "{query2}"
Top Results for Query 2:
{context2}

Please provide a short comparison that:
1. Highlights the key differences between these two food preferences
2. Notes any similarities or overlaps
3. Explains which query might be better for different situations
4. Recommends the best option from each query
5. Keeps the analysis concise but insightful

Comparison:'''

        completion = client_openai.chat.completions.create(
            model="gpt-3.5-turbo", # Or "gpt-4"
            messages=[
                {"role": "system", "content": "You are a helpful food recommendation assistant for comparing queries."},
                {"role": "user", "content": comparison_prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ LLM Error during comparison generation: {e}")
        return generate_simple_comparison(query1, query2, results1, results2)

# --- Enhanced Query Handler ---
def handle_enhanced_rag_query(collection, query: str, conversation_history: List[str]):
    """Handle user query with enhanced RAG approach using OpenAI"""
    print(f"\n🔍 Searching vector database for: '{query}'...")

    # Perform similarity search with more results for better context
    search_results = perform_similarity_search(collection, query, 3) # Get top 3 results

    if not search_results:
        print("🤖 Bot: I couldn't find any food items matching your request.")
        print("      Try describing what you're in the mood for with different words!")
        return

    print(f"✅ Found {len(search_results)} relevant matches")
    print("🧠 Generating AI-powered response...")

    # Generate enhanced RAG response using OpenAI
    ai_response = generate_llm_rag_response(query, search_results)

    print(f"\n🤖 Bot: {ai_response}")

    # Show detailed results for reference
    print(f"\n📊 Search Results Details:")
    print("-" * 45)
    for i, result in enumerate(search_results[:3], 1): # Display top 3 for details
        print(f"{i}. 🍽️  {result['food_name']}")
        print(f"   📍 {result['cuisine_type']} | 🔥 {result['food_calories_per_serving']} cal | 📈 {result['similarity_score']*100:.1f}% match")
        if i < 3:
            print()

# --- Enhanced Comparison Mode Handler ---
def handle_enhanced_comparison_mode(collection):
    """Enhanced comparison between two food queries using LLM"""
    print("\n🔄 ENHANCED COMPARISON MODE")
    print("   Powered by AI Analysis")
    print("-" * 35)

    query1 = input("Enter first food query: ").strip()
    query2 = input("Enter second food query: ").strip()

    if not query1 or not query2:
        print("❌ Please enter both queries for comparison")
        return

    print(f"\n🔍 Analyzing '{query1}' vs '{query2}' with AI...")

    # Get results for both queries
    results1 = perform_similarity_search(collection, query1, 3)
    results2 = perform_similarity_search(collection, query2, 3)

    # Generate AI-powered comparison
    comparison_response = generate_llm_comparison(query1, query2, results1, results2)

    print(f"\n🤖 AI Analysis: {comparison_response}")

    # Show side-by-side results
    print(f"\n📊 DETAILED COMPARISON")
    print("=" * 60)
    print(f"{'Query 1: ' + query1[:20] + '...' if len(query1) > 20 else 'Query 1: ' + query1:<30} | {'Query 2: ' + query2[:20] + '...' if len(query2) > 20 else 'Query 2: ' + query2}")
    print("-" * 60)

    max_results = max(len(results1), len(results2))
    for i in range(min(max_results, 3)): # Display top 3 for comparison
        left = f"{results1[i]['food_name']} ({results1[i]['similarity_score']*100:.0f}%)" if i < len(results1) else "---"
        right = f"{results2[i]['food_name']} ({results2[i]['similarity_score']*100:.0f}%)" if i < len(results2) else "---"
        print(f"{left[:30]:<30} | {right[:30]}")

# --- Help Function for RAG Chatbot ---
def show_enhanced_rag_help():
    """Display help information for enhanced RAG chatbot"""
    print("\n📖 ENHANCED RAG CHATBOT HELP")
    print("=" * 45)
    print("🧠 This chatbot uses OpenAI's models to understand your")
    print("   food preferences and provide intelligent recommendations.")
    print("\nHow to get the best recommendations:")
    print("  • Be specific: 'healthy Italian pasta under 350 calories'")
    print("  • Mention preferences: 'spicy comfort food for cold weather'")
    print("  • Include context: 'light breakfast for busy morning'")
    print("  • Ask about benefits: 'protein-rich foods for workout recovery'")
    print("\nSpecial features:")
    print("  • 🔍 Vector similarity search finds relevant foods")
    print("  • 🧠 AI analysis provides contextual explanations")
    print("  • 📊 Detailed nutritional and cuisine information")
    print("  • 🔄 Smart comparison between different preferences")
    print("\nCommands:")
    print("  • 'compare' - AI-powered comparison of two queries")
    print("  • 'help' - Show this help menu")
    print("  • 'quit' - Exit the chatbot")
    print("\nTips for better results:")
    print("  • Use natural language - talk like you would to a friend")
    ("  • Mention dietary restrictions or preferences")
    print("  • Include meal timing (breakfast, lunch, dinner)")
    print("  • Specify if you want healthy, comfort, or indulgent options")

# --- Main Chatbot Interface ---
def enhanced_rag_food_chatbot(collection):
    """Enhanced RAG-powered conversational food chatbot with OpenAI"""
    print("\n" + "="*70)
    print("🤖 ENHANCED RAG FOOD RECOMMENDATION CHATBOT")
    print("   Powered by OpenAI Models")
    print("="*70)
    print("💬 Ask me about food recommendations using natural language!")
    print("\nExample queries:")
    print("  • 'I want something spicy and healthy for dinner'")
    print("  • 'What Italian dishes do you recommend under 400 calories?'")
    print("  • 'I'm craving comfort food for a cold evening'")
    print("  • 'Suggest some protein-rich breakfast options'")
    print("\nCommands:")
    print("  • 'help' - Show detailed help menu")
    print("  • 'compare' - Compare recommendations for two different queries")
    print("  • 'quit' - Exit the chatbot")
    print("-" * 70)

    conversation_history = []

    while True:
        try:
            user_input = input("\n👤 You: ").strip()

            if not user_input:
                print("🤖 Bot: Please tell me what kind of food you're looking for!")
                continue

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n🤖 Bot: Thank you for using the Enhanced RAG Food Chatbot!")
                print("      Hope you found some delicious recommendations! 👋")
                break

            elif user_input.lower() in ['help', 'h']:
                show_enhanced_rag_help()

            elif user_input.lower() in ['compare']:
                handle_enhanced_comparison_mode(collection)

            else:
                handle_enhanced_rag_query(collection, user_input, conversation_history)
                conversation_history.append(user_input)

                # Keep conversation history manageable
                if len(conversation_history) > 5:
                    conversation_history = conversation_history[-3:]

        except KeyboardInterrupt:
            print("\n\n🤖 Bot: Goodbye! Hope you find something delicious! 👋")
            break
        except Exception as e:
            print(f"❌ Bot: Sorry, I encountered an error: {e}")


# --- Main Function and Entry Point ---
def main():
    """Main function for enhanced RAG chatbot system"""
    try:
        print("🤖 Enhanced RAG-Powered Food Recommendation Chatbot")
        print("   Powered by OpenAI & ChromaDB")
        print("=" * 55)

        # Load food data
        global food_items
        food_data_file = './FoodDataSet.json'
        food_items = load_food_data(food_data_file)
        if not food_items:
            print("❌ Failed to load food data. Exiting.")
            sys.exit(1)
        print(f"✅ Loaded {len(food_items)} food items")

        # Create collection for RAG system
        client_chromadb = chromadb.Client() # Initialize ChromaDB client here
        print("✅ ChromaDB client initialized for RAG system.")

        collection = create_similarity_search_collection(
            client_chromadb, # Pass the ChromaDB client
            "enhanced_rag_food_chatbot",
            {'description': 'Enhanced RAG chatbot with OpenAI integration'}
        )
        populate_similarity_collection(collection, food_items)
        print("✅ Vector database ready")

        # Start enhanced RAG chatbot
        enhanced_rag_food_chatbot(collection)

    except Exception as error:
        print(f"❌ Error initializing RAG system: {error}")
        sys.exit(1)

if __name__ == "__main__":
    main()
