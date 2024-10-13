import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
from sqlalchemy import create_engine
import pandas as pd
import requests
import json
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import streamlit as st
from bokeh.plotting import figure
import numpy as np


#MYSQL CONNECTION ,SQL ALCHEMY
mydb = mysql.connector.connect(host="localhost",user="root",password="",)
print(mydb)
mycursor = mydb.cursor(buffered=True)
user = 'root'
password = ''
host = '127.0.0.1'
port = 3306
database = 'PhonePe'

def get_connection():
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        )
    )
    
engine = get_connection()


#STREAMLIT PART

st.set_page_config(layout="wide")



        
with st.sidebar:
    selected = option_menu(None,
                        ["HOME","EXPLORE","INSIGHTS"],
                        icons=["house-door-fill","tools","card-text"],
                        default_index=0,
                        orientation="vertical",
                        styles={"nav-link":{"font-size": "20px", "text-align": "center", "margin": "0px", "--hover-color": "#8B008B"},
                        "icon": {"font-size": "30px"},
                        "container" : {"max-width": "6000px"},
                        "nav-link-selected": {"background-color": "#8B008B"}})


if selected =='HOME':
        st.title(':blue[PHONEPE DATA VISUALIZATION AND EXPLORATION]')
    
        st.write(" PhonePe is India's leading digital payments platform, offering a wide range of services to millions of users across the country. Founded in 2015, PhonePe has revolutionized the way people transact, making it simple, secure, and convenient to send and receive money, pay bills, recharge mobile phones, and much more, all from the comfort of their smartphones.")

        st.write(" With over a billion transactions processed every month,PhonePe collects vast amounts of data that provide valuable insights into consumer behavior, spending patterns, and emerging trends in the digital payments ecosystem.Our mission is to empower individuals, businesses, and policymakers with actionable insights derived from data, driving innovation, and fostering financial inclusion across the country.")

        st.subheader(":violet[TECHNOLOGIES USED]")
        
        st.write(" Technologies used in this project include GitHub Cloning, Python, Pandas, MySQL, mysql-connector-python, SQL_Alchemy,Streamlit, and Plotly.")
        
        st.subheader("Aim")
        st.write(" PhonePe Pulse is a project aimed at visualizing and exploring data related to various metrics and statistics available in the PhonePe Pulse GitHub repository.")
        
        st.subheader("Domain")
        st.write("Fintech")
        st.write(" The project falls under the domain of Fintech, focusing on analyzing transaction data and user behavior.")

        
        st.subheader("Final Approach")
        st.write(" Explore the insights and visualizations provided by the dashboard!")


