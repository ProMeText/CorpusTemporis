from pathlib import Path
import streamlit as st
import pandas as pd
from datalign.conversions import xml_to_txt


if "selected_text" not in st.session_state:
    st.session_state['selected_text'] = None
st.set_page_config(layout="wide")
filename = st.session_state['selected_text']['filename']
filename_xml = st.session_state['selected_text']['filename_xml']

base_folder = Path('data/')

# Notice that 
xmls_folder = base_folder / 'formatted_xmls'
txts_folder = base_folder / 'txts'
derived_txts_folder = base_folder / 'derived_txts'




if pd.isna(filename):
    # You do not have txt filename
    xml_path = xmls_folder / filename_xml
    c1, c2 = st.columns([20, 20])
    with c1:
        with st.container(height=2000):
            xml_content = xml_path.read_text()
            st.code(xml_content, language="xml")
    with c2:
        txt_content = (derived_txts_folder / (xml_path.stem  + '.txt')).read_text()
        st.code(txt_content, language="txt", wrap_lines=True)
elif pd.isna(filename_xml):
    # You just have an txt
    txt_path = txts_folder / filename
    st.code(txt_path.read_text(), language="txt", wrap_lines=True)
else:
    # You have both
    xml_col, txt_col = st.columns([20, 20])
    xml_path = xmls_folder / filename_xml
    txt_path = txts_folder / filename
    with xml_col:
        with st.container(height=2000):
            xml_content = xml_path.read_text()
            st.code(xml_content, language="xml")
    with txt_col:
        st.code(txt_path.read_text(), language="txt", wrap_lines=True)

