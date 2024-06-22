from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import openai 
from dotenv import load_dotenv
import os
import shutil
import logging
from pathlib import Path

log = logging.getLogger(__name__)

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

CHROMA_PATH = Path(os.path.abspath("app/data/chroma"))

# Update DATA_PATH to the path of the directory containing the markdown file
DATA_PATH = Path(os.path.abspath("app/data/paul_graham"))


def main():
    generate_data_store()


def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    return documents


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    log.info(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[10]
    log.info(document.page_content)
    log.info(document.metadata)

    return chunks


def save_to_chroma(chunks: list[Document]):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings()
    )
    db.persist()
    log.info(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    main()