elif selected =="EXPLORE":
    st.markdown("<h1 style='text-align: center; color:WHITE;'>EXPLORE</h1>", unsafe_allow_html=True)
    select = option_menu(None,options=["AGGREGATED", "MAP", "TOP"],default_index=0,orientation="horizontal",styles={"container": {"width": "100%"},"nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px"},"nav-link-selected": {"background-color": "#00008B"}})
    if select == "AGGREGATED":
        tab1, tab2 = st.tabs(["TRANSACTION","USER"])
        with tab1:
            col1, col2, col3 = st.columns([1,2,3])
            
            with col1:
                Agg_year = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022', '2023'), key='Agg_year')
                
            with col2:
                Agg_quarter = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='Agg_quarter')
                
            with col3:
                Agg_trans_type = st.selectbox('**Select Transaction type**',('Recharge & bill payments', 'Peer-to-peer payments','Merchant payments', 'Financial Services', 'Others'), key='Agg_trans_type')
                mycursor.execute(f"SELECT State,Transaction_amount FROM phonepe.agg_trans WHERE Year = '{Agg_year}' AND Quarter = '{Agg_quarter}' AND Transaction_type = '{Agg_trans_type}';")
                transaction_query = mycursor.fetchall()
                
                agg_transpd= pd.DataFrame(transaction_query,columns=['State', 'Transaction_amount'])
                
                agg_tran_output= agg_transpd.set_index(pd.Index(range(1, len(agg_transpd) + 1)))
                
                #geo visualization
                
                agg_transpd.drop(columns=['State'], inplace=True)
                url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response = requests.get(url)
                data1 = json.loads(response.content)
                state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
                state_names_tra.sort()
                
                df_state_names_tra = pd.DataFrame({'State': state_names_tra})

                df_state_names_tra['Transaction_amount']=agg_transpd

                df_state_names_tra.to_csv('agg_trans.csv', index=False)

                agg_trans = pd.read_csv('agg_trans.csv')
                
                fig = px.choropleth(
                    agg_trans,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Transaction_amount',
                    color_continuous_scale='rainbow',
                    title='Trans_Amount Analysis')
                fig.update_geos(fitbounds="locations", visible=False)

                fig.update_layout(title_font=dict(size=33), title_font_color='#7FFFD4', 
                                height=750,
                                geo=dict(scope='asia',
                                projection=dict(type='mercator'),
                                lonaxis=dict(range=[65.0, 100.0]),
                                lataxis=dict(range=[5.0, 40.0])))
                

                st.plotly_chart(fig, use_container_width=True)
                
                agg_tran_output['State'] = agg_tran_output['State'].astype(str)
                agg_tran_output['Transaction_amount'] = agg_tran_output['Transaction_amount'].astype(float)
                
                fig1 = px.sunburst(agg_tran_output, 
                                path=['State','Transaction_amount'], 
                                values='Transaction_amount',
                                color='Transaction_amount',
                                color_continuous_scale='rainbow',
                                title='TransactionAmount Chart',
                                height=500)
                fig1.update_layout(title_font=dict(size=33), title_font_color='#FFFFFF')

                st.plotly_chart(fig1, use_container_width=True)
            #agguser    
            with tab2:
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    
                    agg_user_yr = st.selectbox('Select Year', ['2018', '2019', '2020', '2021', '2022', '2023'], key='agg_user_yr')

                with col2:
                    
                    if agg_user_yr == '2022':
                        
                        in_us_qtr = st.selectbox('Select Quarter', ['1'], key='in_us_qtr')
                    else:
                        in_us_qtr = st.selectbox('Select Quarter', ['1', '2', '3', '4'], key='in_us_qtr')
                
                    
                mycursor.execute(f"SELECT State, SUM(Transaction_count) AS Total_Count FROM phonepe.agg_user WHERE Year = '{Agg_year}' AND Quarter = '{Agg_quarter}' GROUP BY State;")
                transaction_query2 = mycursor.fetchall()
                agg_userpd = pd.DataFrame(transaction_query2, columns=['State', 'User Count'])
                agg_user_output = agg_userpd.set_index(pd.Index(range(1, len(agg_userpd) + 1)))
                
                # GEO VISUALIZATION
                agg_userpd.drop(columns=['State'], inplace=True)
                url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response = requests.get(url)
                data2 = json.loads(response.content)
                state_names_user = [feature['properties']['ST_NM'] for feature in data2['features']]
                state_names_user.sort()
                user_state_names = pd.DataFrame({'State': state_names_user})
                user_state_names['User Count'] = agg_userpd['User Count'] 
                
                user_state_names.to_csv('user.csv', index=False)
                
                Agg_user = pd.read_csv('user.csv')

                fig2 = px.choropleth(
                    Agg_user,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='User Count',
                    color_continuous_scale='rainbow',
                    title='User Count Analysis'
                )

            
                fig2.update_geos(fitbounds="locations", visible=False)

                fig2.update_layout(title_font=dict(size=33), title_font_color='#7FFFD4', 
                                height=750,
                                geo=dict(scope='asia',
                                projection=dict(type='mercator'),
                                lonaxis=dict(range=[65.0, 100.0]),
                                lataxis=dict(range=[5.0, 40.0])))

                st.plotly_chart(fig, use_container_width=True)
                
                agg_user_output['State'] = agg_user_output['State'].astype(str)
                agg_user_output['Transaction_amount'] = agg_user_output['User Count'].astype(float)
                
                fig2 = px.sunburst(agg_user_output, 
                                path=['State','User Count'], 
                                values='User Count',
                                color='User Count',
                                color_continuous_scale='rainbow',
                                title='User Count Chart',
                                height=750)
                fig2.update_layout(title_font=dict(size=33), title_font_color='#FFFFFF')

                st.plotly_chart(fig1, use_container_width=True)
                
                
                                                        ########## MAP  #################
                                                            
                                                            
                                                            
                                                            
    if select == "MAP":
        tab3,tab4= st.tabs(["TRANSACTION","USER"]) 
        #map_trans
        with tab3:
                col1, col2, col3 = st.columns(3)
                with col1:
                    map_st = st.selectbox('**Select State**',('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                            'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                            ' Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                            'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                            'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                            'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                            'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                            'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                            'Uttarakhand', 'West Bengal'),key='st_tr_st')
                    map_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022','2023'), key='st_tr_yr')
                with col3:
                    map_qr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='st_tr_qtr')
                    
                #for bar chart
                mycursor.execute(f"SELECT Districts, Transaction_count FROM phonepe.map_trans WHERE State = '{map_st}' AND Year = '{map_yr}' AND Quarter = '{map_qr}';")
                mapquery = mycursor.fetchall()
                maptrans_df = pd.DataFrame(mapquery,columns=['Districts', 'Transaction_count'])
                map_tran_output = maptrans_df.set_index(pd.Index(range(1, len(maptrans_df) + 1)))
                
                map_fig = px.bar(map_tran_output, y='Transaction_count', x='Districts',title='Transaction Count Analysis by State')
                st.plotly_chart(map_fig, use_container_width=True)  

            

        #map_user        
        with tab4:
                col1, col2, col3 = st.columns(3)
                with col1:
                    map_st = st.selectbox('**Select State**', (
                        'Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                        'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                        'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                        'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                        'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                        'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                        'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                        'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                        'Uttarakhand', 'West Bengal'), key='map_st')
                with col2:
                    map_user_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022','2023'), key='map_user_yr')
                with col3:
                    map_user_qr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='map_user_qr')
                    
                mycursor.execute(f"SELECT Districts,RegisteredUsers FROM phonepe.map_user WHERE State = '{map_st}' AND Year = '{map_user_yr}' AND Quarter = '{map_user_qr}';")
                mapuserquery = mycursor.fetchall()
                map_user_df = pd.DataFrame(mapuserquery, columns=['Districts','RegisteredUsers'])
                map_user_output = map_user_df.set_index(pd.Index(range(1, len(map_user_df) + 1)))
                
                map_user_output['RegisteredUsers'] = map_user_output['RegisteredUsers'].astype(float)
                    
                map_user_fig = px.bar(map_user_output, x='Districts', y='RegisteredUsers',title='RegisteredUsers Analysis by District')
                
                map_user_fig.update_layout(title_font=dict(size=33),title_font_color='#8B008B',font=dict(size=14),height=500,width=600)

                
                st.plotly_chart(map_user_fig, use_container_width=True)

                

                

            

                
                
                                        ################### TOP ######################################################
                                        
    if select == "TOP":
            tab5 ,tab6 = st.tabs(["TRANSACTION","USER"])
            #top_trans
            with tab5:
                col1, col2, col3 = st.columns(3)
                with col1:
                    top_st = st.selectbox('**Select State**', (
                        'Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                        'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                        'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                        'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                        'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                        'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                        'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                        'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                        'Uttarakhand', 'West Bengal'), key='top_st')
                with col2:
                    
                    top_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022','2023'), key='top_yr')
                with col3:
                    top_qr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='top_qr')
                    
                    
                    mycursor.execute(f"SELECT State, SUM(Transaction_amount) FROM phonepe.top_trans WHERE Year = '{top_yr}' AND Quarter = '{top_qr}' GROUP BY State;")
                    top_transc_query = mycursor.fetchall()
                    df_top_transc_query = pd.DataFrame(top_transc_query, columns=['State', 'Transaction amount'])
                    df_top_transc_result = df_top_transc_query.set_index(pd.Index(range(1, len(df_top_transc_query) + 1)))
            
                    # GEO VISUALIZATION FOR USER

                    df_top_transc_query.drop(columns=['State'], inplace=True)

                    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                    response = requests.get(url)
                    data5 = json.loads(response.content)

                    top_state_names = [feature['properties']['ST_NM'] for feature in data5['features']]
                    top_state_names.sort()

                    df_state_names = pd.DataFrame({'State': top_state_names})

                    df_state_names['Transaction_amount'] = df_top_transc_query

                    df_state_names.to_csv('State_tran_amount.csv', index=False)

                    top_trans = pd.read_csv('State_tran_amount.csv')
                    st.write(top_trans)

                    # Geo plot
                    fig7 = px.choropleth(
                            top_trans,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Transaction_amount',
                            color_continuous_scale='rainbow',
                            title='transaction amount of top'
                        )

                    fig7.update_geos(fitbounds="locations", visible=False)

                    fig7.update_layout(title_font=dict(size=33), title_font_color='#7FFFD8', 
                                height=750,
                                geo=dict(scope='asia',
                                projection=dict(type='mercator'),
                                lonaxis=dict(range=[65.0, 100.0]),
                                lataxis=dict(range=[5.0, 40.0])))

                st.plotly_chart(fig7, use_container_width=True)
                
                    
                # Create the pie chart    
                mycursor.execute(f"SELECT Pincodes, Transaction_amount FROM phonepe.top_trans WHERE State = '{top_st}' AND Year = '{top_yr}' AND Quarter = '{top_qr}';")
                topcountquery = mycursor.fetchall()
                toptrans_df = pd.DataFrame(topcountquery, columns=['Pincodes','Transaction_amount'])
                toptrans_output = toptrans_df.set_index(pd.Index(range(1, len(toptrans_df) + 1)))
                toptrans_output['Pincodes'] = toptrans_output['Pincodes'].astype(float)
                toptrans_output['Transaction_amount'] = toptrans_output['Transaction_amount'].astype(int)

                #piechart
                toptrans_pie_fig = px.pie(toptrans_output, values='Transaction_amount', names='Pincodes',color_discrete_sequence=px.colors.sequential.Turbo,title='Pincodes')
                #color
                toptrans_pie_fig.update_layout(title_font=dict(size=33),title_font_color='#0000FF',font=dict(size=14),height=700,width=800)
                st.plotly_chart(toptrans_pie_fig, use_container_width=True)
                
            #top_user    
            with tab6:
                col1, col2, col3 = st.columns(3)
                with col1:
                    top_user_st = st.selectbox('**Select State**', (
                        'Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                        'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                        'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                        'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                        'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                        'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                        'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                        'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                        'Uttarakhand', 'West Bengal'), key='top_user_st')   
                with col2:
                    top_user_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022','2023'), key='top_user_yr')
                with col3:
                    top_user_qr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='top_user_qr')
                    
                mycursor.execute(f"SELECT State,RegisteredUsers FROM phonepe.top_user WHERE State='{top_user_st}' AND Year = '{top_user_yr}' AND Quarter = '{top_user_qr}'GROUP BY State;")
                top_user_query = mycursor.fetchall()
                df_top_user_query = pd.DataFrame(top_user_query,columns=['State','RegisteredUsers'])
                df_top_user_result = df_top_user_query.set_index(pd.Index(range(1, len(df_top_user_query) + 1)))
                
                df_top_user_query.drop(columns=['State'], inplace=True)
                

                url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response = requests.get(url)
                data6 = json.loads(response.content)

                top_user_state_names = [feature['properties']['ST_NM'] for feature in data6['features']]
                top_user_state_names.sort()

                

                
                mycursor.execute(f"SELECT State,Pincodes,RegisteredUsers FROM phonepe.top_user WHERE State='{top_user_st}' AND Year = '{top_user_yr}' AND Quarter = '{top_user_qr}'GROUP BY Pincodes;")
                top_user_query = mycursor.fetchall()
                df_top_user_query = pd.DataFrame(top_user_query,columns=['State','Pincodes', 'RegisteredUsers'])
                df_top_user_result = df_top_user_query.set_index(pd.Index(range(1, len(df_top_user_query) + 1)))

                topuser_fig = px.sunburst(df_top_user_result, path=['State', 'Pincodes', 'RegisteredUsers'], values='RegisteredUsers',color='RegisteredUsers',color_continuous_scale='mygbm',title='RegisteredUsers Chart',height=700,labels={'Pincodes': 'Pincode'})

                topuser_fig.update_layout(title_font=dict(size=33), title_font_color='#ff0007')
                st.plotly_chart(topuser_fig, use_container_width=True)
                
                #           #            <<<<<<<  DROPDOWNDOWN QUESTIONS   >>>>>>>     #          ##########
