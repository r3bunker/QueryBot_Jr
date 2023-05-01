# Load required packages
import streamlit as st
import pandas as pd
import re
import pyodbc as dbc
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from cryptography.fernet import Fernet
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
pd.options.mode.chained_assignment = None
import io
import zipfile
import shutil
import os
import psutil

st.set_page_config(
    layout="wide",
    initial_sidebar_state='expanded')


process = psutil.Process()
memory_usage = process.memory_info().rss / 1024 / 1024  # in MB
print(f"Memory usage: {memory_usage:.2f} MB")

# @st.cache_resource
# def combine_csv_files(base_filename, num_chunks):
#     # Initialize empty dataframe
#     combined_df = pd.DataFrame()

#     # Read each chunk and append to combined dataframe
#     for i in range(num_chunks):
#         chunk_filename = f"{base_filename}_{i}.csv"
#         chunk_df = pd.read_csv(chunk_filename)
#         combined_df = combined_df.append(chunk_df, ignore_index=True)

#     # Write combined dataframe to CSV file
#     combined_filename = f"{base_filename}_combined.csv"
#     combined_df.to_csv(combined_filename, index=False)
#     memory_usage = process.memory_info().rss / 1024 / 1024  # in MB

#     print(f"Memory usage: {memory_usage:.2f} MB")
#     return combined_filename



# @st.cache_resource
# def assemble_file(filename):
#     with open(filename, 'wb') as output_file:
#         part_num = 1
#         while True:
#             part_filename = f"{filename}.part{part_num}"
#             if not os.path.exists(part_filename):
#                 break
#             with open(part_filename, 'rb') as input_file:
#                 shutil.copyfileobj(input_file, output_file)
#             part_num += 1

# assemble_file('encrypted_applied_option_related.zip')


@st.cache_resource
def load_csv(filename):
    if isinstance(filename, str):
        # If filename is a string, read the CSV file
        memory_usage = process.memory_info().rss / 1024 / 1024  # in MB

        print(f"Memory usage: {memory_usage:.2f} MB")
        return pd.read_csv(filename)
    elif isinstance(filename, io.StringIO):
        # If filename is a string or bytes buffer, read the CSV data from the buffer
        memory_usage = process.memory_info().rss / 1024 / 1024  # in MB

        print(f"Memory usage: {memory_usage:.2f} MB")
        return pd.read_csv(filename)
    else:
        # If filename is not a string or buffer, raise an error
        raise ValueError("Invalid input type. Expected string or buffer.")
    
# @st.cache_resource
# def decrypt_csv(filename):
#     # Read encrypted file as bytes
#     with open(filename, 'rb') as f:
#         encrypted_bytes = f.read()

#     # Read key from file
#     with open('mykey.key', 'rb') as f:
#         key = f.read()

#     # Initialize Fernet object with key
#     f = Fernet(key)

#     # Decrypt bytes
#     decrypted_bytes = f.decrypt(encrypted_bytes)

#     # Decode decrypted bytes and create pandas dataframe
#     decrypted_df = pd.read_csv(io.StringIO(decrypted_bytes.decode()))
#     memory_usage = process.memory_info().rss / 1024 / 1024  # in MB
#     print(f"Memory usage: {memory_usage:.2f} MB")
#     return decrypted_df
@st.cache_resource
def decrypt_csv():
    # Read the encryption key from a file
    key = st.secrets["querybot_jr"]["encryption_key"]

    # Create a Fernet instance with the key
    fernet = Fernet(key)

    # Read the encrypted data from a file
    with open('cleaned_applied_option_related.parquet.enc', 'rb') as f:
        ciphertext = f.read()

    # Decrypt the ciphertext with Fernet
    plaintext = fernet.decrypt(ciphertext)

    # Convert the decrypted data to a pyarrow buffer
    buf = pa.BufferReader(plaintext)

    # Read the Parquet file into a PyArrow table
    table = pq.read_table(buf)

    # Convert the table to a pandas DataFrame
    df = table.to_pandas()
    memory_usage = process.memory_info().rss / 1024 / 1024  # in MB
    print(f"Memory usage: {memory_usage:.2f} MB")
    return df
# # THIS FUNCTION WORKS
# def load_decrypted_csv():
#     key = st.secrets["querybot_jr"]["encryption_key"]
#     f = Fernet(key)
#     with open('encrypted_applied_option_related.csv', 'rb') as encrypted_applied_option_related:
#         encrypted = encrypted_applied_option_related.read()

