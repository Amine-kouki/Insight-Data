import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go 
import io
from agent_logic.analysis_agent import (
    generate_pandas_code, 
    generate_overview_analysis,  # Replaces generate_analysis
    generate_markdown_analysis,
    generate_recommendations
)
from report_builder.pdf_generator import build_pdf_report


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    st.error("GEMINI_API_KEY not found in environment variables.")
    st.stop()


def main():
    st.title("Data Analysis AI Agent 🤖")

    if "report_cart" not in st.session_state:
        st.session_state.report_cart = []
    if "df" not in st.session_state:
        st.session_state.df = None

    uploaded_file = st.file_uploader("Upload your CSV file here:", type="csv")

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
            
            st.success("File uploaded successfully!")
            st.write("Here is a preview of your data (first 5 rows):")
            st.dataframe(df.head())
            
            st.info("🧠 Generating data overview...")
            overview_context = f"Data Head:\n{df.head().to_string()}\n\nData Types:\n{df.dtypes.to_string()}"
            overview_prompt = "What is this data about? Give a one-sentence summary."
            overview = generate_overview_analysis(overview_context)
            st.write(overview)
            
            st.divider()


            st.subheader("Recommendations")
            recommendations = generate_recommendations(overview_context)
            for rec in recommendations:
                st.code(rec)

            st.divider()

            query = st.text_input(
                "Ask a question about your data:", 
                placeholder="e.g., 'What is the average sales per region?'"
            )

            if query:
                generated_code = generate_pandas_code(df, query)

                if generated_code:
                    with st.expander("🤖 Show Agent's Generated Code"):
                        st.code(generated_code, language="python")
                    
                    st.write("### 📊 Result")
                    
                    try:
                        exec_vars = {'df': df, 'pd': pd, 'px': px}
                        exec(generated_code, exec_vars, exec_vars)
                        result = exec_vars.get('result')

                        if result is None:
                            st.warning("The agent ran code, but did not produce a 'result'.")
                        elif isinstance(result, go.Figure):
                            st.write("Here is the chart you asked for:")
                            st.plotly_chart(result, use_container_width=True)
                        elif isinstance(result, (pd.DataFrame, pd.Series)):
                            st.write("Here is the data you asked for:")
                            st.dataframe(result)
                        else:
                            st.write("Here is the result:")
                            st.write(result)
                        
                        if result is not None:
                            st.info("🧠 Generating chart analysis...")
                            analysis_context = str(result)
                            analysis_prompt = query

                            analysis = generate_markdown_analysis(
                                prompt_question=analysis_prompt,
                                data_context=analysis_context
                            )
                            st.write(analysis, unsafe_allow_html=True)

                            if st.button("Add to Report 🛒", key=query):
                                item_type = "data"
                                if isinstance(result, go.Figure):
                                    item_type = "plot"
                                elif isinstance(result, (pd.DataFrame, pd.Series)):
                                    item_type = "data"
                                else:
                                    item_type = "value"
                                
                                new_item = {
                                    "query": query,
                                    "code": generated_code,
                                    "result": result,
                                    "analysis": analysis,
                                    "type": item_type 
                                }
                                
                                st.session_state.report_cart.append(new_item)
                                st.toast("Added to report!", icon="✅")
                                
                    except Exception as e:
                        st.error(f"Error executing or displaying code: {e}")

        except Exception as e:
            st.error(f"An error occurred: {e}")

    with st.sidebar:
        st.title("About")
        st.markdown(
            """
            This app uses a Gemini AI agent to analyze your data.
            Upload a CSV file, ask questions, and generate a PDF report of the findings.
            """
            "\n\n"
            "connect with me:"
            "[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?logo=linkedin)](https://www.linkedin.com/in/amine-kouki-org/)"
            "\n\n"
            "[![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github&logoColor=white)](https://github.com/Amine-kouki/Insight-Data)"
        )
        st.divider()
    st.sidebar.title("Report Builder 📄")
    st.sidebar.write(f"Items in report: {len(st.session_state.report_cart)}")

    if st.sidebar.button("Generate PDF Report"):
        if st.session_state.df is None:
            st.sidebar.error("No data loaded. Please upload a file.")
        elif not st.session_state.report_cart:
            st.sidebar.error("No items in the report. Please add some analysis first.")
        else:
            st.sidebar.info("Generating PDF report... this may take a moment.")
            
            df_head = st.session_state.df.head()
            overview_context = f"Data Head:\n{st.session_state.df.head().to_string()}\n\nData Types:\n{st.session_state.df.dtypes.to_string()}"
            main_overview = generate_overview_analysis(overview_context)

            pdf_bytes = build_pdf_report(
                dataset_name=uploaded_file.name if uploaded_file else "Uploaded Data",
                main_overview=main_overview,
                data_head=df_head,
                report_cart=st.session_state.report_cart
            )

            st.sidebar.download_button(
                label="Download PDF Report",
                data=pdf_bytes,
                file_name="data_analysis_report.pdf",
                mime="application/pdf")
    
if __name__ == "__main__":
    main()
