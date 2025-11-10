import google.generativeai as genai
import streamlit as st
import os
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
def generate_analysis(prompt_question,data_context):
    """
    A simple agent that takes a question and data,
    and returns a text-based analysis.
    """
    model = genai.GenerativeModel(
        'gemini-flash-latest',
        system_instruction="You are an expert data analyst creating professional business reports with clear, structured analysis."
    )
    full_prompt = f"""
        You are a professional data analyst writing a key insight for a business report.
        A user asked: "{prompt_question}"
        Here is the data:
        ---
        {data_context}
        ---
        Based ONLY on this data, write a professional analysis using the following template.

        CRITICAL RULES:
        - You MUST use the exact headings below in your response.
        - You MUST use markdown (like **bold** or bullet points).
        - DO NOT suggest new queries, future prompts, or 'Future Analysis Suggestions'.

        ### Key Finding
        (Start with a single **bolded sentence** that states the most important insight.)

        ### Detailed Analysis
        (Write 1-2 paragraphs explaining *why* this insight is true, referencing the data.)

        ### Business Impact
        (Write 1-2 bullet points explaining what this insight means for a business.)
        ### Recommendations
        (if this is the over view wrap each bullet point im going to ask to generate later in st.code() don't put any code just the text else don't put them in st.code() : write 2-3 bullet points with suggested data visualuals based on the dataset exact columns to explore next to deepen the analysis.)
        """
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error analyzing data: {e}"

