import argparse
from psd_tools import PSDImage
from PIL import Image
from psd_tools.api.layers import PixelLayer
import cairosvg
import io
import os


def add_image_as_layer(psd_path, image_path, output_path, layer_name):
    # Open the existing PSD file
    psd = PSDImage.open(psd_path)

    # Determine the image format and process accordingly
    _, ext = os.path.splitext(image_path)
    ext = ext.lower()

    if ext == '.svg':
        # Convert SVG to PNG with specified dimensions
        with open(image_path, 'rb') as svg_file:
            png_data = cairosvg.svg2png(
                file_obj=svg_file, output_width=psd.width, output_height=psd.height)
        image = Image.open(io.BytesIO(png_data)).convert('RGBA')
    elif ext == '.png':
        # Open the PNG image directly
        image = Image.open(image_path).convert('RGBA')
        image = image.resize((psd.width, psd.height))
    else:
        raise ValueError("Unsupported image format. Please use SVG or PNG.")

    # Convert PIL image to PixelLayer
    new_image = PixelLayer.frompil(image)
    new_image.name = layer_name

    # Append the new layer to the original PSD
    psd.append(new_image)

    # Save the modified PSD
    psd.save(output_path)


def main():
    parser = argparse.ArgumentParser(
        description='Add an image as a new layer to a PSD file.')
    parser.add_argument('psd_path', type=str, help='Path to the PSD file')
    parser.add_argument('image_path', type=str,
                        help='Path to the SVG or PNG image file')
    parser.add_argument('output_path', type=str,
                        help='Path to save the modified PSD file')
    parser.add_argument('layer_name', type=str, help='Name of the new layer')

    args = parser.parse_args()

    add_image_as_layer(args.psd_path, args.image_path,
                       args.output_path, args.layer_name)
    print(f"Successfully added {
          args.image_path} as a new layer to {args.psd_path}.")
    print(f"Modified PSD saved as {args.output_path}")


if __name__ == '__main__':
    main()
