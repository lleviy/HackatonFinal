from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView

from utils.excelparser import parse_excel_into_consumption_objects
from utils.mapbuilder import build_map
from .forms import SpaceForm
from .models import Space


def check_ownership(request, owner):
    if owner != request.user:
        raise Http404


class SpaceListView(LoginRequiredMixin, View):
    template_name = 'spaces/spaces.html'

    def get(self, request):
        spaces = Space.objects.filter(owner=request.user)
        return render(request, self.template_name, {'spaces': spaces})


class SpaceView(LoginRequiredMixin, View):
    template_name = 'spaces/space.html'

    def get(self, request, space_id):
        space = Space.objects.get(pk=space_id)
        return render(request, self.template_name,
                      {'space': space})

class MapView(LoginRequiredMixin, View):
    template_name = 'spaces/map.html'

    def get(self, request, space_id):
        space = Space.objects.get(pk=space_id)
        check_ownership(request, space.owner)
        fusionMap = build_map(request, space_id)

        # returning complete JavaScript and HTML code, which is used to generate map in the browsers.
        return render(request, self.template_name,
                      {'output': fusionMap.render(), 'space': space})

class SpaceCreateView(LoginRequiredMixin, CreateView):
    template_name = "spaces/new_space.html"
    form_class = SpaceForm
    context = {'form': form_class}

    def get(self, request):
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            new_space = Space.objects.create(name=form.cleaned_data['name'], owner=request.user)
            if request.FILES:
                file = request.FILES['file']
                if not file.name.endswith('.xls'):
                    messages.error(request, 'Это не Excel файл. Загрузите файл в требуемом формате.')
                    return render(request, self.template_name, self.context)
                parse_excel_into_consumption_objects(file, request, new_space.id)
            return HttpResponseRedirect(reverse('spaces:spaces'))
        context = {'form': form}
        return render(request, self.template_name, context)


class SpaceUpdateView(LoginRequiredMixin, View):
    template_name = "spaces/edit_space.html"
    form_class = SpaceForm

    def get(self, request, space_id):
        if space_id:
            space = Space.objects.get(pk=space_id)
            check_ownership(request, space.owner)
            form = self.form_class(instance=space)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, space_id):
        space = Space.objects.get(pk=space_id)
        check_ownership(request, space.owner)
        form = self.form_class(request.POST, instance=space)
        if form.is_valid():
            updated_space = Space.objects.filter(id=space_id).update(name=form.cleaned_data['name'])
            if request.FILES:
                file = request.FILES['file']
                if not file.name.endswith('.xls'):
                    messages.error(request, 'Это не Excel файл. Загрузите файл в требуемом формате.')
                    return render(request, self.template_name, self.context)
                parse_excel_into_consumption_objects(file, request, space_id)
            return HttpResponseRedirect(reverse('spaces:spaces'))
        context = {'form': form}
        return render(request, self.template_name, context)


class SpaceDeleteView(LoginRequiredMixin, DeleteView):
    model = Space
    success_url = reverse_lazy('spaces:spaces')

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(SpaceDeleteView, self).get_object()
        if obj.owner != self.request.user:
            raise Http404
        return obj


def consumption_upload(request):
    # declaring template
    template = "spaces/consumption_upload.html"
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template)
    file = request.FILES['file']

    if not file.name.endswith('.xls'):
        messages.error(request, 'Это не Excel файл. Загрузите файл в требуемом формате.')
        return render(request, template)

    parse_excel_into_consumption_objects(file, request)

    context = {}
    return render(request, template, context)


def index(request):
    fusionMap = build_map(request)

    # returning complete JavaScript and HTML code, which is used to generate map in the browsers.
    return render(request, 'index.html',
                  {'output': fusionMap.render()})

def get_map(request):
    fusionMap = build_map(request)

    # returning complete JavaScript and HTML code, which is used to generate map in the browsers.
    return render(request, 'spaces/map.html',
                  {'output': fusionMap.render()})