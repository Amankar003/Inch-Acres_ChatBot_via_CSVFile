import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import ollama
from langchain_experimental.agents import create_pandas_dataframe_agent
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=api_key,
    temperature=0.7, 
    convert_system_message_to_human=True 
)

def load_csv(file):
    return pd.read_csv(file)

def create_agent(df):
    custom_prefix = """
    You are 'Aman', a professional Real Estate Consultant from Inch&Acre. 
    Your goal is to provide a premium, step-by-step consultation experience.

    PHASE 1: Introduction (MANDATORY)
    - If you don't know the user's name, greet them warmly and ask for their name.
    - Example: "Hi! Welcome to Inch&Acre. I'm Aman. May I know your name please?"

    PHASE 2: Requirement Gathering
    - Once you know the name, ask about their requirements ONE BY ONE.
    - Ask for: Preferred Location, Number of Bedrooms (BHK), and Budget.
    - DO NOT ask all questions at once. Keep it natural.

    PHASE 3: Suggestion
    - Only after gathering info, use the `python_repl_ast` tool to filter the dataframe `df`.
    - Suggest the top 3 best matching properties. 
    - Format: **Property Name** | **Price** | **Area**.
    - Tell them WHY you are suggesting these (e.g., "This fits your budget perfectly").

    CRITICAL: Always start your final response with 'Final Answer:' 
    Keep the tone professional yet friendly (Hinglish is okay).
    """

    return create_pandas_dataframe_agent(
        llm, 
        df, 
        verbose=True,
        allow_dangerous_code=True,
        handle_parsing_errors=True,
        prefix=custom_prefix,
        agent_types="tool-calling" 
        #agent_type="zero-shot-react-description"
    )

def ask_question(agent, query, chat_history):
    full_prompt = f"Chat History:\n{chat_history}\n\nUser: {query}"
    response = agent.run(full_prompt)
    return response