from PIL import Image
import os
import argparse


def add_watermark(input_image_path, watermark_path, output_path, opacity=0.3):
    """
    Applies a watermark to an image while preserving aspect ratio

    Args:
        input_image_path: path to the source image
        watermark_path: path to the watermark image
        output_path: path for saving the result
        opacity: watermark opacity (0-1)
    """
    # Open the source image
    base_image = Image.open(input_image_path).convert('RGBA')
    # Open the watermark
    watermark = Image.open(watermark_path).convert('RGBA')

    # Get dimensions
    base_width, base_height = base_image.size
    watermark_width, watermark_height = watermark.size

    # Calculate new watermark size, stretching to height
    # while preserving aspect ratio
    new_height = base_height
    new_width = int(watermark_width * (new_height / watermark_height))

    # Resize watermark
    watermark = watermark.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Create new transparent layer for watermark
    watermark_layer = Image.new('RGBA', base_image.size, (0, 0, 0, 0))

    # Calculate position for horizontal centering
    x_position = (base_width - new_width) // 2
    y_position = 0

    # Place watermark
    watermark_layer.paste(watermark, (x_position, y_position))

    # Get alpha channel data
    alpha = watermark_layer.split()[3]
    # Apply opacity to alpha channel
    alpha = alpha.point(lambda x: int(x * opacity))
    # Update alpha channel
    watermark_layer.putalpha(alpha)

    # Merge images
    output_image = Image.alpha_composite(base_image, watermark_layer)

    # Save result
    output_image.save(output_path, 'PNG')


def process_directory(input_dir, watermark_path, output_dir, opacity):
    """
    Process all images in the specified directory

    Args:
        input_dir: directory with source images
        watermark_path: path to watermark file
        output_dir: directory for saving results
        opacity: watermark opacity
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Supported image formats
    supported_formats = ['.jpg', '.jpeg', '.png', '.bmp']

    # Check for files in directory
    files = os.listdir(input_dir)
    if not files:
        print(f"Warning: Directory {input_dir} is empty")
        return

    # Counters for statistics
    processed = 0
    skipped = 0
    errors = 0

    # Process each file in directory
    for filename in files:
        # Check file extension
        if any(filename.lower().endswith(fmt) for fmt in supported_formats):
            input_path = os.path.join(input_dir, filename)
            # Create output filename with .png extension
            output_filename = os.path.splitext(filename)[0] + '_watermarked.png'
            output_path = os.path.join(output_dir, output_filename)

            try:
                add_watermark(input_path, watermark_path, output_path, opacity)
                print(f"Processed: {filename}")
                processed += 1
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                errors += 1
        else:
            print(f"Skipped unsupported file: {filename}")
            skipped += 1

    # Display statistics
    print("\nProcessing Statistics:")
    print(f"Successfully processed: {processed}")
    print(f"Skipped: {skipped}")
    print(f"Errors: {errors}")


def validate_opacity(value):
    """Validate opacity value"""
    float_value = float(value)
    if float_value < 0 or float_value > 1:
        raise argparse.ArgumentTypeError(f"{value} must be between 0 and 1")
    return float_value


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Apply watermark to images')

    parser.add_argument('-i', '--input-dir',
                        required=True,
                        help='Directory with source images')

    parser.add_argument('-w', '--watermark',
                        required=True,
                        help='Path to watermark file')

    parser.add_argument('-o', '--output-dir',
                        required=True,
                        help='Directory for saving results')

    parser.add_argument('-a', '--opacity',
                        type=validate_opacity,
                        default=0.3,
                        help='Watermark opacity (0-1), default 0.3')

    return parser.parse_args()


def main():
    """Main program function"""
    # Get command line arguments
    args = parse_args()

    # Check input directory existence
    if not os.path.exists(args.input_dir):
        print(f"Error: Directory {args.input_dir} does not exist")
        return

    # Check watermark file existence
    if not os.path.exists(args.watermark):
        print(f"Error: Watermark file {args.watermark} does not exist")
        return

    # Start processing
    print(f"Starting image processing...")
    print(f"Input directory: {args.input_dir}")
    print(f"Watermark: {args.watermark}")
    print(f"Output directory: {args.output_dir}")
    print(f"Opacity: {args.opacity}")
    print("-" * 50)

    process_directory(args.input_dir, args.watermark, args.output_dir, args.opacity)


if __name__ == "__main__":
    main()