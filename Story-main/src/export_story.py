import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

class StoryExporter:
    def __init__(self):
        self.export_dir = "output_stories"
        os.makedirs(self.export_dir, exist_ok=True)  # Ensure directory exists

    def save_story_txt(self, title, story):
        """Save the story as a text file."""
        clean_title = title.strip().replace(" ", "_").replace('"', '')  # Format file name
        file_path = os.path.join(self.export_dir, f"{clean_title}.txt")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(f"{title}\n\n{story}")

        return file_path

    def save_story_pdf(self, title, story, image_url=None):
        """Generate a properly formatted multi-page PDF file with the story and an optional image."""
        clean_title = title.strip().replace(" ", "_").replace('"', '')
        pdf_path = os.path.join(self.export_dir, f"{clean_title}.pdf")

        # Create a PDF canvas
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        # Function to add a new page when needed
        def add_new_page():
            c.showPage()
            c.setFont("Helvetica", 12)
            return height - 50  # Reset text position

        # Add title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, title)

        # Add image if available
        if image_url:
            try:
                from PIL import Image
                import requests
                from io import BytesIO

                response = requests.get(image_url)
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content))
                    img_path = os.path.join(self.export_dir, f"{clean_title}.jpg")
                    img.save(img_path)

                    # Resize and add image at top
                    c.drawImage(img_path, 50, height - 320, width=500, height=250, preserveAspectRatio=True, mask='auto')
                    story_y_position = height - 350  # Start story below image
                else:
                    story_y_position = height - 80  # No image, start closer to top
            except Exception as e:
                print(f"⚠️ Image could not be added to PDF: {e}")
                story_y_position = height - 80  # No image, start text below title
        else:
            story_y_position = height - 80  # No image, start text below title

        # Story text rendering with multi-page handling
        c.setFont("Helvetica", 12)
        margin_x = 50
        max_width = width - 2 * margin_x  # Text area width
        line_spacing = 14  # Line height

        for line in story.split("\n"):
            wrapped_lines = simpleSplit(line, "Helvetica", 12, max_width)

            for wrapped_line in wrapped_lines:
                if story_y_position <= 50:  # Check if we need a new page
                    story_y_position = add_new_page()
                
                c.drawString(margin_x, story_y_position, wrapped_line)
                story_y_position -= line_spacing  # Move to next line

        # Save PDF
        c.showPage()
        c.save()
        return pdf_path
