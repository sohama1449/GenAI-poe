
import streamlit as st
from workflow import get_medical_response

# Page configuration
st.set_page_config(
    page_title="Medical Healthcare AI",
    page_icon="🏥",
    layout="centered"
)

# Application heading
st.title("🏥 Medical Healthcare AI Assistant")
st.write("Ask a general health-related question and receive AI-generated information.")

st.info(
    "This application provides general health information only. "
    "It does not replace professional medical advice."
)

# User input
question = st.text_area(
    "Enter your health-related question:",
    placeholder="Example: What are some common causes of headaches?"
)

# Submit button
if st.button("Get Medical Information"):
    if question.strip():

        with st.spinner("AI agents are processing your question..."):

            try:
                result = get_medical_response(question)

                st.success("Analysis completed!")

                st.subheader("Question Category")
                st.write(result["category"])

                st.subheader("Medical Information")
                st.markdown(result["final_response"])

            except Exception as e:
                st.error(f"An error occurred: {e}")

    else:
        st.warning("Please enter a question first.")

# Footer
st.divider()
st.caption("Medical Healthcare AI | Powered by LangChain, LangGraph and Groq")
