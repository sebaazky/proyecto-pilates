"""
index/tests/test_views.py
Tests para vistas públicas de la landing page.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from administrador.models import Service, BlogPost, Instructor


class IndexViewTest(TestCase):
    """Tests para la página principal."""

    def setUp(self):
        self.client = Client()

    def test_index_carga_correctamente(self):
        """Verificar que la página principal responde 200."""
        response = self.client.get(reverse('index:index'))
        self.assertEqual(response.status_code, 200)

    # Test comentado porque eliminaste los servicios del index
    # def test_index_muestra_servicios_activos(self):
    #     """Servicios activos deben aparecer en el index."""
    #     imagen = SimpleUploadedFile('test.jpg', b'fake', content_type='image/jpeg')
    #     servicio = Service.objects.create(
    #         name="Clase Pilates Mat",
    #         description="Clase grupal",
    #         price=15000,
    #         is_active=True,
    #         image=imagen
    #     )
    #     response = self.client.get(reverse('index:index'))
    #     self.assertContains(response, "Clase Pilates Mat")

    def test_index_no_muestra_servicios_inactivos(self):
        """Servicios inactivos NO deben aparecer."""
        imagen = SimpleUploadedFile(
            'test.jpg', b'fake', content_type='image/jpeg')
        servicio = Service.objects.create(
            name="Servicio Desactivado",
            description="No debe aparecer",
            price=10000,
            is_active=False,
            image=imagen
        )
        response = self.client.get(reverse('index:index'))
        self.assertNotContains(response, "Servicio Desactivado")


class NosotrosViewTest(TestCase):
    """Tests para la página Nosotros."""

    def setUp(self):
        self.client = Client()

    def test_nosotros_carga_correctamente(self):
        """Verificar que /nosotros/ responde 200."""
        response = self.client.get(reverse('index:nosotros'))
        self.assertEqual(response.status_code, 200)

    def test_instructor_activo_aparece(self):
        """Instructores activos deben aparecer en Nosotros."""
        instructor = Instructor.objects.create(
            name="María González",
            specialties="Mat & Reformer",
            bio="Instructora certificada",
            is_active=True
        )
        response = self.client.get(reverse('index:nosotros'))
        self.assertContains(response, "María González")

    def test_instructor_inactivo_no_aparece(self):
        """Instructores inactivos NO deben aparecer."""
        instructor = Instructor.objects.create(
            name="Carlos Vidal",
            specialties="Kinesiólogo",
            bio="Especialista",
            is_active=False
        )
        response = self.client.get(reverse('index:nosotros'))
        self.assertNotContains(response, "Carlos Vidal")


class ContactoPublicoViewTest(TestCase):
    """Tests para el formulario de contacto público."""

    def setUp(self):
        self.client = Client()
        self.url = reverse('index:contacto_publico')

    def test_contacto_get_carga_formulario(self):
        """GET debe mostrar el formulario."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="nombre"')
        self.assertContains(response, 'name="correo"')

    def test_contacto_post_valido_crea_mensaje(self):
        """POST con datos válidos debe crear mensaje en BD."""
        from administrador.models import ContactMessage

        datos = {
            'nombre': 'Juan Pérez',
            'correo': 'juan@example.com',
            'telefono': '912345678',
            'mensaje': 'Consulta sobre clases'
        }

        response = self.client.post(self.url, datos)

        # Verifica redirección
        self.assertEqual(response.status_code, 302)

        # Verifica que se creó el mensaje
        self.assertEqual(ContactMessage.objects.count(), 1)
        mensaje = ContactMessage.objects.first()
        self.assertEqual(mensaje.name, 'Juan Pérez')
        self.assertEqual(mensaje.email, 'juan@example.com')
        self.assertEqual(mensaje.status, 'new')

    def test_contacto_post_invalido_muestra_errores(self):
        """POST con datos inválidos debe mostrar errores."""
        datos = {
            'nombre': '123',  # Inválido
            'correo': 'email-invalido',  # Inválido
            'mensaje': 'Test'
        }

        response = self.client.post(self.url, datos)

        # No debe redirigir
        self.assertEqual(response.status_code, 200)

        # Debe mostrar errores
        self.assertContains(response, 'solo puede contener letras')


class ServiciosViewTest(TestCase):
    """Tests para la página de servicios."""

    def setUp(self):
        self.client = Client()

    def test_servicios_carga_correctamente(self):
        """Verificar que /servicios/ responde 200."""
        response = self.client.get(reverse('index:servicios'))
        self.assertEqual(response.status_code, 200)

    def test_servicios_muestra_solo_activos(self):
        """Solo deben aparecer servicios activos."""
        imagen = SimpleUploadedFile(
            'test.jpg', b'fake', content_type='image/jpeg')

        activo = Service.objects.create(
            name="Clase Activa",
            description="Debe aparecer",
            price=15000,
            is_active=True,
            image=imagen
        )
        inactivo = Service.objects.create(
            name="Clase Inactiva",
            description="No debe aparecer",
            price=10000,
            is_active=False,
            image=imagen
        )

        response = self.client.get(reverse('index:servicios'))
        self.assertContains(response, "Clase Activa")
        self.assertNotContains(response, "Clase Inactiva")


class NovedadesViewTest(TestCase):
    """Tests para la página de blog/novedades."""

    def setUp(self):
        self.client = Client()

    def test_novedades_carga_correctamente(self):
        """Verificar que /novedades/ responde 200."""
        response = self.client.get(reverse('index:novedades'))
        self.assertEqual(response.status_code, 200)

    def test_novedades_muestra_posts_publicados(self):
        """Solo posts publicados deben aparecer."""
        imagen = SimpleUploadedFile(
            'blog.jpg', b'fake', content_type='image/jpeg')

        publicado = BlogPost.objects.create(
            title="Post Publicado",
            content="Contenido visible",
            is_published=True,
            image=imagen
        )
        borrador = BlogPost.objects.create(
            title="Post Borrador",
            content="No debe aparecer",
            is_published=False,
            image=imagen
        )

        response = self.client.get(reverse('index:novedades'))
        self.assertContains(response, "Post Publicado")
        self.assertNotContains(response, "Post Borrador")
