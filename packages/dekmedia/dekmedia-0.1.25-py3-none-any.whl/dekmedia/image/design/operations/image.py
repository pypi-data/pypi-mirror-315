from PIL import Image, ImageFilter


def gray(image: Image.Image):
    if image.has_transparency_data:
        return image.convert("LA")
    return image.convert("L")


def blur(image: Image.Image, radius=2):
    return image.filter(ImageFilter.GaussianBlur(radius))
