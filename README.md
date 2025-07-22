# 🍽️ Intelligent Food Recommendation System

This project implements an **intelligent food recommendation system** that leverages a **vector database (ChromaDB)** for efficient semantic search and **Large Language Models (LLMs)**—specifically from **OpenAI**—for natural language understanding and conversational responses.

The system supports a full range of food discovery—from basic keyword search to advanced, AI-powered, contextual recommendations.

---

## 🚀 Features

* **🔍 Semantic Food Search** Uses `sentence-transformer` embeddings to find conceptually similar food items, beyond simple keyword matches.

* **🧠 RAG Chatbot (Retrieval-Augmented Generation)** Combines ChromaDB with OpenAI's LLM to deliver intelligent, contextual food suggestions through natural language.

* **⚙️ Advanced Filtering** Search by cuisine type, calorie count, or other metadata.

* **💬 Interactive CLI Interfaces** Easy-to-use command-line tools for trying out each recommendation method.

* **📊 System Comparison Tool** A benchmarking script that compares all three systems based on output and performance.

---

## 🗂️ Project Structure

The project is organized into modular Python files for clarity and reusability:

* `FoodDataSet.json`: The raw dataset containing detailed information about various food items.
* `shared_functions.py`: Contains all the core, reusable backend logic, including data loading, ChromaDB collection creation, population, and various similarity search functions. This acts as the project's central library.
* `interactive_search.py`: Implements a basic command-line interface for quick, semantic food discovery.
* `advanced_search.py`: Provides a command-line interface with advanced filtering capabilities (e.g., by cuisine, calories) on top of semantic search.
* `enhanced_rag_chatbot.py`: The main script for the RAG-powered conversational chatbot, integrating OpenAI's LLM with the vector database.
* `system_comparison.py`: A utility script to run predefined tests and compare the performance and output of all three recommendation systems.
* `requirements.txt`: Lists all Python dependencies required to run the project, ensuring easy environment setup.
* `.gitignore`: Specifies files and directories that Git should ignore (e.g., temporary files, cache).

---

## 🚀 Getting Started

Follow these steps to set up and run the Food Recommendation System on your local machine.

### 📋 Prerequisites

* **Python 3.8+**
* **Git** (for cloning the repository)
* An **OpenAI API Key** (required for the RAG Chatbot)

### ⬇️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/AliAbdallah21/Food-Recommendation-System.git](https://github.com/AliAbdallah21/Food-Recommendation-System.git)
    cd Food-Recommendation-System
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 🔑 OpenAI API Key Setup

The `enhanced_rag_chatbot.py` script requires an OpenAI API Key. You must set this as an environment variable before running the RAG chatbot.

* **For Linux/macOS (in your terminal):**
    ```bash
    export OPENAI_API_KEY="your_openai_api_key_here"
    ```
* **For Windows (in Command Prompt):**
    ```cmd
    set OPENAI_API_KEY="your_openai_api_key_here"
    ```
* **For Windows (in PowerShell):**
    ```powershell
    $env:OPENAI_API_KEY="your_openai_api_key_here"
    ```
    Replace `"your_openai_api_key_here"` with your actual API key.

---

## ▶️ How to Run Each System

Navigate to the project's root directory in your terminal and execute the following commands:

1.  **Interactive Search System:**
    ```bash
    python interactive_search.py
    ```
    * **Try:** "healthy salad"
    * **Notice:** Simple, fast search with immediate results.
    * **Use case:** Quick food discovery with basic similarity.

2.  **Advanced Search System:**
    ```bash
    python advanced_search.py
    ```
    * **Try Option 2:** cuisine search for "pasta" in "Italian"
    * **Try Option 3:** calorie search for "healthy" under 300 calories
    * **Notice:** Powerful filtering capabilities for specific requirements.
    * **Use case:** Detailed search with multiple constraints.

3.  **RAG Chatbot System:**
    *(Ensure your `OPENAI_API_KEY` environment variable is set as described above!)*
    ```bash
    python enhanced_rag_chatbot.py
    ```
    * **Try:** "I want something spicy for dinner tonight"
    * **Notice:** Contextual, conversational responses with explanations.
    * **Use case:** Natural language interaction with intelligent recommendations.

4.  **System Comparison Script:**
    ```bash
    python system_comparison.py
    ```
    * **Notice:** This script will automatically run a predefined query through each system and display a comparative summary of their outputs and approximate performance.

---

## 💡 Understanding the Systems

### 💻 Command Line Interface (CLI)

All systems in this project utilize a **Command Line Interface (CLI)**. This means you interact with the program by typing text commands into your terminal and receiving text-based output. There are no graphical windows, buttons, or visual elements to click. This approach is excellent for demonstrating core logic and backend functionality.

# 🍽️ Intelligent Food Recommendation System

This project implements an **intelligent food recommendation system** that leverages a **vector database (ChromaDB)** for efficient semantic search and **Large Language Models (LLMs)**—specifically from **OpenAI**—for natural language understanding and conversational responses.

The system supports a full range of food discovery—from basic keyword search to advanced, AI-powered, contextual recommendations.

---

## 🚀 Features

* **🔍 Semantic Food Search** Uses `sentence-transformer` embeddings to find conceptually similar food items, beyond simple keyword matches.

