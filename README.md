Smart Context-Aware Study Companion (RAG-based NLP Model)A sophisticated Natural Language Processing (NLP) tool designed to provide context-aware assistance by analyzing user browser history and chat interactions. This project implements a Retrieval-Augmented Generation (RAG) architecture to deliver highly relevant responses based on the user's recent academic or professional activities.🚀 FeaturesContextual Awareness: Scrapes and analyzes local browser history to understand the user's current focus.RAG Implementation: Uses a vector-based approach to retrieve relevant information before generating responses.Topic Modeling: Segments chat history and browsing data into distinct topics for better organizational understanding.Interactive UI: Built with Streamlit for a seamless, user-friendly experience.Automated Insights: Automatically summarizes key learning points from the user's daily activity.🛠️ Tech StackLanguage: Python 3.10+NLP Libraries: Spacy, BERTopic, TransformersFrontend: StreamlitDatabase: SQLite (for local history caching)AI Models: Integration with LLMs (Groq/OpenAI) for generation📁 Project Structure├── app.py              # Main Streamlit application entry point
├── src/                # Source code directory
│   ├── chat_analyzer.py # Logic for analyzing chat patterns
│   ├── db_manager.py    # Database interactions
│   ├── topic_modeler.py # NLP topic modeling implementation
│   └── history_fetcher.py # Browser history extraction logic
├── requirements.txt    # Project dependencies
└── .gitignore          # Files to exclude from version control
Installation & SetupClone the repository:git clone [https://github.com/ALLEE16481/Smart-context-aware-NLP-model-using-RAG.git](https://github.com/ALLEE16481/Smart-context-aware-NLP-model-using-RAG.git)
cd Smart-context-aware-NLP-model-using-RAG
Create a virtual environment:python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:pip install -r requirements.txt
Environment Variables:Create a .env file or update app.py with your API keys:GROQ_API_KEY=your_api_key_here
Run the app:streamlit run app.py
Security NoteThis project is configured to ignore local databases and environment files via .gitignore to protect user privacy and sensitive API credentials.🤝 Contributing Contributions, issues, and feature requests are welcome! Feel free to check the issues page.Developed by Ali Muttahar - AI/ML & GenAI Engineer
