import os
from tkinter import Tk, filedialog, Label, Button
from PIL import Image, ImageTk, ImageEnhance

def select_images():
    global images_folder
    images_folder = filedialog.askdirectory(title="Select Folder Containing Images")
    if images_folder:
        status_label.config(text=f"Selected Images Folder: {images_folder}")

def select_logo():
    global logo_path
    logo_path = filedialog.askopenfilename(title="Select Logo", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if logo_path:
        status_label.config(text=f"Selected Logo: {logo_path}")

def add_logo():
    if not images_folder or not logo_path:
        status_label.config(text="Please select both images folder and logo.")
        return

    output_folder = os.path.join(images_folder, "res")
    os.makedirs(output_folder, exist_ok=True)

    logo = Image.open(logo_path).convert("RGBA")

    for image_file in os.listdir(images_folder):
        if image_file.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(images_folder, image_file)
            image = Image.open(image_path).convert("RGBA")

            # Adjust image colors to make them colder (add a blue tint)
            r, g, b, a = image.split()
            image = Image.merge("RGBA", (r, g, b, a))

            image_width, image_height = image.size

            # Adjust logo width and proportionally scale height
            new_logo_width = int(image_width)         # Full width of the image
            new_logo_height = int(logo.size[1] * (new_logo_width / logo.size[0]))  # Maintain aspect ratio
            resized_logo = logo.resize((new_logo_width, new_logo_height), Image.LANCZOS)

            # Position logo to cover the lower part
            position = (0, image_height - new_logo_height)
            image.paste(resized_logo, position, resized_logo)

            output_path = os.path.join(output_folder, image_file)
            image.save(output_path, format="PNG")

    status_label.config(text=f"Logo added to images! Output folder: {output_folder}")

# Initialize Tkinter app
root = Tk()
root.title("Logo Overlay App")
root.geometry("500x300")

images_folder = ""
logo_path = ""

Label(root, text="Logo Overlay App", font=("Arial", 16)).pack(pady=10)
Button(root, text="Select Images Folder", command=select_images, width=20).pack(pady=5)
Button(root, text="Select Logo", command=select_logo, width=20).pack(pady=5)
Button(root, text="Add Logo to Images", command=add_logo, width=20).pack(pady=10)

status_label = Label(root, text="", wraplength=400, fg="green")
status_label.pack(pady=10)

root.mainloop()
