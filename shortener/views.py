from django.shortcuts import render, redirect, get_object_or_404
from .forms import ShortForm
from .models import ShortURL
from django.contrib import messages
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.http import Http404


import re
import string
import random


def create_slug():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=5))

def view_404(request, exception):
    return render(request, '404.html')

def thanks(request,slug):
    short = get_object_or_404(ShortURL, slug=slug)
    if short.expired:
        raise Http404
    context = {
        'slug' : short.slug,
    }
    return render(request,'thanks.html',context=context)

def home(request):
    if request.method == 'POST':
        form = ShortForm(request.POST)
        if form.is_valid():
            #URL validation
            website = form.cleaned_data['website']
            print("Website = " + website)
            val = URLValidator()
            try:
                val(website)
            except ValidationError:
                messages.error(request, "Invalid URL.")
                return redirect("shortener:home")
            
            #Slug validation
            slug = form.cleaned_data['slug']
            if slug == '':
                print("Genrating slug")
                slug = create_slug()
            else:
                print("slug = " + slug)
                regex = re.compile(r'^[a-zA-Z0-9]+$')
                if re.match(regex, slug) is None:
                    messages.error(request, "Invalid Slug (Letter and numbers only).")
                    return redirect("shortener:home")

            #Checking if slug already used
            qs = ShortURL.objects.filter(slug=slug)
            if qs.exists():
                messages.error(request, "Slug already in use.")
                return redirect("shortener:home")
            else:
                short = ShortURL.objects.create(
                    website = website,
                    slug = slug
                )
                messages.success(request,'URL Created')
                return redirect('shortener:thanks', slug = slug)
        else : 
            messages.error(request, "Error Occured.")
            return redirect("shortener:home")

    else:
        form = ShortForm()

    return render(request, 'form.html', {'form': form})

def redirect_to_website(request,slug):
    short = get_object_or_404(ShortURL, slug=slug)
    if short.expired :
        messages.error(request, "Link expired.")
        return redirect('shortener:home')
    else:
        return redirect(short.website)
