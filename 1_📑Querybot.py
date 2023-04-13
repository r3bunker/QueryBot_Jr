# Load required packages
import streamlit as st
import pandas as pd
import re
import pyodbc as dbc
import pandas as pd

# Load data
sentence_codes = pd.read_csv('sentence_codes.csv')
rvn_groups = pd.read_csv('rvn_groups.csv')

# Split sentences by '.' or ':' and allow exceptions
def sentence_splitter(user_input):
    clean_text = user_input.replace('\u201D', '"').replace('\u201C', '"')
    clean_text = re.sub('\s+', ' ', clean_text.strip())
    exceptions = ['i.e.', 'Mr.', 'L.D.S.', 'U.S.A.']
    pattern = "(?<=[.?!:])\s+"
    for ex in exceptions:
        ex = ex.replace('.','\.')
        pattern = f'(?<!{ex})' + pattern
    sentences = filter(None, re.split(pattern, clean_text))
    sentences = list(sentences)
    return sentences

# Define function to find RVN matches
def find_rvn(user_input):
    match_code = []
    matched_sentences = []
    match_ID = None
    # Clean and split the user_input
    sentences = sentence_splitter(user_input)
    num_splits = len(sentences)
    percent_matches = 0
    for i in range(sentence_codes.shape[0]):
        regex = sentence_codes.loc[i, 'LANGUAGE'].lower()
        # split text into sentence_codes
        for sentence in sentences:
            try:
                rvn_wording = sentence.lower()
                if re.match(regex, rvn_wording):
                    match_ID = sentence_codes.loc[i, 'Match_ID']
                    match_code.append(match_ID)
                    sentences.remove(sentence)
                    matched_sentences.append(sentence)
                    percent_matches += 1
            except:
                continue
    # sort match_code
    match_code = sorted(set(match_code))
    match = ''
    match_code_str = str(match_code)
    if match_code_str in rvn_groups['Match Code'].values:
        match = rvn_groups.loc[rvn_groups['Match Code'] == match_code_str, 'RVN'].values[0]
        match = str(match)
    return match, match_ID, match_code_str, num_splits, percent_matches, sentences, matched_sentences

# Define app
def app():
    st.set_page_config(
        layout="wide",
        initial_sidebar_state='expanded')
    modes = st.radio(
    "Select Mode:",
    ('Paragraph', 'Single Sentence'))

    ## PARAGRAPH MODE
    if modes == 'Paragraph':
        with st.sidebar:
            st.title('FAQs & Instructions')
            st.subheader('How does it work?')
            st.markdown("""Copy and paste paragraphs or sentences from the pdf into the text box. Make sure to fix any spelling errors that may have occured from copying pdf text. This finds any RVN sentence that we have a match for.

            Example:

    Genealogical Society of Utah, a nonprofit corporation 
    (hereinafter "GSU") is hereby given permission to 
    duplicate, circulate, and use the following work(s):
    I/We agree to allow GSU to copy the work (s) described 
    above.
    I/We further agree that GSU will own such copies and 
    may use, reproduce, display, or distribute such copies 
    in any manner, in whole or in part, in any media now 
    known or later developed, and may produce, distribute, 
    sell, or transfer resources such as indexes or other 
    research aids based upon information contained in the 
    work(s).
    I/We further authorize GSU to create derivative works 
    based upon the work(s) and to sell or transfer copies 
    of such derivative works to other organizations or 
    individuals without my/our consent.
    GSU will not sell copies of the work without my/our 
    consent.
    I/We represent that I/we have the authority to allow 
    this use of the work(s) and this use does not conflict 
    with any other agreement or understanding or infringe 
    on the rights of any third parties.

    Results:

    RVN match: 2002-0001-02""")
            st.divider()
            st.subheader('FAQs')
        st.title("Find Potential RVN Matches")
        st.caption("<=**IMPORTANT**: FAQ in sidepanel")
        user_input = st.text_area("Enter Text:",height=300)
        if st.button("Find Matches"):
            match, match_ID, match_code, num_splits, percent_matches, sentences, matched_sentences = find_rvn(user_input)
            if match:
                st.subheader(f"RVN match: {match}")
                st.write(matched_sentences)
                if percent_matches != num_splits:
                    st.subheader("Sentence(s) with no match:")
                    st.write(sentences)
                    st.write("**Why did these sentences not find a match?\n")
                    st.markdown("1. They are not an RVN sentence.\n2. If you think they are, check to see if there are any spelling errors in the contract pdf.\n3. They are unique and require a new regular expression (send to Kylee).")
            elif percent_matches == num_splits:
                st.subheader(f"No match. Need a new RVN for: {match_code}")
                st.subheader('Contact Kylee for confirmation.')
            else:
                st.subheader(f"No Match...Percent Match: {int((percent_matches/num_splits)*100)}% | Matched: {percent_matches}/{num_splits} sentences")
                st.write(matched_sentences)
                st.subheader("Sentence(s) with no match:")
                st.write(sentences)
                st.write("**Why did these sentences not find a match?\n")
                st.markdown("1. They are not an RVN sentence.\n2. If you think they are, check to see if there are any spelling errors in the contract pdf.\n3. They are unique and require a new regular expression (send to Kylee).")

    ## SINGLE SENTENCE MODE
    elif modes == 'Single Sentence':
        with st.sidebar:
            st.title('FAQs & Instructions')
            st.subheader('How does it work?')
            st.markdown("""Enter in a single RVN sentence. You will receive a table of all the RVNs that sentence is contained in.
            
            Example:
            
    It is assumed that you are authorized to grant to the 
    Society, permission to both acquire and use these 
    materials.
    
    Results:
    RVN
    1987-0001-36
    1997-0002-02
    1987-0001-51""")
        st.title('Find ALL RVN Matches For Sentence')
        user_input = st.text_input('Enter Sentence:')
        if st.button("Find Matches"):
            match, match_ID, match_code, num_splits, percent_matches, sentences, matched_sentences = find_rvn(user_input)
            if match_ID:
                rvn_matches = rvn_groups[rvn_groups['Match Code'].str.contains(match_ID)]['RVN']
                # CSS to inject contained in a string
                hide_table_row_index = """
                            <style>
                            thead tr th:first-child {display:none}
                            tbody th {display:none}
                            </style>
                            """
                # Inject CSS with Markdown
                st.markdown(hide_table_row_index, unsafe_allow_html=True)
                st.table(rvn_matches)
            else:
                st.subheader('No match. Make sure there are no spelling errors.')



# Run the app
if __name__ == '__main__':
    app()