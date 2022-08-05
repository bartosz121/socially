from typing import Tuple
from PIL import Image
from django.db import models


class ResizeImageMixin:
    def resize(self, img_path: str, size: Tuple[int, int]):
        img = Image.open(img_path)
        img.thumbnail(size)
        img.save(img_path)