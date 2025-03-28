import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(
    page_title="US Foster Care Dashboard",
    layout="wide"
)

st.markdown("<h1 style='text-align: center;'>Children in Foster Care in the United States</h1>", 
            unsafe_allow_html=True)

df = pd.read_csv('data/adoptios_Usa_2013_2022.csv')

df["Year"] = pd.to_datetime(df["Year"], format="%Y")
df.set_index("Year", inplace=True)

def card1():
    # Resetando o índice
    df.reset_index(inplace=True)

    # Selecionar os dados de 2013 e 2021
    adopted_2013 = df.loc[df["Year"].dt.year == 2013, "Adopted"].values[0]
    adopted_2021 = df.loc[df["Year"].dt.year == 2021, "Adopted"].values[0]

    # Calcular o crescimento percentual
    growth_percentage = ((adopted_2021 - adopted_2013) / adopted_2013) * 100
    
    return adopted_2021, growth_percentage  

def card2():
    # Resetando o índice
    df.reset_index(inplace=True)

    # Selecionar os dados de 2013 e 2021
    served_2013 = df.loc[df["Year"].dt.year == 2013, 'Served'].values[0]
    served_2021 = df.loc[df["Year"].dt.year == 2021, 'Served'].values[0]

    # Calcular o crescimento percentual (2013 para 2021)
    growth_served = ((served_2021 - served_2013) / served_2013) * 100
    
    return served_2021, growth_served  

def cards():
    # Chama as funções card1 e card2 passando o df
    adopted_2021, growth_percentage = card1()
    served_2021, growth_served = card2()
    
    # Definindo os valores para o cartão
    data = {
        'Label': ['Adopted', 'Served', 'Growth of Adoptions', 'Total Children'],
        'Value': [f'{adopted_2021:1}', served_2021, 56.7, 912345],
        'Delta': [f'{growth_percentage:.2f}%', f'{growth_served:.2f}%', 12.3, 313]  
    }   
    
    df_cards = pd.DataFrame(data)

    # Dividindo o layout em 4 colunas
    cols = st.columns(4)  

    
    for idx, row in df_cards.iterrows():
        col_idx = idx % 4
        with cols[col_idx]:
            if row['Delta'] is not None:
                # Usando st.metric para exibir o valor e a variação percentuals
                st.metric(
                    label=row['Label'],
                    value=row['Value'],
                    delta=row['Delta'],
                    border = True
                )
            else:
                st.write(f"{row['Label']}: {row['Value']}")

cards()

df_adopted = pd.read_csv('data/estates_adopteds.csv')
df_served = pd.read_csv('data/estates_served.csv')

col = st.columns((2.5, 4.5, 2.5), gap='medium')
col1, col2, col3 = st.columns(3)

def nation_kids():
    st.markdown('''
    
    ''')
    st.line_chart(df[['Served', "Adopted"]])


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
    
    ''')
    
    df = pd.DataFrame(
        {
            "Year": ["2021"] * 5,  
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
   
   