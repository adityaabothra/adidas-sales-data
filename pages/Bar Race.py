# import streamlit as st
# import pandas as pd
# import plotly.express as px



# # Sample DataFrame
# def load_data(path :str):
#     data=pd.read_excel(path)
#     return data

# df = load_data('./AdidasUSSales.xlsx')
# # Streamlit app
# st.set_page_config(page_title="Bar Race Chart", page_icon="📊")
# st.title("Bar Race Chart - Total Sales by Retailer")

# # Select retailer for the bar race chart
# selected_retailers = st.multiselect("Select Retailers", df["Retailer"].unique(), default=df["Retailer"].unique())

# # Filter DataFrame based on selected retailers
# filtered_df = df[df["Retailer"].isin(selected_retailers)].sort_values(by="Total Sales", ascending=False)

# # Create a placeholder for the bar race chart
# bar_race_chart = st.empty()

# # Bar Race Chart
# fig = px.bar(
#     filtered_df,
#     x="Total Sales",
#     y="Retailer",
#     orientation="h",
#     text="Total Sales",
#     title=f"Total Sales Race for {selected_retailers}",
#     labels={"Total Sales": "Total Sales ($)"},
# )

# # Display the bar race chart
# bar_race_chart.plotly_chart(fig)

# # Simulate the race with a play button
# if st.button("Start Race"):
#     for i in range(1, len(filtered_df) + 1):
#         # Update the chart dynamically
#         fig = px.bar(
#             filtered_df.iloc[:i],
#             x="Total Sales",
#             y="Retailer",
#             orientation="h",
#             text="Total Sales",
#             title=f"Total Sales Race for {selected_retailers}",
#             labels={"Total Sales": "Total Sales ($)"},
#         )
#         bar_race_chart.plotly_chart(fig)
#           # Adjust the sleep duration as needed
