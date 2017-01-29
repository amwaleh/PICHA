from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from .forms import PhotoForm
from .models import Album
from .effects import Presets
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
        return context


class Photos(ListView):
    template_name = 'photos.html'
    model = Album
    context_object_name = 'photos'
    paginate_by = 9
    ordering = '-pk'

