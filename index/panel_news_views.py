# index/panel_news_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseRedirect

from .models import NewsPost
from .forms import NewsPostForm


def _only_staff(user):
    if not user.is_authenticated:
        return False
    return (
        getattr(user, "is_superuser", False)
        or getattr(user, "is_staff", False)
        or user.groups.filter(name__in=["Administradores", "Staff"]).exists()
    )


@login_required(login_url='login:login')
def news_list(request):
    if not _only_staff(request.user):
        return redirect('administrador:home')

    # Orden general
    qs = NewsPost.objects.order_by(
        '-featured', '-published', '-published_at', '-updated_at', '-id'
    )

    # HERO = primer post Publicado + Destacado
    hero = qs.filter(published=True, featured=True).first()

    # Resto (si hay hero lo excluimos)
    posts = qs.exclude(pk=hero.pk) if hero else qs

    return render(
        request,
        'panel/news_list.html',
        {
            'posts': posts,
            'hero': hero,
            'is_panel': True,
        }
    )


@login_required(login_url='login:login')
def news_create(request):
    if not _only_staff(request.user):
        return redirect('administrador:home')

    if request.method == 'POST':
        form = NewsPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index:panel_news_list')
    else:
        form = NewsPostForm()

    return render(request, 'panel/news_form.html', {'form': form})


@login_required(login_url='login:login')
def news_edit(request, pk):
    if not _only_staff(request.user):
        return redirect('administrador:home')

    post = get_object_or_404(NewsPost, pk=pk)

    if request.method == 'POST':
        form = NewsPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('index:panel_news_list')
    else:
        form = NewsPostForm(instance=post)

    return render(request, 'panel/news_form.html', {'form': form})


@login_required(login_url='login:login')
def news_delete(request, pk):
    if not _only_staff(request.user):
        return redirect('administrador:home')

    post = get_object_or_404(NewsPost, pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('index:panel_news_list')

    return render(request, 'panel/news_confirm_delete.html', {'object': post})


@login_required(login_url='login:login')
def news_toggle_publish(request, pk):
    if not _only_staff(request.user):
        return redirect('administrador:home')

    post = get_object_or_404(NewsPost, pk=pk)
    post.published = not post.published
    if post.published and not post.published_at:
        post.published_at = timezone.now()
    post.save(update_fields=['published', 'published_at'])

    next_url = request.GET.get('next')
    return HttpResponseRedirect(next_url) if next_url else redirect('index:panel_news_list')


@login_required(login_url='login:login')
def news_toggle_featured(request, pk):
    if not _only_staff(request.user):
        return redirect('administrador:home')

    post = get_object_or_404(NewsPost, pk=pk)
    post.featured = not post.featured
    post.save(update_fields=['featured'])

    next_url = request.GET.get('next')
    return HttpResponseRedirect(next_url) if next_url else redirect('index:panel_news_list')