* **🧠 RAG Chatbot (Retrieval-Augmented Generation)** Combines ChromaDB with OpenAI's LLM to deliver intelligent, contextual food suggestions through natural language.

* **⚙️ Advanced Filtering** Search by cuisine type, calorie count, or other metadata.

* **💬 Interactive CLI Interfaces** Easy-to-use command-line tools for trying out each recommendation method.

* **📊 System Comparison Tool** A benchmarking script that compares all three systems based on output and performance.

---

## 🗂️ Project Structure

The project is organized into modular Python files for clarity and reusability:

* `FoodDataSet.json`: The raw dataset containing detailed information about various food items.
* `shared_functions.py`: Contains all the core, reusable backend logic, including data loading, ChromaDB collection creation, population, and various similarity search functions. This acts as the project's central library.
* `interactive_search.py`: Implements a basic command-line interface for quick, semantic food discovery.
* `advanced_search.py`: Provides a command-line interface with advanced filtering capabilities (e.g., by cuisine, calories) on top of semantic search.
* `enhanced_rag_chatbot.py`: The main script for the RAG-powered conversational chatbot, integrating OpenAI's LLM with the vector database.
* `system_comparison.py`: A utility script to run predefined tests and compare the performance and output of all three recommendation systems.
* `requirements.txt`: Lists all Python dependencies required to run the project, ensuring easy environment setup.
* `.gitignore`: Specifies files and directories that Git should ignore (e.g., temporary files, cache).

---

## 🚀 Getting Started

Follow these steps to set up and run the Food Recommendation System on your local machine.

### 📋 Prerequisites

* **Python 3.8+**
* **Git** (for cloning the repository)
* An **OpenAI API Key** (required for the RAG Chatbot)

### ⬇️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/AliAbdallah21/Food-Recommendation-System.git](https://github.com/AliAbdallah21/Food-Recommendation-System.git)
    cd Food-Recommendation-System
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 🔑 OpenAI API Key Setup

The `enhanced_rag_chatbot.py` script requires an OpenAI API Key. You must set this as an environment variable before running the RAG chatbot.

* **For Linux/macOS (in your terminal):**
    ```bash
    export OPENAI_API_KEY="your_openai_api_key_here"
    ```
* **For Windows (in Command Prompt):**
    ```cmd
    set OPENAI_API_KEY="your_openai_api_key_here"
    ```
* **For Windows (in PowerShell):**
    ```powershell
    $env:OPENAI_API_KEY="your_openai_api_key_here"
    ```
    Replace `"your_openai_api_key_here"` with your actual API key.

---

## ▶️ How to Run Each System

Navigate to the project's root directory in your terminal and execute the following commands:

1.  **Interactive Search System:**
    ```bash
    python interactive_search.py
    ```
    * **Try:** "healthy salad"
    * **Notice:** Simple, fast search with immediate results.
    * **Use case:** Quick food discovery with basic similarity.

2.  **Advanced Search System:**
    ```bash
    python advanced_search.py
    ```
    * **Try Option 2:** cuisine search for "pasta" in "Italian"
    * **Try Option 3:** calorie search for "healthy" under 300 calories
    * **Notice:** Powerful filtering capabilities for specific requirements.
    * **Use case:** Detailed search with multiple constraints.

3.  **RAG Chatbot System:**
    *(Ensure your `OPENAI_API_KEY` environment variable is set as described above!)*
    ```bash
    python enhanced_rag_chatbot.py
    ```
    * **Try:** "I want something spicy for dinner tonight"
    * **Notice:** Contextual, conversational responses with explanations.
    * **Use case:** Natural language interaction with intelligent recommendations.

4.  **System Comparison Script:**
    ```bash
    python system_comparison.py
    ```
    * **Notice:** This script will automatically run a predefined query through each system and display a comparative summary of their outputs and approximate performance.

---

## 💡 Understanding the Systems

### 💻 Command Line Interface (CLI)

All systems in this project utilize a **Command Line Interface (CLI)**. This means you interact with the program by typing text commands into your terminal and receiving text-based output. There are no graphical windows, buttons, or visual elements to click. This approach is excellent for demonstrating core logic and backend functionality.

### 🧠 Retrieval-Augmented Generation (RAG) Explained

The RAG Chatbot is a prime example of a RAG architecture, which involves three key steps:

1.  **Retrieval:** When you ask a question (e.g., "Suggest a healthy Italian meal"), the system first performs a semantic search on the ChromaDB vector database to find the most relevant food items.
2.  **Augmentation / Context Building:** The raw information from these retrieved food items (descriptions, ingredients, calories, etc.) is then formatted into a concise, structured "context" that is easy for an LLM to understand.
3.  **Generation:** This structured context, along with your original query, is then sent to OpenAI's LLM. The LLM uses this combined input to generate a natural, conversational, and factually grounded response. This prevents the LLM from "hallucinating" information and ensures its recommendations are based on your specific food database.

---

## 📞 Contact

For questions or feedback, feel free to reach out:

* **Email:** [Aliabdalla2110@gmail.com](mailto:Aliabdalla2110@gmail.com)
* **GitHub:** [AliAbdallah21](https://github.com/AliAbdallah21)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. *(You'll need to create a separate `LICENSE` file in your repository with the MIT License text if you choose this.)*
