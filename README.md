🧠 TrendWhisper – Your AI-Powered News Research Assistant

TrendWhisper helps you cut through information overload. Simply provide URLs of news articles, and it will parse, understand, and answer your questions using Google’s powerful Gemini LLM — all with traceable sources.

🚀 Features

- 🌐 **Multi-Article Ingestion** – Enter up to 3 news article URLs at once.
- ✂️ **Smart Chunking** – Automatically splits content for optimal semantic embedding.
- 🧠 **Context-Aware Q&A** – Ask any question about the articles and get direct, relevant answers.
- 🧾 **Source Traceability** – Displays the source documents behind each answer.
- 💾 **Local Vector Storage** – Uses FAISS to store and retrieve document chunks efficiently.
- ♻️ **Conversational Memory** – Keeps track of the context across multiple questions.


📸 Preview

![image](https://github.com/user-attachments/assets/5c4ac3aa-62e7-4b33-8fe5-b0e67623610a)

⚙️ Tech Stack

**Frontend:** Streamlit
**LLM:** Google Gemini (via `GoogleGenerativeAI`)
**Embeddings:** GoogleGenerativeAIEmbeddings
**Vector DB:** FAISS
**Document Loader:** SeleniumURLLoader
**Memory:** LangChain `ConversationBufferMemory`


🧪 How It Works

1. Input up to 3 news article URLs in the sidebar.
2. The app loads and splits article content using Selenium and LangChain.
3. It embeds content into a FAISS vector store.
4. You enter a query; Gemini answers using relevant chunks from the vector store.
5. The system shows the answer and relevant source(s).

🛠️ Setup Instructions

1. **Clone the repository:**


   git clone https://github.com/Phoenixarjun/TrendWhisper
   cd trendwhisper


2. **Install dependencies:**

   pip install -r requirements.txt

3. **Set up your environment variables:**

   Create a `.env` file with:


   GOOGLE_API_KEY=your_google_gemini_api_key


4. **Run the app:**

   streamlit run main.py


🧑‍💻 Author

Built with ❤️ by [Naresh](https://github.com/Phoenixarjun)
Inspired to reimagine how we consume news in the AI age.



📄 License

MIT License – use freely, improve openly.