#     decrypted = f.decrypt(encrypted)

#     with open('decrypted_applied_option_related.csv', 'wb') as decrypted_applied_option_related:
#         decrypted_applied_option_related.write(decrypted)
#     decoded_data = decrypted.decode('utf-8')
#     string_io = io.StringIO(decoded_data)
#     memory_usage = process.memory_info().rss / 1024 / 1024  # in MB

#     print(f"Memory usage: {memory_usage:.2f} MB")
#     return load_csv(string_io)


#     # DECRYPT FILE
#     with zipfile.ZipFile('encrypted_applied_option_related.zip', 'r') as zip_ref:
#         # Read the encrypted data from the ZIP file
#         with zip_ref.open('encrypted_applied_option_related.csv', 'r') as encrypted_file:
#             encrypted = encrypted_file.read()

#         # Decrypt the data
#         decrypted = f.decrypt(encrypted)

#     # Convert the decrypted data to a Pandas DataFrame
#     decoded_data = decrypted.decode('utf-8')
#     string_io = io.StringIO(decoded_data)
    
#     return load_csv(string_io)

# f = Fernet(key)

# Load data
sentence_codes = load_csv('sentence_codes.csv')
rvn_groups = load_csv('rvn_groups.csv')
# applied_option_related = decrypt_csv('encrypted_applied_option_related_combined.csv')
# applied_option_related = combine_csv_files('encrypted_applied_option_related', 4)
# combined_filename = combine_csv_files('encrypted_applied_option_related', 4)
applied_option_related = decrypt_csv()

# Split sentences by '.' or ':' and allow exceptions
def sentence_splitter(user_input):
    clean_text = user_input.replace('\u201D', '"').replace('\u201C', '"')
    clean_text = re.sub('\s+', ' ', clean_text.strip())
    exceptions = ['i.e.', 'Mr.', 'L.D.S.', 'U.S.A.', 'No.', 'Rev.', 'includes:'] #list of exceptions to avoid incorrect sentence splitting
    pattern = "(?<=[.?!:])\s+"
    for ex in exceptions:
        ex = ex.replace('.','\.').replace(':','\:')
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

