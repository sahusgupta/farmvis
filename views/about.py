import streamlit as st
from PIL import Image
import pandas as pd

st.set_page_config(
    layout='wide'
)

def load_image(image_path):
    """
    Load an image from a given path.
    """
    return Image.open(image_path)

def header_section():
    """
    Creates the header section with a hero image, title, subtitle, and a call-to-action button.
    """

    st.markdown(
        f"""
        <div style='position: relative; text-align: center; color: white;'>
            <img src='https://picsum.photos/1200/400' alt='Hero Image' style='width:100%; height:auto; opacity:0.8;'>
            <div style='position: absolute; top:50%; left:50%; transform: translate(-50%, -50%);'>
                <b><h1 style='font-size:50px; color: #00ba2b'>Empowering New Farmers</h1></b>
                <p style='font-size:20px;'>Innovative Solutions for a Thriving Agricultural Community</p>
                <a href='#' style='background-color:#4CAF50; color:white; padding:10px 20px; text-align:center; text-decoration:none; display:inline-block; border-radius:5px; font-size:16px;'>Learn More About Our Impact</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def introduction_section():
    """
    Creates the introduction section with mission statement and an illustrative image.
    """
    st.markdown("## Our Mission")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("""
            Starting off in agriculture is an extremely daunting task for new farmers, who lack the experience that grisled veterans of the industry have. We aspire to provide realtime, easily accessible information and recommendations that are relevant to farmers' goals with their farms, helping to improve their experience using data from NASA.
        """)
    
    with col2:
        st.image("https://picsum.photos/500/300", use_column_width=True)

def key_features_section():
    """
    Highlights key features/values in three columns with icons.
    """
    st.markdown("## What We Offer")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("https://img.icons8.com/?size=100&id=0CoUpe9OEb6W&format=png&color=000000", width=80)
        st.markdown("### Personalized Recomendations")
        st.write("""
           Our proprietary recommender system will offer valuable insights on how to act upon the information that we provide you.
        """)
    
    with col2:
        st.image("https://img.icons8.com/fluency/100/000000/tractor.png", width=80)
        st.markdown("### Modern Tools")
        st.write("""
            We utilize advanced mapping and data visualization tools and algorithms to ensure that the alerts and information you recieve is as accurate as possible.
        """)
    
    with col3:
        st.image("https://img.icons8.com/fluency/100/000000/data-configuration.png", width=80)
        st.markdown("### Expert Approved")
        st.write("""
            The features we provide originate from input from seasoned farmers within the agricultural community, making sure to remain true to farmers.
        """)


def footer_section():
    """
    Displays the footer with contact information, social media links, and newsletter signup.
    """
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Contact Us")
        st.write("""
            **Email:** info@farmingaid.com  
            **Phone:** +1 (234) 567-890  
            **Location:** 123 Farm Lane, AgriCity, Country
        """)
    
    with col2:
        st.markdown("### Follow Us")
        st.write("""
            [![Facebook](https://img.icons8.com/ios-glyphs/30/000000/facebook-new.png)](https://facebook.com)  
            [![Twitter](https://img.icons8.com/ios-glyphs/30/000000/twitter--v1.png)](https://twitter.com)  
            [![Instagram](https://img.icons8.com/ios-glyphs/30/000000/instagram-new.png)](https://instagram.com)
        """)
    
    with col3:
        st.markdown("### Newsletter")
        st.write("""
            Stay updated with the latest farming tips and innovations.
        """)
        email = st.text_input("Enter your email", "")
        if st.button("Subscribe"):
            st.success("Subscribed successfully!")

def load_page():
    """
    Loads all sections to build the About Page.
    """
    # Header Section
    header_section()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Introduction Section
    introduction_section()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Key Features Section
    key_features_section()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Footer Section
    footer_section()

def main():
    """
    Main function to run the Streamlit app.
    """
    load_page()

if __name__ == "__main__":
    main()
