########################
# Import Libraries

import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

########################
# Page config
st.set_page_config(
    page_title="US foster kids",
    layout="wide"
)
alt.themes.enable('dark')

########################
# Title

st.markdown("<h1 style='text-align: center;'>Children in Foster Care in the United States</h1>", 
            unsafe_allow_html=True)
######################## 
# Load file
df = pd.read_csv('data/adoptios_Usa_2013_2022.csv')
df_adopted = pd.read_csv('data/estates_adopteds.csv')
df_served = pd.read_csv('data/estates_served.csv')

########################
    # Define format Year and put Year as fixed X
df["Year"] = pd.to_datetime(df["Year"], format="%Y")
df.set_index("Year", inplace=True)

######################## 
# Columns
col = st.columns((2.5,4.5,2.5), gap='medium')

def nation_kids():
    st.markdown('''
    ### National Trends: Children in Foster Care vs. Adopted (2013-2022)
    ''')
    st.line_chart(df[['Served', "Adopted"]])
    
    
    df.reset_index(inplace=True)

    # Selecionar os dados de 2013 e 2022
    adopted_2013 = df.loc[df["Year"].dt.year == 2013, "Adopted"].values[0]
    adopted_2021 = df.loc[df["Year"].dt.year == 2021, "Adopted"].values[0]

    # Calcular o crescimento percentual
    growth_percentage = ((adopted_2021 - adopted_2013) / adopted_2013) * 100
    
    st.markdown(f'''
    #### From 2013 to 2022, the adoption rate from foster care increased by :green[↑{growth_percentage:.2f}%] nationally
    ''')

def states_kids():
    st.subheader("States Data ")
    df_adopted.columns = ['State'] + [col.replace("FY ", "") for col in df_adopted.columns[1:]]
    df_served.columns = ['State'] + [col.replace("FY ", "") for col in df_served.columns[1:]]


    selected_states = st.multiselect(
        "Select one or more states:",
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
        
        st.subheader("State Comparison: Adopted vs Served by Year")
        st.bar_chart(comparison_data)
    else:
        st.warning("Por favor, selecione pelo menos um estado.")
    
    
def age():
    st.markdown('''
    ### Key Foster Care Statistics (2021)
    ''')
    
    df = pd.DataFrame(
        {
            "Year": ["2021"] * 5,  # Repetindo "2021" para cada linha
            "Age": ['< 1', '1 to 5', '6 to 10', '11 to 15', '16 to 20'],
            "Number": [28.690, 133.049, 87.383, 86.793, 55.396],
        }
    )

    ano = df[df["Year"] == "2021"]
    
    data_age = ano[ano["Age"].isin(['< 1', '1 to 5', '6 to 10', '11 to 15', '16 to 20'])][["Age", "Number"]]

    fig = px.pie(
        data_age,
        names='Age',
        values='Number',
        title='Distribution of age group',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
def gender():
    df = pd.DataFrame(
        {
            "Year": ["2021"]*2,
            "Gender": ["Male", "Female"],
            "Number":[210622,191518],
        }
    )
    
    ano = df[df["Year"]=='2021']
    data_gender = ano[ano["Gender"].isin(["Male", "Female"])][["Gender", "Number"]]
    
    fig1 = px.pie(
        data_gender,
        names='Gender',
        values='Number',
        title='Distribution of gender group',
        color_discrete_sequence=px.colors.qualitative.G10
    )
    
    st.plotly_chart(fig1, use_container_width=True)
    
with col[0]:
    
    age()
    gender()
    
   
with col[1]:
    nation_kids()
    
    
    st.divider()

    states_kids()
   
   