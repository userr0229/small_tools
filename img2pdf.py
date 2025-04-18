# This program converts images to PDF files
#
# Expected file structure:
# 
# └── your_folder/
#     ├── img2pdf.py
#     └── asstes/
#         ├── folder1/
#         │   ├── image1.jpg
#         │   ├── image2.png
#         │   └── image3.webp
#         ├── folder2/
#         │   └── ...
#         └── output_pdf/
#             ├── folder1.pdf
#             └── folder2.pdf
#
# Features:
# 1. Automatically scans all subfolders in the 'asstes' directory
# 2. Supports image formats: PNG, JPG, JPEG, BMP, GIF, WEBP
# 3. Automatically resizes images to max 1300px
# 4. Converts RGBA/P mode to RGB automatically
# 5. Outputs PDF with lower resolution (72dpi) and compression (73%) to reduce file size



import os
from PIL import Image

# Get current working directory
base_dir = os.getcwd()
img_dir = os.path.join(base_dir, 'asstes')

# Create output PDF folder (output_pdf) if it doesn't exist
output_dir = os.path.join(img_dir, 'output_pdf')
os.makedirs(output_dir, exist_ok=True)

# Get all folders that don't start with output_pdf
for folder in os.listdir(img_dir):
    folder_path = os.path.join(img_dir, folder)
    if os.path.isdir(folder_path) and not folder.startswith('output_pdf'):
        # Search for image files in folder (including webp format)
        image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                       if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp'))]
        if not image_files:
            print(f"No image files found in {folder} folder.")
            continue
        
        # Sort images by filename
        image_files.sort()

        images = []
        for img_path in image_files:
            with Image.open(img_path) as img:
                # Resize image (max width/height 1300px)
                img.thumbnail((1300, 1300))
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                images.append(img.copy())

        # Set output PDF filename
        pdf_filename = os.path.join(output_dir, f"{folder}.pdf")

        # Save PDF with compression quality and resolution settings
        images[0].save(pdf_filename, "PDF", resolution=72, save_all=True, append_images=images[1:], quality=73)
        print(f"Generated PDF: {pdf_filename}")