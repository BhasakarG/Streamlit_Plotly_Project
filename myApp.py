import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

## output page configuration

st.set_page_config(layout='wide')

## **** Start of code for data fetching
latlong_df      = pd.read_csv("project_dataset/district wise centroids.csv")
census_2011_df  = pd.read_csv("project_dataset/india-districts-census-2011.csv")

# take a few columns from census_2011 dataframe for building the project
cencus_col = ['District code','District name','Population',
              'Male','Female', 'Literate',
              'Male_Literate', 'Female_Literate',
              'Cultivator_Workers',
             'Agricultural_Workers',
             'Households_with_Internet','Housholds_with_Electric_Lighting',
             'Having_latrine_facility_within_the_premises_Total_Households',
             'Not_having_latrine_facility_within_the_premises_Alternative_source_Open_Households',
             'Total_Power_Parity']

census_2011_df = census_2011_df[cencus_col]

# now merge latlong DF with census_2011_df,
# after merge, there exists same information in District & District Name columns
# hence we are deleting "District" and saving into final_df
final_df = latlong_df.merge(census_2011_df,left_on='District',right_on='District name').drop(columns='District')


# now calculate sex ratio, and add as a new column
# Sex ratio=(Female Population)*1000/(Male Population)
# => number of females per thousand males
final_df['Sex Ratio'] = round((final_df['Female']*1000 / final_df['Male']))

## Calculating the Literatcy Rate
final_df['Literate Ratio'] =  round(final_df['Literate'] / final_df['Population']*100)

# collect all the state name in list to display in dropdown
list_of_states = list(final_df['State'].unique())
list_of_states.insert(0,'Overall India')


## **** End of code for data fetching



### ****
# following code is streamlit related code

st.sidebar.title("India Census Data Visualization ")
state_selected = st.sidebar.selectbox("-- Select the State --",list_of_states)
primary_select = st.sidebar.selectbox("-- Primary Selection --", final_df.columns[5:] )
secondary_select = st.sidebar.selectbox("-- Secondary Selection --", final_df.columns[5:] )

plot = st.sidebar.button("Plot Graph")

if plot:
    st.text("Color Represents Primary Parameter")
    st.text("Size Represents Secondary Parameter")
    if state_selected == 'Overall India' :
        fig = px.scatter_mapbox(final_df, lat="Latitude", lon="Longitude",
                                zoom=5,hover_name='District name',
                                width=1000, height=800,
                                size= secondary_select,
                                color= secondary_select,
                                mapbox_style="carto_position")
        st.plotly_chart(fig,use_container_width=True)
    else:
        pass

