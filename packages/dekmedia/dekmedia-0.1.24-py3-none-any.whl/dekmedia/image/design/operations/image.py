from PIL import Image


def gray(image: Image.Image):
    if image.has_transparency_data:
        return image.convert("LA")
    return image.convert("L")
