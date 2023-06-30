from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QFileDialog


class PdfGen():
    def __init__(self):
        pass
    
    def save_as_pdf(self, comments, dialog):
        file_path, _ = QFileDialog.getSaveFileName(dialog, "Save gait analysis results", "", "PDF Files (*.pdf)")

        if file_path:
            # Create a new PDF file
            c = canvas.Canvas(file_path, pagesize=A4)

            # Set the font and size for the comments
            c.setFont("Helvetica", 12)

            # Add a logo to the top left corner
            image_path = "logo.png"  # Replace with the actual path to your image file
            c.drawImage(image_path, 10, 720, width=130, height=100)

            # Split comments into paragraphs based on line breaks
            paragraphs = comments.split('\n')

            # Set initial y-coordinate for the first paragraph
            y = 680

            # Write the paragraphs to the PDF
            c.drawString(50, 680, "Comments:")
            y -= 20  # Move to the next line
            for paragraph in paragraphs:
                c.drawString(100, y, paragraph)
                y -= 20  # Move to the next line

            # Save and close the PDF
            c.save()

        # Close the dialog
        dialog.close()