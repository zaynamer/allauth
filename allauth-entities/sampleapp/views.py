from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def sampleview(request):
    if request.user.has_perm('sampleapp.can_view_sampleapp_entries'):
        
        template = loader.get_template('sampleapphome.html')
        return HttpResponse(template.render())
    else:
        template = loader.get_template('sampleapphome_2.html')
        return HttpResponse(template.render())





# custom 404 view
def custom_page_not_found(request, exception):
    return render(request, '404.html', status=404)