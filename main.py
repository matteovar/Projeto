import streamlit as st
import pandas as pd

st.title("Number of foster kids in US over the years")

df = pd.read_csv('adoptios_Usa_2013_2022.csv')


df["Year"] = pd.to_datetime(df["Year"], format="%Y")
df.set_index("Year", inplace=True)

st.subheader("National Data")
st.line_chart(df[['Served', "Adopted"]])

df_adopted = pd.read_csv('estates_adopteds.csv')
df_served = pd.read_csv('estates_served.csv')

st.subheader("States Data ")
df_adopted.columns = ['State'] + [col.replace("FY ", "") for col in df_adopted.columns[1:]]
df_served.columns = ['State'] + [col.replace("FY ", "") for col in df_served.columns[1:]]

selected_states = st.multiselect(
    "Escolha um ou mais Estados:",
    options=df_adopted["State"].unique(),
    default=['Alaska']  
)

def prepare_state_data(df, states):
    return df[df["State"].isin(states)].set_index("State").T

if selected_states:
    adopted_data = prepare_state_data(df_adopted, selected_states)
    served_data = prepare_state_data(df_served, selected_states)
    
    comparison_data = pd.concat([adopted_data.add_suffix(' (Adopted)'),served_data.add_suffix(' (Served)')], axis=1)
    
    comparison_data = comparison_data.sort_index(axis=1)
    
    st.subheader("State Comparison: Adopted vs Served")
    st.bar_chart(comparison_data)
else:
    st.warning("Por favor, selecione pelo menos um estado.")