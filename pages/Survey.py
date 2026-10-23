# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Music Listening Survey 📝")
st.write("Tell me about your music habits! Your answers will be added to the dataset.")

# DATA INPUT FORM
# 'st.form' groups the inputs so the page only reruns when Submit is clicked.
with st.form("survey_form"):
    # Text inputs: everything the user types comes in as a string
    genre_input = st.text_input("What's your favorite music genre? (e.g. Pop, Hip Hop, Rock)")
    hours_input = st.text_input("How many hours a week do you listen to music?")
    age_input = st.text_input("How old are you?")

    submitted = st.form_submit_button("Submit Data")

    # This block runs ONLY when the submit button is clicked
    if submitted:
        # Clean up the text: remove extra spaces, capitalize each word
        # and remove commas (a comma would break the CSV columns)
        genre = genre_input.strip().title().replace(",", "")
        hours = hours_input.strip()
        age = age_input.strip()

        if genre == "" or hours == "" or age == "":
            st.error("Please answer all three questions.")
        else:
            try:
                # Convert the strings to numbers so we can graph them later
                hours_num = float(hours)
                age_num = int(age)
            except ValueError:
                st.error("Hours and age must be numbers (for example: 10 and 19).")
            else:
                if hours_num < 0 or age_num <= 0:
                    st.error("Hours and age must be positive numbers.")
                else:
                    # Open data.csv in append mode ('a') so we add a new line
                    # instead of erasing what's already there
                    with open("data.csv", "a") as file:
                        file.write(f"{genre},{hours_num},{age_num}\n")

                    st.success("Your data has been submitted!")
                    st.write(f"You entered: **Genre:** {genre}, **Hours:** {hours_num}, **Age:** {age_num}")


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
    