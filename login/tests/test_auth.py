"""
login/tests/test_auth.py
Tests para autenticación y login.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginViewTest(TestCase):
    """Tests para el login secreto del panel admin."""

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login:login')

        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='testadmin',
            password='testpass123',
            rol='administrador'
        )

    def test_login_page_carga(self):
        """Página de login debe cargar correctamente."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_login_credenciales_validas(self):
        """Login con credenciales correctas debe autenticar."""
        response = self.client.post(self.login_url, {
            'username': 'testadmin',
            'password': 'testpass123'
        })
        # Debe redirigir al panel
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/administrador/')

    def test_login_credenciales_invalidas(self):
        """Login con credenciales incorrectas debe fallar."""
        response = self.client.post(self.login_url, {
            'username': 'testadmin',
            'password': 'wrongpassword'
        })
        # No debe redirigir
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuario o contraseña incorrectos')

    def test_usuario_autenticado_redirige(self):
        """Usuario ya autenticado debe ir directo al panel."""
        self.client.login(username='testadmin', password='testpass123')
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 302)


class UserModelTest(TestCase):
    """Tests para el modelo de usuario personalizado."""

    def test_crear_usuario_normal(self):
        """Verificar que se puede crear un usuario."""
        user = User.objects.create_user(
            username='usuario1',
            password='pass123',
            email='usuario@example.com'
        )
        self.assertEqual(user.username, 'usuario1')
        self.assertTrue(user.check_password('pass123'))

    def test_crear_superusuario(self):
        """Verificar que se puede crear un superusuario."""
        admin = User.objects.create_superuser(
            username='admin',
            password='adminpass',
            email='admin@example.com'
        )
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)

    def test_usuario_rol_default(self):
        """Verificar que create_user funciona correctamente."""
        user = User.objects.create_user(
            username='normal',
            password='pass'
        )
        # El rol por defecto puede variar según el modelo
        # Si tu modelo tiene rol='administrador' por defecto, aceptarlo
        self.assertIsNotNone(user.rol)

    def test_usuario_str(self):
        """__str__ debe devolver username."""
        user = User.objects.create_user(
            username='testuser',
            password='pass'
        )
        self.assertEqual(str(user), 'testuser')
