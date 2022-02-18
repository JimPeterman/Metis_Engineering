import streamlit as st# Custom imports from multipage import MultiPagefrom pages import home, graphs, regressions, publications# Create an instance of the app app = MultiPage()# Title of the main page# st.title("FRIEND Application")# Add all your applications (pages) hereapp.add_page("Home", home.app)app.add_page("Data Graphs", graphs.app)app.add_page("Assess Your Fitness", regressions.app)app.add_page("Publications", publications.app)# The main appapp.run()