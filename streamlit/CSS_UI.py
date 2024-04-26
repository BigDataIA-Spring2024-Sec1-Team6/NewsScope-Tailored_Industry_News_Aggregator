import streamlit as st
def apply_custom_styles():
    st.markdown('<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">', unsafe_allow_html=True)
    st.markdown("""
            <style>
            html, body, [class*="st-"] {
                font-family: 'Roboto', sans-serif;
            }
            body {
                background-color: #FAFAFA;
            }
            .stApp {
                background: linear-gradient(to right, #dae2f8, #d6a4a4);
            }
            .stSelectbox > div, .stButton > button {
                background-color: #f0f0f0;
                border: none;
                border-radius: 4px;
            }
            .stButton > button {
                background-color: #E8C1E1;
                color: black;
                border: 1px solid black;
                padding: 10px 24px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                transition-duration: 0.4s;
                cursor: pointer;
            }
            .stButton > button:hover {
                background-color: white;
                color: black;
                border: 1px solid #E8C1E1;
            }
            .summary-text {
                font-family: 'Roboto', sans-serif;
                font-size: 16px;
                text-align: justify;
                background-color: #FFFFFF;
                padding: 2rem;
                border-radius: 0.5rem;
                margin-bottom: 1rem;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            </style>
            """, unsafe_allow_html=True)