# QueryBot Function
def find_matches(pdf_titles, regex_df, contracts_df, rvn_groupings):
    rvn_groups = rvn_groupings
    matches = []
    for pdf_title in pdf_titles:
        red_bucket = False
        sixty_day = False
        electronic_letter = False
        xdn1 = ''
        xdn2 = ''
        xdn3 = ''
        # Filter the contracts dataframe to only include the specified pdf title
        pdf_contracts = contracts_df[(contracts_df['pdfTitle'] == pdf_title) & (contracts_df['isDeleted'] == False)]
        # apply sentence splitter function to 'wording' column
        pdf_contracts.loc[:, 'wording'] = pdf_contracts['wording'].apply(sentence_splitter)
        # explode the 'wording' column to create separate rows for each sentence
        pdf_contracts = pdf_contracts.explode('wording').reset_index(drop=True)

        # Create an empty list to hold the matches
        match_code = []
        contract_sentences = []
        # Iterate over the rows in the filtered contracts dataframe
        progress_bar = st.progress(0)
        total_iterations = len(pdf_contracts)
        for i, row in pdf_contracts.iterrows():
            progress_bar.progress(int((i+1)/total_iterations*100))
            # Get the wording of the current row
            wording = row['wording']
            if len(wording) < 20 and 'yes' not in wording:
                continue
            opt_wording = row['optWording']
            opt_selected = row['optSelected']
            wordID = row['wordID']
            red_bucket_wording = 'red bucket'
            sixty_day_letter = 'through past cooperative agreements'
            electronic_letter_wording = 'gradually make the information available electronically in our system'
            if re.search(red_bucket_wording, wording.lower()):
                # print(', 0001')
                red_bucket = True
            if re.search(sixty_day_letter, wording.lower()):
                # print(', 0002')
                sixty_day = True
            if re.search(electronic_letter_wording, wording.lower()):
                # print(', 0099')
                electronic_letter = True
            
            # Iterate over the rows in the regex dataframe
            for j, regex_row in regex_df.iterrows():
                # Get the regex pattern of the current row
                pattern = regex_row['LANGUAGE']
                match_id = regex_row['Match_ID']
                
                # Find all matches of the regex pattern in the wording
                found_matches = re.findall(pattern, wording.lower())
                
                #OptSelected
                wordID_table = pdf_contracts[pdf_contracts['wordID'] == wordID]
                wordID_table_length = len(wordID_table)
                if found_matches and opt_selected == False and opt_wording == wording:
                    continue
                # If matches were found, add them to the list
                elif found_matches and (opt_selected == True or opt_selected == False):
                    if (opt_selected == True or opt_selected == False) and wordID_table_length <= 1:
                        if 'does not authorize' not in wording:
                            match_id = match_id
                        else:
                            match_id = '0000121.0'
                    elif wordID_table_length > 1:
                        opt_false = wordID_table[wordID_table['optSelected'] == 0]['optWording'].iloc[0]
                        opt_true = wordID_table[wordID_table['optSelected'] == 1]['optWording'].iloc[0]
                        opt_false_pos = wordID_table['wording'].iloc[0].find(opt_false)
                        opt_true_pos = wordID_table['wording'].iloc[0].find(opt_true)
                        if opt_false_pos < opt_true_pos:
                            match_id = f'{match_id}.0.1'
                        else:
                            match_id = f'{match_id}.1.0'
                    else:
                        match_id = match_id
                    match_code.append(match_id)
                    contract_sentences.append(f'{match_id} | {wording}')
                elif found_matches:
                    match_code.append(match_id)
                    contract_sentences.append(f'{match_id} | {wording}')
        match_code = list(set(match_code))
        match_code = sorted(match_code)
        match_code = str(match_code)
        unique_sentences = []
        seen_sentences = set()

        for sentence in contract_sentences:
            if sentence not in seen_sentences:
                unique_sentences.append(sentence)
                seen_sentences.add(sentence)
        if red_bucket == True:
            xdn1 = ' | 0001'
        if sixty_day == True:
            xdn2 = ' | 0002'
        if electronic_letter == True:
            xdn3 = ' | 0099'
        if match_code in rvn_groups['Match Code'].values and match_code != []:
            match = rvn_groups[rvn_groups['Match Code'] == match_code]['RVN'].values[0]
            match = f'{match}{xdn1}{xdn2}{xdn3}'
            matches.append({'Contract_Number':pdf_title,'Match_Code':match_code,'Contract_Sentences': unique_sentences, 'RVN': match})
        else:
            match = 'No RVN match'
            match = f'{match}{xdn1}{xdn2}{xdn3}'
            matches.append({'Contract_Number':pdf_title,'Match_Code':match_code,'Contract_Sentences': unique_sentences, 'RVN': match})

    # Return the list of matches
    matches = pd.DataFrame(matches)
    pd.set_option('display.max_colwidth', 0)
    memory_usage = process.memory_info().rss / 1024 / 1024  # in MB

    print(f"Memory usage: {memory_usage:.2f} MB")
    return matches

# APP #

# Querybot Modes
modes = st.radio(
"Select Mode:",
('Single Sentence', 'Paragraph', 'Full Contract'))

## SINGLE SENTENCE MODE
if modes == 'Single Sentence':
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
            st.warning('No match. Make sure there are no spelling errors.')

## PARAGRAPH MODE
if modes == 'Paragraph':
    with st.sidebar:
        st.title('FAQs & Instructions')
        st.subheader('How does it work?')
        st.markdown("""Copy and paste paragraphs or sentences from the pdf into the text box. Make sure to fix any spelling errors that may have occured from copying pdf text. This finds any RVN sentence that we have a match for.""")
        with st.expander("See Example"):
            st.markdown("""
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

## FULL CONTRACT MODE ##
elif modes == 'Full Contract':
    with st.sidebar:
        st.title('FAQs & Instructions')
        st.subheader('How does it work?')
        st.markdown("""Enter in a the contract number.

        I.e 7347-000189""")
    st.title('Find RVN Match')
    user_input = st.text_input('Enter Contract Number:')
    user_input = user_input.strip()
    contract_pattern = r"\d{4}-\d{6}"
    contract_pattern_match = re.findall(contract_pattern, user_input)
    if st.button("Find Match:"):
        if contract_pattern_match:
            matches = find_matches([user_input], sentence_codes, applied_option_related, rvn_groups)
            # CSS to inject contained in a string
            hide_table_row_index = """
                        <style>
                        thead tr th:first-child {display:none}
                        tbody th {display:none}
                        </style>
                        """
            # Inject CSS with Markdown
            st.markdown(hide_table_row_index, unsafe_allow_html=True)
            st.table(matches)
        else:
            st.warning("Make sure the contract number is in the correct format. (xxxx-xxxxxx)")