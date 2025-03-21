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

# Custom CSS for styling
st.markdown("""
<style>
    /* Global Styles */
    body {
        font-family: 'Inter', sans-serif;
        background-color: white;
    }
    
    /* Header Styles */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 0;
        border-bottom: 1px solid #f0f0f0;
        margin-bottom: 20px;
    }
    .header-logo {
        font-size: 24px;
        font-weight: bold;
        color: #1a1a1a;
    }
    .header-nav a {
        margin-left: 20px;
        color: #666;
        text-decoration: none;
    }
    
    /* Hero Section */
    .hero-container {
        text-align: center;
        padding: 40px 0;
        max-width: 800px;
        margin: 0 auto;
    }
    .hero-badge {
        background-color: #f8f8f8;
        color: #666;
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
        color: #1a1a1a;
        margin-bottom: 20px;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 40px;
        line-height: 1.6;
    }
    
    /* Action Buttons */
    .button-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 60px;
    }
    .primary-button {
        background-color: #1a1a1a;
        color: white;
        padding: 12px 24px;
        border-radius: 30px;
        font-weight: 600;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        cursor: pointer;
    }
    .secondary-button {
        background-color: #f0f0f0;
        color: #1a1a1a;
        padding: 12px 24px;
        border-radius: 30px;
        font-weight: 600;
        text-decoration: none;
        cursor: pointer;
    }
    
    /* Form Styles */
    .form-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 30px;
        background-color: white;
        border-radius: 12px;
    }
    .form-title {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    .form-subtitle {
        font-size: 16px;
        color: #666;
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
    }
    .form-input, .form-select {
        width: 100%;
        padding: 12px;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        font-size: 16px;
    }
    
    /* Story Container */
    .story-container {
        max-width: 800px;
        margin: 40px auto;
        padding: 30px;
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    .story-title {
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 20px;
        text-align: center;
    }
    .story-content {
        font-size: 18px;
        line-height: 1.6;
        color: #333;
    }
    
    /* Feature Icons */
    .feature-icons {
        display: flex;
        justify-content: center;
        gap: 80px;
        margin-top: 60px;
    }
    .feature-icon {
        font-size: 32px;
        color: #1a1a1a;
    }
    
    /* Hiding Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Button Styles */
    div.stButton > button {
        background-color: #1a1a1a;
        color: white;
        padding: 12px 24px;
        border-radius: 30px;
        font-weight: 600;
        border: none;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #333;
        border: none;
    }
    
    /* Length Selector Buttons */
    .length-selector {
        display: flex;
        gap: 10px;
    }
    .length-button {
        flex: 1;
        text-align: center;
        padding: 12px;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        cursor: pointer;
    }
    .length-button.active {
        background-color: #1a1a1a;
        color: white;
        border-color: #1a1a1a;
    }
    
    /* Custom Tabs */
    .custom-tabs {
        display: flex;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 20px;
    }
    .tab-item {
        padding: 10px 20px;
        cursor: pointer;
        border-bottom: 2px solid transparent;
    }
    .tab-item.active {
        border-bottom: 2px solid #1a1a1a;
        font-weight: bold;
    }
    
    /* Audio Player Styling */
    .audio-container {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 20px;
    }
    .audio-button {
        background-color: #f0f0f0;
        color: #1a1a1a;
        padding: 8px 16px;
        border-radius: 30px;
        font-weight: 600;
        cursor: pointer;
    }
    
    /* Story Image */
    .image-container {
        margin: 20px 0;
        border-radius: 12px;
        overflow: hidden;
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
st.markdown("""
<div class="header-container">
    <div class="header-logo">✨ StoryBloom</div>
    <div class="header-nav">
        <a href="#">Home</a>
        <a href="#">Create</a>
        <a href="#">Library</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ===== Page Content =====
if st.session_state.page == "home":
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">✨ Story generation reimagined</div>
        <h1 class="hero-title">Create beautiful stories with a few simple inputs</h1>
        <p class="hero-subtitle">Craft unique tales with stunning visuals and immersive narration, using our intuitive story generation platform</p>
        
        <div class="button-container">
            <div class="primary-button" id="create-story-btn">Create Your Story →</div>
            <div class="secondary-button" id="sample-story-btn">View Sample Story</div>
        </div>
        
        <div class="feature-icons">
            <div class="feature-icon">📚</div>
            <div class="feature-icon">🖼️</div>
            <div class="feature-icon">🎙️</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # JavaScript for button interactions
    st.markdown("""
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('create-story-btn').addEventListener('click', function() {
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'create_form'}, '*');
            });
            
            document.getElementById('sample-story-btn').addEventListener('click', function() {
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'sample_story'}, '*');
            });
        });
    </script>
    """, unsafe_allow_html=True)
    
    # Since JavaScript doesn't work directly in Streamlit, we'll use buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        create_story_btn = st.button("Create Your Story →")
        view_sample_btn = st.button("View Sample Story")
    
    if create_story_btn:
        go_to_page("create_form")
    
    if view_sample_btn:
        create_sample_story()

elif st.session_state.page == "create_form":
    # Story Creation Form
    st.markdown("""
    <div class="form-container">
        <h2 class="form-title">Craft Your Story</h2>
        <p class="form-subtitle">Fill in the details below to generate your custom story</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Form Layout with Two Columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="form-label">🎭 Theme</div>', unsafe_allow_html=True)
        topic = st.text_input("", "A magical adventure in an enchanted forest", key="theme_input",
                            placeholder="e.g. Space exploration, Medieval quest")
    
    with col2:
        st.markdown('<div class="form-label">📚 Genre</div>', unsafe_allow_html=True)
        genre = st.selectbox("", 
                            ["Fantasy", "Sci-Fi", "Mystery", "Adventure", "Romance", "Horror", "Fairy Tale"], 
                            key="genre_select")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="form-label">⏱️ Length</div>', unsafe_allow_html=True)
        length_options = {"Short": 250, "Medium": 500, "Long": 750}
        length_choice = st.radio("", ["Short", "Medium", "Long"], horizontal=True, index=1)
        length = length_options[length_choice]
    
    with col2:
        st.markdown('<div class="form-label">👤 Main Character</div>', unsafe_allow_html=True)
        character_name = st.text_input("", "Alex", key="character_input",
                                     placeholder="e.g. A brave knight, A curious child")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="form-label">🏞️ Setting</div>', unsafe_allow_html=True)
        setting = st.text_input("", "Enchanted forest with ancient trees", key="setting_input",
                              placeholder="e.g. Enchanted forest, Desert city")
    
    with col2:
        st.markdown('<div class="form-label">🕰️ Era</div>', unsafe_allow_html=True)
        era = st.text_input("", "Medieval times", key="era_input",
                          placeholder="e.g. Medieval times, Future, 1920s")
    
    # Keywords field
    st.markdown('<div class="form-label mt-20">🔑 Keywords (comma-separated)</div>', unsafe_allow_html=True)
    keywords = st.text_area("", "magic, forest, adventure, discovery, ancient secrets", key="keywords_input",
                          height=100)
    
    # Options
    col1, col2 = st.columns(2)
    
    with col1:
        generate_image = st.checkbox("Generate illustration", value=True)
    
    with col2:
        generate_speech = st.checkbox("Generate audio narration", value=True)
    
    # Generate Button (centered)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        generate_story_btn = st.button("✨ Generate Story", use_container_width=True)
    
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
    # Story View Page
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
            audio_col1, audio_col2 = st.columns([1, 4])
            
            with audio_col1:
                if st.button("🎙️ " + ("Pause" if st.session_state.play_audio else "Read Aloud")):
                    toggle_audio()
            
            with audio_col2:
                if st.session_state.play_audio:
                    st.audio(st.session_state.audio_file, format="audio/mp3")
        
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
        st.markdown("### Story Details")
        
        # Display metadata as metrics
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Words", len(st.session_state.story.split()))
        with col_b:
            st.metric("Reading Time", f"{len(st.session_state.story.split()) // 200 + 1} min")
        
        # Create New Story Button
        st.button("✨ Create Another Story", on_click=lambda: go_to_page("create_form"))

# Footer
st.markdown("""
<div style="text-align: center; padding: 40px 0; color: #666; font-size: 14px;">
    © 2025 StoryBloom AI • Create magical stories with AI
</div>
""", unsafe_allow_html=True)
