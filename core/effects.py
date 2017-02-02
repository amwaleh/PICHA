
import os
from PIL import Image, ImageEnhance,ImageFilter
from django.conf import settings




class Presets(object):
    def __init__(self, image=None):
        self.img = image

    def contrast(self , rate=0.33):
        rate = rate*10
        enh = ImageEnhance.Contrast(self.img)
        return enh.enhance(rate)

    def brightness(self,rate=0.11):
        rate = rate*10
        enh = ImageEnhance.Brightness(self.img)
        return enh.enhance(rate)

    def color(self,rate=0.17):
        rate = rate*10
        enh = ImageEnhance.Color(self.img)
        return enh.enhance(rate)

    def sharpen(self,rate=0.03):
        rate = rate*10
        enh = ImageEnhance.Sharpness(self.img)
        return enh.enhance(rate)

    def blur(self,rate=0):
        rate = rate*10
        im = self.img.filter(ImageFilter.GaussianBlur(radius=rate))
        return im


    def thumbnail(self):
        media_path = os.path.join(settings.BASE_DIR,settings.MEDIA_ROOT,'preset')
        thumbnails_paths=[]
        eff = self.presets_dict()
        if not os.path.isdir(media_path):
            os.mkdir(media_path)

        for Key, effect in eff.items():
            x = effect().resize((256,200))
            save_path = os.path.join(settings.MEDIA_ROOT,'preset','{}.PNG'.format(Key))
            x.save(save_path)
            obj = [Key, os.path.join('preset','{}.PNG'.format(Key))]

            thumbnails_paths.append(obj)

        return thumbnails_paths

    def presets_dict(self):
        return {
            'contrast':self.contrast,
            'brightness':self.brightness,
            'color':self.color,
            'blur': self.blur,
            'sharpen':self.sharpen,
        }



EFFECTS = Presets().presets_dict().keys()



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