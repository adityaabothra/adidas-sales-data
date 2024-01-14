import streamlit as st
import pandas as pd
import inspect
import textwrap
import plotly_express as px


def show_code(demo):
    """Showing the code of the demo."""
    show_code = st.sidebar.checkbox("Show code", True)
    if show_code:
        # Showing the code of the demo.
        st.markdown("## Code")
        sourcelines, _ = inspect.getsourcelines(demo)
        st.code(textwrap.dedent("".join(sourcelines[1:])))
@st.cache_data
def load_data(path :str):
    data=pd.read_excel(path)
    return data


st.set_page_config(
    page_title="Adidas Sales Dashboard",
    page_icon="bar_chart:",
    layout='wide')
st.title("Dashboard and Summary")
st.write(''' Welcome To Adidas US Sales Dashboard''')


df=load_data('./AdidasUSSales.xlsx')
df.dropna()
# Convert 'Invoice Date' to datetime
df['Invoice Date'] = pd.to_datetime(df['Invoice Date'])
df['Cumulative Total Sales'] = df.groupby('Retailer')['Total Sales'].cumsum()
df['Cumulative Total Sales Month Wise']=df.groupby('Month')['Total Sales'].cumsum()
# Convert numeric columns to numeric types
numeric_columns = ['Price per Unit', 'Units Sold', 'Total Sales', 'Operating Profit', 'Operating Margin']
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

with st.expander("Data Preview"):
    st.dataframe(df)
st.write('''
         USE THE FOLLOWING TAB FOR FILTERING RETAILER WISE
         ''')


# Select retailer for the bar race chart
selected_retailers = st.multiselect("Select Retailers", df["Retailer"].unique(), default=df["Retailer"].unique())

# Filter DataFrame based on selected retailers
filtered_df = df[df["Retailer"].isin(selected_retailers)].sort_values(by="Total Sales", ascending=False)


# Sunburst Chart
st.subheader('Retailer Wise Categorical Sunburst Chart')
sunburst_chart = px.sunburst(filtered_df, path=['Retailer', 'Product'], values='Total Sales',
                             title='Sunburst Chart')
st.plotly_chart(sunburst_chart, use_container_width=True)



st.subheader("Bar Race Chart - Total Sales by Retailer")

# Create a placeholder for the bar race chart
bar_race_chart = st.empty()
# Bar Race Chart
fig = px.bar(
    filtered_df,
    x=["Operating Profit"],
    y="Retailer",
    orientation="h",
    text="Total Sales",
    title=f"Total Sales Race for {selected_retailers} Monthly Numbers",
    animation_frame="Month",
    labels={"Total Sales": "Total Sales ($)"},
)
# Display the bar race chart
bar_race_chart.plotly_chart(fig,use_container_width=True)
# Simulate the race with a play button
if st.button("Start Race"):
    for i in range(1, len(filtered_df) + 1):
        # Update the chart dynamically
        updated_race = px.bar(
            filtered_df.iloc[:i],
            x="Total Sales",
            y="Retailer",
            orientation="h",
            text="Total Sales",
            title=f"Total Sales Race for {selected_retailers}",
            labels={"Total Sales": "Total Revenue($)"},
                  
        )
        bar_race_chart.plotly_chart(updated_race)    
        

st.subheader("Market Share")
# Group the data by retailer and sum the total sales for each retailer
retailer_sales = filtered_df.groupby('Retailer')['Total Sales'].sum()
# Calculate the total sales of all retailers
total_sales = retailer_sales.sum()
# Calculate the market share of each retailer by dividing their total sales by the total sales of all retailers
market_share = retailer_sales / total_sales
# Create a pie chart using plotly
fig = px.pie(market_share, values=market_share, names=market_share.index, title='Market Share of Retailers')
# Show the plot
st.plotly_chart(fig)



st.subheader('Cumulative Retailer Sales Trendline Animation')
animated_trendline_place = st.empty()

# Animated trendline chart for cumulative sales comparison
animated_trendline_cumulative = px.scatter(
    df,
    x='Operating Profit',
    y='Cumulative Total Sales',
    color='Retailer',
    title='Cumulative Retailer Sales Trendline',
    labels={'Cumulative Total Sales': 'Cumulative Sales'},
    animation_frame='Total Sales',
    animation_group='Retailer',
    width=800,
    height=500,
    trendline='ols'  # Ordinary Least Squares trendline
)

# Display the animated trendline chart
if st.button("Start"):
    animated_trendline_place.plotly_chart(animated_trendline_cumulative)



# Advanced Scatter Plot Matrix
st.subheader('Advanced Scatter Plot Matrix')
scatter_matrix = px.scatter_matrix(filtered_df, dimensions=["Retailer","Product","Total Sales", "State", "Operating Profit"], color='Operating Profit',
                                  title='Advanced Scatter Plot Matrix',width=1200, height=800)
st.plotly_chart(scatter_matrix, use_container_width=True)