elif selected == 'INSIGHTS':

    st.write("<h1 style='color:blue;text-align:center;'> DROPDOWN QUESTIONS</h1>", unsafe_allow_html=True)
    
    options = ["--Select any of the Questions--",
            "1.What are the top 10 states in india with highest no.of Transaction amount?",
            "2.What are the last 5 states in india which have lowest no.of Transaction amount?",
            "3.What are the top 10 states which have highest no.of registeredusers ?",
            "4.How the transaction count vary by Brands?",
            "5.How does the transaction percentages vary among different states in 2020?",
            "6.what are the top 20  pincodes that which have highest registeredusers ?",
            "7.What are the top 22 states in india which have highest no.of registered users ?",
            "8.How does AppOpens vary by states?",
            "9.What are the top 16 districts have highest Transaction count?",
            "10.what are the states which have highest no.of AppOpens in 2020 ?"]
    select = st.selectbox("Select the option", options)
    
    if select=="1.What are the top 10 states in india with highest no.of Transaction amount?":
        mycursor.execute('SELECT State, SUM(Transaction_amount) AS total_transaction_amount FROM phonepe.agg_trans GROUP BY state ORDER BY total_transaction_amount DESC LIMIT 10;')
        total_transaction_amount=mycursor.fetchall()
        df = pd.DataFrame(total_transaction_amount, columns=['State', 'Transaction_amount'])
        st.write(df)
        fig = px.bar(df, x='State', y='Transaction_amount', title='Transaction amount Across Different State')
        fig.update_xaxes(type='category')
        fig.update_traces(marker_color='crimson')
        st.plotly_chart(fig, use_container_width=True)
        
        fig = px.choropleth(
                            df,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Transaction_amount',
                            color_continuous_scale='rainbow',
                            title='top 10 states high transaction amount'
                        )

        fig.update_geos(fitbounds="locations", visible=False)

        fig.update_layout(title_font=dict(size=33), title_font_color='#7FFFD8', 
                                height=750,
                                geo=dict(scope='asia',
                                projection=dict(type='mercator'),
                                lonaxis=dict(range=[65.0, 100.0]),
                                lataxis=dict(range=[5.0, 40.0])))

        st.plotly_chart(fig, use_container_width=True)
        
    elif select=="2.What are the last 5 states in india which have lowest no.of Transaction amount?":
        mycursor.execute('SELECT State, SUM(Transaction_amount) AS Total_Transaction_amount FROM phonepe.agg_trans GROUP BY State ORDER BY Transaction_amount ASC LIMIT 5;')
        total_low_transaction_amount=mycursor.fetchall()
        df2 = pd.DataFrame(total_low_transaction_amount, columns=['State', 'Transaction_amount'])
        st.write(df2)
        fig2 = px.line(df2, x='State', y='Transaction_amount', title='Transaction amount Across Different lowest State')
        fig2.update_xaxes(type='category')
        fig2.update_traces(marker_color='purple')
        st.plotly_chart(fig2, use_container_width=True)
        
    elif select=="3.What are the top 10 states which have highest no.of registeredusers ?":
        mycursor.execute('SELECT State, SUM(RegisteredUsers) AS RegisteredUsers FROM phonepe.map_user GROUP BY State ORDER BY Registeredusers DESC LIMIT 10;')
        RegisteredUsers_query=mycursor.fetchall()
        df3 = pd.DataFrame(RegisteredUsers_query, columns=['State','RegisteredUsers'])
        st.write(df3)
        fig3 = px.bar(df3, x='State', y='RegisteredUsers', title='RegisteredUsers of top 10 states')
        fig3.update_xaxes(type='category')
        fig3.update_traces(marker_color='orange')
        st.plotly_chart(fig3, use_container_width=True)

    elif select=="4.How the transaction count vary by Brands?":
        mycursor.execute("SELECT Brands,SUM(Transaction_count)AS total_count FROM phonepe.agg_user GROUP BY Brands;")
        brand_trans_query = mycursor.fetchall()
        df4 = pd.DataFrame(brand_trans_query, columns=['Brands','Transaction_count'])
        st.write(df4)
        fig4 = px.bar(df4, y='Transaction_count', x='Brands', title='Transaction_count vary by Brands')
        fig4.update_xaxes(type='category')
        st.plotly_chart(fig4, use_container_width=True)
        
    elif select== "5.How does the transaction percentages vary among different states in 2020?":
        mycursor.execute("SELECT State, Year, Percentage FROM phonepe.agg_user WHERE Year = 2020 GROUP BY State ORDER BY State,Percentage DESC;")
        transaction_per_query= mycursor.fetchall()
        df5 = pd.DataFrame(transaction_per_query, columns=["State", "Year", "Percentage"])
        st.write(df5)
        fig5= px.line(df5, x='State', y='Percentage', title=' In 2020 percent vary from state')
        fig5.update_xaxes(type='category')
        fig5.update_traces(marker_color='red')
        st.plotly_chart(fig5, use_container_width=True)
        
    elif select== "6.what are the top 20  pincodes that which have highest registeredusers ?":
        mycursor.execute('SELECT Pincodes, COUNT(RegisteredUsers) AS registered_Users FROM phonepe.top_user GROUP BY Pincodes ORDER BY RegisteredUsers DESC LIMIT 34;')
        pincodes_reg_query=mycursor.fetchall()
        df6 = pd.DataFrame(pincodes_reg_query, columns=["Pincodes","RegisteredUsers"])
        st.write(df6)
        fig6 = px.pie(df6, values="RegisteredUsers", names="Pincodes", title="Registered Users by Pincodes")
        fig6.update_traces(textposition='inside', textinfo='label+value+percent')
        fig6.update_layout(height=600, width=800)
        st.plotly_chart(fig6,use_container_width=True)
        
        
    elif select=="7.What are the top 22 states in india which have highest no.of registered users ?":
        mycursor.execute("SELECT State, MAX(RegisteredUsers) AS max_users FROM phonepe.top_user GROUP BY State ORDER BY max_users DESC LIMIT 22;")
        reg_user_query=mycursor.fetchall()
        df7 = pd.DataFrame(reg_user_query, columns=["State","RegisteredUsers"])
        st.write(df7)
        fig7 = go.Figure(data=[go.Bar(x=df7['State'], y=df7['RegisteredUsers'], text=df7['RegisteredUsers'],marker_color='purple',)])
        fig7.update_layout(title='Registered Users by State', xaxis_title='State',yaxis_title='Registered Users')
        st.plotly_chart(fig7, use_container_width=True) 
        
    elif select=="8.How does AppOpens vary by states?":
        mycursor.execute('SELECT State, SUM(AppOpens) AS total_opens FROM phonepe.map_user GROUP BY AppOpens')
        appOpens_query=mycursor.fetchall()
        df8 = pd.DataFrame(appOpens_query, columns=["State","AppOpens"])
        st.write(df8)
        fig8 = px.pie(df8, values='AppOpens', names='State', title='App Opens by State', hole=0.4)  # Create a donut chart
        fig8.update_traces(marker_colors=['#FFD700', '#FF8C00', '#00FF00', '#0000FF', '#FF00FF', '#808080'],
                textinfo='label+value+percent',  # Display label, value, and percentage
                textposition='outside')
        fig8.update_layout(legend_title='State', font_family='Arial', font_size=14)
        st.plotly_chart(fig8, use_container_width=True)
        
        
    elif select=="9.What are the top 16 districts have highest Transaction count?":
        mycursor.execute('SELECT Districts, SUM(Transaction_amount) AS Transaction_amount FROM phonepe.map_trans GROUP BY Districts ORDER BY Transaction_amount DESC LIMIT 16;')
        Trans_query=mycursor.fetchall()
        df9 = pd.DataFrame(Trans_query, columns=['Districts','Transaction_amount'])
        st.write(df9)
        fig9 = px.pie(df9, names='Districts', values='Transaction_amount', title='top 16 highest transaction count', color_discrete_sequence=px.colors.sequential.Viridis)
        fig9.update_layout(xaxis_title='Districts', yaxis_title='Transaction_amount')
        st.plotly_chart(fig9, use_container_width=True)
        
    elif select=="10.what are the states which have highest no.of AppOpens in 2020 ?":
        mycursor.execute('SELECT State, COUNT(AppOpens) AS total_app_opens FROM phonepe.map_user WHERE YEAR = 2020 GROUP BY State ORDER BY total_app_opens DESC LIMIT 7;')
        appopen_2020_query=mycursor.fetchall()
        df10 = pd.DataFrame(appopen_2020_query, columns=['State','AppOpens'])
        st.write(df10)
        fig10 = px.bar(df10, x='State', y='AppOpens', title='Top App Opens states in 2020',color_discrete_sequence=px.colors.sequential.Viridis)
        fig10.update_layout(xaxis_title='State', yaxis_title='AppOpens')
        st.plotly_chart(fig10, use_container_width=True)
            
    