import streamlit as st
import os
import time
from src.story_generator import StoryGenerator
from src.image_generator import ImageGenerator
from src.tts_generator import TTSGenerator
from src.export_story import StoryExporter
from src.cleanup import clear_all_temp_files

# ===== App Configuration =====
st.set_page_config(
    page_title="TaleScape AI - Craft Magical Stories",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== CSS Styling =====
st.markdown("""
<style>
    /* Main App Style */
    .main {
        background-color: #fcfcff;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #4a3d7c;
        font-family: 'Georgia', serif;
    }
    
    /* Title Styling */
    .title-container {
        background-color: #f0f0ff;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border-left: 5px solid #7c4bc9;
        text-align: center;
    }
    
    /* Story Container */
    .story-container {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        border: 1px solid #e0e0ff;
    }
    
    /* Story Text */
    .story-text {
        font-family: 'Garamond', serif;
        font-size: 1.1rem;
        line-height: 1.6;
        color: #333;
        white-space: pre-line;
    }
    
    /* Button Styling */
    .stButton>button {
        background-color: #7c4bc9;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 1.5rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #6438a7;
        border: none;
    }
    
    /* Image Container */
    .image-container {
        border-radius: 10px;
        overflow: hidden;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Audio Player Styling */
    .audio-container {
        background-color: #f0f0ff;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #f5f5ff;
    }
    
    /* Form Fields */
    input, textarea, select {
        border-radius: 5px !important;
        border: 1px solid #d0d0ff !important;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Download Button */
    .download-btn {
        background-color: #4caf50 !important;
        color: white !important;
    }
    
    /* Story Title */
    .story-title {
        font-family: 'Georgia', serif;
        font-size: 2rem;
        margin-bottom: 1rem;
        color: #4a3d7c;
        text-align: center;
        font-weight: bold;
    }
    
    /* Loading Animation */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
    }
    
    /* Separator */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background-color: #e0e0ff;
    }
</style>
""", unsafe_allow_html=True)

# ===== App Initialization =====
# Ensure directories exist
os.makedirs("output_stories", exist_ok=True)
os.makedirs("output_audio", exist_ok=True)

# Initialize session state
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    clear_all_temp_files()  # This will run only once when the app starts

for key in ["story", "title", "image_url", "pdf_path", "audio_file", "story_generated", "play_audio"]:
    if key not in st.session_state:
        st.session_state[key] = None

if "play_audio" not in st.session_state:
    st.session_state.play_audio = False

# ===== Helper Functions =====
def toggle_audio():
    """Toggle audio playback state"""
    st.session_state.play_audio = not st.session_state.play_audio

# ===== App Header =====
st.markdown("""
<div class="title-container">
    <h1>✨ TaleScape AI ✨</h1>
    <p>Create magical stories, stunning images, and immersive audio with AI</p>
</div>
""", unsafe_allow_html=True)

# ===== Sidebar Controls =====
with st.sidebar:
    st.image("https://img.freepik.com/free-vector/hand-drawn-fairy-tale-background_23-2149144907.jpg", use_column_width=True)
    
    st.markdown("## 🧙‍♂️ Story Wizard")
    
    # Genre Selection with emojis
    genre_options = {
        "Fantasy": "🧙‍♂️ Fantasy",
        "Sci-Fi": "🚀 Sci-Fi", 
        "Mystery": "🔍 Mystery",
        "Romance": "❤️ Romance",
        "Horror": "👻 Horror",
        "Adventure": "🏔️ Adventure",
        "Fairy Tale": "🧚 Fairy Tale"
    }
    genre = st.selectbox(
        "Choose your story genre:",
        list(genre_options.keys()),
        format_func=lambda x: genre_options[x]
    )
    
    # Story Length Selection
    st.markdown("### 📏 Story Length")
    length_options = {"Small": 250, "Medium": 500, "Large": 750}
    length_choice = st.select_slider(
        "Select story size:",
        options=["Small", "Medium", "Large"],
        value="Medium"
    )
    length = length_options[length_choice]
    st.caption(f"Approximately {length} words")
    
    # Story Details
    st.markdown("### 📝 Story Details")
    topic = st.text_input("Story topic or theme", "A magical forest with hidden secrets")
    character_name = st.text_input("Main character's name", "Alex")
    
    # Keywords with better UI
    st.markdown("### 🔑 Key Elements")
    st.caption("Add important elements to include in your story (comma-separated)")
    keywords = st.text_area("", "forest, magic, adventure, ancient tree, hidden door")
    
    # Generate options
    st.markdown("### 🎨 Media Options")
    col1, col2 = st.columns(2)
    with col1:
        generate_image = st.checkbox("Story Image", value=True)
    with col2:
        generate_speech = st.checkbox("Audio Narration", value=True)
    
    # Generate Button
    st.markdown("### 🪄 Create Your Story")
    generate_button = st.button("✨ Generate Story", use_container_width=True, type="primary")

# ===== Story Generation Logic =====
if generate_button:
    if not keywords.strip() or not topic.strip():
        st.error("Please enter a story topic and at least one keyword!")
    else:
        # Step 1: Generate Story
        with st.spinner("🧙‍♂️ Crafting your magical story..."):
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
        
        # Step 2: Generate Image
        if generate_image:
            with st.spinner("🎨 Creating a beautiful illustration..."):
                image_gen = ImageGenerator()
                image_url = image_gen.generate_image(genre, topic, keywords)
                st.session_state.image_url = image_url
        
        # Step 3: Generate Speech
        if generate_speech:
            with st.spinner("🎙️ Narrating your story..."):
                tts_gen = TTSGenerator()
                st.session_state.audio_file = tts_gen.generate_speech(st.session_state.story)
        
        # Step 4: Generate PDF
        with st.spinner("📄 Preparing your story book..."):
            st.session_state.pdf_path = exporter.save_story_pdf(
                st.session_state.title, 
                st.session_state.story, 
                st.session_state.image_url
            )

# ===== Display Story Content =====
if st.session_state.story_generated:
    # Layout columns for content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display story container
        st.markdown(f"""
        <div class="story-container">
            <div class="story-title">{st.session_state.title}</div>
            <div class="story-text">{st.session_state.story.replace("\n", "<br>")}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Audio controls
        if st.session_state.audio_file and os.path.exists(st.session_state.audio_file):
            st.markdown('<div class="audio-container">', unsafe_allow_html=True)
            
            audio_col1, audio_col2 = st.columns([1, 3])
            with audio_col1:
                if st.button("🎙️ " + ("Pause" if st.session_state.play_audio else "Read Aloud"), 
                             key="read_aloud"):
                    toggle_audio()
            
            with audio_col2:
                if st.session_state.play_audio:
                    st.audio(st.session_state.audio_file, format="audio/mp3")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Download PDF
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
                st.error(f"Error opening PDF: {str(e)}")
                if st.session_state.title and st.session_state.story:
                    exporter = StoryExporter()
                    st.session_state.pdf_path = exporter.save_story_pdf(
                        st.session_state.title,
                        st.session_state.story,
                        st.session_state.image_url
                    )
    
    with col2:
        # Display generated image
        if st.session_state.image_url:
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.image(
                st.session_state.image_url,
                caption=f"AI Illustration for '{st.session_state.title}'",
                use_column_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Display story stats
        st.markdown("### 📊 Story Stats")
        
        stats_col1, stats_col2 = st.columns(2)
        with stats_col1:
            st.metric("Words", len(st.session_state.story.split()))
        with stats_col2:
            st.metric("Characters", len(st.session_state.story))
        
        # Add genre icon
        genre_icons = {
            "Fantasy": "🧙‍♂️", "Sci-Fi": "🚀", "Mystery": "🔍",
            "Romance": "❤️", "Horror": "👻", "Adventure": "🏔️",
            "Fairy Tale": "🧚"
        }
        current_genre = next((g for g in genre_icons.keys() if g in genre), "Fantasy")
        st.markdown(f"### Genre: {genre_icons.get(current_genre, '📚')} {current_genre}")
        
        # Share button (placeholder - would need backend integration)
        st.button("🔗 Share Story", use_container_width=True, disabled=True)
        st.caption("Sharing feature coming soon!")

# ===== Footer =====
st.markdown("""
<hr>
<p style="text-align: center; color: #888; font-size: 0.8rem;">
    TaleScape AI - Create magical stories with the power of artificial intelligence.
    <br>Built with Streamlit and Azure OpenAI.
</p>
""", unsafe_allow_html=True)
