# This file contains the advanced search system with filtering capabilities.

from shared_functions import * # Import all functions from our shared module
import sys # Needed for sys.exit() for clean exits
import json # Ensure json is available for loading food data

# --- Helper Functions (defined before they are called) ---

def display_search_results(results, title, show_details=True):
    """Display search results in a formatted way"""
    print(f"\n📋 {title}")
    print("=" * 50)

    if not results:
        print("❌ No matching results found")
        print("💡 Try adjusting your search terms or filters")
        return

    for i, result in enumerate(results, 1):
        score_percentage = result['similarity_score'] * 100

        if show_details:
            print(f"\n{i}. 🍽️  {result['food_name']}")
            print(f"   📊 Similarity Score: {score_percentage:.1f}%")
            print(f"   🏷️  Cuisine: {result['cuisine_type']}")
            print(f"   🔥 Calories: {result['food_calories_per_serving']}")
            print(f"   📝 Description: {result['food_description']}")
        else:
            print(f"   {i}. {result['food_name']} ({score_percentage:.1f}% match)")

    print("=" * 50)

def perform_basic_search(collection):
    """Perform basic similarity search without filters"""
    print("\n🔍 BASIC SIMILARITY SEARCH")
    print("-" * 30)

    query = input("Enter search query: ").strip()
    if not query:
        print("❌ Please enter a search term")
        return

    print(f"\n🔍 Searching for '{query}'...")
    results = perform_similarity_search(collection, query, 5)

    display_search_results(results, "Basic Search Results")

def perform_cuisine_filtered_search(collection):
    """Perform cuisine-filtered similarity search"""
    print("\n🍽️ CUISINE-FILTERED SEARCH")
    print("-" * 30)

    # Show available cuisines from our dataset
    cuisines = ["Italian", "Thai", "Mexican", "Indian", "Japanese", "French",
                "Mediterranean", "American", "Health Food", "Dessert", "International"] # Added International as it appears in data
    print("Available cuisines:")
    for i, cuisine in enumerate(cuisines, 1):
        print(f"  {i}. {cuisine}")

    query = input("\nEnter search query: ").strip()
    cuisine_choice = input("Enter cuisine number (or cuisine name): ").strip()

    if not query:
        print("❌ Please enter a search term")
        return

    # Handle cuisine selection - accept both number and text input
    cuisine_filter = None
    if cuisine_choice.isdigit():
        idx = int(cuisine_choice) - 1
        if 0 <= idx < len(cuisines):
            cuisine_filter = cuisines[idx]
    else:
        # Simple capitalization for matching, or direct use
        cuisine_filter = cuisine_choice.title() if cuisine_choice else None

    if not cuisine_filter:
        print("❌ Invalid cuisine selection or empty input.")
        return

    print(f"\n🔍 Searching for '{query}' in {cuisine_filter} cuisine...")
    results = perform_filtered_similarity_search(
        collection, query, cuisine_filter=cuisine_filter, n_results=5
    )

    display_search_results(results, f"Cuisine-Filtered Results ({cuisine_filter})")

def perform_calorie_filtered_search(collection):
    """Perform calorie-filtered similarity search"""
    print("\n🔥 CALORIE-FILTERED SEARCH")
    print("-" * 30)

    query = input("Enter search query: ").strip()
    max_calories_input = input("Enter maximum calories (or press Enter for no limit): ").strip()

    if not query:
        print("❌ Please enter a search term")
        return

    max_calories = None
    if max_calories_input.isdigit():
        max_calories = int(max_calories_input)
    elif max_calories_input: # If not digit but not empty, it's invalid
        print("❌ Invalid calorie input. Please enter a number or leave blank.")
        return

    print(f"\n🔍 Searching for '{query}'" +
          (f" with max {max_calories} calories..." if max_calories else "..."))

    results = perform_filtered_similarity_search(
        collection, query, max_calories=max_calories, n_results=5
    )

    calorie_text = f"under {max_calories} calories" if max_calories else "any calories"
    display_search_results(results, f"Calorie-Filtered Results ({calorie_text})")

def perform_combined_filtered_search(collection):
    """Perform search with multiple filters combined"""
    print("\n🎯 COMBINED FILTERS SEARCH")
    print("-" * 30)

    query = input("Enter search query: ").strip()
    cuisine = input("Enter cuisine type (optional): ").strip()
    max_calories_input = input("Enter maximum calories (optional): ").strip()

    if not query:
        print("❌ Please enter a search term")
        return

    cuisine_filter = cuisine.title() if cuisine else None # Capitalize for consistency
    max_calories = int(max_calories_input) if max_calories_input.isdigit() else None

    # Build description of applied filters
    filter_description = []
    if cuisine_filter:
        filter_description.append(f"cuisine: {cuisine_filter}")
    if max_calories is not None: # Check explicitly for None
        filter_description.append(f"max calories: {max_calories}")

    filter_text = ", ".join(filter_description) if filter_description else "no filters"

    print(f"\n🔍 Searching for '{query}' with {filter_text}...")

    results = perform_filtered_similarity_search(
        collection, query,
        cuisine_filter=cuisine_filter,
        max_calories=max_calories,
        n_results=5
    )

    display_search_results(results, f"Combined Filtered Results ({filter_text})")

