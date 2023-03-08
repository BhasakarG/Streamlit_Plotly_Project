
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

## output page configuration, wide shows map in wider
st.set_page_config(layout='wide')

## Here , I am using 2 datas sets (1) which gives the Lat. & Long. values (Geo-spatial Indexing)
## (2) country (India) census Information and details are based on lat. & long.

## TO-DO --> Display the census details on the map based on the Longitude & Latitude

## vvv **** Start of code for data fetching
latlong_df      = pd.read_csv("project_dataset/district wise centroids.csv")
census_2011_df  = pd.read_csv("project_dataset/india-districts-census-2011.csv")

# taking a few columns as below from census_2011 (country=India) dataframe for building the project
census_col = ['District code',
              'District name',
              'Population',
              'Male','Female',
              'Literate',
              'Male_Literate',
              'Female_Literate',
              'Cultivator_Workers',
              'Agricultural_Workers',
              'Households_with_Internet',
              'Housholds_with_Electric_Lighting',
              'Having_latrine_facility_within_the_premises_Total_Households',
              'Not_having_latrine_facility_within_the_premises_Alternative_source_Open_Households',
              'Total_Power_Parity']

census_2011_df = census_2011_df[census_col]

# now merge latlong DF with census_2011_df on column "District" & "Disrict name",
# after merge, there exists same information in District & District Name columns
# hence we are delete one column, here removing "District" and saving into final_df

final_df = latlong_df.merge(census_2011_df,left_on='District',right_on='District name').drop(columns='District')

# now calculate the sex ratio, and add as a new column ("Sex_Ratio")
# Sex ratio=(Female Population)*1000/(Male Population)
# => number of females per thousand males
final_df['Sex_Ratio'] = round((final_df['Female']*1000 / final_df['Male']))

# now Calculate the Literatcy Rate, and add another new column ("Literate_Ratio")

final_df['Literate_Ratio'] =  round(final_df['Literate'] / final_df['Population']*100)

# collect all the State names in list to display in dropdown, and add "Overall India" at the first index
list_of_states = list(final_df['State'].unique())
list_of_states.insert(0,'Overall India')

## ^^^ **** End of code for data fetching


### ****
# following code is streamlit related code
# Here, creating the format of the GUI, like sidebar & main window
# taking only the columns from 5, which are displaying in Primary/Secondary dropdown
st.sidebar.title("India Census Data Visualization ")
state_selected = st.sidebar.selectbox("-- Select the State --",list_of_states)
primary_select = st.sidebar.selectbox("-- Primary Selection --", final_df.columns[5:] )
secondary_select = st.sidebar.selectbox("-- Secondary Selection --", final_df.columns[5:] )
plot = st.sidebar.button("Plot Graph")

if plot:
    if state_selected == 'Overall India' :
        st.text("Color Represents Primary Parameter")
        st.text("Size Represents Secondary Parameter")
        fig = px.scatter_mapbox(final_df, lat="Latitude", lon="Longitude",
                                zoom=4,hover_name='District name',
                                width=1200, height=800,
                                size= secondary_select,
                                color= primary_select,
                                mapbox_style="carto-positron")
        st.plotly_chart(fig,use_container_width=True)

    else:
        ## Selected States
        state_df = final_df[final_df['State'] == state_selected]

        fig = px.scatter_mapbox(state_df, lat="Latitude", lon="Longitude",
                                zoom=4,hover_name='District name',
                                width=1200, height=800,
                                size= secondary_select,
                                color= primary_select,
                                mapbox_style="carto-positron")
        st.plotly_chart(fig,use_container_width=True)

        pass




