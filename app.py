from utils.constants import MAX_YEAR, MIN_YEAR
from utils.time import calculate_century
from utils.versions import get_last_version, save
from utils.backup import backup
from utils.iterables import replace
from utils.xmls import prittify_xml


from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import os
from options import support_options, type_options, genre_options

#################################################
#    SESSION MANAGMENT FOR TEXTS and SLECTEC_TEST
##################################################

#################################
#     FOR  TEXTS
##################################


if "texts" not in st.session_state:
    try:
        st.session_state['texts'] = pd.read_csv('data.csv').to_dict(orient='records')
    except FileNotFoundError:
        st.session_state['texts'] = []

df = pd.DataFrame(st.session_state['texts'])

#################################
#     FOR  SELECTED TEXT
##################################

if "selected_text" not in st.session_state:
    st.session_state['selected_text'] = None


def pandas_row_to_record(pandas_row):
    if pandas_row is None:
        return None
    def parse_value(value):
        if pd.isna(value):
            return None
        return value
    return {field_name: parse_value(pandas_row[field_name]) for field_name in pandas_row}
 

text_selected_pandas_row = st.session_state['selected_text']
text_selected_record = pandas_row_to_record(text_selected_pandas_row)

# note that if text_selected_record is None  everithing is None and so field do not have defualt values

def get_default_value(field_name):
    if text_selected_record is None:
        return None
    return text_selected_record[field_name]

def get_default_index(field_name, options):
    value = get_default_value(field_name)
    if value is None:
        return None
    return options.index(value)

##################################
#   SIDEBAR
#################################
if len(df):
    select_text_name = st.sidebar.selectbox('Text', options=list(df.text))            
    st.sidebar.dataframe(df.set_index('id')[df.columns[1:2]])
st.sidebar.write(st.session_state['selected_text'])

########################################
#               HADER
#########################################

# Display title and description
st.title("Multiple Multilingual Alignment: Corpus Construction")
st.header("Medieval Multilingual Corpus")

if st.session_state['selected_text'] is None:
    st.title('Add a new text')
    is_update = False
else:
    st.title(f"Update text ID = {text_selected_record['id']}")
    is_update = True