def run_search_demonstrations(collection):
    """Run predetermined demonstrations of different search types"""
    print("\n📊 SEARCH DEMONSTRATIONS")
    print("=" * 40)

    demonstrations = [
        {
            "title": "Italian Cuisine Search",
            "query": "creamy pasta",
            "cuisine_filter": "Italian",
            "max_calories": None
        },
        {
            "title": "Low-Calorie Healthy Options",
            "query": "healthy meal",
            "cuisine_filter": None,
            "max_calories": 300
        },
        {
            "title": "Asian Light Dishes",
            "query": "light fresh meal",
            "cuisine_filter": "Japanese",
            "max_calories": 250
        }
    ]

    for i, demo in enumerate(demonstrations, 1):
        print(f"\n{i}. {demo['title']}")
        print(f"   Query: '{demo['query']}'")

        filters = []
        if demo['cuisine_filter']:
            filters.append(f"Cuisine: {demo['cuisine_filter']}")
        if demo['max_calories'] is not None: # Check explicitly for None
            filters.append(f"Max Calories: {demo['max_calories']}")

        if filters:
            print(f"   Filters: {', '.join(filters)}")

        results = perform_filtered_similarity_search(
            collection,
            demo['query'],
            cuisine_filter=demo['cuisine_filter'],
            max_calories=demo['max_calories'],
            n_results=3
        )

        display_search_results(results, demo['title'], show_details=False)

        input("\n⏸️  Press Enter to continue to next demonstration...")

def show_advanced_help():
    """Display help information for advanced search"""
    print("\n📖 ADVANCED SEARCH HELP")
    print("=" * 40)
    print("Search Types:")
    print("  1. Basic Search - Standard similarity search")
    print("  2. Cuisine Filter - Search within specific cuisine types")
    print("  3. Calorie Filter - Search for foods under calorie limits")
    print("  4. Combined Filters - Use multiple filters together")
    print("  5. Demonstrations - See predefined search examples")
    print("\nTips:")
    print("  • Use descriptive terms: 'creamy', 'spicy', 'light'")
    print("  • Combine ingredients: 'chicken vegetables'")
    print("  • Try cuisine names: 'Italian', 'Thai', 'Mexican'")
    print("  • Filter by calories for dietary goals")


def interactive_advanced_search(collection):
    """Interactive advanced search with filtering options"""
    print("\n" + "="*50)
    print("🔧 ADVANCED SEARCH WITH FILTERS")
    print("="*50)
    print("Search Options:")
    print("  1. Basic similarity search")
    print("  2. Cuisine-filtered search")
    print("  3. Calorie-filtered search")
    print("  4. Combined filters search")
    print("  5. Demonstration mode")
    print("  6. Help")
    print("  7. Exit")
    print("-" * 50)

    while True:
        try:
            choice = input("\n📋 Select option (1-7): ").strip()

            if choice == '1':
                perform_basic_search(collection)
            elif choice == '2':
                perform_cuisine_filtered_search(collection)
            elif choice == '3':
                perform_calorie_filtered_search(collection)
            elif choice == '4':
                perform_combined_filtered_search(collection)
            elif choice == '5':
                run_search_demonstrations(collection)
            elif choice == '6':
                show_advanced_help()
            elif choice == '7':
                print("👋 Exiting Advanced Search System. Goodbye!")
                break
            else:
                print("❌ Invalid option. Please select 1-7.")

        except KeyboardInterrupt:
            print("\n\n👋 System interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


# --- Main Function and Entry Point ---

def main():
    """Main function for advanced search demonstrations"""
    try:
        print("🔬 Advanced Food Search System")
        print("=" * 50)
        print("Loading food database with advanced filtering capabilities...")

        # Load food data from JSON file
        food_data_file = './FoodDataSet.json'
        food_items = load_food_data(food_data_file)
        if not food_items:
            print("❌ Failed to load food data. Exiting.")
            sys.exit(1)

        print(f"✅ Loaded {len(food_items)} food items successfully")

        # Initialize ChromaDB client.
        client = chromadb.Client() # Using the simpler client()
        print("✅ ChromaDB client initialized for advanced search.")

        # Create collection specifically for advanced search operations
        collection = create_similarity_search_collection(
            client, # Pass the client instance
            "advanced_food_search",
            {'description': 'A collection for advanced search demos'}
        )
        print(f"✅ Collection '{collection.name}' created or retrieved.")

        populate_similarity_collection(collection, food_items)
        print(f"✅ Populated collection with {len(food_items)} food items.")

        # Start the interactive advanced search interface
        interactive_advanced_search(collection)

    except Exception as error:
        print(f"❌ Error initializing advanced search system: {error}")
        sys.exit(1) # Exit with an error code

if __name__ == "__main__":
    main()
