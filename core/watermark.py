import os
from PIL import Image, ImageEnhance
from django.conf import settings

class Watermark(object):
    def process(self, image):
        mark = Image.open(os.path.join(settings.BASE_DIR,'core','wmark.png'))
        layer = Image.new('RGBA', image.size, (0,0,0,0))
        mark = self.reduce_opacity(mark, 0.8)
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        mark = mark.resize((50, 50))
        w = int(mark.size[0])
        h = int(mark.size[1])
        layer.paste(mark, (int(layer.width/2)-w, layer.height-h))
        return Image.composite(layer, image, layer)

    def reduce_opacity(self, im, opacity):
        assert opacity >= 0 and opacity <= 1
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        else:
            im = im.copy()
        alpha = im.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        im.putalpha(alpha)
        return im
