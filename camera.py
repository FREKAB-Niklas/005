import cv2
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

class PhotoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Production Procedure Documentation")

        # Initialize variables
        self.image = None
        self.image_path = "captured_image.jpg"
        self.annotated_image_path = "annotated_image.jpg"
        self.description = ""
        self.pointer_coords = (0, 0)

        # Camera capture
        self.video_capture = cv2.VideoCapture(0)

        # Create UI Elements
        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()

        self.capture_button = tk.Button(root, text="Capture Photo", command=self.capture_image)
        self.capture_button.pack()

        self.description_button = tk.Button(root, text="Add Description", command=self.add_description)
        self.description_button.pack()

        self.pointer_button = tk.Button(root, text="Add Pointer", command=self.add_pointer)
        self.pointer_button.pack()

        self.finalize_button = tk.Button(root, text="Finalize and Create PDF", command=self.create_pdf)
        self.finalize_button.pack()

        # Update canvas with video feed
        self.update_video_feed()

    def update_video_feed(self):
        ret, frame = self.video_capture.read()
        if ret:
            self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.frame_pil = Image.fromarray(self.frame)
            self.frame_tk = ImageTk.PhotoImage(self.frame_pil)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.frame_tk)
        self.root.after(10, self.update_video_feed)

    def capture_image(self):
        cv2.imwrite(self.image_path, cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR))
        self.image = Image.open(self.image_path)
        print("Image captured and saved as", self.image_path)

    def add_description(self):
        self.description = simpledialog.askstring("Input", "Enter a description for the image:")
        print("Description added:", self.description)

    def add_pointer(self):
        def click_event(event):
            x, y = event.x, event.y
            self.pointer_coords = (x, y)
            self.image = Image.open(self.image_path)
            draw = ImageDraw.Draw(self.image)

            # Draw the red circle for the pointer
            draw.ellipse((x-10, y-10, x+10, y+10), outline="red", width=3)

            # Save temporary image with pointer
            self.image.save(self.annotated_image_path)

            # Update canvas with new annotated image
            self.frame_tk = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.frame_tk)
            print(f"Pointer added at ({x}, {y})")

        # Bind click event to canvas
        self.canvas.bind("<Button-1>", click_event)

    def draw_chat_bubble(self, img, text, coords):
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        # Get the bounding box of the text (replaces textsize)
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        bubble_padding = 10
        bubble_width = text_width + 2 * bubble_padding
        bubble_height = text_height + 2 * bubble_padding
        bubble_x = coords[0] + 20  # Position the bubble to the right of the pointer
        bubble_y = coords[1] - bubble_height - 10  # Above the pointer

        # Draw bubble rectangle
        draw.rectangle([bubble_x, bubble_y, bubble_x + bubble_width, bubble_y + bubble_height], fill="white", outline="black")

        # Draw the text in the bubble
        draw.text((bubble_x + bubble_padding, bubble_y + bubble_padding), text, fill="black", font=font)

        return img


    def create_pdf(self):
        if not self.image:
            print("No image captured yet.")
            return

        # Annotate the image with chat bubble and pointer
        annotated_image = Image.open(self.annotated_image_path)
        annotated_image_with_bubble = self.draw_chat_bubble(annotated_image, self.description, self.pointer_coords)
        annotated_image_with_bubble.save(self.annotated_image_path)  # Save the final image

        pdf_filename = "procedure_documentation.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=A4)

        # Set margins and positioning for A4 format
        c.setFont("Helvetica", 12)

        # Add title or description on the first page
        c.drawString(50, 800, f"Procedure Documentation: {self.description}")

        # Add the final annotated image to the PDF
        c.drawImage(self.annotated_image_path, 50, 300, width=500, height=400)  # Fits image in A4 format

        # Draw a border around the image for a professional look
        c.rect(45, 295, 510, 410, stroke=1, fill=0)

        # Add some professional footer text (optional)
        c.setFont("Helvetica", 10)
        c.drawString(50, 50, "Document created using Raspberry Pi-based system")

        # Save PDF
        c.save()
        print("PDF created as", pdf_filename)

# Main application loop
if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoApp(root)
    root.mainloop()
