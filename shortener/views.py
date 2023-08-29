
from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ShortForm
from .models import ShortURL
from .utils import create_random_slug, is_expired, is_slug_available



def view_404(request, exception):
    return render(request, "404.html")


def thanks(request, slug):
    short = get_object_or_404(ShortURL, slug=slug)
    if short.expired:
        raise Http404
    context = {
        "slug": short.slug,
    }
    return render(request, "thanks.html", context=context)


def home(request):
    if request.method == "POST":
        form = ShortForm(request.POST)
        if form.is_valid():
            # Slug validation
            slug = form.cleaned_data["slug"]
            print(f"Slug = '{slug}'")
            if slug == "":
                print("Genrating slug")
                slug = create_random_slug()
            if not is_slug_available(slug):
                form.add_error("slug", "Slug already in use.")
                return render(request, "form.html", {"form": form})

            # Create short URL
            website = form.cleaned_data["website"]
            ShortURL.objects.create(website=website, slug=slug)
            messages.success(request, "URL Created")
            return redirect("shortener:thanks", slug=slug)
        else:
            # Render form with errors
            messages.error(request, "Invalid form.")
            return render(request, "form.html", {"form": form})

    else:
        form = ShortForm()

    return render(request, "form.html", {"form": form})


def redirect_to_website(request, slug):
    short = get_object_or_404(ShortURL, slug=slug)
    if is_expired(short):
        short.expired = True
        short.save()
        messages.error(request, "Link expired.")
        return redirect("shortener:home")
    else:
        return redirect(short.website)
