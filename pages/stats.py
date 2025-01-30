import streamlit as st
import pandas as pd

st.write('Basic statistics')

if "texts" not in st.session_state:
    st.session_state['texts'] = []

df = pd.DataFrame(st.session_state['texts'])
num_texts = len(df)

filename_mask = df['filename'].isna()
num_texts_with_plain = len(df[~filename_mask])
num_texts_with_xml = len(df[~df['filename_xml'].isna()])

contain_do_mask = df['text'].str.contains('Do')

tab_progress, tab_metric, tab_genre, tab_lang, tab_genre_lang, tab_corpus = st.tabs(["Progress", 'Metrics', 'Genre', 'Language', 'Genre-Language', 'Corpus'])

with tab_progress:
    group_by_langage = df.groupby("language")["num_tokens"].sum().reset_index().set_index('language')
    for language in group_by_langage.index:
        num_tokens = group_by_langage.loc[language, 'num_tokens']
        progress= min( num_tokens / 100_000, 1.)
        st.progress(progress, language)
        #st.write(progress, num_tokens)


with tab_metric:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Number of texts', num_texts)
        st.metric('Number of tokens', df['num_tokens'].sum())
    with col2:
        st.metric('Texts in TXT format.', num_texts_with_plain)
        st.metric('Number multi fragments.', len(df.query('completness == "multi-fragment"')))
        st.metric('Number multi fragments Tokens.', df.query('completness == "multi-fragment"')['num_tokens'].sum())

    with col3:
        st.metric('Text in XML format.', num_texts_with_xml)
        st.metric('Number Single fragments.', len(df.query('completness == "single-fragment"')))
        st.metric('Number Single fragments Tokens.', df.query('completness == "single-fragment"')['num_tokens'].sum())







#distribution by language
#st.metric(f'There are x texts in x language.', text_by_language)
# distribution by century
#distribution by type

# st.write(df[contain_do_mask])   
# st.metric('Contain Do', len(df[contain_do_mask]))


# source = df.groupby("century").agg('count').reset_index()
# st.write(source)
# st.bar_chart(source, x="century", y="text", stack=False)


# Assuming 'df' is your DataFrame and 'text' is a column to count.
# Replace 'text' with the actual column name you want to count.

with tab_genre:
    df_by_genre = df.groupby("genre")["text"].size().reset_index(name='count')
    source_2 = df.groupby("genre")["num_tokens"].sum().reset_index()

    #st.write("Data grouped by genre:", df_by_genre)
    st.bar_chart(df_by_genre, x='genre', y='count', use_container_width=True)
    st.bar_chart(source_2, x='genre', y='num_tokens', use_container_width=True)


with tab_lang:
    # By language
    source = df.groupby("language")["text"].size().reset_index(name='count')
    source_2 = df.groupby("language")["num_tokens"].sum().reset_index()

    col_df, col_plot = st.columns(2)

    st.write(source_2)
    with col_df:
        # # Display the DataFrame in Streamlit
        #st.write("Data grouped by language:", source)
        st.bar_chart(source_2, x='language', y='num_tokens', use_container_width=True)

    with col_plot:
        # # Create a bar chart
        st.bar_chart(source, x='language', y='count', use_container_width=True)

with tab_genre_lang:
    df_by_genre = df.groupby(["genre", 'language'])["text"].size().reset_index(name='count')
    source_2 = df.groupby(["genre", 'language'])["num_tokens"].sum().reset_index()

    #st.write("Data grouped by genre:", df_by_genre)
    st.bar_chart(df_by_genre, x='language', y='count', color='genre', use_container_width=True, stack=False)
    st.bar_chart(source_2, x='language', y='num_tokens', color='genre', use_container_width=True, stack=False)


with tab_corpus:
    # By language
    source = df.groupby("corpus_name")["text"].size().reset_index(name='count')
    source_2 = df.groupby("corpus_name")["num_tokens"].sum().reset_index()
    source_mean = df.groupby("corpus_name")["num_tokens"].mean().reset_index()


    col_df, col_plot, col_mean = st.columns(3)
    
    with col_df:
        # # Display the DataFrame in Streamlit
        #st.write("Data grouped by language:", source)
        st.bar_chart(source_2, x='corpus_name', y='num_tokens', use_container_width=True)
        st.bar_chart(source_mean, x='corpus_name', y='num_tokens', use_container_width=True)



    with col_plot:
        # # Create a bar chart
        st.bar_chart(source, x='corpus_name', y='count', use_container_width=True)

    #ith col_mean:
        # # Create a bar chart


# import streamlit as st
# import pandas as pd

# # Example DataFrame creation (use your actual DataFrame 'df' instead)
# data = {
#     'century': [1200, 1300, 1400, 1200, 1300, 1400, 1200],  # Assume years are given, convert to centuries
#     'text': ['a', 'b', 'c', 'd', 'e', 'f', 'g']
# }
# df = pd.DataFrame(data)

# # Preprocessing to convert year to century if needed
# df['century'] = (df['century'] // 100) - 1  # Convert year to century, e.g., 1200 becomes 12

# # Group by 'century' and count occurrences in 'text'
# source = df.groupby("century")["text"].size().reset_index(name='count')

# # Display the DataFrame in Streamlit
# st.write("Data Grouped by Century:", source)

# # Create a bar chart
# st.bar_chart(source, x='century', y='count', use_container_width=True)
