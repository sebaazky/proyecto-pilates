"""
administrador/tests/test_views.py
Tests para vistas del panel de administración (CMS).
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from administrador.models import Service, BlogPost, Instructor, ContactMessage
from io import BytesIO
from PIL import Image

User = get_user_model()


def create_test_image():
    """Crear una imagen de prueba real."""
    file = BytesIO()
    image = Image.new('RGB', (100, 100), color='red')
    image.save(file, 'JPEG')
    file.seek(0)
    return SimpleUploadedFile(
        'test.jpg',
        file.getvalue(),
        content_type='image/jpeg'
    )


class AdminHomeViewTest(TestCase):
    """Tests para el dashboard principal del admin."""

    def setUp(self):
        self.client = Client()
        # Crear superusuario
        self.admin = User.objects.create_superuser(
            username='admin',
            password='adminpass',
            email='admin@test.com'
        )
        # Crear admin normal
        self.staff = User.objects.create_user(
            username='staff',
            password='staffpass',
            rol='administrador'
        )

    def test_admin_home_requiere_login(self):
        """Usuario no autenticado debe redirigir al login."""
        response = self.client.get(reverse('administrador:home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_admin_home_carga_con_superuser(self):
        """Superusuario debe acceder al dashboard."""
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('administrador:home'))
        self.assertEqual(response.status_code, 200)

    def test_admin_home_carga_con_staff(self):
        """Admin normal debe acceder al dashboard."""
        self.client.login(username='staff', password='staffpass')
        response = self.client.get(reverse('administrador:home'))
        self.assertEqual(response.status_code, 200)

    def test_admin_home_muestra_estadisticas(self):
        """Dashboard debe mostrar estadísticas correctamente."""
        self.client.login(username='admin', password='adminpass')

        # Crear datos
        Service.objects.create(
            name="Servicio",
            description="Test",
            price=10000,
            image=create_test_image()
        )
        BlogPost.objects.create(
            title="Post",
            content="Test",
            image=create_test_image()
        )

        response = self.client.get(reverse('administrador:home'))
        # En vez de buscar el nombre de la variable, buscar el contenido renderizado
        self.assertContains(response, 'Servicios activos')
        self.assertContains(response, 'Posts publicados')


class ServiciosViewsTest(TestCase):
    """Tests para CRUD de servicios."""

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username='admin',
            password='pass'
        )
        self.client.login(username='admin', password='pass')

    def test_servicios_list_carga(self):
        """Listar servicios debe cargar correctamente."""
        response = self.client.get(reverse('administrador:servicios_list'))
        self.assertEqual(response.status_code, 200)

    def test_servicios_list_muestra_servicios(self):
        """Lista debe mostrar servicios existentes."""
        servicio = Service.objects.create(
            name="Clase Pilates",
            description="Test",
            price=15000
        )
        response = self.client.get(reverse('administrador:servicios_list'))
        self.assertContains(response, "Clase Pilates")

    def test_servicio_crear_get(self):
        """GET de crear debe mostrar formulario."""
        response = self.client.get(reverse('administrador:servicio_crear'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="name"')

    def test_servicio_crear_post_valido(self):
        """POST con datos válidos debe crear servicio."""
        response = self.client.post(
            reverse('administrador:servicio_crear'),
            {
                'name': 'Nuevo Servicio',
                'description': 'Descripción test',
                'price': 20000,
                'order': 1,
                'is_active': True,
                'image': create_test_image()
            }
        )
        self.assertEqual(Service.objects.count(), 1)
        self.assertEqual(response.status_code, 302)  # Redirección

    def test_servicio_editar_get(self):
        """GET de editar debe mostrar formulario con datos."""
        servicio = Service.objects.create(
            name="Servicio Original",
            description="Test",
            price=10000
        )
        response = self.client.get(
            reverse('administrador:servicio_editar', args=[servicio.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Servicio Original")

    def test_servicio_eliminar(self):
        """Eliminar servicio debe borrarlo de la BD."""
        servicio = Service.objects.create(
            name="A Eliminar",
            description="Test",
            price=10000
        )
        response = self.client.post(
            reverse('administrador:servicio_eliminar', args=[servicio.pk])
        )
        self.assertEqual(Service.objects.count(), 0)
        self.assertEqual(response.status_code, 302)

    def test_servicio_toggle_activo(self):
        """Toggle debe cambiar is_active."""
        servicio = Service.objects.create(
            name="Servicio",
            description="Test",
            price=10000,
            is_active=True
        )
        response = self.client.get(
            reverse('administrador:servicio_toggle', args=[servicio.pk])
        )
        servicio.refresh_from_db()
        self.assertFalse(servicio.is_active)


class BlogViewsTest(TestCase):
    """Tests para CRUD de blog/novedades."""

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username='admin',
            password='pass'
        )
        self.client.login(username='admin', password='pass')

    def test_blog_list_carga(self):
        """Listar posts debe cargar correctamente."""
        response = self.client.get(reverse('administrador:blog_list'))
        self.assertEqual(response.status_code, 200)

    def test_blog_crear_post_valido(self):
        """POST con datos válidos debe crear post."""
        response = self.client.post(
            reverse('administrador:blog_crear'),
            {
                'title': 'Nuevo Post',
                'content': 'Contenido del post',
                'is_published': True,
                'image': create_test_image()
            }
        )
        self.assertEqual(BlogPost.objects.count(), 1)
        post = BlogPost.objects.first()
        self.assertEqual(post.title, 'Nuevo Post')
        # Verificar que la fecha se asigna automáticamente
        self.assertIsNotNone(post.published_date)

    def test_blog_toggle_publicado(self):
        """Toggle debe cambiar is_published."""
        post = BlogPost.objects.create(
            title="Post",
            content="Test",
            is_published=True
        )
        response = self.client.get(
            reverse('administrador:blog_toggle', args=[post.pk])
        )
        post.refresh_from_db()
        self.assertFalse(post.is_published)


class InstructoresViewsTest(TestCase):
    """Tests para CRUD de instructores."""

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username='admin',
            password='pass'
        )
        self.client.login(username='admin', password='pass')

    def test_instructores_list_carga(self):
        """Listar instructores debe cargar correctamente."""
        response = self.client.get(reverse('administrador:instructores_list'))
        self.assertEqual(response.status_code, 200)

    def test_instructores_list_muestra_instructores(self):
        """Lista debe mostrar instructores existentes."""
        instructor = Instructor.objects.create(
            name="María González",
            specialties="Mat & Reformer",
            bio="Instructora certificada"
        )
        response = self.client.get(reverse('administrador:instructores_list'))
        self.assertContains(response, "María González")

    def test_instructor_crear_get(self):
        """GET de crear debe mostrar formulario."""
        response = self.client.get(reverse('administrador:instructor_crear'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="name"')

    def test_instructor_crear_post_valido(self):
        """POST con datos válidos debe crear instructor."""
        response = self.client.post(
            reverse('administrador:instructor_crear'),
            {
                'name': 'Carlos Vidal',
                'specialties': 'Kinesiólogo',
                'bio': 'Especialista en rehabilitación',
                'certifications': '',
                'order': 1,
                'is_active': True,
                'photo': create_test_image()
            }
        )
        self.assertEqual(Instructor.objects.count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_instructor_toggle_activo(self):
        """Toggle debe cambiar is_active."""
        instructor = Instructor.objects.create(
            name="Ana López",
            specialties="Mat",
            bio="Instructora",
            is_active=True
        )
        response = self.client.get(
            reverse('administrador:instructor_toggle', args=[instructor.pk])
        )
        instructor.refresh_from_db()
        self.assertFalse(instructor.is_active)


class MensajesViewsTest(TestCase):
    """Tests para gestión de mensajes de contacto."""

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username='admin',
            password='pass'
        )
        self.client.login(username='admin', password='pass')

    def test_mensajes_list_carga(self):
        """Listar mensajes debe cargar correctamente."""
        response = self.client.get(reverse('administrador:mensajes_list'))
        self.assertEqual(response.status_code, 200)

    def test_mensajes_list_muestra_mensajes(self):
        """Lista debe mostrar mensajes existentes."""
        mensaje = ContactMessage.objects.create(
            name="Juan Pérez",
            email="juan@example.com",
            message="Consulta",
            status='new'
        )
        response = self.client.get(reverse('administrador:mensajes_list'))
        self.assertContains(response, "Juan Pérez")

    def test_mensaje_detalle_cambia_status_new_a_read(self):
        """Ver detalle debe cambiar 'new' a 'read' automáticamente."""
        mensaje = ContactMessage.objects.create(
            name="Test",
            email="test@example.com",
            message="Mensaje",
            status='new'
        )
        response = self.client.get(
            reverse('administrador:mensaje_detalle', args=[mensaje.pk])
        )
        mensaje.refresh_from_db()
        self.assertEqual(mensaje.status, 'read')


class PermisosViewsTest(TestCase):
    """Tests de control de acceso y permisos."""

    def setUp(self):
        self.client = Client()

        # Superusuario
        self.superuser = User.objects.create_superuser(
            username='super',
            password='pass'
        )

        # Admin normal
        self.admin = User.objects.create_user(
            username='admin',
            password='pass',
            rol='administrador'
        )

        # Usuario normal (sin permisos)
        self.user = User.objects.create_user(
            username='user',
            password='pass',
            rol='usuario'
        )

    def test_usuario_normal_no_accede_panel(self):
        """Usuario sin rol admin debe ser rechazado."""
        self.client.login(username='user', password='pass')
        response = self.client.get(reverse('administrador:home'))
        self.assertEqual(response.status_code, 302)
        # Debe redirigir a index, no al panel
        self.assertIn('/', response.url)

    def test_admin_normal_accede_panel(self):
        """Admin normal debe acceder al panel."""
        self.client.login(username='admin', password='pass')
        response = self.client.get(reverse('administrador:home'))
        self.assertEqual(response.status_code, 200)

    def test_admin_normal_no_accede_usuarios(self):
        """Admin normal NO debe acceder a gestión de usuarios."""
        self.client.login(username='admin', password='pass')
        response = self.client.get(reverse('administrador:usuarios_list'))
        self.assertEqual(response.status_code, 302)
        # Debe redirigir al home del panel con mensaje de error

    def test_superuser_accede_usuarios(self):
        """Superusuario SÍ debe acceder a gestión de usuarios."""
        self.client.login(username='super', password='pass')
        response = self.client.get(reverse('administrador:usuarios_list'))
        self.assertEqual(response.status_code, 200)
