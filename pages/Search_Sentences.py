import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import re


sentence_codes = pd.read_csv('sentence_codes.csv')
rvn_groups = pd.read_csv('rvn_groups.csv')
def sentence_splitter(user_input):
    clean_text = user_input.replace('\u201D', '"').replace('\u201C', '"')
    clean_text = re.sub('\s+', ' ', clean_text.strip())
    exceptions = ['i.e.', 'Mr.', 'L.D.S.', 'U.S.A.', 'No.', 'Rev.', 'includes:', 'Dept.'] #list of exceptions to avoid incorrect sentence splitting
    pattern = "(?<=[.?!:])\s+"
    for ex in exceptions:
        ex = ex.replace('.','\.').replace(':','\:')
        pattern = f'(?<!{ex})' + pattern
    sentences = filter(None, re.split(pattern, clean_text))
    sentences = list(sentences)
    return sentences

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


modes = option_menu(
  menu_title=None,  # required
  options=["Search Regex", "Search RVNs"],  # required
  icons=["asterisk","archive"],  # optional
  menu_icon="cast",  # optional
  default_index=0,  # optional
  orientation="horizontal",
        )

if modes == 'Search Regex':
  st.title("Enter key word(s) to search for RVN sentence")
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
  # num_strings = st.radio(
  #     "How many separate string searches?",
  #     ('1', '2', '3'))
  num_strings = option_menu(
              menu_title=None,  # required
              options=["1", "2", "3"],  # required
              icons=["1-circle-fill", "2-circle-fill", "3-circle-fill"],  # optional
              menu_icon="cast",  # optional
              default_index=0,  # optional
              orientation="horizontal",
          )
  if num_strings == '1':
    user_input = st.text_input("Enter string:")
    if st.button("Find Matches"):
      result_df = sentence_codes[(sentence_codes['LANGUAGE'].str.contains(user_input))][['Match_ID', 'LANGUAGE']]
      if len(result_df) == 0:
        st.subheader('No matches found.')
      else:
        result_df['RVN'] = result_df.apply(lambda x: rvn_groups.loc[rvn_groups['Match Code'].str.contains(x['Match_ID']), 'RVN'].tolist(), axis=1)
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
      if len(result_df) == 0:
        st.subheader('No matches found.')
      else:
        result_df['RVN'] = result_df.apply(lambda x: rvn_groups.loc[rvn_groups['Match Code'].str.contains(x['Match_ID']), 'RVN'].tolist(), axis=1)
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
      if len(result_df) == 0:
        st.subheader('No matches found.')
      else:
        result_df['RVN'] = result_df.apply(lambda x: rvn_groups.loc[rvn_groups['Match Code'].str.contains(x['Match_ID']), 'RVN'].tolist(), axis=1)

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

if modes == 'Search RVNs':
  st.title('Find ALL RVN Matches For Sentence')
  with st.sidebar:
    st.title('FAQs & Instructions')
    st.subheader('How does it work?')
    st.markdown("""Enter in a single RVN sentence. You will receive a table of all the RVNs that sentence is contained in.""")
    with st.expander("See Example"):
        st.markdown("""
    Example:
        
    It is assumed that you are authorized to grant to the 
    Society, permission to both acquire and use these 
    materials.

    Results:
    RVN
    1987-0001-36,
    1997-0002-02,
    1987-0001-51""")
            
  
  user_input = st.text_input('Enter Sentence:')
  if st.button("Find Matches"):
      match, match_ID, match_code, num_splits, percent_matches, sentences, matched_sentences = find_rvn(user_input)
      if match_ID:
          rvn_matches = rvn_groups[rvn_groups['Match Code'].str.contains(match_ID)]['RVN']
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
          st.warning('No match. Make sure there are no spelling errors.')

  