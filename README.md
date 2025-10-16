# CMSE 830 Midterm Project

To access the app, [Click Here](https://appapppy-gq82ywhwiz5bocbfmhzrwf.streamlit.app/)!

## Project Overview
This project is an Interactive Data Analysis (IDA) and Exploratory Data Analysis (EDA) of NHL defensemen from the 2024–25 season. The data was collected from nhl.com/stats and merged into a single dataset combining player Bio Statistics and Season Performance. 

The Goal was to explore what factors most strongly influence point production among defencemen in the league as well as setting up a foundation for future predictive modeling. 

The Streamlit web app allows users to interactively explore the data through visualizations, filters, and explanations — making it easy to identify trends, outliers, and relationships across features.

## Why I Chose This Dataset
I chose this dataset because I enjoy sports, especially hockey, and defensemen are my favorite type of hockey player. They play a unique role that balances offensive and defensive contributions, which makes analyzing their stats both challenging and exciting.

## What I've Learned From IDA/EDA
- The highest-performing defensemen tend to come from the USA, Canada, and Sweden.
- High-performing players are evenly distributed across NHL divisions, suggesting balanced talent throughout the league.
- Assists and Even Strength Points (EVP) are the features most correlated with total Points (P), which will be key predictors in future modeling.

## Data Preprocessing
- Merged two datasets (`Bio.xlsx` and `SS.xlsx`) into one unified table.
- Dropped unnecessary columns (`Pos`, `Season`, `S%`) for clarity.
- Added new features:
  - `Div` — Player’s division (Atlantic, Metro, Central, Pacific)
  - `Conf` — Player’s conference (Eastern or Western)
- Cleaned team data for players who were listed on multiple teams (only showing their final team).

## Streamlit Features
- Sidebar navigation with structured pages
- Interactive Plotly graphs
- Expandable text boxes for more analysis
- Tabs for interactive visulizations and multiple views
