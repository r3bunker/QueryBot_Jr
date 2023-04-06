# Load required packages
import streamlit as st
import pandas as pd
import re
import pyodbc as dbc
import pandas as pd

sql_conn = dbc.connect("""
    Driver={SQL Server Native Client 11.0}; 
    Server=(LocalDb)\LocalDB; 
    Database=RvnSentences; 
    Trusted_Connection=yes;
    """)
# connection string for SentenceCodes table
sentences_query = """
SELECT [LANGUAGE]
      ,[Match_ID]
  FROM [RvnSentences].[dbo].[SentenceCodes]
  """

# connection string for RvnGroups table
codes_query = """
SELECT [RVN]
      ,[Match Code]
  FROM [RvnSentences].[dbo].[RvnGroups]
"""

sentences_codes = pd.read_sql(sentences_query, sql_conn)
rvn_groups = pd.read_sql(codes_query, sql_conn)
# Load data
# sentences_codes = pd.read_csv('sentence_codes.csv')
# rvn_groups = pd.read_csv('rvn_groups.csv')

# Define function to find RVN matches
def find_rvn(user_input):
    match_code = []
    # split user input into list of RVN sentences_codes
    user_input = user_input.splitlines()
    user_input = [line.strip() for line in user_input if line.strip()]
    for i in range(sentences_codes.shape[0]):
        regex = sentences_codes.loc[i, 'LANGUAGE'].lower()
        # split text into sentences_codes
        for sentence in user_input:
            try:
                rvn_wording = sentence.lower()
                # rvn_wording = f'^{rvn_wording}$'
                if re.match(regex, rvn_wording):
                    match_code.append(sentences_codes.loc[i, 'Match_ID'])
            except:
                # print(e)
                # print(sentence)
                continue
    # sort match_code
    match_code = sorted(set(match_code))
    match = ''
    match_code_str = str(match_code)
    if match_code_str in rvn_groups['Match Code'].values:
        match = rvn_groups.loc[rvn_groups['Match Code'] == match_code_str, 'RVN'].values[0]
        match = str(match)
    return match, match_code_str

# Define app
def app():
    st.title("Find Potential RVN Matches")
    st.caption("**IMPORTANT**: Make sure each sentence is separated by a new line.")
    user_input = st.text_area("Enter Text:",height=500)
    if st.button("Find Matches"):
        match, match_code = find_rvn(user_input)
        if match:
            st.subheader(f"RVN match: {match}")
            # st.write("Match Code:", match_code)
        else:
            st.write("No match. Need a new RVN for:", match_code)

# Run the app
if __name__ == '__main__':
    app()
