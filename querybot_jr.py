# Load required packages
import streamlit as st
import pandas as pd
import re
import pyodbc as dbc
import pandas as pd

# Load data
sentences_codes = pd.read_csv('sentence_codes.csv')
rvn_groups = pd.read_csv('rvn_groups.csv')

# Define function to find RVN matches
def find_rvn(user_input):
    match_code = []
    # split user input into list of RVN sentences_codes
    user_input = user_input.splitlines()
    user_input = [line.strip() for line in user_input if line.strip()]
    num_splits = len(user_input)
    percent_matches = 0
    for i in range(sentences_codes.shape[0]):
        regex = sentences_codes.loc[i, 'LANGUAGE'].lower()
        # split text into sentences_codes
        for sentence in user_input:
            try:
                rvn_wording = sentence.lower()
                # rvn_wording = f'^{rvn_wording}$'
                if re.match(regex, rvn_wording):
                    match_code.append(sentences_codes.loc[i, 'Match_ID'])
                    user_input.remove(sentence)
                    percent_matches += 1
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
    return match, match_code_str, num_splits, percent_matches, user_input

# Define app
def app():
  st.set_page_config(layout="wide")
  st.title("Find Potential RVN Matches")
  st.caption("**IMPORTANT**: Make sure each sentence is separated by a new line.")
  user_input = st.text_area("Enter Text:",height=300)
  if st.button("Find Matches"):
      match, match_code, num_splits, percent_matches, user_input = find_rvn(user_input)
      if match:
          st.subheader(f"RVN match: {match}")
      elif percent_matches == num_splits:
          st.subheader(f"No match. Need a new RVN for: {match_code}")
      else:
          st.subheader(f"No Match...Percent Match: {int((percent_matches/num_splits)*100)}% | Matched: {percent_matches}/{num_splits} sentences")
          no_match_string = ' \n'.join(user_input)
          st.text_area("Sentence(s) with no match:", no_match_string,height=150)
          st.write("**These sentences either have a spelling error (check the contract pdf) or are unique and require a new regular expression (send to Ryan).")



# Run the app
if __name__ == '__main__':
    app()
