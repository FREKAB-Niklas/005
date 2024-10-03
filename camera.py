import cv2
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk, ImageDraw
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
            self.image = Image.open(self.image_path)
            draw = ImageDraw.Draw(self.image)
            draw.ellipse((x-10, y-10, x+10, y+10), outline="red", width=3)
            self.image.save(self.annotated_image_path)
            print(f"Pointer added at ({x}, {y})")

            # Update canvas with the new annotated image
            self.frame_tk = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.frame_tk)

        # Bind click event to canvas
        self.canvas.bind("<Button-1>", click_event)

    def create_pdf(self):
        if not self.image:
            print("No image captured yet.")
            return

        pdf_filename = "procedure_documentation.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=A4)

        # Add description to the PDF
        if self.description:
            c.drawString(100, 750, f"Description: {self.description}")

        # Add image to the PDF
        if self.annotated_image_path:
            c.drawImage(self.annotated_image_path, 50, 300, width=500, height=400)
        else:
            c.drawImage(self.image_path, 50, 300, width=500, height=400)

        c.save()
        print("PDF created as", pdf_filename)

# Main application loop
if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoApp(root)
    root.mainloop()
