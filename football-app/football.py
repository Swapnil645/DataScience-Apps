

import matplotlib
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np



st.title('NFL Football Stats (Rushing) Explorer')

st.markdown("""
This app performs simple webscarping of NFL Football player stats data
* **Python libraries:** base64, pandas, streamlit
* **Data Source:** [pro-football-reference.com] (https://www.pro-football-reference.com/years/2020/rushing.htm
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year',list(reversed(range(1990,2020))))

def load_data(year):
    url = "https://www.pro-football-reference.com/years/" + str(year) +"/rushing.htm"
    html = pd.read_html(url,header = 1)    ### webscraping througfh pandas
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)
    raw.fillna(0,inplace=True)
    playerstats = raw.drop(['Rk'], axis = 1)
    return playerstats

playerstats = load_data(selected_year)

sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team',sorted_unique_team,sorted_unique_team)
unique_pos = ['RB','QB','WR','FB','TE']
selected_pos = st.sidebar.multiselect('Position',unique_pos,unique_pos)

#Filtering data according to teamand position and year
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]




st.header('Display Stats of Selected Team(s)')
st.write('Data Dimension: {} rows and {} columns'.format(playerstats.shape[0],playerstats.shape[1]))
st.dataframe(df_selected_team)


#Download NBA player stats data
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 =base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team),unsafe_allow_html=True)
 #Heatmap
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_team.to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(f)



