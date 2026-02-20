"""
administrador/tests/test_forms.py
Tests para formularios del panel de administración.
"""
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from administrador.forms import ServiceForm, InstructorForm
from io import BytesIO
from PIL import Image


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


class ServiceFormTest(TestCase):
    """Tests para el formulario de servicios."""

    def test_precio_positivo_valido(self):
        """Precio mayor a 0 debe ser válido."""
        form = ServiceForm(
            data={
                'name': 'Clase Pilates',
                'description': 'Clase grupal',
                'price': 15000,
                'order': 1,
                'is_active': True
            },
            files={'image': create_test_image()}
        )
        if not form.is_valid():
            print("Errores:", form.errors)
        self.assertTrue(form.is_valid())

    def test_precio_cero_invalido(self):
        """Precio 0 debe ser inválido."""
        form = ServiceForm(
            data={
                'name': 'Clase Pilates',
                'description': 'Clase grupal',
                'price': 0,
                'order': 1,
                'is_active': True
            },
            files={'image': create_test_image()}
        )
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)
        self.assertIn('mayor a $0', str(form.errors['price']))

    def test_precio_negativo_invalido(self):
        """Precio negativo debe ser inválido."""
        form = ServiceForm(
            data={
                'name': 'Clase Pilates',
                'description': 'Clase grupal',
                'price': -5000,
                'order': 1,
                'is_active': True
            },
            files={'image': create_test_image()}
        )
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

    def test_nombre_requerido(self):
        """Nombre es obligatorio."""
        form = ServiceForm(
            data={
                'name': '',
                'description': 'Clase grupal',
                'price': 15000,
                'order': 1,
                'is_active': True
            },
            files={'image': create_test_image()}
        )
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)


class InstructorFormTest(TestCase):
    """Tests para el formulario de instructores."""

    def test_instructor_valido(self):
        """Formulario con datos correctos debe ser válido."""
        form = InstructorForm(
            data={
                'name': 'María González',
                'specialties': 'Mat & Reformer',
                'bio': 'Instructora certificada con 8 años de experiencia',
                'certifications': 'Balanced Body Certified',
                'order': 1,
                'is_active': True
            },
            files={'photo': create_test_image()}
        )
        if not form.is_valid():
            print("Errores:", form.errors)
        self.assertTrue(form.is_valid())

    def test_nombre_requerido(self):
        """Nombre es obligatorio."""
        form = InstructorForm(
            data={
                'name': '',
                'specialties': 'Mat',
                'bio': 'Test',
                'order': 1,
                'is_active': True
            },
            files={'photo': create_test_image()}
        )
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_especialidades_requeridas(self):
        """Especialidades son obligatorias."""
        form = InstructorForm(
            data={
                'name': 'Carlos',
                'specialties': '',
                'bio': 'Test',
                'order': 1,
                'is_active': True
            },
            files={'photo': create_test_image()}
        )
        self.assertFalse(form.is_valid())
        self.assertIn('specialties', form.errors)

    def test_certificaciones_opcional(self):
        """Certificaciones son opcionales."""
        form = InstructorForm(
            data={
                'name': 'Ana López',
                'specialties': 'Mat',
                'bio': 'Instructora',
                'certifications': '',  # Vacío
                'order': 1,
                'is_active': True
            },
            files={'photo': create_test_image()}
        )
        if not form.is_valid():
            print("Errores:", form.errors)
        self.assertTrue(form.is_valid())
