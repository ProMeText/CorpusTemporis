import streamlit as st
import pandas as pd

if "texts" not in st.session_state:
    st.session_state['texts'] = []

if "selected_text" not in st.session_state:
    st.session_state['selected_text'] = None


df = pd.DataFrame(st.session_state['texts'])
# Multiselect for column selection
selected_columns = st.sidebar.multiselect(
    "Select columns to display:",
    options=df.columns,  # Available columns to choose from
    default=df.columns,  # Pre-select all columns initially
)

# Display DataFrame with selected columns
if selected_columns:
    filtered_df = df[selected_columns]
    event = st.dataframe(filtered_df,  selection_mode="single-row",  on_select="rerun",         use_container_width=True,
        hide_index=True,)


    if event.selection.rows:
        num_row = event.selection.rows[0]
        st.session_state['selected_text'] = st.session_state['texts'][num_row]
        st.write(st.session_state['selected_text'])
        if st.button('remove'):
            st.session_state['texts'] = [text for num, text in enumerate(st.session_state['texts']) if num != num_row ]
            st.session_state['selected_text'] = None
            st.rerun()
else:
    st.write("Please select at least one column to display.")