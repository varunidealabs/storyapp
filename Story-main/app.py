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

# Page config
st.set_page_config(page_title="AI Story Generator", page_icon="📖")

# ✅ FIX: Only clear temp files on the very first app launch, never on refresh
if "initialized" not in st.session_state:
    st.session_state.initialized = True  # Set flag first before clearing files!
    clear_all_temp_files()  # This will now run only once when the app starts

# ✅ Ensure all session state keys are initialized to avoid KeyError
for key in ["story", "title", "image_url", "pdf_path", "audio_file", "story_generated", "play_audio"]:
    if key not in st.session_state:
        st.session_state[key] = None

# Initialize play_audio state
if "play_audio" not in st.session_state:
    st.session_state.play_audio = False

def toggle_audio():
    """Toggle audio playback state"""
    st.session_state.play_audio = not st.session_state.play_audio
    # No rerun needed - state change will trigger rerender

st.sidebar.header("Story Settings")
genre = st.sidebar.selectbox("Choose a genre:", ["Fantasy", "Sci-Fi", "Mystery", "Romance", "Horror"])

# 🔹 Story Length Selection
length_options = {"Small": 200, "Medium": 500, "Large": 700}
length_choice = st.sidebar.selectbox("Story Length:", ["Small", "Medium", "Large"])
length = length_options[length_choice]  # Convert selection to word count

st.sidebar.subheader("Story Details")
topic = st.sidebar.text_input("Enter a short topic", "A knight's journey to find the lost treasure")
character_name = st.sidebar.text_input("Main Character's Name", "Alex")
keywords = st.sidebar.text_area("Enter important keywords (comma-separated)", "castle, dragon, treasure")

# Image & Speech Options
generate_image = st.sidebar.checkbox("Generate Story Image 🎨")
generate_speech = st.sidebar.checkbox("Generate Audio 🎙️")

# Generate story button
if st.sidebar.button("Generate Story"):
    if not keywords.strip() or not topic.strip():
        st.error("Please enter a short topic and at least one keyword!")
    else:
        with st.spinner("Generating your story..."):
            story_gen = StoryGenerator()
            title, story = story_gen.generate_story(genre, length, topic, character_name, keywords)

            if story:
                # ✅ Store story in session state (Ensures it persists after refresh)
                st.session_state.title = title.strip().replace('"', '')
                st.session_state.story = story
                st.session_state.story_generated = True  # Flag to indicate story was generated
                st.session_state.play_audio = False  # Reset audio state

                # ✅ Export Story as text (PDF will be generated after image)
                exporter = StoryExporter()
                exporter.save_story_txt(st.session_state.title, st.session_state.story)

        # ✅ Step 2: Generate Image (if selected)
        image_url = None  # Temporary variable
        if generate_image:
            with st.spinner("Generating AI image... 🎨"):
                image_gen = ImageGenerator()
                image_url = image_gen.generate_image(genre, topic, keywords)
                st.session_state.image_url = image_url  # Store in session state

        # ✅ Step 3: Generate Speech (if selected)
        if generate_speech:
            with st.spinner("Generating audio... 🎙️"):
                tts_gen = TTSGenerator()
                st.session_state.audio_file = tts_gen.generate_speech(st.session_state.story)

        # ✅ Step 4: Generate PDF (after everything else is done)
        with st.spinner("Generating your story PDF... 📄"):
            exporter = StoryExporter()
            st.session_state.pdf_path = exporter.save_story_pdf(st.session_state.title, st.session_state.story, st.session_state.image_url)

# ✅✅ ALWAYS display the content if it exists in session state
# This ensures content is shown after download button is clicked
if st.session_state.story_generated:
    # Display title and story
    st.header(st.session_state.title)
    st.write("### ✨ Your AI-Generated Story:")
    st.markdown(st.session_state.story)
    
    # Display image if it exists
    if st.session_state.image_url:
        st.image(st.session_state.image_url, caption=f"AI Illustration for {st.session_state.title}", use_container_width=True)
    
    # Handle audio - show only a simple button
    if st.session_state.audio_file and os.path.exists(st.session_state.audio_file):
        # Create a single standard button that toggles audio state
        if st.button("🎙️ Read Aloud", key="read_aloud", 
                     type="primary" if not st.session_state.play_audio else "secondary"):
            toggle_audio()
            
        # Only show audio player if play_audio is True (but it will be hidden by CSS)
        if st.session_state.play_audio:
            # Use a container with no visual elements to play the audio
            with st.container():
                st.audio(st.session_state.audio_file, format="audio/mp3")
    
    # ✅ PDF Download
    if st.session_state.pdf_path:
        try:
            with open(st.session_state.pdf_path, "rb") as file:
                st.download_button("📥 Download Story as PDF", file, file_name=f"{st.session_state.title}.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"Error opening PDF: {str(e)}")
            # If there's an error, try regenerating the PDF
            if st.session_state.title and st.session_state.story:
                exporter = StoryExporter()
                st.session_state.pdf_path = exporter.save_story_pdf(st.session_state.title, st.session_state.story, st.session_state.image_url)
                with open(st.session_state.pdf_path, "rb") as file:
                    st.download_button("📥 Download Story as PDF", file, file_name=f"{st.session_state.title}.pdf", mime="application/pdf")
