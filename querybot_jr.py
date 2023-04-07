# Load required packages
import streamlit as st
import pandas as pd
import re
import pyodbc as dbc
import pandas as pd

# Load data
sentence_codes = pd.read_csv('sentence_codes.csv')
rvn_groups = pd.read_csv('rvn_groups.csv')

# Define function to find RVN matches
def find_rvn(user_input):
    match_code = []
    matched_sentences = []
    # split user input into list of RVN sentence_codes
    
    # user_input = user_input.splitlines()
    # user_input = [line.strip() for line in user_input if line.strip()]
    clean_text = re.sub('\s+', ' ', user_input.strip())

    sentences = re.findall(r'[^:.\s][^:.]*[:.?!]', clean_text)
    
    # Add the last sentence, if any (it won't end with period or colon)
    # if not re.match(r'^.*[:.?!]\s*$', user_input):
    #     sentences.append(user_input.rsplit(' ', 1)[-1])
    num_splits = len(sentences)
    percent_matches = 0
    for i in range(sentence_codes.shape[0]):
        regex = sentence_codes.loc[i, 'LANGUAGE'].lower()
        # split text into sentence_codes
        for sentence in sentences:
            try:
                rvn_wording = sentence.lower()
                # rvn_wording = f'^{rvn_wording}$'
                if re.match(regex, rvn_wording):
                    match_code.append(sentence_codes.loc[i, 'Match_ID'])
                    sentences.remove(sentence)
                    matched_sentences.append(sentence)
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
    return match, match_code_str, num_splits, percent_matches, sentences, matched_sentences

# Define app
def app():
  st.set_page_config(layout="wide")
  with st.sidebar:
    st.title('FAQs & Instructions')
    st.write('Enter in contract language into text box.')
  st.title("Find Potential RVN Matches")
  st.caption("<=**IMPORTANT**: FAQ in sidepanel")
  user_input = st.text_area("Enter Text:",height=300)
  if st.button("Find Matches"):
      match, match_code, num_splits, percent_matches, sentences, matched_sentences = find_rvn(user_input)
      if match:
          st.subheader(f"RVN match: {match}")
          st.write(matched_sentences)
          # no_match_string = ' \n'.join(sentences)
          # st.text_area("Sentence(s) with no match:", no_match_string,height=150)
          # st.write("**Why did these sentences not find a match?\n")
          # st.markdown("1. They are not an RVN sentence.\n2. If you think they are, check to see if there are any spelling errors in the contract pdf.\n")
      elif percent_matches == num_splits:
          st.subheader(f"No match. Need a new RVN for: {match_code}")
      else:
          st.subheader(f"No Match...Percent Match: {int((percent_matches/num_splits)*100)}% | Matched: {percent_matches}/{num_splits} sentences")
          no_match_string = ' \n'.join(sentences)
          st.text_area("Sentence(s) with no match:", no_match_string,height=150)
          st.write("**Why did these sentences not find a match?\n")
          st.markdown("1. They are not an RVN sentence.\n2. If you think they are, check to see if there are any spelling errors in the contract pdf.\n3. They are unique and require a new regular expression (send to Kylee).")



# Run the app
if __name__ == '__main__':
    app()
