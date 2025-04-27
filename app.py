import pandas as pd
import plotly.express as px
import streamlit as st

dfEV = pd.read_csv(r'C:\Users\danie\my-new-repo\Electric_Vehicle_Population_Data.csv')
st.title(":green[E]lectric :green[V]ehicles in :blue[Washington]")

st.write("This dataset contains information about Battery Electric Vehicles (BEVs) and Plug-in Hybrid Electric Vehicles (PHEVs) currently registered with the Washington State Department of Licensing (DOL). The data was obtained from Data.gov, an official website of the United States government")
st.header("Dataset Preview")
st.dataframe(dfEV.head())
st.write("This dataset contains information about Battery Electric Vehicles (BEVs) and Plug-in Hybrid Electric Vehicles (PHEVs) currently registered with the Washington State Department of Licensing (DOL). The data was obtained from Data.gov, an official website of the United States government")

# # # # # # # #BAR PLOT # # # # # # # #
st.header("Top 10 Electric Vehicle Brands", divider="rainbow")
current_year = 2025
make_counts = dfEV['Make'].value_counts().head(10).reset_index()
make_counts.columns = ['Make', 'Count']

fig = px.bar(make_counts, 
             x='Make',
             y='Count', 
             text='Count', 
             color='Make', 
             color_discrete_sequence=px.colors.qualitative.Vivid)

fig.update_layout(xaxis_title="Brand", yaxis_title="Number of Vehicles", xaxis_tickangle=45)

st.plotly_chart(fig)
st.write("This top ten plot is taken from data from data.wa.gov which is updated monthly and present only currently registered through Washington State Department of Licensing (DOL).")

# # # # # # # # # #  HISTPLOT # # # # # # # #
st.header("EV Brand Trends Over the Last 5 Years", divider=True)
last_5_years = dfEV[(dfEV['Model Year'] >= 2021) & (dfEV['Model Year'] <= 2025)]
brand_year_counts = last_5_years.groupby(['Model Year', 'Make']).size().reset_index(name='Vehicle Count')

fig = px.line(brand_year_counts, 
              x='Model Year', 
              y='Vehicle Count', 
              color='Make',              
              labels={'Model Year': 'Year', 'Vehicle Count': 'Number of Vehicles'}, 
              markers=True,
             color_discrete_sequence=px.colors.qualitative.Vivid)

fig.update_layout(xaxis_title="Year", yaxis_title="Number of Vehicles", xaxis=dict(tickmode='linear', tick0=current_year-5, dtick=1))
st.plotly_chart(fig)
st.write("In this graphic, we can see that Tesla has the fist place in the last 5 years, to have a better overview, we are going to remove Tesla from this chart, and see how the other brands has change thru the last 5 years.")

# # # # # # # # # # # # # HISTPLOT EXCLUDING TESLA # # # # # # # #
st.header("EV Brand Trends (Excluding TESLA)", divider=True)
df_no_tesla = dfEV[dfEV['Make'] != 'TESLA']
last_5_years_no_tesla = df_no_tesla[(df_no_tesla['Model Year'] >= 2021) & (df_no_tesla['Model Year'] <= 2025)]
brand_year_counts_no_tesla = last_5_years_no_tesla.groupby(['Model Year', 'Make']).size().reset_index(name='Vehicle Count')

fig = px.line(brand_year_counts_no_tesla, 
              x='Model Year', 
              y='Vehicle Count', 
              color='Make',              
              labels={'Model Year': 'Year', 'Vehicle Count': 'Number of Vehicles'}, 
              markers=True,
             color_discrete_sequence=px.colors.qualitative.Vivid)
fig.update_layout(xaxis_title="Year", yaxis_title="Number of Vehicles", xaxis=dict(tickmode='linear', tick0=current_year-5, dtick=1))
st.plotly_chart(fig)
st.write("This graph shows how closely contested the battle for second place has been each year.")


# # # # # # # # #  NUMBER INPUT # # # # # # #
st.header("Top 10 Popular EV Brands by Year", divider=True)
year = st.number_input("Select a Year", min_value=2000, max_value=2025, value=2020)
df_filtered = dfEV[dfEV['Model Year'] == year]
top_10_brands = df_filtered['Make'].value_counts().head(10)
st.write(f"Top 10 EV Brands in {year}:")
st.write(top_10_brands)



# # # # # # # # SCATTER PLOT # # # # # # # #
st.header("Electric Range vs Base MSRP", divider="blue")
st.write("Since we have many zeros and missing values in the Range and MSRP columns, we are going to drop them. Since there are no free cars or cars with zero range, we will assume that these zeros represent missing values.")
scatter_df = dfEV[(dfEV['Base MSRP'] > 0) & (dfEV['Electric Range'] > 0)]
fig = px.scatter(
    scatter_df,
    x='Base MSRP',
    y='Electric Range',
    color='Electric Vehicle Type',
    hover_data=['Make', 'Model', 'Model Year'],
    title='Electric Range vs Base Price (Cleaned Data)',
    labels={'Base MSRP': 'Base Price ($)', 'Electric Range': 'Range (miles)'},
    color_discrete_sequence=px.colors.qualitative.Vivid
)

fig.update_layout(
    xaxis_title="Base MSRP ($)",
    yaxis_title="Electric Range (miles)",
    height=600
)

st.plotly_chart(fig)

st.write("Here we can observe that price and range not be related, some cars (like luxury PHEVs) are expensive because of luxury features, not range and some cheap BEVs have excellent range because of efficient tech (e.g., small lightweight cars).")