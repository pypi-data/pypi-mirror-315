# Pixel Palette

A Python package to extract dominant colors from an image and display them in RGB, Hex, and HSL formats.

## Installation

Install the package using pip:

```bash
pip install pixelpalette
```

## Usage

```py
from pixelpalette import extract_colors

image_path = "you_image_path"
colors = extract_colors(image_path, n_colors=10)

for i, color in enumerate(colors):
    print(f"Color {i+1}:")
    print(f"  RGB: {color['RGB']}")
    print(f"  Hex: {color['Hex']}")
    print(f"  HSL: {color['HSL']}")
```

### Outout

```bash
Color 1:
  RGB: rgb(255, 200, 100)
  Hex: #ffc864
  HSL: hsl(30, 100%, 70%)
...
```

## Dependencies
- numpy
- matplotlib
- scikit-learn