import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

import streamlit as st
from src.fact_checker import FactCheckerBot
import time

st.title("AI Fact-Checker Bot")
st.write("Enter a claim or question to verify its accuracy")

if "bot" not in st.session_state:
    st.session_state.bot = FactCheckerBot()
if "history" not in st.session_state:
    st.session_state.history = []

claim = st.text_input("Enter your claim or question:")
if st.button("Check Fact") and claim:
    with st.spinner("Fact-checking in progress..."):
        start_time = time.time()
        result = st.session_state.bot.check_fact(claim)
        elapsed_time = time.time() - start_time
        
        st.session_state.history.append(result)
        
        if "final_response" in result:
            st.subheader("Final Verified Response")
            st.write(result["final_response"])
            
            st.subheader("Details")
            with st.expander("Initial Response"):
                st.write(result["initial_response"])
            
            with st.expander("Assumptions Verified"):
                for assumption in result["assumptions"]:
                    st.markdown(f"**Assumption:** {assumption['assumption']}")
                    st.markdown(f"**Verdict:** {assumption['verification']}")
                    st.markdown(f"**Confidence:** {assumption['confidence']}")
                    st.write("---")
        else:
            st.error(f"An error occurred: {result.get('error', 'Unknown error')}")
        
        st.caption(f"Fact-check completed in {elapsed_time:.2f} seconds")

if st.session_state.history:
    st.sidebar.title("History")
    for i, item in enumerate(reversed(st.session_state.history)):
        if st.sidebar.button(f"{item['claim'][:50]}...", key=f"hist_{i}"):
            st.experimental_rerun()