# Create a new form
with st.form(key="corpus_form", clear_on_submit=True):

    #########################################################################################################
    #                             INPUT                                                                     #
    #########################################################################################################

    st.markdown("**Information required**")
    
    text_title = st.text_input("Text*", placeholder="Text title", value=get_default_value('text'))
    language=st.text_input("Language*", placeholder="Text language", value=get_default_value('language'))
    if is_update is False:
        text_uploader  = st.file_uploader("Upload") 
        st.caption("Please upload a .txt file using the uploader above.")
    source = st.text_input("Source*", placeholder="Source from where the data was obtained", value=get_default_value('source'))    
    type_selected = st.selectbox("Type", options=type_options, index= get_default_index("type", type_options))
    genre = st.selectbox("Genre", options=genre_options, index=get_default_index('genre', genre_options))
    # date_from date_to
    date_from = get_default_value("date_from") or MIN_YEAR
    date_to = get_default_value("date_to") or MAX_YEAR
    date_from, date_to = st.slider("Date*", min_value=MIN_YEAR, max_value=MAX_YEAR, value=(date_from,date_to))
    # century
    century_label, centuries = calculate_century(date_from, date_to)
    century = st.text_input("Century", value=century_label, disabled=True)
    support_selected = st.selectbox("Support", options=support_options, index=get_default_index("support", support_options))
    doc = st.text_input("Document", placeholder="City, library, call number", value=get_default_value("document"))
    loc = st.text_input("Localisation", placeholder="Text placement in the document", value=get_default_value("localisation"))
    # xml_file
    if is_update is False:
        xml_uploader = st.file_uploader("XML")
        st.caption("Please upload a xml file using the uploader above.")

    obs = st.text_area("Additional Information", value=get_default_value("observations"))
    text_id = st.text_input("Text ID", placeholder="Philobiblon, Arlima, Jonas...", value=get_default_value("text_id"))
    biblio = st.text_area("Bibliography", placeholder="eg. critical editions", value=get_default_value("bibliography"))
    corpus_name = st.text_input('Corpus name', value=get_default_value('corpus_name'))

    # buttons
    if is_update is False:
        save_version = st.checkbox('Save Version')
        submit_button = st.form_submit_button("Submit Text Form")
    else:
        submit_button = st.form_submit_button(f"Update id {text_selected_record['id']}")

    ##############################
    ##  What happen if you click the submit
    ###################################################

    if submit_button:
        ### Check MANDATORY FIELD 
        mandatory_fields = [
            (text_title, "Text Title"),
            (language, "language"),
            (source, "source"),
            (date_from, "date"),
            (date_to, "date"),

        ]
        for field_value, field_label  in mandatory_fields:
            if not field_value:
                st.error(f'{field_label} is mandatory')      
        
        if (is_update is False) and not( text_uploader or xml_uploader ) :
            st.error(f'You need to upload at least one file either xml or txt')

        ### FIND ID
        if is_update is True:
            id_ = text_selected_record['id']
        else:
            if st.session_state['texts']:
                last_id = st.session_state['texts'][-1]['id']
                id_ = last_id + 1
            else:
                id_ = 0
        
        ### BUILD RECORD
        if is_update is False:
            filename = None if not text_uploader else text_uploader.name
            filename_xml = None if not xml_uploader else xml_uploader.name
        record = {
                "id": id_,
                "text": text_title,
                "language": language,
                "filename": text_selected_record['filename'] if is_update else filename,
                "type": type_selected,
                "genre": genre,
                "date_from": date_from,
                "date_to": date_to,
                "century": century,
                "support": support_selected,
                "document": doc,
                "localisation": loc,
                "source": source,
                "filename_xml": text_selected_record['filename_xml'] if is_update else filename_xml,
                "observations": obs,
                "text_id": text_id,
                "bibliography": biblio,
                "corpus_name": corpus_name
            }
        records = st.session_state['texts']


        ### ADD or update record
        if is_update is True:
            replace(record, records)
            st.session_state['selected_text'] = None  
        else:                
            records.append(record)
            if text_uploader :
                bytes_data = text_uploader.read()
                filename = text_uploader.name
                Path(f'txts/{filename}').write_bytes(bytes_data)
                text_uploader.close()
            if xml_uploader :
                bytes_data = xml_uploader.read()
                filename = xml_uploader.name
                Path(f'xmls/{filename}').write_bytes(bytes_data)
                try:
                    formatted_xml = prittify_xml(bytes_data.encode('utf-8'))
                    Path(f'data/formatted_xmls/{filename}').write_text(formatted_xml)
                    st.success('Xml Formatted')
                except Exception as ex:
                    st.error('Problem with xmls formatting')
                    print(ex)
                    st.error(str(ex)[:20])

                xml_uploader.close()            
        
        # SAVE RECORDS
        st.session_state['texts'] = records
        df = pd.DataFrame(records)
        
        backup('data.csv', Path('backup/'), f'Update id={id_}' if is_update else f"Add id={id_}")
        df.to_csv('data.csv', index=False)
        if save_version is True:
            save('data.csv', Path('versions/'))
        st.success(f'The text {text_title} is saved.' )

        # RETURN TO THE DEFAULT is_update = False
        if is_update is True:
            is_update = False
            text_selected_pandas_row = st.session_state['selected_text']
            text_selected_record = pandas_row_to_record(text_selected_pandas_row)
            def get_default_value(field_name):
                if text_selected_record is None:
                    return None
                return text_selected_record[field_name]
            
            def get_default_index(field_name, options):
                value = get_default_value(field_name)
                if value is None:
                    return None
                return options.index(value)
