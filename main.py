import os
import streamlit as st
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import SeleniumURLLoader
from langchain.memory import ConversationBufferMemory

# Load environment variables
load_dotenv()

# Set API Key from environment or paste directly (avoid hardcoding in production)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "YOUR_API_KEY")

# Streamlit UI
st.title("🧠 News Research Assistant")

st.sidebar.title("📌 News Article URLs")
urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    if url:
        urls.append(url)

process_button = st.sidebar.button("⚙️ Process URLs")
main_placeholder = st.empty()

# Embeddings model
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GOOGLE_API_KEY
)

# Process the URLs
if process_button:
    if not urls:
        st.warning("Please enter at least one valid URL.")
        st.stop()

    # Using SeleniumURLLoader to load the content of multiple URLs
    loader = SeleniumURLLoader(urls=urls)
    main_placeholder.info("📤 Loading and parsing article content...")
    documents = loader.load()

    documents = [doc for doc in documents if doc.page_content.strip()]
    if not documents:
        st.error("No valid content found from the URLs. Try different links.")
        st.stop()

    main_placeholder.info("✂️ Splitting text into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.split_documents(documents)

    main_placeholder.info("🔎 Creating vectorstore...")
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("faiss_index")  # Save vectorstore locally
    st.success("✅ Documents processed and stored!")

# User Query Input
query = st.text_input("🔍 Ask a question about the articles:")

if query:
    if not os.path.exists("faiss_index"):
        st.warning("Please process URLs first.")
        st.stop()

    # Load vectorstore
    vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    # Set up Gemini LLM - Using GoogleGenerativeAI instead of ChatGoogleGenerativeAI
    llm = GoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0.1,
        google_api_key=GOOGLE_API_KEY
    )

    # Set up memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )


    # Set up retrieval chain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
        memory=memory,
        return_source_documents=True,
        output_key="answer"
    )
    print(qa_chain)

    main_placeholder.info("🧠 Thinking...")
    result = qa_chain({"question": query})

    # Display results
    st.header("📘 Answer")
    st.write(result["answer"])

    st.subheader("🔗 Sources")
    for doc in result.get("source_documents", []):
        st.write(doc.metadata.get("source", "No source available"))
