import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import seaborn as sns

# --- Page setup ---
st.set_page_config(page_title="NHL Defensemen: Data Analysis", layout="wide")
st.title("🏒 NHL Defensemen: IDA & EDA")
st.markdown("**Interactive Exploratory Data Analysis (EDA)**")

# --- Load Data ---
@st.cache_data
def load_data():
    hockey = pd.read_excel('SS.xlsx')
    bio = pd.read_excel('Bio.xlsx')
    hockey_filtered = hockey.drop(columns=['Pos', 'Season', 'S%'], errors='ignore')
    bio_filtered = bio[['Ctry', 'Ht', 'Wt', 'Draft Yr', 'Round', 'Overall']]
    data = pd.concat([hockey_filtered, bio_filtered], axis=1)

    # Add Div and Conf columns
    ATL = ['BOS', 'BUF', 'DET', 'FLA', 'MTL', 'OTT', 'TBL', 'TOR']
    MET = ['CAR', 'CBJ', 'NJD', 'NYI', 'NYR', 'PHI', 'PIT', 'WSH']
    CEN = ['CHI', 'COL', 'DAL', 'MIN', 'NSH', 'STL', 'UTA', 'WPG']
    PAC = ['ANA', 'CGY', 'EDM', 'LAK', 'SJS', 'SEA', 'VAN', 'VGK']

    def get_div(team):
        if team in ATL:
            return 'ATL'
        elif team in MET:
            return 'MET'
        elif team in CEN:
            return 'CEN'
        elif team in PAC:
            return 'PAC'
        else:
            return 'Unknown'

    def get_conf(team):
        if team in ATL or team in MET:
            return 'EC'
        elif team in CEN or team in PAC:
            return 'WC'
        else:
            return 'Unknown'

    if 'Team' in data.columns:
        data['Div'] = data['Team'].apply(get_div)
        data['Conf'] = data['Team'].apply(get_conf)
    else:
        data['Div'] = 'Unknown'
        data['Conf'] = 'Unknown'
    return data
df = load_data()

