import streamlit as st
import streamlit.components.v1 as components

def embed_arcgis_map():
    html_code = """
    <style>
    .embed-container {
        position: relative;
        padding-bottom: 80%;
        height: 0;
        max-width: 100%;
    }
    .embed-container iframe, .embed-container object, .embed-container iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    }
    small {
        position: absolute;
        z-index: 40;
        bottom: 0;
        margin-bottom: -15px;
    }
    </style>
    <div class="embed-container">
        <iframe width="500" height="400" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" title="NASA soil moisture"
            src="//www.arcgis.com/apps/Embed/index.html?webmap=1724c0ca318741f5ac11e4ab54a94d90&extent=-136.8385,10.2197,-36.9947,62.2229&zoom=true&previewImage=false&scale=true&search=true&searchextent=true&legend=true&disable_scroll=true&theme=dark">
        </iframe>
    </div>
    """
    components.html(html_code, height=500)

if __name__ == "__main__":
    st.title("Soil Moisture Map Visualization")
    embed_arcgis_map()
