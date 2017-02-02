
import os
import random
from django.shortcuts import render, get_object_or_404, get_list_or_404,HttpResponse
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from .forms import PhotoForm
from .models import Album
from .effects import Presets,EFFECTS
from PIL import Image
from django.views import View
from django.conf import settings

class MainView(TemplateView):
    template_name = 'index.html'
    pone = None


    def get_context_data(self, **kwargs):
        context = super(MainView,self).get_context_data(**kwargs)
        context['pic'] = self.pone
        return context

class ProcessView(CreateView):
    template_name = 'index.html'
    model = Album
    form_class = PhotoForm



class PicView(DetailView):
    template_name = 'index.html'
    model = Album
    context_object_name = 'picdetails'


    def get_context_data(self, **kwargs):
        context = super(PicView,self).get_context_data(**kwargs)
        context['presets'] = self.object.preset_thumbnails()
        context['effects'] = EFFECTS
        return context


class Photos(ListView):
    template_name = 'photos.html'
    model = Album
    context_object_name = 'photos'
    paginate_by = 9
    ordering = '-pk'

class Effects(View):
    MEDIA_PATH = settings.MEDIA_ROOT
    BASE_DIR = settings.BASE_DIR
    TEMP_FOLDER = 'CACHE/preset/tmp'
    TEMP_PATH = os.path.join(settings.MEDIA_ROOT,TEMP_FOLDER)


    def get(self, request, *args, **kwargs):
        effect, pk  = args
        pic = get_object_or_404(Album,pk=pk)
        save_path = os.path.join(self.TEMP_PATH,'{}.PNG'.format(pk))
        # declare path for accessing an image on the browser view
        temp_image = os.path.join(settings.MEDIA_URL,self.TEMP_FOLDER,'{}.PNG'.format(pk))

        # check if path
        if not os.path.isdir(self.TEMP_PATH):
            os.makedirs(self.TEMP_PATH)
        # create an absolute for opening image
        pic_path ="{}{}".format(self.BASE_DIR, pic.image.url)
        im = Image.open(os.path.abspath(pic_path))

        # check if its a preset
        if request.GET.get('rate'):
            return self.process_temp_file(request)

        preset_pic = Presets(im).presets_dict()
        image = preset_pic[effect]()
        image.save(save_path)
        return render(request,'index.html',context={'presets':pic.preset_thumbnails(),
                                                    'picdetails':{
                                                        'pk':pk,
                                                        'image':
                                                            {'url':temp_image}
                                                    },
                                                    'effects':EFFECTS
                                                    })


    def process_temp_file(self, request):
        rand = random.random()
        effect, pk = self.args
        canvas_image = request.GET.get('image')
        save_path = os.path.join(self.TEMP_PATH,'{}{}.PNG'.format(pk,rand))
        temp_image = os.path.join(settings.MEDIA_URL,self.TEMP_FOLDER,'{}{}.PNG'.format(pk,rand))
        tempfile = "{}{}".format(settings.BASE_DIR,canvas_image)

        if os.path.isfile(tempfile):
            im =Image.open("{}{}".format(settings.BASE_DIR, canvas_image))

        preset_pic = Presets(im).presets_dict()
        image = preset_pic[effect](float(request.GET.get('rate')))
        image.save(save_path)
        return HttpResponse(content=temp_image.encode())

