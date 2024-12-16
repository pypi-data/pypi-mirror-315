from langchain_google_genai import ChatGoogleGenerativeAI

def initialize_llm(api_key):

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key= api_key
    )
    
    return llm
