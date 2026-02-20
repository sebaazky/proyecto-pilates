"""
index/tests/test_forms.py
Tests para el formulario público de contacto.
"""
from django.test import TestCase
from index.forms import ContactoPublicoForm


class ContactoPublicoFormTest(TestCase):
    """Tests para validaciones del formulario de contacto público."""

    # ─────────────────────────────────────────────────────────
    # TESTS DE NOMBRE
    # ─────────────────────────────────────────────────────────

    def test_nombre_solo_letras_valido(self):
        """Nombre con solo letras debe ser válido."""
        form = ContactoPublicoForm(data={
            'nombre': 'María González',
            'correo': 'maria@example.com',
            'mensaje': 'Hola, me interesa una clase de prueba'
        })
        self.assertTrue(form.is_valid())

    def test_nombre_con_acentos_valido(self):
        """Nombre con acentos y ñ debe ser válido."""
        form = ContactoPublicoForm(data={
            'nombre': 'José Muñoz Pérez',
            'correo': 'jose@example.com',
            'mensaje': 'Consulta'
        })
        self.assertTrue(form.is_valid())

    def test_nombre_con_guion_valido(self):
        """Nombre con guión debe ser válido."""
        form = ContactoPublicoForm(data={
            'nombre': 'Ana-María Rodríguez',
            'correo': 'ana@example.com',
            'mensaje': 'Consulta'
        })
        self.assertTrue(form.is_valid())

    def test_nombre_con_numeros_invalido(self):
        """Nombre con números debe ser inválido."""
        form = ContactoPublicoForm(data={
            'nombre': 'María123',
            'correo': 'maria@example.com',
            'mensaje': 'Consulta'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)
        self.assertIn('solo puede contener letras', str(form.errors['nombre']))

    def test_nombre_con_caracteres_especiales_invalido(self):
        """Nombre con caracteres especiales (@#$) debe ser inválido."""
        form = ContactoPublicoForm(data={
            'nombre': 'María@#$',
            'correo': 'maria@example.com',
            'mensaje': 'Consulta'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    def test_nombre_vacio_invalido(self):
        """Nombre vacío debe ser inválido."""
        form = ContactoPublicoForm(data={
            'nombre': '',
            'correo': 'maria@example.com',
            'mensaje': 'Consulta'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    def test_nombre_muy_corto_invalido(self):
        """Nombre con menos de 2 caracteres debe ser inválido."""
        form = ContactoPublicoForm(data={
            'nombre': 'A',
            'correo': 'maria@example.com',
            'mensaje': 'Consulta'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)
        self.assertIn('al menos 2 caracteres', str(form.errors['nombre']))

    # ─────────────────────────────────────────────────────────
    # TESTS DE TELÉFONO
    # ─────────────────────────────────────────────────────────

    def test_telefono_valido(self):
        """Teléfono con solo números debe ser válido."""
        form = ContactoPublicoForm(data={
            'nombre': 'Juan Pérez',
            'correo': 'juan@example.com',
            'telefono': '912345678',
            'mensaje': 'Consulta'
        })
        self.assertTrue(form.is_valid())

    def test_telefono_con_espacios_valido(self):
        """Teléfono con espacios debe ser válido (se limpian)."""
        form = ContactoPublicoForm(data={
            'nombre': 'Juan Pérez',
            'correo': 'juan@example.com',
            'telefono': '9 1234 5678',
            'mensaje': 'Consulta'
        })
        self.assertTrue(form.is_valid())

    def test_telefono_con_guiones_valido(self):
        """Teléfono con guiones debe ser válido (se limpian)."""
        form = ContactoPublicoForm(data={
            'nombre': 'Juan Pérez',
            'correo': 'juan@example.com',
            'telefono': '9-1234-5678',
            'mensaje': 'Consulta'
        })
        self.assertTrue(form.is_valid())

    def test_telefono_con_parentesis_valido(self):
        """Teléfono con paréntesis debe ser válido (se limpian)."""
        form = ContactoPublicoForm(data={
            'nombre': 'Juan Pérez',
            'correo': 'juan@example.com',
            'telefono': '(9) 1234-5678',
            'mensaje': 'Consulta'
        })
        self.assertTrue(form.is_valid())

    def test_telefono_vacio_valido(self):
        """Teléfono vacío debe ser válido (es opcional)."""
        form = ContactoPublicoForm(data={
            'nombre': 'Juan Pérez',
            'correo': 'juan@example.com',
            'mensaje': 'Consulta'
        })
        self.assertTrue(form.is_valid())

    def test_telefono_con_letras_invalido(self):
        """Teléfono con letras debe ser inválido."""
        form = ContactoPublicoForm(data={
            'nombre': 'Juan Pérez',
            'correo': 'juan@example.com',
            'telefono': 'abc123def',
            'mensaje': 'Consulta'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('telefono', form.errors)
        self.assertIn('solo puede contener números',
                      str(form.errors['telefono']))

    def test_telefono_muy_corto_invalido(self):
        """Teléfono con menos de 8 dígitos debe ser inválido."""
        form = ContactoPublicoForm(data={
            'nombre': 'Juan Pérez',
            'correo': 'juan@example.com',
            'telefono': '1234',
            'mensaje': 'Consulta'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('telefono', form.errors)
        self.assertIn('entre 8 y 15 dígitos', str(form.errors['telefono']))

    def test_telefono_muy_largo_invalido(self):
        """Teléfono con más de 15 dígitos debe ser inválido."""
        form = ContactoPublicoForm(data={
            'nombre': 'Juan Pérez',
            'correo': 'juan@example.com',
            'telefono': '12345678901234567890',
            'mensaje': 'Consulta'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('telefono', form.errors)

    # ─────────────────────────────────────────────────────────
    # TESTS DE EMAIL
    # ─────────────────────────────────────────────────────────

    def test_email_valido(self):
        """Email con formato correcto debe ser válido."""
        form = ContactoPublicoForm(data={
            'nombre': 'Ana López',
            'correo': 'ana.lopez@example.com',
            'mensaje': 'Consulta'
        })
        self.assertTrue(form.is_valid())

    def test_email_invalido(self):
        """Email con formato incorrecto debe ser inválido."""
        form = ContactoPublicoForm(data={
            'nombre': 'Ana López',
            'correo': 'email-invalido',
            'mensaje': 'Consulta'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('correo', form.errors)

    def test_email_vacio_invalido(self):
        """Email vacío debe ser inválido."""
        form = ContactoPublicoForm(data={
            'nombre': 'Ana López',
            'correo': '',
            'mensaje': 'Consulta'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('correo', form.errors)

    # ─────────────────────────────────────────────────────────
    # TESTS DE MENSAJE
    # ─────────────────────────────────────────────────────────

    def test_mensaje_valido(self):
        """Mensaje con contenido debe ser válido."""
        form = ContactoPublicoForm(data={
            'nombre': 'Carlos Díaz',
            'correo': 'carlos@example.com',
            'mensaje': 'Hola, me gustaría obtener información sobre las clases de Pilates.'
        })
        self.assertTrue(form.is_valid())

    def test_mensaje_vacio_invalido(self):
        """Mensaje vacío debe ser inválido."""
        form = ContactoPublicoForm(data={
            'nombre': 'Carlos Díaz',
            'correo': 'carlos@example.com',
            'mensaje': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('mensaje', form.errors)

    # ─────────────────────────────────────────────────────────
    # TESTS DE INTEGRACIÓN
    # ─────────────────────────────────────────────────────────

    def test_formulario_completo_valido(self):
        """Formulario con todos los campos correctos debe ser válido."""
        form = ContactoPublicoForm(data={
            'nombre': 'Sofía Ramírez',
            'correo': 'sofia@example.com',
            'telefono': '9 8765 4321',
            'mensaje': 'Me gustaría agendar una clase de prueba para la próxima semana.'
        })
        self.assertTrue(form.is_valid())

    def test_datos_limpios_correctos(self):
        """Verificar que cleaned_data contiene los valores correctos."""
        form = ContactoPublicoForm(data={
            'nombre': 'Pedro Castro',
            'correo': 'pedro@example.com',
            'telefono': '9-1234-5678',
            'mensaje': 'Consulta sobre precios'
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['nombre'], 'Pedro Castro')
        self.assertEqual(form.cleaned_data['correo'], 'pedro@example.com')
        self.assertEqual(form.cleaned_data['telefono'], '9-1234-5678')
        self.assertEqual(
            form.cleaned_data['mensaje'], 'Consulta sobre precios')
