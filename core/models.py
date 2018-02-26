from django.db import models
from django.shortcuts import reverse, redirect
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, AddBorder, ResizeToFit, Thumbnail
from .watermark import Watermark
from .effects import Presets
from PIL import Image
from django.conf import settings
import os
# Create your models here.

class Album(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    image = ProcessedImageField(
        upload_to='store',
        processors=[ResizeToFit(800, 600,), Watermark()],
        format='PNG',
        options={'quality': 100}
    )

    thumb = ImageSpecField(
        processors=[Thumbnail(200, 100)],
        format='PNG',
        options={'quality': 50}
    )

    def get_absolute_url(self):
        return reverse('picdetails', args=[self.pk])

    def preset_thumbnails(self):
        path = os.path.abspath('{}/{}'.format(settings.BASE_DIR, self.image.url))
        pic = Image.open(path)
        img = Presets(pic)
        return img.thumbnail()

    def __str__(self):
        return "{}".format(self.image)
