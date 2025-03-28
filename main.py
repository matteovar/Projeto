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

st.markdown("<h1 style='text-align: center; '>Foster Kids in US</h1>", unsafe_allow_html=True)

######################## 
# Load file
df = pd.read_csv('data/adoptios_Usa_2013_2022.csv')
df_age = pd.read_csv('data/age.csv')
df_adopted = pd.read_csv('data/estates_adopteds.csv')
df_served = pd.read_csv('data/estates_served.csv')

########################
    # Define format Year and put Year as fixed X
df["Year"] = pd.to_datetime(df["Year"], format="%Y")
df.set_index("Year", inplace=True)

######################## 
# Columns
col = st.columns((2.5,4.5,2.5), gap='medium')

with col[0]:
    df.reset_index(inplace=True)

    # Selecionar os dados de 2013 e 2022
    adopted_2013 = df.loc[df["Year"].dt.year == 2013, "Adopted"].values[0]
    adopted_2022 = df.loc[df["Year"].dt.year == 2022, "Adopted"].values[0]

    # Calcular o crescimento percentual
    growth_percentage = ((adopted_2022 - adopted_2013) / adopted_2013) * 100

    # Exibir o crescimento percentual usando st.metric
    st.metric(
        label="Crescimento Percentual de Adoções",
        value=f"{adopted_2022}",
        delta=f"{growth_percentage:.2f}%",
        delta_color="normal" if growth_percentage > 0 else "red",
        border = True,
        
    )
    st.markdown('''
                *Comparacao de crescimento de 2013 e 2022*
                ''')
    
    st.divider()
    
    ano_selecionado = st.selectbox(
        "Selecione o ano",
        options = df_age["Year"],
        index =0 
    )
    
    dados_ano = df_age[df_age['Year'] == ano_selecionado]
    
    faixa_etarias = ['< 1','1 to 5', '6 to 10', '11 to 15', '16 to 20']
    dados_pizza = dados_ano[faixa_etarias].transpose().reset_index()
    dados_pizza.columns = ['Faixa Etaria', 'Quantidade']
    
    fig = px.pie(
        dados_pizza,
        names = 'Faixa Etaria',
        values = 'Quantidade',
        title = f'Distirbuicao de Faixa Etaria - {ano_selecionado}',
        color_discrete_sequence = px.colors.qualitative.Pastel,˜
    )
    
    st.plotly_chart(fig,use_container_width = True)
with col[1]:
    ######################## 
    # Create Chart
    st.markdown('''
    ### Country comparation: Served x Adopted by Year
    ''')
    st.line_chart(df[['Served', "Adopted"]])
    st.markdown('''
    *Here is showing the difference by the number of foster kids in foster care  
                 and the number of adoptions that were realised in the entered year from **2013 to 2022** in the US*    
    ''')

    st.divider()

    ########################
    # Set Column and Lines
    st.subheader("States Data ")
    df_adopted.columns = ['State'] + [col.replace("FY ", "") for col in df_adopted.columns[1:]]
    df_served.columns = ['State'] + [col.replace("FY ", "") for col in df_served.columns[1:]]

    ######################## 
    # Create Multiselect
    selected_states = st.multiselect(
        "Select one or more states:",
        options=df_adopted["State"].unique(),
        default=['Alaska']  
    )

    ########################
    # Confire the main page with the usage of multisellect
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
    
    st.markdown('''
    *Here is showing the difference by the number of foster kids in foster care  
                 and the number of adoptions that were realised in the entered year from **2013 to 2022** by states in the US*    
    ''')
