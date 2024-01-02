import time
import requests
from dotenv import load_dotenv
load_dotenv()
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import BSHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language


def rag(url, driver):
    driver.get(url) 
    time.sleep(1)
    html = driver.page_source

    # RAG
    html_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.HTML, chunk_size=60, chunk_overlap=0
    )
    html_docs = html_splitter.create_documents([html])
    vectorstore = FAISS.from_documents(html_docs, OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()
    
    print(retriever.get_relevant_documents("find 아이디 input box class id"))
    print("------------------")
    print(retriever.get_relevant_documents("find 비밀번호 input box class id"))