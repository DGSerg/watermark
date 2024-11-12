# Image Watermark Tool

A Python-based command-line tool for adding watermarks to images while maintaining aspect ratio. The watermark is scaled to fit the full height of the image and centered horizontally.

## Features

- Batch processing of images in a directory
- Preserves watermark aspect ratio
- Centers watermark horizontally
- Supports various image formats (JPG, JPEG, PNG, BMP)
- Adjustable watermark opacity
- Detailed processing statistics
- Command-line interface with argument parsing

## Requirements

- Python 3.6+
- Pillow (PIL Fork) library

Install the required package using pip:
```bash
pip install Pillow
```

## Usage

Basic usage:
```bash
python watermark.py -i input_directory -w watermark.png -o output_directory
```

With custom opacity:
```bash
python watermark.py -i input_directory -w watermark.png -o output_directory -a 0.5
```

### Arguments

| Argument | Short | Long | Description | Default |
|----------|-------|------|-------------|---------|
| Input Directory | -i | --input-dir | Directory containing source images | Required |
| Watermark File | -w | --watermark | Path to watermark image | Required |
| Output Directory | -o | --output-dir | Directory for processed images | Required |
| Opacity | -a | --opacity | Watermark opacity (0-1) | 0.3 |

### Examples

1. Basic usage with default opacity (0.3):
```bash
python watermark.py -i ./my_photos -w ./logo.png -o ./watermarked_photos
```

2. Set custom opacity (0.5):
```bash
python watermark.py -i ./my_photos -w ./logo.png -o ./watermarked_photos -a 0.5
```

3. Using full argument names:
```bash
python watermark.py --input-dir ./my_photos --watermark ./logo.png --output-dir ./watermarked_photos --opacity 0.4
```

## Processing Details

The tool performs the following operations:
1. Loads each image from the input directory
2. Scales the watermark to match the height of the input image while maintaining aspect ratio
3. Centers the watermark horizontally
4. Applies the specified opacity
5. Saves the processed image in PNG format

## Supported Image Formats

- JPEG/JPG
- PNG
- BMP

Output images are always saved in PNG format to preserve transparency.

## Error Handling

The tool includes comprehensive error handling:
- Validates input directory existence
- Validates watermark file existence
- Validates opacity value range
- Provides detailed error messages for failed operations
- Generates processing statistics

## Output Statistics

After processing, the tool displays:
- Number of successfully processed images
- Number of skipped files
- Number of errors encountered

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.