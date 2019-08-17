from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from system.models import UserWrite


def about_me(request):
    return render(request,'about.html')


class WriteSome(ListView):
    model = UserWrite
    template_name = 'write_some.html'
    paginate_by = 12


class WriteContent(DetailView):
    model = UserWrite
    template_name = 'write_content.html'
    slug_url_kwarg = 'pk'
    slug_field = 'pk'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.increase_view_count()
        # self.object.view_count += 1
        # self.object.save(update_fields=['view_count'])
        return response