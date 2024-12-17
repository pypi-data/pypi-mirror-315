import numpy as np
import matplotlib.image as mpimg
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


# Helper function to convert RGB to Hexadecimal
def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))


# Helper function to convert RGB to HSL
def rgb_to_hsl(rgb):
    r, g, b = [x / 255.0 for x in rgb]  # Normalize RGB to [0, 1]
    max_val, min_val = max(r, g, b), min(r, g, b)
    delta = max_val - min_val

    # Calculate Lightness
    light = (max_val + min_val) / 2

    # Calculate Saturation
    if delta == 0:
        s = 0
    else:
        s = delta / (1 - abs(2 * light - 1))

    # Calculate Hue
    if delta == 0:
        h = 0
    elif max_val == r:
        h = ((g - b) / delta) % 6
    elif max_val == g:
        h = (b - r) / delta + 2
    elif max_val == b:
        h = (r - g) / delta + 4
    h = h * 60
    if h < 0:
        h += 360

    return [round(h), round(s * 100), round(light * 100)]  # HSL in degrees, %


# Main function to extract colors
def extract_colors(image_path, n_colors=5, show=False, print_palette=False):
    """
    Extract dominant colors from an image.

    Args:
        image_path (str): Path to the image file.
        n_colors (int): Number of colors to extract.
        show (bool): Show the Color Palette App.
        print_palette (bool): Print the Color Palette Colors.

    Returns:
        list: A list of dictionaries with RGB, Hex, and HSL color formats.
    """
    image = mpimg.imread(image_path)
    w, h, d = image.shape
    pixels = np.reshape(image, (w * h, d))

    model = KMeans(n_clusters=n_colors, random_state=42).fit(pixels)
    palette = np.uint8(model.cluster_centers_)

    color_list = []
    for color in palette:
        rgb = list(color)
        hex_color = rgb_to_hex(rgb)
        hsl = rgb_to_hsl(rgb)
        colors_format = {
            "RGB": f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})",
            "Hex": hex_color,
            "HSL": f"hsl({hsl[0]}, {hsl[1]}%, {hsl[2]}%)",
        }
        color_list.append(colors_format)
        if print_palette:
            RGB, Hex, HSL = colors_format.values()
            print(f"RGB: {RGB}\nHex: {Hex}\nHSL: {HSL}", end="\n\n")

    if show:
        # Display the palette
        fig = plt.figure()
        fig.suptitle("Color Palette Colors Visualization")
        fig.canvas.manager.set_window_title("Color Palette")

        plt.imshow([palette])
        plt.axis("off")  # Hide axes for better visualization
        plt.show()

    return color_list
