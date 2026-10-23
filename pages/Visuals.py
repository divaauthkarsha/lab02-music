# This creates the page for displaying data visualizations.

import json
import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
# --- YOUR CODE GOES HERE ---

# Read the JSON file into a Python dictionary
with open("data.json", "r") as file:
    data = json.load(file)

# Use the title and description from the JSON file
st.header(data["project_title"])
st.write(data["description"])

# Turn the list of weekly dictionaries into a table
# Each dictionary becomes one row, and each key becomes a column
df = pd.DataFrame(data["weekly_listening"])

# Use the "week" column as the row labels instead of 0, 1, 2...
df = df.set_index("week")

st.subheader("Raw Data")
st.dataframe(df)

# ---------- STATIC VISUALIZATION (Plotly pie chart) ----------
st.subheader("Total Listening by Genre")

# Add up each genre's minutes across all 6 weeks
totals = df.sum()

pie = px.pie(
    names=totals.index,      # genre names (Pop, Hip Hop, etc.)
    values=totals.values,    # total minutes for each genre
    title="Share of Total Listening Time by Genre (All 6 Weeks)",
)
pie.update_layout(legend_title_text="Genre")
st.plotly_chart(pie)

# ---------- DYNAMIC VISUALIZATION (line chart) ----------
st.subheader("Listening Over Time")

genre_names = list(df.columns)   # ["Pop", "Hip Hop", "R&B", "Rock", "Classical"]
num_weeks = len(df)              # 6

# Set default values in session state the first time the page loads
if "selected_genres" not in st.session_state:
    st.session_state.selected_genres = genre_names
if "week_range" not in st.session_state:
    st.session_state.week_range = (1, num_weeks)

# User inputs, connected to session state through their key
st.multiselect("Choose genres to compare:", options=genre_names, key="selected_genres")
st.slider("Choose a week range:", min_value=1, max_value=num_weeks, key="week_range")

# Read the user's choices from session state
selected = st.session_state.selected_genres
start, end = st.session_state.week_range

if selected:
    # Keep only the chosen weeks (rows) and chosen genres (columns)
    filtered = df.iloc[start - 1:end][selected]
    st.line_chart(filtered, x_label="Week", y_label="Minutes Listened")
        # ---------- EXTRA CREDIT: summary stats ----------
    st.subheader("Summary Stats for Your Selection")

    # Total minutes per week for only the selected genres and weeks
    weekly_totals = filtered.sum(axis=1)
    mean_now = float(weekly_totals.mean())
    median_now = float(weekly_totals.median())

    # On the first load there's no previous value, so compare to the current one
    prev_mean = st.session_state.get("prev_mean", mean_now)
    prev_median = st.session_state.get("prev_median", median_now)

    col1, col2 = st.columns(2)
    col1.metric("Mean minutes per week", f"{mean_now:.1f}", delta=f"{mean_now - prev_mean:.1f}")
    col2.metric("Median minutes per week", f"{median_now:.1f}", delta=f"{median_now - prev_median:.1f}")

    # Save the current values so the next change can compare against them
    st.session_state.prev_mean = mean_now
    st.session_state.prev_median = median_now
else:
    st.warning("Pick at least one genre to see the chart.")


# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---

st.divider()

# Read the survey answers from the CSV file into a table
survey_df = pd.read_csv("data.csv")

st.header("Music Survey Results")
st.write(f"Based on {len(survey_df)} survey responses.")

st.subheader("Survey Data")
st.dataframe(survey_df)

# ---------- STATIC VISUALIZATION (Plotly bar chart) ----------
st.subheader("Average Listening Hours by Genre")

# Group the rows by genre and take the average hours for each genre
avg_hours = survey_df.groupby("genre")["hours"].mean().reset_index()

bar = px.bar(
    avg_hours,
    x="genre",
    y="hours",
    title="Average Weekly Listening Hours by Favorite Genre",
    labels={"genre": "Favorite Genre", "hours": "Average Hours per Week"},
)
st.plotly_chart(bar)

# ---------- DYNAMIC VISUALIZATION (scatter chart) ----------
st.subheader("Age vs. Listening Hours")

genre_options = sorted(survey_df["genre"].unique().tolist())
max_hours = int(survey_df["hours"].max())

# Set default values in session state the first time the page loads
if "survey_genres" not in st.session_state:
    st.session_state.survey_genres = genre_options
if "min_hours" not in st.session_state:
    st.session_state.min_hours = 0

# User inputs, connected to session state through their key
st.multiselect("Choose genres to show:", options=genre_options, key="survey_genres")
st.slider("Only show people who listen at least this many hours a week:",
          min_value=0, max_value=max_hours, key="min_hours")

# Read the user's choices from session state
chosen = st.session_state.survey_genres
min_hours = st.session_state.min_hours

# Keep only rows with a chosen genre AND enough listening hours
survey_filtered = survey_df[
    (survey_df["genre"].isin(chosen)) & (survey_df["hours"] >= min_hours)
]

if len(survey_filtered) > 0:
    st.scatter_chart(survey_filtered, x="age", y="hours", color="genre",
                     x_label="Age", y_label="Hours per Week")

    # ---------- EXTRA CREDIT: summary stats ----------
    st.subheader("Summary Stats for Selected Responses")
    s_mean_now = float(survey_filtered["hours"].mean())
    s_median_now = float(survey_filtered["hours"].median())

    s_prev_mean = st.session_state.get("prev_survey_mean", s_mean_now)
    s_prev_median = st.session_state.get("prev_survey_median", s_median_now)

    c1, c2 = st.columns(2)
    c1.metric("Mean hours per week", f"{s_mean_now:.1f}", delta=f"{s_mean_now - s_prev_mean:.1f}")
    c2.metric("Median hours per week", f"{s_median_now:.1f}", delta=f"{s_median_now - s_prev_median:.1f}")

    st.session_state.prev_survey_mean = s_mean_now
    st.session_state.prev_survey_median = s_median_now
else:
    st.warning("No responses match your choices. Try picking more genres or lowering the slider.")
    


