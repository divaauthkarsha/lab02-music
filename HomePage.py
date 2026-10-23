# This creates the main landing page for the Streamlit application.
# Contains an introduction to the project and guide users to other pages.

# Import Streamlit
import streamlit as st

# st.set_page_config() is used to configure the page's appearance in the browser tab.
# It's good practice to set this as the first Streamlit command in your script.
st.set_page_config(
    page_title="Homepage",  # The title that appears in the browser tab
    page_icon="🏠",         # An emoji that appears as the icon in the browser tab
)

# WELCOME PAGE TITLE
st.title("My Music Listening Dashboard 🎧")

# INTRODUCTORY TEXT
st.write("""
Welcome! This app explores my music listening habits over 6 weeks,
tracking how many minutes I spent on Pop, Hip Hop, R&B, Rock and Classical.

### How to use this app:
- **Visuals Page**: See my listening data as charts. Use the dropdown and slider
  to compare genres and weeks, and watch the summary stats update.
- **Survey Page**: Coming in Part 2, where you'll be able to submit your own data.

Created by DIVAA UTHKARSHA for CS 1301 Lab 2.
""")

# OPTIONAL: ADD AN IMAGE
# 1. Navigate to the 'images' folder in your Lab02 directory.
# 2. Place your image file (e.g., 'welcome_image.png') inside that folder.
# 3. Uncomment the line below and change the filename to match yours.
#
st.image("images/music.jpeg")