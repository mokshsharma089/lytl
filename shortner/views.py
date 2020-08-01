from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from shortner.models import rickUrl
from django.views import View
from shortner.forms import SubmitUrlForm
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def GetFirstorCreate(nurl):
    instance = rickUrl.objects.filter(url=nurl)
    if not instance.exists():
         obj = rickUrl.objects.create(url=nurl)
         created=True
    else:
        obj=instance.first()
        created=False
    return obj,created

class HomeView(View):
    def get(self, request, *args, **kwargs):
        the_form = SubmitUrlForm()
        context = {
            "title": "RickUrl.co",
            "form": the_form,
        }
        return render(request, "home/home.html", context) 

    def post(self, request, *args, **kwargs):
        form = SubmitUrlForm(request.POST)
        if form.is_valid():
            if not form.data['shortcode']:
                new_url = form.cleaned_data.get("url")
                if "http://" not in new_url and "https://" not in new_url:
                    new_url="http://"+new_url
                obj, created = GetFirstorCreate(new_url)
                context = {
                    "object": obj,
                    "created": created,
                    "form": form
                }
            else:
                new_url = form.cleaned_data.get("url")
                short_code=form.cleaned_data.get("shortcode")
                if "http://" not in new_url and "https://" not in new_url:
                    new_url="http://"+new_url
                if rickUrl.objects.filter(shortcode=short_code).exists():
                    the_form = SubmitUrlForm()
                    context = {
                    "title": "RickUrl.co",
                    "form": the_form,
                    "message":"Shortcode Already Taken . Please Try Another"
                    }
                    return render(request,"home/home.html",context)
                obj, created = rickUrl.objects.get_or_create(url=new_url,shortcode=short_code)
                context = {
                    "object": obj,
                    "created": created,
                    "form": form
                }
        if created:
                template = "home/sucess.html"
        else:
                template = "home/failure.html"
    
        return render(request, template ,context)

def view1(request,slug,*args,**kwargs):
    shortname=slug
    obj=get_object_or_404(rickUrl,shortcode=shortname)
    return HttpResponseRedirect(obj.url)
    