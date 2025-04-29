import pandas as pd
import plotly.express as px
import streamlit as st
import pyarrow as pa


dfEV = pd.read_csv('Electric_Vehicle_Population_Data.csv')
#try:
 #   table = pa.Table.from_pandas(dfEV)
  #  print("PyArrow conversion successful!")
#except Exception as e:
 #   print(f"PyArrow conversion failed: {e}")
#print(dfEV.dtypes)

#dfEV = dfEV.drop(columns=['VIN (1-10)'])
#dfEV = dfEV.drop(columns=['City'])
#dfEV = dfEV.drop(columns=['County'])
#dfEV['State'] = dfEV['State'].astype(str)
#dfEV['State'] = dfEV['State'].fillna('Unknown')
#dfEV = dfEV.applymap(lambda x: str(x) if not pd.isnull(x) else x)
dfEV.columns = dfEV.columns.str.replace(' ', '_')
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
last_5_years = dfEV[(dfEV['Model_Year'] >= 2021) & (dfEV['Model_Year'] <= 2025)]
brand_year_counts = last_5_years.groupby(['Model_Year', 'Make']).size().reset_index(name='Vehicle_Count')

fig = px.line(brand_year_counts, 
              x='Model_Year', 
              y='Vehicle_Count', 
              color='Make',              
              labels={'Model_Year': 'Year', 'Vehicle_Count': 'Number of Vehicles'}, 
              markers=True,
             color_discrete_sequence=px.colors.qualitative.Vivid)

fig.update_layout(xaxis_title="Year", yaxis_title="Number of Vehicles", xaxis=dict(tickmode='linear', tick0=current_year-5, dtick=1))
st.plotly_chart(fig)
st.write("In this graphic, we can see that Tesla has the fist place in the last 5 years, to have a better overview, we are going to remove Tesla from this chart, and see how the other brands has change thru the last 5 years.")

# # # # # # # # # # # # # HISTPLOT EXCLUDING TESLA # # # # # # # #
st.header("EV Brand Trends (Excluding TESLA)", divider=True)
df_no_tesla = dfEV[dfEV['Make'] != 'TESLA']
last_5_years_no_tesla = df_no_tesla[(df_no_tesla['Model_Year'] >= 2021) & (df_no_tesla['Model_Year'] <= 2025)]
brand_year_counts_no_tesla = last_5_years_no_tesla.groupby(['Model_Year', 'Make']).size().reset_index(name='Vehicle_Count')

fig = px.line(brand_year_counts_no_tesla, 
              x='Model_Year', 
              y='Vehicle_Count', 
              color='Make',              
              labels={'Model_Year': 'Year', 'Vehicle_Count': 'Number of Vehicles'}, 
              markers=True,
             color_discrete_sequence=px.colors.qualitative.Vivid)
fig.update_layout(xaxis_title="Year", yaxis_title="Number of Vehicles", xaxis=dict(tickmode='linear', tick0=current_year-5, dtick=1))
st.plotly_chart(fig)
st.write("This graph shows how closely contested the battle for second place has been each year.")


# # # # # # # # #  NUMBER INPUT # # # # # # #
st.header("Top 10 Popular EV Brands by Year", divider=True)
year = st.number_input("Select a Year", min_value=2000, max_value=2025, value=2020)
df_filtered = dfEV[dfEV['Model_Year'] == year]
top_10_brands = df_filtered['Make'].value_counts().head(10)
st.write(f"Top 10 EV Brands in {year}:")
st.write(top_10_brands)



# # # # # # # # SCATTER PLOT # # # # # # # #
st.header("Electric Range vs Base MSRP", divider="blue")
st.write("Since we have many zeros and missing values in the Range and MSRP columns, we are going to drop them. Since there are no free cars or cars with zero range, we will assume that these zeros represent missing values.")
scatter_df = dfEV[(dfEV['Base_MSRP'] > 0) & (dfEV['Electric_Range'] > 0)]
fig = px.scatter(
    scatter_df,
    x='Base_MSRP',
    y='Electric_Range',
    color='Electric Vehicle Type',
    hover_data=['Make', 'Model', 'Model_Year'],
    title='Electric Range vs Base Price (Cleaned Data)',
    labels={'Base_MSRP': 'Base Price ($)', 'Electric_Range': 'Range (miles)'},
    color_discrete_sequence=px.colors.qualitative.Vivid
)

fig.update_layout(
    xaxis_title="Base MSRP ($)",
    yaxis_title="Electric Range (miles)",
    height=600
)

st.plotly_chart(fig)

st.write("Here we can observe that price and range not be related, some cars (like luxury PHEVs) are expensive because of luxury features, not range and some cheap BEVs have excellent range because of efficient tech (e.g., small lightweight cars).")
