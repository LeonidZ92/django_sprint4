from django.shortcuts import render
from django.views.generic import TemplateView


class About(TemplateView):
    template_name = 'pages/about.html'


class Rules(TemplateView):
    template_name = 'pages/rules.html'


def csrf_failure_view(request, reason=''):
    return render(request=request,
                  template_name='pages/403csrf.html',
                  status=403)


def page_not_found(request, exception):
    return render(request=request, template_name='pages/404.html', status=404)


def server_error(request):
    return render(request=request, template_name='pages/500.html', status=500)
