import streamlit as st
import pandas as pd


sentence_codes = pd.read_csv('sentence_codes.csv')


st.title("Enter key word(s) to search for RVN sentences")
with st.sidebar:
    st.title('FAQs & Instructions')
    st.subheader('How does it work?')
    st.write("""Search for keywords or strings of keywords in RVN sentences.
    You can select how many different strings you want to search for.\n
    Example:\n
    1) 'made available'
    2) 'made available' and 'public'
    3) 'made available' and 'public' and 'stored'""")
    st.divider()
    st.subheader('FAQs')
num_strings = st.radio(
    "How many separate string searches?",
    ('1', '2', '3'))
if num_strings == '1':
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
    st.write(f'Number of results: {len(result_df)}')
    st.table(result_df)
elif num_strings == '2':
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
    st.write(f'Number of results: {len(result_df)}')
    st.table(result_df)
elif num_strings == '3':
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
    st.write(f'Number of results: {len(result_df)}')
    st.table(result_df)
