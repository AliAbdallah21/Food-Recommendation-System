# This script compares the capabilities of the three food search systems.

from shared_functions import *
import time
import sys # For sys.exit()

# Note: For the RAG Chatbot part of this comparison, we'll simulate the LLM
# response generation as we cannot directly call the OpenAI API within this
# comparison script without re-initializing the client and passing API keys,
# which complicates the comparison setup.
# In a real-world scenario, you would integrate the LLM call directly.

def main():
    """Compare all three search systems with the same query"""
    print("🔬 FOOD SEARCH SYSTEMS COMPARISON")
    print("=" * 50)

    # Initialize ChromaDB client once for all collections
    try:
        client_chromadb = chromadb.Client()
        print("✅ ChromaDB client initialized for comparison.")
    except Exception as e:
        print(f"❌ Error initializing ChromaDB client: {e}")
        sys.exit(1)

    # Load data once for all systems
    food_data_file = './FoodDataSet.json'
    food_items = load_food_data(food_data_file)
    if not food_items:
        print("❌ Failed to load food data. Exiting comparison.")
        sys.exit(1)
    print(f"✅ Loaded {len(food_items)} food items for comparison.")

    # Create and populate collections for each system
    # Using distinct names to avoid conflicts if they persist in memory
    interactive_collection = create_similarity_search_collection(client_chromadb, "comparison_interactive")
    advanced_collection = create_similarity_search_collection(client_chromadb, "comparison_advanced")
    rag_collection = create_similarity_search_collection(client_chromadb, "comparison_rag")

    populate_similarity_collection(interactive_collection, food_items)
    populate_similarity_collection(advanced_collection, food_items)
    populate_similarity_collection(rag_collection, food_items)
    print("✅ All comparison collections populated.")

    # Test query
    test_query = "chocolate dessert"

    print(f"\n🔍 Testing query: '{test_query}'")
    print("=" * 50)

    # System 1: Interactive Search Style
    print("\n1️⃣ INTERACTIVE SEARCH APPROACH:")
    print("-" * 30)
    start_time = time.time()
    interactive_results = perform_similarity_search(interactive_collection, test_query, 3)
    interactive_time = time.time() - start_time

    for i, result in enumerate(interactive_results, 1):
        print(f"{i}. {result['food_name']} ({result['similarity_score']*100:.1f}% match)")
        print(f"   {result['food_description']}")
    print(f"⏱️ Response time: {interactive_time:.3f} seconds")

    # System 2: Advanced Search Style
    print("\n2️⃣ ADVANCED SEARCH APPROACH:")
    print("-" * 30)
    start_time = time.time()

    # Show basic search
    basic_results = perform_similarity_search(advanced_collection, test_query, 3)
    print("📋 Basic results:")
    for i, result in enumerate(basic_results, 1):
        print(f"   {i}. {result['food_name']} - {result['cuisine_type']} ({result['food_calories_per_serving']} cal)")

    # Show filtered search (example: filter for a specific cuisine)
    # Note: The original prompt used "spicy" which isn't a cuisine.
    # I'll use "Indian" as an example cuisine that might have spicy dishes.
    spicy_results = perform_filtered_similarity_search(
        advanced_collection, test_query, cuisine_filter="Indian", n_results=2
    )
    print("🌶️ Filtered for Indian cuisine:")
    for i, result in enumerate(spicy_results, 1):
        print(f"   {i}. {result['food_name']} ({result['similarity_score']*100:.1f}% match)")

    advanced_time = time.time() - start_time
    print(f"⏱️ Response time: {advanced_time:.3f} seconds")

    # System 3: RAG Chatbot Style (Simulated LLM response for comparison)
    print("\n3️⃣ RAG CHATBOT APPROACH:")
    print("-" * 30)
    start_time = time.time()

    rag_results = perform_similarity_search(rag_collection, test_query, 3)

    # Generate a *simulated* RAG-style response for comparison purposes.
    # In a real RAG system, this would be an actual LLM call using the context.
    rag_response = f"Perfect! I found some excellent chocolate dessert options for you. "
    if rag_results:
        rag_response += f"I'd highly recommend the {rag_results[0]['food_name']} - it's a {rag_results[0]['similarity_score']*100:.0f}% match "
        rag_response += f"and offers that sweet, rich flavor you're craving. "
        if rag_results[0]['cuisine_type']:
            rag_response += f"This {rag_results[0]['cuisine_type']} dessert is perfect for chocolate lovers! "
        rag_response += f"At {rag_results[0]['food_calories_per_serving']} calories, it's a delightful treat. "
        if len(rag_results) > 1:
            rag_response += f"You might also enjoy {rag_results[1]['food_name']} as an alternative."
    else:
        rag_response += "Unfortunately, I couldn't find specific chocolate desserts in my database for a detailed recommendation."

    print(f"🤖 Bot: {rag_response}")

    rag_time = time.time() - start_time
    print(f"⏱️ Response time: {rag_time:.3f} seconds")

    # Comparison Summary
    print("\n📊 SYSTEM COMPARISON SUMMARY:")
    print("=" * 50)
    print("Interactive Search:")
    print("  ✅ Fast and simple")
    print("  ✅ Direct results display")
    print("  ❌ Limited context")

    print("\nAdvanced Search:")
    print("  ✅ Powerful filtering options")
    print("  ✅ Multiple search modes")
    print("  ✅ Precise control")
    print("  ❌ Requires user to know filter options")

    print("\nRAG Chatbot:")
    print("  ✅ Natural language interaction")
    print("  ✅ Contextual explanations")
    print("  ✅ Conversational experience")
    print("  ❌ More complex implementation (and potentially slower due to LLM calls)")

    print(f"\n⏱️ Performance Comparison (approximate):")
    print(f"  Interactive: {interactive_time:.3f}s")
    print(f"  Advanced: {advanced_time:.3f}s")
    print(f"  RAG Chatbot: {rag_time:.3f}s (Note: This is simulated, actual LLM calls add latency)")

if __name__ == "__main__":
    main()