# --- Sidebar Navigation ---
st.sidebar.image("NHL-Logo.png", use_container_width=True)
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Select Analysis:",
    [
        "**About this App**",
        "Dataset Overview",
        "Class Imbalance",
        "Missing Values",
        "Correlation Analysis",
        "Scatter Plots",
        "**Wrapping Up**"
    ]
)
if page == "**About this App**":
    st.markdown("""
        <div style="background-color:#f0f2f6;padding:32px 24px 24px 24px;border-radius:12px;margin-bottom:24px;">
            <h2 style="color:#1a202c;margin-bottom:8px;">Get ready for Puck Drop!</h2>
            <p style="font-size:1.1rem;color:#444;line-height:1.6;margin-bottom:18px;">
                The main focus of this project is to use <b>Initial Data Analysis (IDA)</b> and <b>Exploratory Data Analysis (EDA)</b> to preprocess two raw datasets containing NHL defenseman data from the last year.<br><br>
                The goal is to get the data to a point where we can see who is producing the most points and what features correlate with point production. This will set the stage for my semester-end project: <b>predicting points using linear regression</b>.
            </p>
            <ul style="font-size:1.05rem;color:#333;margin-left:1.2em;">
                <li>You will find <b>interactive graphs</b> throughout the app to help you explore the data.</li>
                <li>There are <b>dropdown text boxes</b> on each page, providing explanations and insights for every analysis.</li>
            </ul>
            <div style="margin-top:24px;color:#888;font-size:0.98rem;">
                <i>Created by <b>Keshavi Dave</b> for her CMSE Midterm Project</i>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# --- Dataset Overview ---
if page == "Dataset Overview":
    st.header("Dataset Overview")

    # Metric boxes with gray stripes
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.markdown('<div style="display:flex;align-items:center;background:#fff;border-radius:8px;box-shadow:0 1px 4px #e5e7eb;margin-bottom:8px;">'
                    '<div style="width:8px;height:48px;background:#e5e7eb;border-radius:8px 0 0 8px;margin-right:12px;"></div>'
                    '<div style="padding:8px 0;">'
                    f'<div style="font-size:1.1rem;color:#444;">Total Defensemen (entries)</div>'
                    f'<div style="font-size:1.7rem;font-weight:600;color:#1a202c;">{df.shape[0]}</div>'
                    '</div></div>', unsafe_allow_html=True)
    with metric_col2:
        st.markdown('<div style="display:flex;align-items:center;background:#fff;border-radius:8px;box-shadow:0 1px 4px #e5e7eb;margin-bottom:8px;">'
                    '<div style="width:8px;height:48px;background:#e5e7eb;border-radius:8px 0 0 8px;margin-right:12px;"></div>'
                    '<div style="padding:8px 0;">'
                    f'<div style="font-size:1.1rem;color:#444;">Total Features</div>'
                    f'<div style="font-size:1.7rem;font-weight:600;color:#1a202c;">{df.shape[1]}</div>'
                    '</div></div>', unsafe_allow_html=True)
    with metric_col3:
        st.markdown('<div style="display:flex;align-items:center;background:#fff;border-radius:8px;box-shadow:0 1px 4px #e5e7eb;margin-bottom:8px;">'
                    '<div style="width:8px;height:48px;background:#e5e7eb;border-radius:8px 0 0 8px;margin-right:12px;"></div>'
                    '<div style="padding:8px 0;">'
                    f'<div style="font-size:1.1rem;color:#444;">Total Missing Values</div>'
                    f'<div style="font-size:1.7rem;font-weight:600;color:#1a202c;">{df.isnull().sum().sum()}</div>'
                    '</div></div>', unsafe_allow_html=True)

    st.subheader("Original Datasets")
    bio = pd.read_excel('Bio.xlsx')
    hockey = pd.read_excel('SS.xlsx')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Bio Stats** `(Bio.xlsx)`")
        st.dataframe(bio, use_container_width=True, height=320)
    with col2:
        st.markdown("**Season Stats** `(SS.xlsx)`")
        st.dataframe(hockey, use_container_width=True, height=320)

    # Dropdown for raw data info
    with st.expander("**About The Raw Data**", expanded=False):
        st.markdown("""
        - [Bio Stats](https://www.nhl.com/stats/skaters?report=bios&reportType=season&seasonFrom=20242025&seasonTo=20242025&gameType=2&position=D&sort=a_skaterFullName&page=0&pageSize=100) & [Season Stats](https://www.nhl.com/stats/skaters?reportType=season&seasonFrom=20242025&seasonTo=20242025&gameType=2&position=D&sort=skaterFullName&page=2&pageSize=100) pulled from _nhl.com/stats_ from the 2024-25 regular season
        - Much of the missing data comes from `FOW%` and the categories associated with being drafted into the NHL (`Draft Yr`, `Round`, `Overall`), we will cover this more on the Missing Values page
        - **Bio Stats**: 
            - `S/C` - Skater Shoots (Left or Right)
            - `S/P` - Player Birth State/Provence (US/CAN)
            - `Ht` - Height (inches)
            - `Wt` - Weight (lbs)
            - `HOF` - Yes/No if player is in the Hall of Fame
            - `GP` - Games Played
            - `G` - Goals
            - `A` - Assists
            - `P` - Points (Goals + Assists)
                    
        - **Season Stats:**
            - `+/-` - Plus/Minus (goal differential)
            - `PIM` - Penalty Minutes
            - `P/GP` - Points per Game Played
            - `EVG` - Even Strength Goals
            - `EVP` - Even Strength Points
            - `PPG` - Power Play Goals
            - `PPP` - Power Play Points
            - `SHG` - Shorthanded Goals
            - `SHP` - Shorthanded Points
            - `OTG`	- Overtime Goals
            - `GWG` - Game Winning Goals
            - `S` - Shots on Goal
            - `S%` - Shooting Percentage
            - `TOI/GP` - Time On Ice per Game Played
            - `FOW%` - Face Off Win Percentage
        """)

    st.subheader("Combined Dataset")
    st.dataframe(df, use_container_width=True, height=320)

    # Dropdown for combined data info
    with st.expander("**How is this more useful, and what's changed?**", expanded=False):
        st.markdown("""
        - The two raw datasets have been merged to be used for analysis.
        - **Taken from Bio Stats:** `Ctry`, `Ht`, `Wt`, `Draft Yr`, `Round`, and `Overall`
        - **Taken from Season Stats:** All features except for `Season`, `Pos`, and `S%`
        - Additional features such as `Div` (Division player is in based off of `Team`: Metro, Pacific, Atlantic, Central) and `Conf` (Conference player is in based off of `Div`: Eastern or Western), have been added for additional categorization
        - For housekeeping, players recorded with more than 2 teams were cleaned to only show the team they ended their season with
        """)

    st.subheader("Data Types and Summary Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df.dtypes.rename("Type").reset_index().rename(columns={'index': 'Column'}))
    with col2:
        st.dataframe(df.describe().T)

# --- Class Imbalance ---
elif page == "Class Imbalance":
    st.header("Class Imbalance Analysis")
    # Remove Player and Team from categorical options
    categorical_cols = [col for col in df.select_dtypes(exclude=[np.number]).columns if col not in ['Player', 'Team', 'TOI/GP']]

    options = categorical_cols
    if not options:
        st.info("No categorical columns available.")
    else:
        selected_cat = st.selectbox("Select Category:", options)
        cat_counts = df[selected_cat].value_counts()
        # Charts side by side
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            fig = px.bar(
                x=cat_counts.index, y=cat_counts.values, color=cat_counts.index,
                labels={'x': selected_cat, 'y': 'Count'},
                title=f'{selected_cat} Distribution'
            )
            st.plotly_chart(fig, use_container_width=True)
        with chart_col2:
            fig = px.pie(values=cat_counts.values, names=cat_counts.index, hole=0.3,
                         title=f'{selected_cat} Proportion')
            st.plotly_chart(fig, use_container_width=True)
    st.write("Click on the dropdown below that dives more into the category chosen above in the graphs")
    with st.expander("**`S/C` - Skater Shoots**", expanded=False):
        st.markdown("""
        A little bit more of the Defensemen in the league shoot left than right, this doesn't nessicariarly impact how many points they get in the season, rather just a fun category to see if there are any differences between those who favor to shoot left or right.
        """)   
    with st.expander("**`Ctry` - Player's Represented Country**", expanded=False):
        st.markdown("""
        Here we can see more clearly that the majority of Defensemen in the league come from the US or Canada, closly followed up by Sweden and Russia. We will most likely see that the top producing Defensemen will come from those top 3-5 countries rather than countries represented with a smaller number of Defensemen.
        - I.E. Defensemen that perform the best will most likely come from a small subset of countries, instead of being spread across the different countries represented in the NHL.
        """)   
    with st.expander("**`Div` & `Conf` - Player's Division & Conference**", expanded=False):
        st.markdown("""
        These values are the most evenly distributed, as they are based off of the team the player is on. There are 16 teams in each division, and 8 teams in each conference, so we would expect to see a more even distribution here.
        - We may be able to see what parts of the NHL produce the best Defensemen by categorizing by Division and Conference. But we expect it to even out due to the nature of how the league is split up.
        """)   


# --- Missing Values ---
elif page == "Missing Values":
    st.header("Missing Values Analysis")

    tab1, tab2 = st.tabs(["Missing Values Overview", "Imputation"])

    # --- TAB 1: Existing Missing Values Visualization ---
    with tab1:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(min(12, len(df.columns)*0.6), 6))
        sns.heatmap(df.isnull(), cbar=False, cmap="Blues", yticklabels=False)
        plt.xlabel("Features")
        plt.title("Missing Values Heatmap")
        st.pyplot(plt.gcf())

        with st.expander("**There is a reason as to why we're missing values...**", expanded=False):
            st.markdown("""
            - Faceoffs are generally not taken by defensemen, rather forwards  
               - They will only take the faceoff if the referee has waived off all the forwards on the ice.
            - It is not mandatory to be drafted by the NHL to play in the league.  
               - There will always be a handful of players who come into the league straight out of College or from a different hockey league.
            """)

    # --- TAB 2: Imputation ---
    with tab2:
        st.subheader("Imputation of Missing Values - Filled with Column Averages")
        df_imputed = df.copy()

        # Columns to impute
        cols_to_impute = ['Draft Yr', 'Round', 'Overall']
        for col in cols_to_impute:
            if col in df_imputed.columns:
                mean_val = df_imputed[col].mean()
                df_imputed[col] = df_imputed[col].fillna(mean_val)

        # --- Show correlation heatmaps before and after imputation ---
        numeric_df = df.select_dtypes(include=[np.number])
        corr_orig = numeric_df.corr()
        mask = np.triu(np.ones_like(corr_orig, dtype=bool))

        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(
            corr_orig, mask=mask, cmap='RdBu_r', center=0,
            annot=False, linewidths=.5, cbar_kws={"shrink": .8}, ax=ax
        )
        ax.set_title("Original Combined Data - Correlation (Lower Triangle)")
        st.pyplot(fig)

        numeric_df_imp = df_imputed.select_dtypes(include=[np.number])
        corr_imp = numeric_df_imp.corr()
        mask_imp = np.triu(np.ones_like(corr_imp, dtype=bool))

        fig2, ax2 = plt.subplots(figsize=(12, 8))
        sns.heatmap(
            corr_imp, mask=mask_imp, cmap='RdBu_r', center=0,
            annot=False, linewidths=.5, cbar_kws={"shrink": .8}, ax=ax2
        )
        ax2.set_title("Imputed Combined Data - Correlation (Lower Triangle)")
        st.pyplot(fig2)

        with st.expander("**What changed after imputation?**", expanded=False):
            st.markdown("""
            The reason it doesn’t look like much has changed after imputation is because, quite frankly, not much has. Sports data, especially draft and performance data, is complex and often doen't bode well with general statistical fixes. If we could accurately “fill in the blanks” for missing sports data, the entire sports gambling industry would be in shambles.

            When we filled the missing values in `Draft Yr`, `Round`, and `Overall` with their column averages, we basically smoothed out any extremes. However, in reality, there’s a wide distribution of players drafted across all rounds (1–7), and averaging these numbers flattens that diversity.  
            
            So overall, this means the imputed values aren't adding any new information, it's just “evening the playing field” for analysis purposes, helping us keep the data complete for modeling without introducing strong bias.
            """)
        with st.expander("**Another Imputation Technique: Ignoring the missing values**", expanded=False):
            st.markdown("""
            In terms of my overall semester project, having missing values for `Draft Yr`, `Round`, `Overall`, and `FOW%` isn’t a major concern. These features don’t strongly correlate with predicting the number of points a defenseman earns in a season, especially when compared to numerical variables like Assists and Even Strength Points that have a much more direct impact on performance.

            For the purposes of my analysis, I’ll be using a much simpler imputation strategy: _ignoring these columns altogether_. Since they contribute little value to the overall narrative of my project, removing them allows me to focus on the features that truly drive on-ice production and point prediction.
            """)



# --- Correlation Analysis ---
elif page == "Correlation Analysis":
    st.header("Correlation Analysis")
    numeric_df = df.select_dtypes(include=[np.number])

    corr = numeric_df.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    import matplotlib.pyplot as plt
    # Make cells rectangular: wider figure, not square
    fig, ax = plt.subplots(figsize=(max(14, len(corr.columns)*1.2), 6))
    fig, ax = plt.subplots(figsize=(max(14, len(corr.columns)*1.2), 12))  # Double the height from 6 to 12
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt='.2f',
        cmap='RdBu_r',
        center=0,
        square=False,
        linewidths=.5,
        cbar_kws={"shrink": .8},
        annot_kws={"size": 12},
        ax=ax
    )
    plt.title('Correlation Matrix (Lower Triangle)')
    plt.yticks(rotation=0)
    plt.xticks(rotation=45, ha='right')
    fig.tight_layout()
    st.pyplot(fig)
    with st.expander("**Why do we need Correlation Analysis?**", expanded=False):
        st.markdown("""
        This heatmap helps I as the analyst identify strong relationships between the number of Points (`P`) a player records in a season; so that for my final project of the semester, I am able to run regression and prediction tests using the right features that have a strong correlation with each other
        """)
    with st.expander("**What do we see here that's helpful?**", expanded=False):
        st.markdown("""
        As we are using Points (`P`) as our target variable, we can see that the features that correlate the most are Assists (`A`) and Even Strength Points (`EVP`).
        
        I will continue to keep these features in mind for my final project when it comes to my regression and prediction Tests
        - Assists are potentially highly correlated with Points as playing on Defense is not the top position to score the most goals. Rather they are the ones that help to set up most of the goals shot in by a Forward. Hense why many of their Points come from Assists
        - In addition, it would also make sense as to why there is a high correlation between Points and Even Strength Points as any time a team is up one skater (on the power play) or down one skater (on the penality kill), the Defenseman is spending more time making sure other players don't interfere with the Offencemen and their scoring channces
            - A Defenseman works best on getting Points when the whole team is on the ice, working together
        """)


# --- Scatter Plots ---
elif page == "Scatter Plots":
    st.header("Scatter Plots")
    st.write("Explore Relationships Between Features")
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    tab1, tab2 = st.tabs(["Interactive Scatter Plot", "Pairplot"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox("Select X-axis:", numeric_cols, key="scatter_x")
        with col2:
            y_axis = st.selectbox("Select Y-axis:", numeric_cols, index=min(1, len(numeric_cols)-1), key="scatter_y")

        allowed_color_cols = [col for col in ['S/C', 'Ctry', 'Div', 'Conf', 'Team'] if col in df.columns]
        color_by = st.selectbox("Color by (optional):", [None] + allowed_color_cols, key="scatter_color")
        hover_cols = [col for col in ['Player', 'Team', 'GP', 'P', 'Ctry', 'Div', 'Conf'] if col in df.columns]
        fig = px.scatter(
            df, x=x_axis, y=y_axis, color=color_by,
            title=f"{y_axis} vs {x_axis}", hover_data=hover_cols
        )
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("**What to do here?**", expanded=False):
            st.markdown("""
            This scatter plot allows us to visually explore relationships between different numeric features in the dataset. By selecting different x and y axes, we can see trends, clusters, or outliers that may not be obvious in summary statistics alone. 
                        
            In addition- coloring by categorical variables helps to see how different groups behave in relation to the selected features.
            """)
        with st.expander("**What is Class Imbalance doing here?** (_Color by_ tab)", expanded=False):
            st.markdown("""
            Earlier we discussed how class imbalance can impact our analysis. In this scatter plot, if we color by a categorical variable that is imbalanced (`Ctry`, `S/C`, `Div`, `Conf`), we see that certain groups dominate the higher points of the plots.

            We wondered if top producing defencemen would all come from a certain class, but as we work through different features against eachother and color them by class- we come to see that at the top of the charts there's always a good bland of defencemen from different Divisions, Confrences, and Shooting Habits
            - However, in terms of `Ctry`, we do see that the top producing players exclusively only hail from the US, Canada, and Sweden. We were incorrect about assuming there would be more Russians at the top of the chart!
            """)

    with tab2:
        st.info("Below are all the possible combinations of features against each other. This tab is here to give a an overall view of how all the numeric features in the dataset relate to each other.")
        st.subheader("Pairplot (Lower Triangle)")
        import matplotlib.pyplot as plt
        import seaborn as sns
        pairplot_cols = numeric_cols[:6] if len(numeric_cols) > 6 else numeric_cols
        if len(pairplot_cols) > 1:
            def lower_triangle_pairplot(data, vars):
                g = sns.pairplot(
                    data[vars],
                    corner=True,
                    plot_kws={'alpha':0.7, 's':20, 'color':'dodgerblue'},
                    diag_kws={'color':'dodgerblue', 'edgecolor':'black'}
                )
                return g
            g = lower_triangle_pairplot(df, pairplot_cols)
            st.pyplot(g.fig)
        else:
            st.info("Not enough numeric columns for a pairplot.")
# --- Wrapping Up Page ---
elif page == "**Wrapping Up**":
    st.header("Wrapping Up")
    st.info("**Congratulations!** We have completed an interactive EDA of NHL defensemen data. Here is a summary of what was accomplished in this app:")
    st.markdown("""
    - Explored and cleaned two raw datasets (Bio and Season Stats) for NHL defensemen
    - Investigated missing values and their impact on analysis
    - Examined class imbalance and its effect on feature distributions
    - Analyzed feature correlations, focusing on what drives point production
    - Used interactive scatter plots and pairplots to visualize relationships
    - Drew insights about which features matter most for predicting points
    
    **Final Thoughts:**
    - Assists and Even Strength Points are the most important features for predicting Points among defensemen
    - Top producing defensemen come from a mix of divisions and conferences, but the highest scorers are mostly from the US, Canada, and Sweden
    - My data is now ready for regression and prediction modeling for the final project!
    """)
    st.info("Thank you for exploring my data! I hope for this to be a valuable part of my work towards Defencemen point predictions.")
