#For my webdev people (Sarah for now), the following is where you are going to start setting up the webpage using streamlit. You can check 
#the changes by running: streamlit run app.py - press Ctrl C to stop
#Your browser should open automatically, showing you the "Home" page with a title and a clickable button.


import streamlit as st

def main():
    """Main function to run the Streamlit app."""
    
    # --- Page Configuration ---
    # Set the title and icon for the browser tab
    st.set_page_config(
        page_title="CareerCompass: SHPE Opportunity Analyzer",
        page_icon="🚀",
        layout="wide"
    )

    # --- Sidebar Navigation ---
    # Create a menu in the sidebar to select the page
    st.sidebar.title("Navigation")
    page_selection = st.sidebar.radio(
        "Go to",
        [
            "🏠 Home",
            "📊 In-Demand Skills Dashboard",
            "📄 Resume Matcher"
        ]
    )

    # --- Page Content ---
    
    # Display the "Home" page
    if page_selection == "🏠 Home":
        st.title("Welcome to CareerCompass 🚀")
        st.subheader("The SHPE Opportunity & Skill Analyzer")
        st.write("""
        This tool is designed to help you bridge the gap between your skills and the job market.
        
        Use the navigation panel on the left to explore:
        - **In-Demand Skills Dashboard**: See what skills our sponsor companies are looking for right now.
        - **Resume Matcher**: Upload your resume to see how you stack up against a job description.
        """)
        
        # Test button to check if Streamlit interactivity is working
        if st.button("Click me to test!"):
            st.success("Streamlit is working!")

    # Placeholder for the "Dashboard" page
    elif page_selection == "📊 In-Demand Skills Dashboard":
        st.title("📊 In-Demand Skills Dashboard")
        st.write("This page will show a dashboard of the top skills. (Coming soon!)")
        # You will import and call your dashboard functions here

    # Placeholder for the "Resume Matcher" page
    elif page_selection == "📄 Resume Matcher":
        st.title("📄 Resume Matcher")
        st.write("This page will let you upload a resume and match it to a job. (Coming soon!)")
        # You will import and call your resume matching functions here

if __name__ == "__main__":
    main()