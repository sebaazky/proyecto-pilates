"""
administrador/tests/test_models.py
Tests para los modelos del panel de administración.
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from administrador.models import Service, BlogPost, Instructor, ContactMessage


class ServiceModelTest(TestCase):
    """Tests para el modelo Service."""

    def test_crear_servicio(self):
        """Verificar que se puede crear un servicio."""
        servicio = Service.objects.create(
            name="Clase Pilates",
            description="Clase grupal de mat",
            price=15000,
            is_active=True,
            order=1
        )
        self.assertEqual(servicio.name, "Clase Pilates")
        self.assertEqual(servicio.price, 15000)
        self.assertTrue(servicio.is_active)

    def test_servicio_str(self):
        """__str__ debe devolver el nombre del servicio."""
        servicio = Service.objects.create(
            name="Kinesiología",
            description="Tratamiento personalizado",
            price=25000
        )
        self.assertEqual(str(servicio), "Kinesiología")

    def test_servicio_orden_default(self):
        """Orden por defecto debe ser 0."""
        servicio = Service.objects.create(
            name="Clase",
            description="Test",
            price=10000
        )
        self.assertEqual(servicio.order, 0)

    def test_servicio_activo_default(self):
        """is_active por defecto debe ser True."""
        servicio = Service.objects.create(
            name="Clase",
            description="Test",
            price=10000
        )
        self.assertTrue(servicio.is_active)


class BlogPostModelTest(TestCase):
    """Tests para el modelo BlogPost."""

    def test_crear_blogpost(self):
        """Verificar que se puede crear un post."""
        post = BlogPost.objects.create(
            title="Beneficios del Pilates",
            content="El Pilates mejora tu postura...",
            is_published=True
        )
        self.assertEqual(post.title, "Beneficios del Pilates")
        self.assertTrue(post.is_published)

    def test_blogpost_str(self):
        """__str__ debe devolver el título."""
        post = BlogPost.objects.create(
            title="Mi Título",
            content="Contenido"
        )
        self.assertEqual(str(post), "Mi Título")

    def test_get_excerpt_corto(self):
        """get_excerpt debe devolver texto completo si es corto."""
        post = BlogPost.objects.create(
            title="Test",
            content="Texto corto de cinco palabras"
        )
        excerpt = post.get_excerpt(words=10)
        self.assertEqual(excerpt, "Texto corto de cinco palabras")

    def test_get_excerpt_largo(self):
        """get_excerpt debe truncar texto largo."""
        post = BlogPost.objects.create(
            title="Test",
            content="Esta es una oración muy larga que tiene muchas más de cinco palabras"
        )
        excerpt = post.get_excerpt(words=5)
        self.assertTrue(excerpt.endswith('...'))
        self.assertLess(len(excerpt.split()), 7)  # 5 palabras + '...'


class InstructorModelTest(TestCase):
    """Tests para el modelo Instructor."""

    def test_crear_instructor(self):
        """Verificar que se puede crear un instructor."""
        instructor = Instructor.objects.create(
            name="María González",
            specialties="Mat & Reformer",
            bio="Instructora certificada",
            is_active=True,
            order=1
        )
        self.assertEqual(instructor.name, "María González")
        self.assertTrue(instructor.is_active)

    def test_instructor_str(self):
        """__str__ debe devolver el nombre."""
        instructor = Instructor.objects.create(
            name="Carlos Vidal",
            specialties="Kinesiólogo",
            bio="Especialista"
        )
        self.assertEqual(str(instructor), "Carlos Vidal")

    def test_instructor_activo_default(self):
        """is_active por defecto debe ser True."""
        instructor = Instructor.objects.create(
            name="Ana Riquelme",
            specialties="Mat",
            bio="Instructora"
        )
        self.assertTrue(instructor.is_active)

    def test_instructor_orden_default(self):
        """order por defecto debe ser 0."""
        instructor = Instructor.objects.create(
            name="Pedro Soto",
            specialties="Reformer",
            bio="Instructor"
        )
        self.assertEqual(instructor.order, 0)


class ContactMessageModelTest(TestCase):
    """Tests para el modelo ContactMessage."""

    def test_crear_mensaje(self):
        """Verificar que se puede crear un mensaje."""
        mensaje = ContactMessage.objects.create(
            name="Juan Pérez",
            email="juan@example.com",
            phone="912345678",
            message="Consulta sobre clases",
            status='new'
        )
        self.assertEqual(mensaje.name, "Juan Pérez")
        self.assertEqual(mensaje.status, 'new')

    def test_mensaje_str(self):
        """__str__ debe incluir nombre, email y estado."""
        mensaje = ContactMessage.objects.create(
            name="Ana López",
            email="ana@example.com",
            message="Hola",
            status='new'
        )
        str_mensaje = str(mensaje)
        self.assertIn("Ana López", str_mensaje)
        self.assertIn("ana@example.com", str_mensaje)
        self.assertIn("Nuevo", str_mensaje)  # get_status_display()

    def test_mensaje_status_default(self):
        """status por defecto debe ser 'new'."""
        mensaje = ContactMessage.objects.create(
            name="Test",
            email="test@example.com",
            message="Mensaje"
        )
        self.assertEqual(mensaje.status, 'new')

    def test_mensaje_telefono_opcional(self):
        """Teléfono debe ser opcional (blank=True)."""
        mensaje = ContactMessage.objects.create(
            name="Test",
            email="test@example.com",
            message="Sin teléfono"
        )
        self.assertEqual(mensaje.phone, '')

    def test_mensaje_notas_opcional(self):
        """admin_notes debe ser opcional."""
        mensaje = ContactMessage.objects.create(
            name="Test",
            email="test@example.com",
            message="Sin notas"
        )
        self.assertEqual(mensaje.admin_notes, '')
