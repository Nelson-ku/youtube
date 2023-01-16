import pandas as pd 
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st 
from datetime import datetime

@st.cache
def load_data():
    """ Loads in 4 dataframes and does light feature engineering"""
    df_agg = pd.read_csv('Aggregated_Metrics_By_Video.csv').iloc[1:,:]
    df_agg.columns = ['Video','Video title','Vtime','Comments added','Shares','Dislikes','Likes',
                      'Subscribers lost','Subscribers gained','RPM(USD)','CPM(USD)','Average % viewed','Average view duration',
                      'Views','Watch time (hours)','Subscribers','Your estimated revenue (USD)','Impressions','Impressions ctr(%)']
    df_agg['Vtime'] = pd.to_datetime(df_agg['Vtime'])
    df_agg['Average view duration'] = df_agg['Average view duration'].apply(lambda x: datetime.strptime(x,'%H:%M:%S'))
    df_agg['Avg_duration_sec'] = df_agg['Average view duration'].apply(lambda x: x.second + x.minute*60 + x.hour*3600)
    df_agg['Engagement_ratio'] =  (df_agg['Comments added'] + df_agg['Shares'] +df_agg['Dislikes'] + df_agg['Likes'])/df_agg.Views
    df_agg['Views / sub gained'] = df_agg['Views'] / df_agg['Subscribers gained']
    df_agg.sort_values('Vtime', ascending = False, inplace = True) 
    df_agg=pd.read_csv('Aggregated_Metrics_By_Video.csv').iloc[1:,:]
    df_agg_sub=pd.read_csv('Aggregated_Metrics_By_Country_And_Subscriber_Status.csv')
    df_comments=pd.read_csv('Aggregated_Metrics_By_Video.csv')
    df_time=pd.read_csv('Video_Performance_Over_Time.csv')
    df_time['Date'] = pd.to_datetime(df_time['Date'])
    return df_agg, df_agg_sub, df_comments, df_time

#create dataframes from the function 
df_agg, df_agg_sub, df_comments, df_time = load_data()

df_agg_diff=df_agg.copy()

# metric_date_12mo = df_agg_diff['Vtime'].max() - pd.DateOffset(months =12)
# median_agg = df_agg_diff[df_agg_diff['Vtime'] >= metric_date_12mo].median()
# numeric_cols = np.array((df_agg_diff.dtypes == 'float64') | (df_agg_diff.dtypes == 'int64'))
# df_agg_diff.iloc[:,numeric_cols] = (df_agg_diff.iloc[:,numeric_cols] - median_agg).div(median_agg)

#Just numeric columns

add_sidebar = st.sidebar.selectbox('Aggregate or Individual Video', ('Aggregate Metrics','Individual Video Analysis'))
if add_sidebar=='Aggregate Metrics':
    st.write('Agg')
if add_sidebar=='Individual Video Analysis':
    st.write('Ind')
