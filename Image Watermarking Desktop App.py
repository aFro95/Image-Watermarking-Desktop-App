import os

from tkinter import Tk, Label, Button, filedialog, simpledialog, Entry

from PIL import Image, ImageDraw, ImageFont


class WatermarkApp:
    def __init__(self, master):
        self.image_path = None
        self.output_dir = None
        self.watermark_text = None
        self.master = master
        master.title("Watermark App")
        self.label = Label(master, text="Enter the path of the image or click 'Browse' to select:")
        self.label.pack()
        self.image_path_entry = Entry(master, width=50)  # Entry widget for the image path
        self.image_path_entry.pack()
        self.browse_button = Button(master, text="Browse", command=self.upload_image)
        self.browse_button.pack()
        self.add_watermark_button = Button(master, text="Add Watermark", command=self.add_watermark)
        self.add_watermark_button.pack()
        self.set_parameters_button = Button(master, text="Save As!", command=self.set_parameters)
        self.set_parameters_button.pack()

    def upload_image(self):
        file_path = filedialog.askopenfilename(initialdir="/", title="Select Image",
                                               filetypes=(("JPEG files", "*.jpg"), ("all files", "*.*")))
        self.image_path = file_path
        self.image_path_entry.delete(0, 'end')  # Clear the Entry widget
        self.image_path_entry.insert(0, file_path)  # Insert the selected path into the Entry widget
        self.label.config(text=f"Selected Image: {os.path.basename(file_path)}")

    def set_parameters(self):
        self.output_dir = filedialog.askdirectory(title="Select Output Directory")
        self.watermark_text = simpledialog.askstring("Input", "Enter Watermark Text:")
        self.label.config(text="Parameters set. You can now add a watermark.")

    def add_watermark(self):
        if hasattr(self, 'image_path') and hasattr(self, 'output_dir') and hasattr(self, 'watermark_text'):
            original_image = Image.open(self.image_path)
            width, height = original_image.size
            watermarked_image = original_image.copy()
            draw = ImageDraw.Draw(watermarked_image)
            font = ImageFont.load_default()
            text_width, text_height = draw.textsize(self.watermark_text, font)
            text_position = ((width - text_width) // 2, (height - text_height) // 2)
            draw.text(text_position, self.watermark_text, font=font, fill=(255, 255, 255, 128))
            output_path = os.path.join(self.output_dir, f"watermarked_{os.path.basename(self.image_path)}")
            watermarked_image.save(output_path)
            self.label.config(text=f"Watermarked Image saved at: {output_path}")

        else:
            self.label.config(text="Please enter a valid image path and set parameters before adding a watermark.")


if __name__ == "__main__":
    root = Tk()
    app = WatermarkApp(root)
    root.mainloop()
