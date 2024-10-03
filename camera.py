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
        self.images = []  # Store all captured images
        self.descriptions = []  # Store descriptions for each image
        self.pointer_coords = []  # Store pointer coordinates for each image
        self.current_image_index = -1  # Track current image index
        self.image = None
        self.image_path = ""
        self.annotated_image_path = ""
        self.part_number = ""

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

        self.next_button = tk.Button(root, text="Next", command=self.next_step)
        self.next_button.pack()

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
        self.current_image_index += 1
        self.image_path = f"captured_image_{self.current_image_index}.jpg"
        self.annotated_image_path = f"annotated_image_{self.current_image_index}.jpg"
        cv2.imwrite(self.image_path, cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR))
        self.image = Image.open(self.image_path)
        print("Image captured and saved as", self.image_path)
        self.images.append(self.image)

    def add_description(self):
        description = simpledialog.askstring("Input", "Enter a description for the image:")
        part_number = simpledialog.askstring("Input", "Enter the part number:")
        print("Description added:", description)
        self.descriptions.append((description, part_number))

    def add_pointer(self):
        def click_event(event):
            x, y = event.x, event.y
            self.pointer_coords.append((x, y))

            self.image = Image.open(self.image_path)
            draw = ImageDraw.Draw(self.image)
            draw.ellipse((x-10, y-10, x+10, y+10), outline="red", width=3)
            self.image.save(self.annotated_image_path)

            self.frame_tk = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.frame_tk)
            print(f"Pointer added at ({x}, {y})")

        self.canvas.bind("<Button-1>", click_event)

    def next_step(self):
        # After adding pointer and description, move to next step
        self.capture_image()
        self.add_description()

    def draw_chat_bubble(self, img, text, coords):
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        # Bounding box calculation for text size
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        bubble_padding = 10
        bubble_width = text_width + 2 * bubble_padding
        bubble_height = text_height + 2 * bubble_padding
        bubble_x = coords[0] + 20  # Position the bubble to the right of the pointer
        bubble_y = coords[1] - bubble_height - 10  # Above the pointer

        # Draw the chat bubble and text
        draw.rectangle([bubble_x, bubble_y, bubble_x + bubble_width, bubble_y + bubble_height], fill="white", outline="black")
        draw.text((bubble_x + bubble_padding, bubble_y + bubble_padding), text, fill="black", font=font)

        return img

    def create_pdf(self):
        if not self.images:
            print("No images captured.")
            return

        pdf_filename = "procedure_documentation.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=A4)

        for i, (image, description_data) in enumerate(zip(self.images, self.descriptions)):
            description, part_number = description_data
            pointer_coord = self.pointer_coords[i]

            # Draw chat bubble on the image
            annotated_image = self.draw_chat_bubble(image, description, pointer_coord)
            annotated_image.save(self.annotated_image_path)

            # PDF Layout similar to your provided structure
            c.setFont("Helvetica", 12)
            c.drawString(50, 800, f"Step {i+1}: {description}")
            c.drawString(50, 780, f"Part Number: {part_number}")
            c.drawImage(self.annotated_image_path, 50, 300, width=500, height=400)
            c.rect(45, 295, 510, 410, stroke=1, fill=0)

            # New page after each step
            c.showPage()

        c.save()
        print("PDF created as", pdf_filename)

# Main application loop
if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoApp(root)
    root.mainloop()
