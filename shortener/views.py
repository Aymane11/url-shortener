from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import ShortForm
from .models import ShortURL
from .utils import (create_available_random_slug, expire, is_active,
                    is_slug_available)


def view_404(request, exception):
    return render(request, "404.html")


def thanks(request, slug):
    try:
        short = ShortURL.objects.get(
            slug=slug, active=True, expiration__gt=timezone.now()
        )
        return render(
            request,
            "thanks.html",
            context={
                "slug": short.slug,
                "website": short.website,
                "expiration": short.expiration,
            },
        )
    except ShortURL.DoesNotExist:
        raise Http404


def home(request):
    if request.method == "POST":
        form = ShortForm(request.POST)
        if form.is_valid():
            # Slug validation
            slug = form.cleaned_data["slug"]
            print(f"Slug = '{slug}'")
            if slug == "":
                print("Genrating slug")
                slug = create_available_random_slug()
            if not is_slug_available(slug):
                form.add_error("slug", "Slug already in use.")
                messages.error(request, "Slug already in use.")
                return render(request, "form.html", {"form": form})

            # Create short URL
            website = form.cleaned_data["website"]
            ShortURL.objects.create(website=website, slug=slug)
            messages.success(request, "URL Created")
            return redirect("shortener:thanks", slug=slug)
        else:
            # Render form with errors
            return render(request, "form.html", {"form": form})

    else:
        form = ShortForm()

    return render(request, "form.html", {"form": form})


def redirect_to_website(request, slug):
    try:
        short = ShortURL.objects.filter(slug=slug).latest()
    except ShortURL.DoesNotExist:
        raise Http404
    if is_active(short):
        return redirect(short.website)
    else:
        expire(short)
        messages.error(request, "This link has expired.")
        return redirect("shortener:home")
