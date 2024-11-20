import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

left_co, cent_co,last_co = st.columns([.2, .6, .2])
with left_co:
    st.image('logo-umk.png')


df = pd.read_excel('drop_out_dyscypliny_v2.xlsx')

df['Dziedzina nauk'] = df['Dziedzina nauk'].replace({'nauki społeczne': 'społeczne'}).str.strip()

kolory = {"społeczne": "#AA2896", "ścisłe i przyrodnicze": "#AAD23C", "inżynieryjno-techniczne": "#AAD23C", 
"humanistyczne": "#00AFFA", "teologiczne": "#00A550", "medyczne i o zdrowiu": "#FA1414",
"sztuka": "#FF8228", "weterynaryjne": "#AAD23C"}

markery = {"społeczne": "o", "ścisłe i przyrodnicze": "o", "inżynieryjno-techniczne": "P",     
"humanistyczne": "o", "teologiczne": "o", "medyczne i o zdrowiu": "o", "sztuka": "o", "weterynaryjne": "^"}

df['Dyscyplina'] = df['Dyscyplina'].replace({'nauki i Ziemi i środowisku': 'nauki o Ziemi i środowisku',
                         'nauka o zarządzaniu i jakości': 'nauki o zarządzaniu i jakości',
                         'nauka o zdrowiu': 'nauki o zdrowiu'})
df = df[df['przyjeci'] > 0]
col_dict = {}

st.subheader('Skreślenia na pierwszym roku studiów pierwszego stopnia rozpoczynających się w roku akademickim 2021/2022')

df2 = pd.read_excel('Dane/do_1st.xlsx').dropna(axis=0)
df2['drop_out_proc'] = df2['1 rok']/df2['Wszyscy']
df2['Dziedzina nauk'] = df2['Dziedzina nauk'].str.strip()
df2['markers'] = [markery[d] for d in df2['Dziedzina nauk']]
df2.rename(columns = {'1 rok': 'drop_out_sum'}, inplace=True)
y_tr2 = df2['drop_out_proc'].median()
x_tr2 = df2['drop_out_sum'].median()
st.plotly_chart(px.scatter(df2,
                    x = 'drop_out_sum', 
                    y = 'drop_out_proc',
                
                symbol = 'markers', color = 'Dziedzina nauk',         
                           width=1000, height=800,
                color_discrete_map=kolory,
                #        symbol_map=markery,
                hover_name = 'Kierunek wydziału',
                labels={
                     "drop_out_sum": "Liczba osób rezygnujących ze studiów",
                     "drop_out_proc": "Odsetek osób rezygnujących ze studiów"}).add_hline(y=y_tr2, 
                                                    line_width=1, 
                                                    line_dash="dash", 
                                                    line_color="gray").add_vline(x=x_tr2, 
                                                                                  line_width=1, 
                                                                                  line_dash="dash", 
                                                                                  line_color="gray"))


st.subheader('Łączna liczba skreśleń na studiach rozpoczynających się w roku akademickim 2021/2022')

for i, col in enumerate(df['Dyscyplina']):
    col_dict[col] = kolory[df.iloc[i, 2]]

df['kolor'] = [kolory[df.iloc[i, 2]] for i in range(df.shape[0])]
df['shape'] = [markery[df.iloc[i, 2]] for i in range(df.shape[0])]

ms_dict = {}
for i, col in enumerate(df['Dyscyplina']):
    ms_dict[col] = markery[df.iloc[i, 2]]






left_c, cent_c, right_c = st.columns([.2, .6, .2])
with cent_c:
    kat = st.selectbox('Proszę wybrać rodzaj studiów: ',['licencjackie','magisterskie','jednolite', 'inżynierskie'])

kat_tr = {'licencjackie': 'lic',
          'magisterskie': 'mag',
          'jednolite': 'jed', 
          'inżynierskie': 'inż.'}

if kat_tr[kat] == 'lic' or kat_tr[kat] == 'mag':
    y_tr = df[df['Rodzaj studiów'] == kat_tr[kat]]['drop_out_proc'].mean()
    x_tr = df[df['Rodzaj studiów'] == kat_tr[kat]]['drop_out_sum'].median()
elif kat_tr[kat] == 'jed':
    y_tr = df[df['Rodzaj studiów'] == kat_tr[kat]]['drop_out_proc'].median()
    x_tr = df[df['Rodzaj studiów'] == kat_tr[kat]]['drop_out_sum'].median()
else:
    y_tr = df[df['Rodzaj studiów'] == kat_tr[kat]]['drop_out_proc'].median()
    x_tr = df[df['Rodzaj studiów'] == kat_tr[kat]]['drop_out_sum'].mean()

l, c, r = st.columns([.2, .6, .2])
with c:
    st.plotly_chart(px.scatter(df[df['Rodzaj studiów'] == kat_tr[kat]],
                        x = 'drop_out_sum', 
                        y = 'drop_out_proc',
                    color = 'Dziedzina nauk', width=800, height=600,
                    color_discrete_map=kolory,
                               symbol_map=markery,
                        hover_name = 'Kierunek wydziału',
                            labels={
                         "drop_out_sum": "Liczba osób rezygnujących ze studiów",
                         "drop_out_proc": "Odsetek osób rezygnujących ze studiów"}).add_hline(y=y_tr, 
                                                        line_width=1, 
                                                        line_dash="dash", 
                                                        line_color="gray").add_vline(x=x_tr, 
                                                                                      line_width=1, 
                                                                                      line_dash="dash", 
                                                                                      line_color="gray"))
