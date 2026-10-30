
import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

# Load API key
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("Groq API key not found in .env file")

# Initialize language model
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.2,
    api_key=api_key
)


# Shared state
class MedicalState(TypedDict):
    question: str
    category: str
    medical_response: str
    final_response: str


# Agent 1: Query Analyzer
def analyze_query(state: MedicalState):

    print("\n[Agent 1] Analyzing query...")

    prompt = f"""
    Classify this health-related question into:
    General Health, Symptoms, Medication, Emergency, or Other.

    Question: {state['question']}

    Return only the category.
    """

    response = llm.invoke(prompt)

    return {"category": response.content}


# Agent 2: Medical Information Agent
def medical_agent(state: MedicalState):

    print("\n[Agent 2] Generating medical information...")

    prompt = f"""
    You are a general medical information assistant.

    User question: {state['question']}
    Category: {state['category']}

    Give clear general health information in simple language.
    Do not diagnose diseases or prescribe medicines.
    If symptoms suggest an emergency, advise immediate medical care.
    """

    response = llm.invoke(prompt)

    return {"medical_response": response.content}


# Agent 3: Safety Reviewer
def safety_reviewer(state: MedicalState):

    print("\n[Agent 3] Reviewing response for safety...")

    prompt = f"""
    Review this response for medical safety.

    Question: {state['question']}
    Draft response: {state['medical_response']}

    Remove diagnosis and prescription claims.
    Preserve emergency warnings.
    Do not add unsupported medical claims.
    Return the revised response in simple language.
    """

    response = llm.invoke(prompt)

    return {"final_response": response.content}


# Create LangGraph workflow
graph = StateGraph(MedicalState)

graph.add_node("query_analyzer", analyze_query)
graph.add_node("medical_agent", medical_agent)
graph.add_node("safety_reviewer", safety_reviewer)

# Connect nodes
graph.add_edge(START, "query_analyzer")
graph.add_edge("query_analyzer", "medical_agent")
graph.add_edge("medical_agent", "safety_reviewer")
graph.add_edge("safety_reviewer", END)

# Compile workflow
medical_workflow = graph.compile()


# Main function
def get_medical_response(question):

    result = medical_workflow.invoke({
        "question": question,
        "category": "",
        "medical_response": "",
        "final_response": ""
    })

    return result
