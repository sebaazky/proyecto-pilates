"""
index/chatbot_views.py
Chatbot informativo para responder preguntas frecuentes.
SOLO INFORMATIVO - No incluye reservas ni registro.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from administrador.models import Service, Instructor, BlogPost
import json
import re
from datetime import datetime


def normalize_text(text):
    """Normaliza texto para comparación (sin tildes, minúsculas)."""
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'a', 'É': 'e', 'Í': 'i', 'Ó': 'o', 'Ú': 'u',
        'ñ': 'n', 'Ñ': 'n', '¿': '', '?': ''
    }
    text = text.lower()
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def detect_intent(message):
    """Detecta la intención del usuario basándose en palabras clave."""
    msg = normalize_text(message)

    patterns = {
        'precios': [
            r'\b(precio|precios|costo|costos|cuanto|cuánto|valor|tarifa)\b',
            r'\b(sale|cobra|cobran|pagar)\b'
        ],
        'horarios': [
            r'\b(horario|horarios|hora|horas|cuando|cuándo|abierto|abren|cierran)\b',
            r'\b(disponibilidad|disponible)\b'
        ],
        'ubicacion': [
            r'\b(donde|dónde|ubicacion|ubicación|direccion|dirección|como llego|llegar)\b',
            r'\b(estacionamiento|parking|metro|locomocion|locomoción)\b'
        ],
        'servicios': [
            r'\b(servicio|servicios|que ofrecen|que hacen|modalidad|modalidades|tratamiento|tratamientos)\b'
        ],
        'instructores': [
            r'\b(instructor|instructores|profesor|profesores|quien|quién|equipo|profesional|profesionales)\b',
            r'\b(certificacion|certificación|experiencia)\b'
        ],
        'novedades': [
            r'\b(novedad|novedades|noticia|noticias|blog|nuevo|nueva|actualizacion|actualización)\b'
        ],
        'contacto': [
            r'\b(contacto|contactar|telefono|teléfono|email|correo|whatsapp|comunicar|hablar|escribir)\b'
        ],
        'saludo': [
            r'\b(hola|buenos dias|buenas tardes|buenas noches|hey|saludos|ola)\b'
        ],
        'despedida': [
            r'\b(chao|chau|adios|adiós|gracias|bye|hasta luego|nos vemos)\b'
        ]
    }

    detected = []
    for intent, regexes in patterns.items():
        for regex in regexes:
            if re.search(regex, msg):
                detected.append(intent)
                break

    if detected:
        return detected[0], 0.9

    return 'unknown', 0.0


def get_precios_response():
    """Genera respuesta sobre precios desde la BD."""
    servicios = Service.objects.filter(is_active=True).order_by('price')

    if not servicios.exists():
        return "Actualmente estamos actualizando nuestros precios. Por favor contáctanos al +56 9 1234 5678 para más información. 📞"

    response = "💰 **Nuestros servicios y precios:**\n\n"

    for servicio in servicios:
        precio_formateado = f"${int(servicio.price):,}".replace(',', '.')
        response += f"• **{servicio.name}**: {precio_formateado} CLP\n"

    response += "\n✨ Todos nuestros servicios incluyen:\n"
    response += "✓ Atención personalizada\n"
    response += "✓ Equipamiento premium\n"
    response += "✓ Profesionales certificados"

    return response


def get_servicios_response():
    """Genera respuesta sobre servicios disponibles."""
    servicios = Service.objects.filter(is_active=True)

    if not servicios.exists():
        return "Estamos actualizando nuestros servicios. Contáctanos para más información."

    response = "🧘‍♀️ **Nuestros servicios:**\n\n"

    for servicio in servicios:
        response += f"**{servicio.name}**\n"
        descripcion_breve = servicio.description[:80] + "..." if len(
            servicio.description) > 80 else servicio.description
        response += f"{descripcion_breve}\n\n"

    return response


def get_instructores_response():
    """Genera respuesta sobre el equipo de instructores."""
    instructores = Instructor.objects.filter(is_active=True).order_by('order')

    if not instructores.exists():
        return "Nuestro equipo está certificado internacionalmente con años de experiencia. Contáctanos para conocerlos."

    response = "👥 **Nuestro equipo de profesionales:**\n\n"

    for instructor in instructores[:3]:
        response += f"**{instructor.name}**\n"
        response += f"{instructor.specialties}\n\n"

    if instructores.count() > 3:
        response += f"...y {instructores.count() - 3} profesionales más.\n\n"

    response += "Puedes conocer a todo el equipo en nuestra página 'Nosotros' 🌟"

    return response


def get_novedades_response():
    """Genera respuesta sobre novedades/blog."""
    posts = BlogPost.objects.filter(
        is_published=True).order_by('-published_date')[:3]

    if not posts.exists():
        return "Aún no tenemos novedades publicadas. ¡Pronto tendremos contenido nuevo!"

    response = "📰 **Últimas novedades:**\n\n"

    for post in posts:
        fecha = post.published_date.strftime(
            '%d/%m/%Y') if post.published_date else 'Reciente'
        response += f"• **{post.title}** ({fecha})\n"

    response += "\nPuedes ver todas nuestras novedades en la sección 'Novedades' del sitio 📖"

    return response


def get_chatbot_response(message):
    """Procesa el mensaje del usuario y genera una respuesta."""
    intent, confidence = detect_intent(message)

    responses = {
        'saludo': (
            "¡Hola! 👋 Bienvenid@ a Pilates Reforma.\n\n"
            "Puedo ayudarte con:\n"
            "• Servicios y precios 💰\n"
            "• Horarios de atención ⏰\n"
            "• Ubicación 📍\n"
            "• Nuestro equipo 👥\n"
            "• Novedades 📰\n"
            "• Contacto 📞"
        ),

        'precios': get_precios_response(),

        'horarios': (
            "⏰ **Nuestros horarios de atención:**\n\n"
            "📅 Lunes a Viernes: 07:00 - 21:00\n"
            "📅 Sábados: 09:00 - 14:00\n"
            "📅 Domingos y festivos: Cerrado"
        ),

        'ubicacion': (
            "📍 **Nuestra ubicación:**\n\n"
            f"{settings.CHATBOT_ADDRESS}\n\n"
            "🚗 Estacionamiento disponible en el edificio\n"
            "🚇 Cerca del metro Grecia (Línea 4)\n\n"
            f"Ver mapa: {settings.CHATBOT_MAP_URL}"
        ),

        'servicios': get_servicios_response(),

        'instructores': get_instructores_response(),

        'novedades': get_novedades_response(),

        'contacto': (
            "📞 **Contáctanos:**\n\n"
            f"Teléfono: {settings.CHATBOT_PHONE}\n"
            "Email: contacto@pilatesreforma.cl\n"
            "WhatsApp: https://wa.me/56912345678\n\n"
            "Instagram: @pilatesreforma\n"
            "Facebook: Pilates Reforma\n\n"
            "También puedes usar el formulario de contacto en nuestra web ✉️"
        ),

        'despedida': (
            "¡Gracias por escribir! 😊\n\n"
            "¡Nos vemos! 🧘‍♀️✨"
        ),

        'unknown': (
            "Disculpa, no estoy seguro de entender. 🤔\n\n"
            "Puedo ayudarte con:\n"
            "• Servicios y precios\n"
            "• Horarios\n"
            "• Ubicación\n"
            "• Equipo\n"
            "• Novedades\n\n"
            f"O contáctanos al {settings.CHATBOT_PHONE} 📞"
        )
    }

    return responses.get(intent, responses['unknown'])


@require_http_methods(["POST"])
def chat_api(request):
    """
    API endpoint para el chatbot.
    Recibe mensaje JSON, retorna respuesta JSON.
    """
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()

        if not user_message:
            return JsonResponse({
                'reply': 'Por favor escribe un mensaje 😊'
            })

        # Generar respuesta
        bot_reply = get_chatbot_response(user_message)

        return JsonResponse({
            'reply': bot_reply,
            'timestamp': datetime.now().isoformat()
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Formato de mensaje inválido'
        }, status=400)

    except Exception as e:
        return JsonResponse({
            'error': 'Error interno del servidor',
            'details': str(e) if settings.DEBUG else None
        }, status=500)
