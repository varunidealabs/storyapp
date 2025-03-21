import streamlit as st
import os
from src.story_generator import StoryGenerator
from src.image_generator import ImageGenerator
from src.tts_generator import TTSGenerator
from src.export_story import StoryExporter
from src.cleanup import clear_all_temp_files

# Ensure directories exist
os.makedirs("output_stories", exist_ok=True)
os.makedirs("output_audio", exist_ok=True)

# Page config with wider layout
st.set_page_config(
    page_title="StoryBloom AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Additional global CSS to fix contrast issues
st.markdown("""
<style>
    /* Fix color contrast on black elements */
    .css-1offfwp, .css-12oz5g7 {
        color: white !important;
    }
    
    /* Ensure buttons with dark backgrounds have white text */
    button, .css-1q8dd3e {
        color: white !important;
    }
    
    /* But buttons with white backgrounds should have black text */
    button.css-1q8dd3e.white-bg, .secondary-button {
        color: black !important;
    }
    
    /* Force color contrast for any black or dark elements */
    .css-1q8dd3e, .css-1offfwp, .css-12oz5g7 {
        --text-color: white !important;
    }
    
    /* Fix for dark modals or overlays */
    .dark-bg *, [style*="background-color: #000"] *, [style*="background-color: rgb(0, 0, 0)"] * {
        color: white !important;
    }
    
    /* Override Streamlit's default button styling */
    .stButton > button {
        color: white !important;
        border: 2px solid black !important;
    }
    
    /* Fix for white buttons specifically */
    .stButton > button.white-btn, .stButton > button:nth-of-type(2) {
        background-color: white !important;
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)

# Custom CSS for styling
st.markdown("""
<style>
    /* Global Styles */
    body {
        font-family: 'Inter', sans-serif;
        background-color: white !important;
        color: black !important;
    }
    
    .stApp {
        background-color: white !important;
    }
</style>
""", unsafe_allow_html=True)
# Custom CSS for styling
st.markdown("""
<style>
    /* Global Styles */
    body {
        font-family: 'Inter', sans-serif;
        background-color: white !important;
        color: black !important;
    }
    
    .stApp {
        background-color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# More CSS styles
st.markdown("""
<style>
    /* Force all text to be black */
    .stMarkdown, p, h1, h2, h3, h4, h5, h6, span, label, .stSelectbox, .stTextInput, .stTextArea, .stRadio, .stCheckbox {
        color: black !important;
    }
    
    /* Make sure all input fields have proper contrast */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div > div {
        color: black !important;
        background-color: white !important;
    }
    
    /* Make sure any black background elements have white text */
    [style*="background-color: black"], [style*="background-color:#000000"], [style*="background-color: #000"] {
        color: white !important;
    }
    
    /* Force white text on black backgrounds for all elements */
    .black-bg, .black-button, div[style*="background-color: black"], .stButton > button[style*="background-color: black"] {
        color: white !important;
    }
    
    /* Ensure radio buttons and checkboxes are visible */
    .stRadio label, .stCheckbox label {
        color: black !important;
    }
    
    /* Force readable text on any button */
    button, .stButton > button {
        color: white !important;
    }
    
    /* For any button that has a light background */
    button[style*="background-color: white"], .stButton > button[style*="background-color: white"] {
        color: black !important;
    }
    
    /* Force background to be white */
    .main .block-container {
        background-color: white !important;
    }
    
    /* Override the metric value and label color */
    .stMetric > div {
        color: black !important;
    }
    .stMetric > div > div > div {
        color: black !important;
    }
    
    /* Fix caption text */
    .stImage > div > div > small {
        color: black !important;
    }
    
    /* Header Styles */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 0;
        border-bottom: 1px solid #f0f0f0;
        margin-bottom: 20px;
        background-color: white;
    }
    .header-logo {
        font-size: 24px;
        font-weight: bold;
        color: black;
    }
    .header-nav a {
        margin-left: 20px;
        color: black;
        text-decoration: none;
    }
    
    /* Hero Section */
    .hero-container {
        text-align: center;
        padding: 40px 0;
        max-width: 800px;
        margin: 0 auto;
        background-color: white;
    }
    .hero-badge {
        background-color: #f8f8f8;
        color: black;
        padding: 8px 16px;
        border-radius: 20px;
        display: inline-flex;
        align-items: center;
        font-size: 14px;
        margin-bottom: 20px;
    }
    .hero-title {
        font-size: 48px;
        font-weight: bold;
        color: black;
        margin-bottom: 20px;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: 18px;
        color: black;
        margin-bottom: 40px;
        line-height: 1.6;
    }
    
    /* Button Styles */
    div.stButton > button {
        background-color: #000000;
        color: white !important; /* Force white text on black buttons */
        padding: 12px 24px;
        border-radius: 30px;
        font-weight: 600;
        border: 2px solid black;
        width: 100%;
        font-size: 16px;
        margin-bottom: 10px;
    }
    div.stButton > button:hover {
        background-color: white;
        color: black !important; /* Force black text on white hover */
        border: 2px solid black;
    }
    
    /* First button (Create Story) */
    div.stButton > button:nth-of-type(1) {
        background-color: #000000;
        color: white !important;
    }
    
    /* Second button (View Sample) */
    div.stButton > button:nth-of-type(2) {
        background-color: white;
        color: black !important;
        border: 2px solid black;
    }
    
    div.stButton > button:nth-of-type(2):hover {
        background-color: #f0f0f0;
    }
    
    /* Form Styles */
    .form-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 30px;
        background-color: white;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .form-title {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
        color: black;
    }
    .form-subtitle {
        font-size: 16px;
        color: black;
        text-align: center;
        margin-bottom: 30px;
    }
    .form-row {
        display: flex;
        gap: 20px;
        margin-bottom: 20px;
    }
    .form-group {
        flex: 1;
    }
    .form-label {
        font-weight: 500;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
        color: black;
    }
    .form-input, .form-select {
        width: 100%;
        padding: 12px;
        border: 1px solid black;
        border-radius: 8px;
        font-size: 16px;
        background-color: white;
        color: black;
    }
    
    /* Story Container */
    .story-container {
        max-width: 800px;
        margin: 40px auto;
        padding: 30px;
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    .story-title {
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 20px;
        text-align: center;
        color: black;
    }
    .story-content {
        font-size: 18px;
        line-height: 1.6;
        color: black;
    }
    
    /* Feature Icons */
    .feature-icons {
        display: flex;
        justify-content: center;
        gap: 80px;
        margin-top: 60px;
        background-color: white;
    }
    .feature-icon {
        font-size: 32px;
        color: black;
        text-align: center;
    }
    
    /* Length Selector Buttons */
    .length-selector {
        display: flex;
        gap: 10px;
        background-color: white;
    }
    .length-button {
        flex: 1;
        text-align: center;
        padding: 12px;
        border: 1px solid black;
        border-radius: 8px;
        cursor: pointer;
        color: black;
        background-color: white;
    }
    .length-button.active {
        background-color: black;
        color: white;
        border-color: black;
    }
    
    /* Audio Player Styling */
    .audio-container {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 20px;
        background-color: white;
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 10px;
    }
    .audio-button {
        background-color: black;
        color: white;
        padding: 8px 16px;
        border-radius: 30px;
        font-weight: 600;
        cursor: pointer;
    }
    
    /* Image Container */
    .image-container {
        margin: 20px 0;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e0e0e0;
    }
    
    /* Custom Tabs */
    .custom-tabs {
        display: flex;
        border-bottom: 1px solid black;
        margin-bottom: 20px;
        background-color: white;
    }
    .tab-item {
        padding: 10px 20px;
        cursor: pointer;
        border-bottom: 2px solid transparent;
        color: black;
    }
    .tab-item.active {
        border-bottom: 2px solid black;
        font-weight: bold;
    }
    
    /* Utility Classes */
    .mt-20 {margin-top: 20px;}
    .mt-40 {margin-top: 40px;}
    .text-center {text-align: center;}
</style>
""", unsafe_allow_html=True)

# ===== Initialize Session State =====
# Only clear temp files once when the app starts
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    clear_all_temp_files()

# Initialize all session state variables
if "page" not in st.session_state:
    st.session_state.page = "home"  # Options: home, create_form, story_view

for key in ["story", "title", "image_url", "pdf_path", "audio_file", "story_generated", "play_audio", "length"]:
    if key not in st.session_state:
        st.session_state[key] = None

# Initialize audio player state
if "play_audio" not in st.session_state:
    st.session_state.play_audio = False

# ===== Helper Functions =====
def toggle_audio():
    """Toggle audio playback state"""
    st.session_state.play_audio = not st.session_state.play_audio

def go_to_page(page):
    """Change the current page"""
    st.session_state.page = page
    
def create_sample_story():
    """Generate a sample story with default values"""
    with st.spinner("Generating a sample story..."):
        # Default values for sample story
        genre = "Fantasy"
        length = 500
        topic = "A magical adventure in an enchanted forest"
        character_name = "Emma"
        keywords = "magic, forest, adventure, discovery, ancient secrets"
        
        # Generate story
        story_gen = StoryGenerator()
        title, story = story_gen.generate_story(genre, length, topic, character_name, keywords)
        
        if story:
            # Store story in session state
            st.session_state.title = title.strip().replace('"', '')
            st.session_state.story = story
            st.session_state.story_generated = True
            st.session_state.play_audio = False
            
            # Export as text
            exporter = StoryExporter()
            exporter.save_story_txt(st.session_state.title, st.session_state.story)
            
            # Generate image
            image_gen = ImageGenerator()
            image_url = image_gen.generate_image(genre, topic, keywords)
            st.session_state.image_url = image_url
            
            # Generate speech
            tts_gen = TTSGenerator()
            st.session_state.audio_file = tts_gen.generate_speech(st.session_state.story)
            
            # Generate PDF
            st.session_state.pdf_path = exporter.save_story_pdf(
                st.session_state.title, 
                st.session_state.story, 
                st.session_state.image_url
            )
            
            # Change to story view page
            go_to_page("story_view")

# ===== Header =====
# Use Streamlit columns for header to avoid HTML rendering issues
header_col1, header_col2 = st.columns([1, 2])

with header_col1:
    st.markdown("<h1 style='font-size: 24px; margin-bottom: 0; color: black; font-weight: bold;'>✨ AI Story Generator </h1>", unsafe_allow_html=True)

# Add a separator line
st.markdown("<hr style='margin-top: 0; border-color: #e0e0e0;'>", unsafe_allow_html=True)

# ===== Page Content =====
if st.session_state.page == "home":
    # Hero Section - Simplified version without custom HTML buttons
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge" style="color: black; font-weight: 500;">✨ Story generation reimagined</div>
        <h1 class="hero-title" style="color: black; font-weight: bold;">Create beautiful stories with a few simple inputs</h1>
        <p class="hero-subtitle" style="color: black;">Craft unique tales with stunning visuals and immersive narration, using our intuitive story generation platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Button Container - Using Streamlit columns for layout instead of HTML
    st.markdown("""
    <style>
    /* Special style for the main buttons */
    .main-button-black {
        background-color: black;
        color: white !important;
        padding: 15px 30px;
        border-radius: 30px;
        font-weight: bold;
        text-align: center;
        margin: 10px 0;
        font-size: 18px;
        cursor: pointer;
        border: 2px solid black;
    }
    .main-button-white {
        background-color: white;
        color: black !important;
        padding: 15px 30px;
        border-radius: 30px;
        font-weight: bold;
        text-align: center;
        margin: 10px 0;
        font-size: 18px;
        cursor: pointer;
        border: 2px solid black;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Button Container - Using Streamlit columns for side-by-side buttons
    # Button Container - Using Streamlit columns for side-by-side buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Additional CSS to ensure the buttons display properly
        st.markdown("""
        <style>
        /* Make both buttons white with black text */
        div.stButton button {
            color: black !important;
            background-color: white !important;
            font-weight: bold !important;
            border: 2px solid black !important;
            border-radius: 30px !important;
            padding: 12px 24px !important;
        }
        
        div.stButton button:hover {
            background-color: #f7f7f7 !important;
        }
        
        /* Make buttons display side by side */
        div.row-widget.stButton {
            display: inline-block;
            width: 48%;
            margin-right: 2%;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Side-by-side buttons with consistent styling
        button_cols = st.columns(2)
        with button_cols[0]:
            if st.button("Create Your Story →", key="create_story_btn", use_container_width=True):
                go_to_page("create_form")
                
        with button_cols[1]:
            if st.button("View Sample Story", key="view_sample_btn", use_container_width=True):
                create_sample_story()

elif st.session_state.page == "create_form":
    # Story Creation Form with improved styling
    st.markdown("""
    <div style="background-color: white; padding: 30px; border-radius: 10px; border: 1px solid #e0e0e0;">
        <h2 style="font-size: 32px; font-weight: bold; text-align: center; color: black;">Craft Your Story</h2>
        <p style="font-size: 16px; color: black; text-align: center; margin-bottom: 30px;">Fill in the details below to generate your custom story</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add some spacing
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # Form with white background container
    st.markdown("<div style='background-color: white; padding: 30px; border-radius: 10px; border: 1px solid #e0e0e0;'>", unsafe_allow_html=True)
    
    # Form Layout with Two Columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div style="font-weight: 500; margin-bottom: 8px; color: black;">🎭 Theme</div>', unsafe_allow_html=True)
        topic = st.text_input("", "A magical adventure in an enchanted forest", key="theme_input",
                            placeholder="e.g. Space exploration, Medieval quest")
    
    with col2:
        st.markdown('<div style="font-weight: 500; margin-bottom: 8px; color: black;">📚 Genre</div>', unsafe_allow_html=True)
        genre = st.selectbox("", 
                            ["Fantasy", "Sci-Fi", "Mystery", "Adventure", "Romance", "Horror", "Fairy Tale"], 
                            key="genre_select")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div style="font-weight: 500; margin-bottom: 8px; color: black;">⏱️ Length</div>', unsafe_allow_html=True)
        length_options = {"Short": 250, "Medium": 500, "Long": 750}
        
        # Custom CSS to make radio buttons more visible
        st.markdown("""
        <style>
        .stRadio > div {
            color: black !important;
            font-weight: 500;
        }
        .stRadio > div > div > label {
            color: black !important;
            font-weight: 500;
        }
        /* Make active radio button text white on black background */
        .stRadio > div > div > label[data-baseweb="radio"] > div > div:first-child {
            background-color: black;
        }
        .stRadio > div > div > label[data-baseweb="radio"] > div > div:first-child > div {
            background-color: white;
        }
        /* Make sure the radio button itself is visible */
        .stRadio > div > div > label > div > div {
            border-color: black !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        length_choice = st.radio("", ["Short", "Medium", "Long"], horizontal=True, index=1, key="length_radio")
        length = length_options[length_choice]
    
    with col2:
        st.markdown('<div style="font-weight: 500; margin-bottom: 8px; color: black;">👤 Main Character</div>', unsafe_allow_html=True)
        character_name = st.text_input("", "Alex", key="character_input",
                                     placeholder="e.g. A brave knight, A curious child")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div style="font-weight: 500; margin-bottom: 8px; color: black;">🏞️ Setting</div>', unsafe_allow_html=True)
        setting = st.text_input("", "Enchanted forest with ancient trees", key="setting_input",
                              placeholder="e.g. Enchanted forest, Desert city")
    
    with col2:
        st.markdown('<div style="font-weight: 500; margin-bottom: 8px; color: black;">🕰️ Era</div>', unsafe_allow_html=True)
        era = st.text_input("", "Medieval times", key="era_input",
                          placeholder="e.g. Medieval times, Future, 1920s")
    
    # Keywords field
    st.markdown('<div style="font-weight: 500; margin-top: 20px; margin-bottom: 8px; color: black;">🔑 Keywords (comma-separated)</div>', unsafe_allow_html=True)
    keywords = st.text_area("", "magic, forest, adventure, discovery, ancient secrets", key="keywords_input",
                          height=100)
    
    # Options
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown('<div style="font-weight: 500; margin-bottom: 8px; color: black;">Options</div>', unsafe_allow_html=True)
    
    # Custom CSS for checkboxes
    st.markdown("""
    <style>
    .stCheckbox > div > div > label {
        color: black !important;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        generate_image = st.checkbox("Generate illustration", value=True, key="gen_image_check")
    
    with col2:
        generate_speech = st.checkbox("Generate audio narration", value=True, key="gen_audio_check")
    
    # Generate Button (centered) with custom styling
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Apply special styling to ensure text is visible
        st.markdown("""
        <style>
        /* Target the specific button */
        button[kind="primaryFormSubmit"] {
            background-color: black !important;
            color: white !important;
            border: 2px solid black !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        generate_story_btn = st.button("✨ Generate Story", use_container_width=True, key="generate_story_btn", type="primary")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Story Generation Logic
    if generate_story_btn:
        if not keywords.strip() or not topic.strip() or not character_name.strip():
            st.error("Please fill out all required fields!")
        else:
            # Combine setting and era into the topic for better context
            full_topic = f"{topic} set in {setting} during {era}"
            
            with st.spinner("✨ Creating your magical story..."):
                story_gen = StoryGenerator()
                title, story = story_gen.generate_story(genre, length, full_topic, character_name, keywords)
                
                if story:
                    # Store story in session state
                    st.session_state.title = title.strip().replace('"', '')
                    st.session_state.story = story
                    st.session_state.story_generated = True
                    st.session_state.play_audio = False
                    
                    # Export as text
                    exporter = StoryExporter()
                    exporter.save_story_txt(st.session_state.title, st.session_state.story)
            
            # Generate Image
            if generate_image:
                with st.spinner("🎨 Creating illustration..."):
                    image_gen = ImageGenerator()
                    image_url = image_gen.generate_image(genre, full_topic, keywords)
                    st.session_state.image_url = image_url
            
            # Generate Speech
            if generate_speech:
                with st.spinner("🎙️ Creating audio narration..."):
                    tts_gen = TTSGenerator()
                    st.session_state.audio_file = tts_gen.generate_speech(st.session_state.story)
            
            # Generate PDF
            with st.spinner("📄 Finalizing your story..."):
                st.session_state.pdf_path = exporter.save_story_pdf(
                    st.session_state.title, 
                    st.session_state.story, 
                    st.session_state.image_url
                )
            
            # Change to story view page
            go_to_page("story_view")

elif st.session_state.page == "story_view" and st.session_state.story_generated:
    # Story View Page with improved layout
    st.markdown("<div style='background-color: white; padding: 20px; border-radius: 10px;'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Story Content
        st.markdown(f"""
        <div class="story-container">
            <h1 class="story-title">{st.session_state.title}</h1>
            <div class="story-content">
                {st.session_state.story.replace('\n', '<br>')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Audio Player
        if st.session_state.audio_file and os.path.exists(st.session_state.audio_file):
            st.markdown("<div style='background-color: #f8f8f8; padding: 15px; border-radius: 10px; margin-top: 20px;'>", unsafe_allow_html=True)
            
            audio_col1, audio_col2 = st.columns([1, 4])
            
            with audio_col1:
                if st.button("🎙️ " + ("Pause" if st.session_state.play_audio else "Read Aloud"), 
                           key="audio_toggle_btn", 
                           type="primary"):
                    toggle_audio()
            
            with audio_col2:
                if st.session_state.play_audio:
                    st.audio(st.session_state.audio_file, format="audio/mp3")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # PDF Download Button
        if st.session_state.pdf_path:
            try:
                with open(st.session_state.pdf_path, "rb") as file:
                    st.download_button(
                        "📥 Download Story as PDF",
                        file,
                        file_name=f"{st.session_state.title}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Error preparing PDF download: {str(e)}")
    
    with col2:
        # Story Image
        if st.session_state.image_url:
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.image(
                st.session_state.image_url,
                caption=f"Illustration for '{st.session_state.title}'",
                use_column_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Story Metadata
        st.markdown("<h3 style='color: black;'>Story Details</h3>", unsafe_allow_html=True)
        
        # Display metadata as metrics
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Words", len(st.session_state.story.split()))
        with col_b:
            st.metric("Reading Time", f"{len(st.session_state.story.split()) // 200 + 1} min")
        
        # Story type
        st.markdown(f"<div style='margin-top: 15px; padding: 10px; background-color: #f8f8f8; border-radius: 5px; text-align: center;'><strong>Genre:</strong> {genre}</div>", unsafe_allow_html=True)
        
        # Create New Story Button
        st.button("✨ Create Another Story", on_click=lambda: go_to_page("create_form"), key="create_another_btn")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 40px 0; color: black; font-size: 14px; background-color: white; margin-top: 40px;">
    © 2025 StoryBloom AI • Create magical stories with AI
</div>
""", unsafe_allow_html=True)
