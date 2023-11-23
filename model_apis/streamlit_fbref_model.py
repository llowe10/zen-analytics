import streamlit as st
from fbref_model import Predict

predictor = Predict()

try:
    df = predictor.load_data('C:/Users/lantz/OneDrive/Documents/My Tableau Repository/Datasources/fbref/ENG-Premier-League-18-23.csv')
    data = df.head()
    st.write("### Data", data.sort_index())
    # countries = st.multiselect(
    #     "Choose countries", list(df.index), ["China", "United States of America"]
    # )
    # if not countries:
    #     st.error("Please select at least one country.")
    # else:
    #     data = df.loc[countries]
    #     data /= 1000000.0
    #     st.write("### Gross Agricultural Production ($B)", data.sort_index())
except RuntimeError as e:
    st.error(
        e.reason
    )