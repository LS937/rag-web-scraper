from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="chai_docs_scraper-2",
    embedding= embedding_model
)

client = OpenAI()

query = input("> ")

search_results = vector_db.similarity_search(
    query=query
)

context = "\n\n\n".join([f"Content: {results.page_content},\n URL : {results.metadata["source"]}" for results in search_results])




SYSTEM_PROMPT = f"""
    You are an expert web page scraper, that answer the user query using the relevant content from web pages.
    You deeply think about the given context from the web pages for the corresponding user query.Next, you curate the perfect response for the user query by using the given context only. 
    Along with the reponse give the user the url to the web page where he or she could find relevant information.

    Note:Don't mention anything beyong the given context of the web page in the response.
    
    Context from relevant Web Pages:
    {context}
"""

response = client.chat.completions.create(
    model = "gpt-4.1-mini",
    messages=[
        {"role" : "system", "content" : SYSTEM_PROMPT},
        {"role" : "user", "content" : query}
    ]
)


print("Response🤖: ", response.choices[0].message.content)