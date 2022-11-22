from ast import For
from errno import EDEADLK
import telebot
import re
import random
from telebot.types import ReplyKeyboardMarkup
from telebot.types import ForceReply
from telebot.types import ReplyKeyboardRemove
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
TELEGRAM_TOKEN = "5688151693:AAEoY21NR-3zNVImKv-Fee453AVvugnsCzo"
usuarios = {}
prueba = True
nombre = ''
id_conversacion = ''
bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(regexp="hola")
def cmd_start(message):
    markup = ReplyKeyboardRemove()
    if prueba:
        bot.send_message(message.chat.id, '👋Hola!! apreciado cliente estamos encantados de que nos escribas. Escribe el comando /start para que podamos atenderte como te lo mereces. \n Que esperas vamos', reply_markup=markup)
    else:
        if nombre != "":
            msg = bot.send_message(message.chat.id, 'Hey!!👋  ' +
                                   usuarios[message.chat.id]['nombre'] + "  Como estas?", reply_markup=markup)
            bot.register_next_step_handler(msg, conversacion)
        else:
            bot.send_message(
                message.chat.id, "Hey! utiliza el comando /alta para que te podamos conocer. \n Entonces que esperas? 🏃")


def conversacion(message):
    markup = ReplyKeyboardRemove()
    if (message.text == 'chao'):
        return bot.send_message(message.chat.id, 'Hasta Luego')
    mensaje = get_response(message.text)
    markup = ForceReply(selective=False)
    msg = bot.send_message(message.chat.id, mensaje, reply_markup=markup)


def get_response(user_input):
    split_message = re.split(r'\s|[,:;.?!-_]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response


def check_all_messages(message):
    highest_prob = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob
        highest_prob[bot_response] = message_probability(
            message, list_of_words, single_response, required_words)

    response('Me alegra escuchar que nuestros clientes se encuentren felices', [
             'Bien', 'excelente', 'increible', 'muy bien', 'bien'], single_response=True)
    response('Lamentamos enormemente escuchar eso. Recuerda que cuentas con nosotros para que te podamos animar', [
             'mal', 'triste', 'deprimido', 'Mal', 'suicidio'], single_response=True)
    response('Estamos ubicados en la calle 23 numero 123', [
             'ubicados', 'direccion', 'donde', 'ubicacion'], single_response=True)
    response('Siempre a la orden', [
             'gracias', 'te lo agradezco', 'thanks'], single_response=True)
    response('Me encuentro bien gracias por preguntar', [
             'estas', 'encuentras', 'que tal tu dia'], single_response=True)
    response('Me llamo kady', [
             'llamas', 'nombre', 'apellido'], single_response=True)
    response('Utiliza la etiqueta /precio para que veas nuestros precios y productos',
             ['precio', 'precios', 'valor', 'productos'], single_response=True)

    best_match = max(highest_prob, key=highest_prob.get)

    return unknown() if highest_prob[best_match] < 1 else best_match


def get_response(user_input):
    split_message = re.split(r'\s|[,:;.?!-_]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response


def message_probability(user_message, recognized_words, single_response=False, required_word=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognized_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognized_words))

    for word in required_word:
        if word not in user_message:
            has_required_words = False
            break
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def unknown():
    response = ['puedes decirlo de nuevo?', 'No estoy seguro de lo quieres',
                'búscalo en google a ver que tal'][random.randrange(3)]
    return response


@bot.message_handler(commands=["start", "ayuda", "help"])
def cmd_start(message):
    global prueba
    prueba = False
    markup = ReplyKeyboardRemove()
    foto = open("./img/logo.jpg", "rb")
    bot.send_photo(message.chat.id, foto, '*Hola Somos tortas kady una empresa de reposteria donde hacemos las mas ricas tortas de la ciudad*\n **',
                   reply_markup=markup, parse_mode="MarkdownV2")

    markup = ForceReply(selective=False)
    bot.send_message(message.chat.id, "Estamos encantados de que nos hayas contactado es por eso que te invitamos a que uses el comando /alta para que podamos conocerte mejor🥳🥳🥳", reply_markup=markup)


@bot.message_handler(commands=["alta"])
def cmd_alta(message):
    markup = ForceReply()
    msg = bot.send_message(
        message.chat.id, "Como te llamas", reply_markup=markup)
    bot.register_next_step_handler(msg, preguntar_edad)


def preguntar_edad(message):

    usuarios[message.chat.id] = {}
    usuarios[message.chat.id]["nombre"] = message.text
    global nombre
    nombre = message.text
    markup = ForceReply()
    bot.send_message(
        message.chat.id, f'Te damos la bienvenida {usuarios[message.chat.id]["nombre"]}')
    msg = bot.send_message(
        message.chat.id, "Cual es tu edad", reply_markup=markup)
    bot.register_next_step_handler(msg, preguntar_sexo)


def preguntar_sexo(message):
    if not message.text.isdigit():
        markup = ForceReply()
        msg = bot.send_message(
            message.chat.id, "Debes indicar un numero.\n¿Cuantos años tienes?", reply_markup=markup)
        bot.register_next_step_handler(msg, preguntar_sexo)
    else:
        usuarios[message.chat.id]["edad"] = int(message.text)

        bot.send_message(
            message.chat.id, f'Tu edad es de {usuarios[message.chat.id]["edad"]} años')
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True, input_field_placeholder="Pulsa un Boton", resize_keyboard=True)
        markup.add("Hombre", "Mujer")
        msg = bot.send_message(
            message.chat.id, "Cual es tu Sexo", reply_markup=markup)
        bot.register_next_step_handler(msg, guardar_datos)


