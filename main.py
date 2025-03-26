import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")

#perguntas (para uma visão mensal): 
#1. Qual o faturamento por unidade?
#2. Qual o tipo de produto mais vendido?
#3. Quanto cada filiam contribui?
#4. Qual o desempenho das formas de pagamento?
#5. Como estão as avaliações das filiais?

#transformando a data de string para date
df["Date"] = pd.to_datetime(df["Date"])
df=df.sort_values("Date")

#criando a coluna de mês por ano para facilitar a análise
df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))
month = st.sidebar.selectbox("Mês", df["Month"].unique())

df_filtered = df[df["Month"] == month]

#criando as colunas para colocar os gráficos
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)


#grafico da pergunta 1
fig_date = px.bar(df_filtered, x="Date", y="Total", color="City", title="Faturamento por dia")
col1.plotly_chart(fig_date, use_container_width=True)

#grafico da pergunta 2
fig_prod = px.bar(df_filtered, x="Date", y="Product line", 
                  color="City", title="Faturamento por tipo de produto",
                  orientation="h")
col2.plotly_chart(fig_prod, use_container_width=True)

#grafico da pergunta 3
#criando um novo dataframe agrupando por cidade, trazendo os valores totais por cidade
city_total = df_filtered.groupby("City")["Total"].sum().reset_index()

fig_city = px.bar(df_filtered, x="City", y="Total", 
                  title="Faturamento por filial")
col3.plotly_chart(fig_city, use_container_width=True)

#grafico da pergunta 4
fig_pay = px.pie(df_filtered, values="Total", names="Payment", 
                  title="Faturamento por tipo de pagamento")
col4.plotly_chart(fig_pay, use_container_width=True)

#grafico da pergunta 5 
filial_rate = df_filtered.groupby("City")["Rating"].mean().reset_index()

fig_rate = px.bar(df_filtered, y="Rating", x="City", 
                  title="Avaliação da filial")
col5.plotly_chart(fig_rate, use_container_width=True)
