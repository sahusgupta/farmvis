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
                <h1 style='font-size:50px;'>Empowering Farmers for a Sustainable Future</h1>
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
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce at dolor sit amet mi laoreet vestibulum. 
            Nulla facilisi. In non massa eget sapien faucibus vehicula. 
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus bibendum ligula non vehicula cursus.
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
        st.image("https://img.icons8.com/fluency/100/000000/eco-friendly.png", width=80)
        st.markdown("### Sustainable Practices")
        st.write("""
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus bibendum ligula non vehicula cursus.
        """)
    
    with col2:
        st.image("https://img.icons8.com/fluency/100/000000/tractor.png", width=80)
        st.markdown("### Modern Tools")
        st.write("""
            Praesent nec arcu eget felis pretium vehicula. Curabitur vel lorem nec metus egestas fermentum.
        """)
    
    with col3:
        st.image("https://img.icons8.com/fluency/100/000000/data-configuration.png", width=80)
        st.markdown("### Data-driven Decisions")
        st.write("""
            Aliquam erat volutpat. Cras sed lectus vel erat tincidunt dapibus sit amet at odio.
        """)

def story_section():
    """
    Tells the story with alternating images and text.
    """
    st.markdown("## Our Journey")
    
    # First Story Block
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("https://picsum.photos/500/300", use_column_width=True)
    
    with col2:
        st.write("""
            Sed suscipit metus id purus auctor, ac suscipit libero malesuada. Integer hendrerit malesuada tortor, 
            at cursus mi facilisis in. Maecenas eu risus a est fermentum tincidunt.
        """)
    
    # Second Story Block
    col3, col4 = st.columns(2)
    
    with col3:
        st.write("""
            Maecenas eu risus a est fermentum tincidunt. Duis sit amet libero hendrerit, cursus dui ac, fermentum velit.
            Donec fringilla, metus nec consectetur cursus, orci urna aliquam turpis, at interdum purus nunc nec augue.
        """)
    
    with col4:
        st.image("https://picsum.photos/500/300", use_column_width=True)

def testimonials_section():
    """
    Showcases farmer testimonials in a grid format.
    """
    st.markdown("## Farmers' Voices")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("https://picsum.photos/100/100", use_column_width=False)
        st.markdown("### John Doe, Kansas")
        st.write("""
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus bibendum ligula non vehicula cursus."
        """)
    
    with col2:
        st.image("https://picsum.photos/100/100", use_column_width=False)
        st.markdown("### Jane Smith, Iowa")
        st.write("""
            "Praesent nec arcu eget felis pretium vehicula. Curabitur vel lorem nec metus egestas fermentum."
        """)
    
    with col3:
        st.image("https://picsum.photos/100/100", use_column_width=False)
        st.markdown("### Mike Johnson, Texas")
        st.write("""
            "Aliquam erat volutpat. Cras sed lectus vel erat tincidunt dapibus sit amet at odio."
        """)

def call_to_action_section():
    """
    Encourages users to get involved with a call-to-action button.
    """
    st.markdown("## Join Our Growing Community")
    st.markdown("""
        <div style='text-align: center;'>
            <a href='#' style='background-color:#FF9800; color:white; padding:15px 30px; text-align:center; text-decoration:none; display:inline-block; border-radius:5px; font-size:18px;'>Get Started</a>
        </div>
    """, unsafe_allow_html=True)

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
    
    # Story Section
    story_section()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Testimonials Section
    testimonials_section()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Call to Action Section
    call_to_action_section()
    
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
