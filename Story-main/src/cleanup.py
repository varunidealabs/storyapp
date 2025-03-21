import os

def clear_directory(directory):
    """Delete all files inside a given directory."""
    if os.path.exists(directory):
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            try:
                os.remove(file_path)  # Delete each file
            except Exception as e:
                print(f"⚠️ Could not delete {file}: {e}")

def clear_all_temp_files():
    """Clear all temporary files in `output_stories/` and `output_audio/`."""
    clear_directory("output_stories")
    clear_directory("output_audio")
