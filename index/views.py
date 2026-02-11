from django.shortcuts import render, redirect, get_object_or_404
from administrador.models import Service, BlogPost, ContactMessage


def index(request):
    """Página principal con servicios y blog desde la BD."""
    context = {
        'services': Service.objects.filter(is_active=True).order_by('order'),
        'blog_posts': BlogPost.objects.filter(is_published=True).order_by('-published_date')[:3],
    }
    return render(request, 'index/index.html', context)


def nosotros(request):
    """Página Nosotros."""
    return render(request, 'index/nosotros.html')


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
    """Formulario de contacto público."""
    if request.method == 'POST':
        nombre = request.POST.get('nombre',   '').strip()
        email = request.POST.get('email',    '').strip()
        telefono = request.POST.get('telefono', '').strip()
        mensaje = request.POST.get('mensaje',  '').strip()

        errores = []
        if not nombre:
            errores.append('El nombre es obligatorio.')
        if not email or '@' not in email:
            errores.append('El email no es válido.')
        if not mensaje:
            errores.append('El mensaje es obligatorio.')

        if errores:
            return render(request, 'index/contacto_form.html', {
                'errores':  errores,
                'nombre':   nombre,
                'email':    email,
                'telefono': telefono,
                'mensaje':  mensaje,
            })

        ContactMessage.objects.create(
            name=nombre, email=email,
            phone=telefono, message=mensaje,
            status='new',
        )
        return redirect('index:contacto_exito')

    return render(request, 'index/contacto_form.html')


def contacto_exito(request):
    """Confirmación tras enviar el formulario de contacto."""
    return render(request, 'index/contacto_exito.html')
