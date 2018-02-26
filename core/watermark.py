import os
from PIL import Image, ImageEnhance
from django.conf import settings

class Watermark(object):
    """
    Adds A water mark to all pictures that are uploaded to the site
    
    """
    def process(self, image):
        """
        Process, resize and paste water mark on the image
        
        :param image: Image JpG, PNG, BMP
        :type image: IMG
        :return: returns watermarke photo
        :rtype: IMG
        """
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
        """REduces the opacity of a given image 
        
        :param im: Image
        :type im: IMG
        :param opacity: The amount of opacity needed btw 0-1
        :type opacity: float
        :return: Image
        :rtype: IMG
        """
        assert opacity >= 0 and opacity <= 1
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        else:
            im = im.copy()
        alpha = im.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        im.putalpha(alpha)
        return im
# TODO: User should be able to custom and upload his/her own watermark