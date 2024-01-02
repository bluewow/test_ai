import time
import requests
from dotenv import load_dotenv
load_dotenv()
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import BSHTMLLoader

def rag(url, driver):
    driver.get(url) 
    time.sleep(1)
    html = driver.page_source

    # HTML 내용을 로컬 파일로 저장
    with open('temp.html', 'w', encoding='utf-8') as file:
        file.write(html)

    # RAG
    loader = UnstructuredHTMLLoader("temp.html")
    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=600,
        chunk_overlap=100,
    )
    docs = loader.load_and_split(text_splitter=splitter)
    vectorstore = FAISS.from_documents(docs, OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()
    
    query = "find login inputbox element id"
    result = retriever.get_relevant_documents(query)
    
    print(result)