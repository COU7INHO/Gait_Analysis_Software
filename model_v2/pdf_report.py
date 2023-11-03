from PyQt5.QtWidgets import QFileDialog
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

# Register font


class PdfGen:
    X_MARGIN = 80

    def __init__(self, name, amp_level, amp_limb):
        self.name = name
        self.amp_level = amp_level
        self.amp_limb = amp_limb

    def save_as_pdf(self, comments, dialog):
        file_path, _ = QFileDialog.getSaveFileName(
            dialog, "Save gait analysis results", "", "PDF Files (*.pdf)"
        )

        if file_path:
            # Create a new PDF file
            c = canvas.Canvas(file_path, pagesize=A4)

            # Set the font and size for the comments
            c.setFont("Helvetica", 12)

            # Add a logo to the top left corner
            image_path = "logo.png"  # Replace with the actual path to your image file
            c.drawImage(image_path, 10, 720, width=130, height=100)

            # Set right margin
            right_margin = A4[0] - inch  # Use inch unit

            # Amputee info
            c.setFont("Helvetica", 12)  # Set bold font for the label
            c.drawString(self.X_MARGIN, 680, f"Name: {self.name}")  # Draw label
            c.drawString(self.X_MARGIN, 660, f"Amputation level:  {self.amp_level}")
            c.drawString(self.X_MARGIN, 640, f"Amputated limb:  {self.amp_limb}")

            # Split comments into paragraphs based on line breaks
            paragraphs = comments.split("\n")

            # Write the paragraphs to the PDF
            c.drawString(self.X_MARGIN, 600, "Comments:")
            y = 580  # Set initial y-coordinate for the first line

            for paragraph in paragraphs:
                if c.stringWidth(paragraph) > right_margin - self.X_MARGIN:
                    # Text exceeds the right margin, split it into lines
                    words = paragraph.split()
                    line = ""
                    for word in words:
                        if (
                            c.stringWidth(line + " " + word)
                            < right_margin - self.X_MARGIN
                        ):
                            line += " " + word
                        else:
                            c.drawString(self.X_MARGIN, y, line)  # Draw the line
                            y -= 20  # Move to the next line
                            line = word
                    c.drawString(
                        self.X_MARGIN, y, line
                    )  # Draw the last line of the paragraph
                    y -= 20  # Move to the next line
                else:
                    c.drawString(
                        self.X_MARGIN, y, paragraph
                    )  # Draw the entire paragraph
                    y -= 20  # Move to the next line

            # Save and close the PDF
            c.save()

        # Close the dialog
        dialog.close()
