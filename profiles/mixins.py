from typing import Tuple
from django.db import models
from PIL import Image


class ResizeImageMixin:
    def resize(self, img_path: str, size: Tuple[int, int]):
        img = Image.open(img_path)
        img.thumbnail(size)
        img.save(img_path)
