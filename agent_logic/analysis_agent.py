import google.generativeai as genai
import streamlit as st
import os
import ast
from .prompts import SYSTEM_PROMPT # The '.' means import from the same folder


@st.cache_data
def generate_pandas_code(df , query):
    """Sends the query and schema to the AI model and returns the generated code."""
    st.info("🧠 Agent is thinking...")
    model = genai.GenerativeModel(
            'gemini-flash-latest',  
            system_instruction=SYSTEM_PROMPT
        )
    columns = df.columns.tolist()
    prompt_part = [
        f"query: \"{query}\"",
        f"Columns: {columns}",
        "Code:"
    ]
    full_prompt = "\n".join(prompt_part)
    try:
        response = model.generate_content(full_prompt)
        code = response.text.strip().strip("```python").strip("```")
        return code
    except Exception as e:
        return f"Error generating code: {e}"
    return None

@st.cache_data
def get_professionnal_title(query):
    """uses ia to turn a user query into a professionnal report title"""
    model = genai.GenerativeModel(
        'gemini-flash-latest',

    )
    prompt = f"""
    You are a professional report editor.
    A user asked the following query: "{query}"
    
    Generate a short, human-readable section heading for a business report based on this query.
    Do not include "Analysis of" or "Chart of". Just the title.

    Example 1:
    Query: "Plot the profit (sales - cost) for each product"
    Title: "Product Profitability"

    Example 2:
    Query: "What is the average sales for each region?"
    Title: "Average Sales by Region"

    Example 3:
    Query: "Show the first 5 rows"
    Title: "Data Sample"

    Title:
    """
    try:
        response = model.generate_content(prompt)
        title = response.text.strip().strip('"')
        return title
    except Exception as e:
        return f"Error generating title: {e}"
    
    
@st.cache_data
def generate_overview_analysis(data_context):
    """
    Agent 1: Generates the simple, 2-3 sentence overview summary.
    """
    model = genai.GenerativeModel(
        'gemini-flash-latest',
        system_instruction="You are a data analyst writing a brief dataset summary."
    )
    
    full_prompt = f"""
    Here is the head of a dataset:
    ---
    {data_context}
    ---
    Based ONLY on this data, write a 2-3 sentence summary of what this dataset is about.

    CRITICAL RULES:
    - DO NOT use markdown, headings, or bullet points.
    - DO NOT suggest any "Future Prompts" or "Recommendations".
    - Just write the plain text summary paragraph.
    """
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error analyzing data: {e}"

@st.cache_data
def generate_markdown_analysis(prompt_question, data_context):
    """
    Agent 2: Generates the detailed, structured analysis for a report item.
    """
    model = genai.GenerativeModel(
        'gemini-flash-latest', # 
        system_instruction="You are a professional data analyst writing a key insight for a business report."
    )
    
    full_prompt = f"""
    A user asked: "{prompt_question}"
    Here is the data/chart result:
    ---
    {data_context}
    ---
    Based ONLY on this data, write a professional analysis using the following template.

    CRITICAL RULES:
    - You MUST use the exact headings below: ### Key Finding, ### Detailed Analysis, ### Business Impact
    - You MUST use markdown (like **bold** or bullet points).
    - DO NOT suggest new queries, future prompts, or 'Recommendations'.

    ### Key Finding
    (Start with a single **bolded sentence**.)

    ### Detailed Analysis
    (Write 1-2 paragraphs explaining the data.)

    ### Business Impact
    (Write 1-2 bullet points.)
    """
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error analyzing data: {e}"
    
    import ast # Add 'import ast' to the top of analysis_agent.py

@st.cache_data
def generate_recommendations(data_context):
    """
    Agent 3: Generates a list of 3 suggested follow-up queries.
    """
    model = genai.GenerativeModel(
        'gemini-flash-latest',
        system_instruction="You are a helpful assistant suggesting new data analysis queries."
    )
    
    full_prompt = f"""
    Here is the head of a dataset:
    ---
    {data_context}
    ---
    Based on these columns, generate 3 interesting follow-up questions.
    
    CRITICAL RULES:
    - Return ONLY a Python list of strings.
    - Example: ['What is the total sales?', 'Plot sales by region']
    """
    try:
        response = model.generate_content(full_prompt)
        # Safely convert the AI's string output into a real Python list
        return ast.literal_eval(response.text)
    except Exception as e:
        return [f"Error generating recommendations: {e}"]