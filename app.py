import streamlit as st
from typing import Annotated, Tuple
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
import requests
import json
import os  # Added to load environment variables

# Load environment variables
huggingface_token = os.getenv('HUGGINGFACEHUB_API_TOKEN')  # Get HuggingFace token from env
serpapi_key = os.getenv('SERPAPI_API_KEY')  # Get SerpAPI key from env

# Tool for web search using SerpAPI
def search_web(query: str) -> str:
    if not serpapi_key:
        return "SerpAPI key not found in environment."
    
    params = {
        "q": query,
        "api_key": serpapi_key,
        "engine": "google",
    }
    response = requests.get("https://serpapi.com/search", params=params)
    if response.status_code == 200:
        search_results = response.json()
        return search_results.get("organic_results", [{}])[0].get("snippet", "No result found.")
    else:
        return "Error fetching search results."

# Another hypothetical tool (customize as needed)
def another_tool(query: str) -> str:
    return f"Processed your query with another tool: {query}"

class State(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize the state graph
graph_builder = StateGraph(State)

# Initialize HuggingFace endpoint with token from environment
chatllm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    task="text-generation",
    max_new_tokens=512,
    do_sample=False,
    repetition_penalty=1.03,
)

llm = ChatHuggingFace(llm=chatllm)

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# Add nodes and edges to the state graph
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

# Function to handle graph updates
def stream_graph_updates(user_input: str):
    responses = []
    for event in graph.stream({"messages": [("user", user_input)]}):
        for value in event.values():
            responses.append(value["messages"][-1].content)
    return responses

# Function to check if LLM indicates tool usage
def parse_llm_response(response: str) -> Tuple[str, str]:
    try:
        # Assuming the LLM response format is JSON
        data = json.loads(response)
        if "tool" in data:
            tool_name = data["tool"]
            tool_query = data.get("query", "")
            return tool_name, tool_query
    except json.JSONDecodeError:
        return "chat", response  # Fallback to chat if not JSON
    return "chat", response

# Streamlit application layout
st.title("Chatbot Interface")
st.markdown("### Talk to the Chatbot")

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_input("User Input:", key="user_input")

# Checkbox for tool usage
use_tool = st.checkbox("Request LLM to use a tool", value=False)

if st.button("Ask to LLM"):
    if user_input:
        # Add user input to chat history
        st.session_state.chat_history.append(f"User Input: {user_input}")

        # Get chatbot responses
        bot_responses = stream_graph_updates(user_input)
        
        for response in bot_responses:
            # Check if the LLM response indicates tool usage
            tool_name, tool_query = parse_llm_response(response)

            if use_tool:
                # If the user has requested tool usage, invoke the tool
                if tool_name == "search_web":
                    search_result = search_web(user_input)
                    st.session_state.chat_history.append(f"Assistant (used tool): {search_result}")
                elif tool_name == "another_tool":
                    tool_response = another_tool(user_input)
                    st.session_state.chat_history.append(f"Assistant (used tool): {tool_response}")
                else:
                    # If no specific tool is indicated but the user wants to use a tool, inform the user
                    st.session_state.chat_history.append("Assistant: I couldn't find a suitable tool to use.")
            else:
                # If the user did not request tool usage, just append the chatbot's response
                if tool_name != "chat":  # Check if a tool was mentioned
                    st.session_state.chat_history.append(f"Assistant (used tool): {response}")
                else:
                    st.session_state.chat_history.append(f"Assistant: {response}")

# Display chat history
st.markdown("### Chat History")
for message in st.session_state.chat_history:
    st.write(message)

# Option to clear the chat
if st.button("Clear Chat"):
    st.session_state.chat_history.clear()
