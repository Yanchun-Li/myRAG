import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from smolagents import OpenAIServerModel, CodeAgent, ToolCallingAgent, HfApiModel, tool, GradioUI

load_dotenv()

def get_model(model_id):
    using_huggingface = os.getenv("USE_HUGGINGFACE", "yes").lower() == "yes"
    using_openai_model = os.getenv("USE_OPENAI", "no").lower() == "yes"
    if using_huggingface:
        print("Using Hugging Face model")
        return HfApiModel(model_id=model_id, token=huggingface_api_token)
    else:
        if using_openai_model:
            print("Using OpenAI model")
            return OpenAIServerModel(model_id=model_id, api_key=openai_api_key)
        else:
            print("Using local server model")
            return OpenAIServerModel(
                model_id=model_id,
                api_base="http://localhost:11434/v1",
                api_key="ollama")


reasoning_model_id = os.getenv("REASONING_MODEL_ID")
tool_model_id = os.getenv("TOOL_MODEL_ID")
huggingface_api_token = os.getenv("HUGGINGFACE_API_TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Create the reasoner
reasoning_model = get_model(reasoning_model_id)
reasoner = CodeAgent(tools=[], model=reasoning_model, add_base_tools=False, max_steps=2)

# Initialize vector store and embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={'device': 'cpu'}
)

db_dir = os.getenv("CHROMA_DB_DIR")
if not db_dir:
    db_dir = os.path.join(os.path.dirname(__file__), "chroma_db")
vectordb = Chroma(persist_directory=db_dir, embedding_function=embeddings)

@tool
def rag_with_reasoner(user_query: str) -> str:
    """
    This is a RAG tool that takes in a user query and searches for relevant content from the vector database.
    The result of the search is given to a reasoning LLM to generate a response, so what you'll get back
    from this tool is a short answer to the user's question based on RAG context.

    Args:
        user_query: The user's question to query the vector database with.
    """
    # Search for relevant documents
    docs = vectordb.similarity_search(user_query, k=3)
    
    # Combine document contents
    context = "\n\n".join(doc.page_content for doc in docs)
    
    # Create prompt with context
    prompt = f"""Based on the following context, answer the user's question. Be concise and specific.
    If there isn't sufficient information, give as your answer a better query to perform RAG with. Answer in Chinese.
    You are a humorous, witty, well-mannered 24-year-old man. Please respond in the same tone as this conversation.
    Have a conversation in place of (or on behalf of) Li Yanchun and Zou Shouzhe.

    
Context:
{context}

Question: {user_query}

Answer:"""
    
    # Get response from reasoning model
    response = reasoner.run(prompt, reset=False)
    return response

# Create the primary agent to direct the conversation
tool_model = get_model(tool_model_id)
primary_agent = ToolCallingAgent(tools=[rag_with_reasoner], model=tool_model, add_base_tools=False, max_steps=3)

# Example prompt: Compare and contrast the services offered by RankBoost and Omni Marketing
def main():
    GradioUI(primary_agent).launch()

if __name__ == "__main__":
    main()