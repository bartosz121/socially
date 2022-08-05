from PIL import Image, ImageChops

class CompareImagesMixin:
    def imgs_are_equal(self, img1: str, img2: str) -> bool:
        """img1 and img2 = path to image"""
        i1 = Image.open(img1).convert("RGB")
        i2 = Image.open(img2).convert("RGB")

        diff = ImageChops.difference(i1, i2)

        return not bool(diff.getbbox())
