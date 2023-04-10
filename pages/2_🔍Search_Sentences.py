import streamlit as st
import pandas as pd


sentence_codes = pd.read_csv('sentence_codes.csv')


st.title("Enter key word(s) to search for RVN sentences")
num_strings = st.radio(
    "How many separate string searches?",
    ('One', 'Two', 'Three'))
if num_strings == 'One':
  user_input = st.text_input("Enter string:")
  if st.button("Find Matches"):
    result_df = sentence_codes[(sentence_codes['LANGUAGE'].str.contains(user_input))][['Match_ID', 'LANGUAGE']]
    # CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """
    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.table(result_df)
elif num_strings == 'Two':
  user_input = st.text_input("Enter string:")
  user_input2 = st.text_input("Second string:")
  if st.button("Find Matches"):
    result_df = sentence_codes[(sentence_codes['LANGUAGE'].str.contains(user_input)) & (sentence_codes['LANGUAGE'].str.contains(user_input2))][['Match_ID', 'LANGUAGE']]
    # CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """
    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.table(result_df)
elif num_strings == 'Three':
  user_input = st.text_input("Enter string:")
  user_input2 = st.text_input("Second string:")
  user_input3 = st.text_input("Third string:")
  if st.button("Find Matches"):
    result_df = sentence_codes[(sentence_codes['LANGUAGE'].str.contains(user_input)) & (sentence_codes['LANGUAGE'].str.contains(user_input2)) & (sentence_codes['LANGUAGE'].str.contains(user_input3))][['Match_ID', 'LANGUAGE']]
    # CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """
    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.table(result_df)
