
import os
from PIL import Image, ImageEnhance,ImageFilter
from django.conf import settings

class Presets(object):
    def __init__(self, image):
        self.img = image

    def contrast(self):
        enh = ImageEnhance.Contrast(self.img)
        return enh.enhance(3.3)

    def brightness(self):
        enh = ImageEnhance.Brightness(self.img)
        return enh.enhance(1.7)

    def color(self):
        enh = ImageEnhance.Color(self.img)
        return enh.enhance(1.7)


    def detail(self):
        return  self.img.filter(ImageFilter.DETAIL)

    def sharpen(self):
        return  self.img.filter(ImageFilter.SHARPEN)

    def presets_dict(self):
        return {
            'contrast':self.contrast(),
            'brightness':self.brightness(),
            'color':self.color(),
            'details':self.detail(),
        }

    def thumbnail(self):
        media_path = os.path.join(settings.BASE_DIR,settings.MEDIA_ROOT,'preset')
        thumbnails_paths=[]
        eff = self.presets_dict()
        if not os.path.isdir(media_path):
            os.mkdir(media_path)

        for k, v in eff.items():
            x = v.resize((256,200))
            save_path = os.path.join(settings.MEDIA_ROOT,'preset','{}.PNG'.format(k))
            x.save(save_path)
            obj = [k, os.path.join('preset','{}.PNG'.format(k))]

            thumbnails_paths.append(obj)

        return thumbnails_paths







if __name__ == '__main__':
    im = Image.open('image.jpg')
    p = Presets(im)
    p.thumbnail()






    # print('hello')
    # im = Image.open('image.jpg')
    # color(im).show()
    # import base64
    # print(dir(im))
    #
    # with open('image.jpg', "rb") as imageFile:
    #     str = base64.b64encode(imageFile.read())
    #     b = bytearray(str)
    #     print(str)