def guardar_datos(message):
    global prueba
    prueba = False
    if message.text != "Hombre" and message.text != "Mujer":
        msg = bot.send_message(
            message.chat.id, "ERROR tienes que elegir entre Hombre o Mujer")
        bot.register_next_step_handler(msg, guardar_datos)
    else:
        global usuarios
        global id_conversacion
        id_conversacion = message.chat.id
        usuarios[message.chat.id]["sexo"] = message.text
        texto = 'Datos Introducidos: \n'
        texto += f'<b>Nombre:</b> {usuarios[message.chat.id]["nombre"]} \n'
        texto += f'<b>EDAD:</b> {usuarios[message.chat.id]["edad"]} \n'
        texto += f'<b>Sexo:</b> {usuarios[message.chat.id]["sexo"]} \n'
        markup = ReplyKeyboardRemove()
        bot.send_message(message.chat.id, texto,
                         parse_mode="html", reply_markup=markup)
        print(usuarios)
        bot.send_message(message.chat.id, "Coloca /precio para ver lista de precios o escribe hola para que nos conoscamos mejor! recuerda despedirte es decirme dime chao para saber que ya no quieres seguir interactuando 🥲🥲")


@bot.message_handler(commands=["precio"])
def mostrar_precio(message):
    foto = open("./img/logo.jpg", "rb")
    bot.send_photo(message.chat.id, foto, "Esta es nuestra lista de Precios")
    markup = InlineKeyboardMarkup(row_width=2)
    b1 = InlineKeyboardButton(
        "Descuentos", url="https://www.instagram.com/tortaskady_/")
    b2 = InlineKeyboardButton(
        "Fondan", url="https://www.instagram.com/p/CjBDduYL9om/")
    b3 = InlineKeyboardButton(
        "A tu gusto", url="https://www.instagram.com/p/CjBDDZVLyai/")
    b4 = InlineKeyboardButton(
        "Elegancia", url="https://www.instagram.com/p/CjBDH3oL1w0/")
    b5 = InlineKeyboardButton(
        "Para cualquier momento especial", url="https://www.instagram.com/p/CiSuWouriOJ/")
    markup.add(b1, b2, b3, b4, b5)
    bot.send_message(message.chat.id, "Mis tortas en ofertas",
                     reply_markup=markup)
    bot.send_message(
        message.chat.id, "Coloca /instagram para obtener enlace de nuestro Instagram y hacer pedido")


@bot.message_handler(commands=["instagram"])
def mostrar_ig(message):
    texto_html = '<b>Enlace para Hacer pedido por Instagram</b>' + '\n'
    texto_html += '<a href="https://www.instagram.com/tortaskady_/">Enlace</a >' + '\n'
    markup = ReplyKeyboardRemove()
    bot.send_message(message.chat.id, texto_html,
                     parse_mode="html", reply_markup=markup)
    bot.send_message(
        message.chat.id, "Coloca /telefono para obtener nuestro numero telefonico")


@bot.message_handler(commands=["telefono"])
def mostrar_telefono(message):
    texto_html = '<b>Nuestro numero telefonico para hacer pedidos via Whatssap es 042666555</b>'
    markup = ReplyKeyboardRemove()
    bot.send_message(message.chat.id, texto_html,
                     parse_mode="html", reply_markup=markup)


if __name__ == '__main__':
    print('Iniciando Bot')
    bot.infinity_polling()
