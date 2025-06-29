# image_tools.py

from PIL import Image

def compress_and_resize_image(input_path, output_path, quality=75, width=None, height=None, keep_aspect=False, out_format=None):
    try:
        img = Image.open(input_path)

        # Resize with aspect ratio preservation
        if width and keep_aspect:
            aspect_ratio = img.height / img.width
            height = int(width * aspect_ratio)

        if width and height:
            img = img.resize((width, height))

        # Determine format
        format_to_use = out_format.upper() if out_format else img.format

        # Convert RGBA to RGB for JPEG
        if format_to_use == "JPEG" and img.mode == "RGBA":
            img = img.convert("RGB")

        # Save image
        if format_to_use == "PNG":
            img.save(output_path, format="PNG", optimize=True, compress_level=9)
        else:
            img.save(output_path, format=format_to_use, quality=quality, optimize=True)

        return True, f"Image saved as {output_path} (Format: {format_to_use}, Size: {img.size})"
    except Exception as e:
        return False, str(e)
