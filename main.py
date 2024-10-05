import streamlit as st
import pandas as pd

# Set the page title
st.set_page_config(page_title="Ad Copy Generator", layout="wide")

# Page header
st.title("Ad Copy Generator & Preview")
st.write("Easily create and preview multiple ad headlines and descriptions.")

# Initialize the session state to store ads
if 'ads_data' not in st.session_state:
    st.session_state.ads_data = []

# Layout with columns: inputs on the left (smaller), ad preview on the right (larger)
col1, col2 = st.columns([1, 3])  # Adjust ratio (1:3) for 3x larger preview section

# Custom CSS to center ad preview
st.markdown("""
    <style>
    .centered-ad {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
    }
    .ad-box {
        border: 1px solid #ccc;
        padding: 10px;
        width: 300px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .mobile-ad-box { width: 300px; }
    .desktop-ad-box { width: 600px; }
    </style>
""", unsafe_allow_html=True)

with col1:
    # Input for the keyword
    st.subheader("Keyword")
    keyword = st.text_input("Keyword for this ad")

    # Split the headline and description sections into half columns
    st.subheader("Headlines (Auto Title Case)")
    half_col1, half_col2 = st.columns(2)

    headlines = []
    for i in range(1, 8):
        with half_col1 if i % 2 == 1 else half_col2:
            headline = st.text_input(f"Headline {i} (Max 30 characters)", max_chars=30, key=f"headline_{i}")
            # Apply title case automatically
            if headline:
                headlines.append(headline.title())

    st.subheader("Descriptions (Auto Title Case)")
    half_col3, half_col4 = st.columns(2)

    descriptions = []
    for i in range(1, 5):
        with half_col3 if i % 2 == 1 else half_col4:
            description = st.text_area(f"Description {i} (Max 90 characters)", max_chars=90, key=f"description_{i}")
            # Apply title case automatically
            if description:
                descriptions.append(description.title())

    # Web URL input field
    web_url = st.text_input("Web URL (Optional)")

    # Add ad button
    if st.button("Add Ad"):
        st.session_state.ads_data.append({
            "Keyword": keyword,
            "Headlines": headlines + [''] * (7 - len(headlines)),  # Fill empty headlines
            "Descriptions": descriptions + [''] * (4 - len(descriptions)),  # Fill empty descriptions
            "Web URL": web_url
        })
        st.success("Ad added successfully!")

    # Show added ads
    if st.session_state.ads_data:
        st.write("### Added Ads")
        for idx, ad in enumerate(st.session_state.ads_data):
            st.write(f"**Ad {idx + 1}:** Keyword: {ad['Keyword']}")
            st.write(f"Headlines: {ad['Headlines']}")
            st.write(f"Descriptions: {ad['Descriptions']}")
            st.write(f"Web URL: {ad['Web URL']}")
            st.write("---")

    # Export option (Save the headlines, descriptions, and web URLs to a CSV file)
    if st.session_state.ads_data and st.button("Export to CSV"):
        # Prepare the data for export
        export_data = []
        for ad in st.session_state.ads_data:
            export_data.append({
                "Keyword": ad["Keyword"],
                "Headline 1": ad["Headlines"][0],
                "Headline 2": ad["Headlines"][1],
                "Headline 3": ad["Headlines"][2],
                "Headline 4": ad["Headlines"][3],
                "Headline 5": ad["Headlines"][4],
                "Headline 6": ad["Headlines"][5],
                "Headline 7": ad["Headlines"][6],
                "Description 1": ad["Descriptions"][0],
                "Description 2": ad["Descriptions"][1],
                "Description 3": ad["Descriptions"][2],
                "Description 4": ad["Descriptions"][3],
                "Web URL": ad["Web URL"]
            })
        
        df = pd.DataFrame(export_data)

        # Create a download button for the CSV file
        csv = df.to_csv(index=False)
        st.download_button(label="Download Ad Copy CSV", data=csv, file_name="ad_copy_bulk.csv", mime="text/csv")
        st.success("Ad copy exported successfully!")

# Column for ad preview (now 3x larger than input section)
with col2:
    # Toggle between mobile and desktop preview
    view_mode = st.radio("Choose Preview Mode", ["Mobile", "Desktop"])

    # Function to render the ad preview
    def render_ad_preview(headlines, descriptions, web_url, mode="Mobile"):
        st.write("---")
        if mode == "Mobile":
            st.write("📱 **Mobile Ad Preview**")
            st.markdown(f"""
            <div class="centered-ad">
                <div class="ad-box mobile-ad-box">
                    <div style="color: grey; font-size: 12px;">Iklan</div>
                    <div style="font-weight:bold; font-size:16px;">{headlines[0] if headlines else '[Your headline here]'}</div>
                    <div style="color: grey; font-size: 12px;">{web_url if web_url else 'www.example.com'}</div>
                    <div style="font-size:14px; margin-top: 10px;">{descriptions[0] if descriptions else '[Your description here]'}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.write("💻 **Desktop Ad Preview**")
            st.markdown(f"""
            <div class="centered-ad">
                <div class="ad-box desktop-ad-box">
                    <div style="color: grey; font-size: 12px;">Iklan</div>
                    <div style="font-weight:bold; font-size:18px;">{headlines[0] if headlines else '[Your headline here]'}</div>
                    <div style="color: grey; font-size: 12px;">{web_url if web_url else 'www.example.com'}</div>
                    <div style="font-size:14px; margin-top: 10px;">{descriptions[0] if descriptions else '[Your description here]'}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Display the ad preview in the chosen mode
    if headlines and descriptions:
        render_ad_preview(headlines, descriptions, web_url, mode=view_mode)
