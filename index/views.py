from django.shortcuts import render, redirect, get_object_or_404
from administrador.models import Service, BlogPost, ContactMessage, Instructor
from .forms import ContactoPublicoForm


def index(request):
    """Página principal con servicios y blog desde la BD."""
    context = {
        'services': Service.objects.filter(is_active=True).order_by('order'),
        'blog_posts': BlogPost.objects.filter(is_published=True).order_by('-published_date')[:3],
    }
    return render(request, 'index/index.html', context)


def nosotros(request):
    """Página Nosotros con instructores dinámicos."""
    instructores = Instructor.objects.filter(is_active=True).order_by('order')
    return render(request, 'index/nosotros.html', {'instructores': instructores})


def novedades(request):
    """Página de blog/novedades completa."""
    posts = BlogPost.objects.filter(
        is_published=True).order_by('-published_date')
    return render(request, 'index/novedades.html', {'posts': posts})


def servicios(request):
    """Página pública de todos los servicios."""
    todos = Service.objects.filter(is_active=True).order_by('order')
    return render(request, 'index/servicios.html', {'servicios': todos})


def servicio_detalle(request, pk):
    """Detalle de un servicio específico."""
    servicio = get_object_or_404(Service, pk=pk, is_active=True)
    otros = Service.objects.filter(is_active=True).exclude(
        pk=pk).order_by('order')[:3]
    return render(request, 'index/servicio_detalle.html', {
        'servicio': servicio,
        'otros': otros,
    })


def contacto_publico(request):
    """
    Formulario de contacto público con validación robusta.
    Usa ContactoPublicoForm que valida nombre (solo letras) y teléfono (solo números).
    """
    if request.method == 'POST':
        # Crear formulario con los datos POST
        form = ContactoPublicoForm(request.POST)

        if form.is_valid():
            # Guardar en ContactMessage (el modelo que usa el admin)
            ContactMessage.objects.create(
                name=form.cleaned_data['nombre'],
                email=form.cleaned_data['correo'],
                phone=form.cleaned_data['telefono'],
                message=form.cleaned_data['mensaje'],
                status='new',
            )
            return redirect('index:contacto_exito')

        # Si hay errores, el form los pasa al template automáticamente
        return render(request, 'index/contacto_form.html', {'form': form})

    # GET → mostrar formulario vacío
    form = ContactoPublicoForm()
    return render(request, 'index/contacto_form.html', {'form': form})


def contacto_exito(request):
    """Confirmación tras enviar el formulario de contacto."""
    return render(request, 'index/contacto_exito.html')
