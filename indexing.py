from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import bs4
from langchain_community.document_loaders import WebBaseLoader

load_dotenv()

page_urls = [
    "https://chaidocs.vercel.app/web-dev/getting-started",
    "https://chaidocs.vercel.app/web-dev/environmnet-setup/mac-os/",
    "https://chaidocs.vercel.app/web-dev/environmnet-setup/windows/",
    "https://chaidocs.vercel.app/devops/environmnet-setup/mac-os/",
    "https://chaidocs.vercel.app/devops/environmnet-setup/windows/"
]

all_docs = []

for url in page_urls:
    loader = WebBaseLoader(web_paths=[url])
    for doc in loader.lazy_load():
        all_docs.append(doc)
        

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vector_store = QdrantVectorStore.from_documents(
    documents= all_docs,
    url="http://localhost:6333",
    collection_name= "chai_docs_scraper-2",
    embedding= embedding_model
)

print("Indexing complete")






