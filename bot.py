# -*- coding: utf-8 -*-

import os, datetime, locale, configparser, forecastio, platform
from slackclient import SlackClient

if platform.system() == "Windows":
    locale.setlocale(locale.LC_TIME, 'es-ES') 
else:
    locale.setlocale(locale.LC_TIME, 'es_ES')

config = configparser.ConfigParser()
config.read("config.ini")
authed_teams = {}

santander = [43.462, -3.81]
next_event_messages = ["PROXIMO EVENTO", "PRÓXIMO EVENTO", "SIGUIENTE EVENTO", "SIGUIENTE CHARLA", "PRÓXIMA QUEDADA", "SIGUIENTE QUEDADA"]
forescat_messages = ["PREVISIÓN", "TIEMPO", "PREVISION"]
greetings_messages = ["HOLA", "HI", "BUENAS", "HEY"]
thanks_messages = ["GRACIAS"]
goodbyes_messages = ["ADIOS", "HASTA LUEGO", "CIAO", "BYE"]
offensive_words_bad = []
offensive_words = []
with open('offensivewords.txt', 'r') as myfile:
    offensive_words_bad = myfile.readlines()

for ow in offensive_words_bad:
   offensive_words.append(ow.rstrip('\n'))



class CodersBot(object):

    def __init__(self):
        super(CodersBot, self).__init__()
        self.name = "codersbot"
        self.emoji = ":keyboard:"
        self.oauth = {"client_id": config.get("slack", "client_id"),
                      "client_secret": config.get("slack", "client_secret"),
                      "scope": "bot"}
        self.verification = config.get("slack", "verification_token")
        self.client = SlackClient(config.get("slack", "oauth_secret"))

    def auth(self, code):
        auth_response = self.client.api_call(
                                "oauth.access",
                                client_id=self.oauth["client_id"],
                                client_secret=self.oauth["client_secret"],
                                code=code
                                )

        team_id = auth_response["team_id"]
        authed_teams[team_id] = {"bot_token":
                                 auth_response["bot"]["bot_access_token"]}

        self.client = SlackClient(authed_teams[team_id]["bot_token"])


    def open_dm(self, user_id):
        new_dm = self.client.api_call("im.open", user=user_id)
        dm_id = new_dm["channel"]["id"]
        return dm_id


    def get_username(self, user_id):
        user_info = self.client.api_call("users.info", user=user_id)
        username = user_info["user"]["real_name"]
        return username

    def get_user(self, user_id):
        user_info = self.client.api_call("users.info", user=user_id)
        users = user_info["user"]["name"]
        return users


    def onboarding_message(self, team_id, user_id):
        self.client.api_call("chat.postMessage",
            channel=self.open_dm(user_id),
            username=self.name,
            icon_emoji=self.emoji,
            text="¡Bienvenido a CodersCantabria! Somos una comunidad de desarrolladores hecha por desarrolladores y para desarrolladores."
             "\n Nos reunimos el primer viernes de cada mes de 18.30 a 20.30."
             "\n Puedes preguntarme ¿Cuándo será el siguiente evento? o ¿Cuál es la previsión del tiempo?"
            )


    def answer_message(self, team_id, user_id, channel, incoming_message):
        if any(s in incoming_message for s in offensive_words):
            self.client.api_call("chat.postMessage",
                channel=channel,
                username=self.name,
                icon_emoji=self.emoji,
                text="Cuida tu lenguaje, @%s https://media.giphy.com/media/GBIzZdF3AxZ6/giphy.gif" % self.get_user(user_id)
                )
        elif any(s in incoming_message.upper() for s in next_event_messages):
            next_event = self.next_event()
            self.client.api_call("chat.postMessage",
                channel=channel,
                username=self.name,
                icon_emoji=self.emoji,
                text="El próximo evento será el viernes %s a las 18.30 hasta las 20:30" % next_event.strftime("%d de %B")
                )
        elif any(s in incoming_message.upper() for s in forescat_messages):
            next_event = self.next_event()
            forecast = forecastio.load_forecast(key=config.get("forecast.io", "secret_key"), lat=santander[0], lng=santander[1], lang="es", time=datetime.datetime.combine(next_event, datetime.time(18, 30, 0)))
            text = "Viernes %s // %s // ↑ %sºC - ↓ %sºC" % (next_event.strftime("%d de %B"), forecast.daily().data[0].summary, forecast.daily().data[0].temperatureHigh, forecast.daily().data[0].temperatureLow)

            self.client.api_call("chat.postMessage",
                channel=channel,
                username=self.name,
                icon_emoji=self.emoji,
                text= text
                )
        elif any(s in incoming_message.upper() for s in greetings_messages):
            self.client.api_call("chat.postMessage",
                channel=channel,
                username=self.name,
                icon_emoji=self.emoji,
                text= "Hola %s" % self.get_username(user_id)
                )
        elif any(s in incoming_message.upper() for s in thanks_messages):
            self.client.api_call("chat.postMessage",
                channel=channel,
                username=self.name,
                icon_emoji=self.emoji,
                text= "Las que tu tienes"
                )
        elif any(s in incoming_message.upper() for s in goodbyes_messages):
            self.client.api_call("chat.postMessage",
                channel=channel,
                username=self.name,
                icon_emoji=self.emoji,
                text= "Hasta la próxima"
                )
        else:
            buttonUrl = 'https://www.google.com/search?q=%s' % incoming_message.replace(" ", "+")
            self.client.api_call("chat.postMessage",
                channel=channel,
                username=self.name,
                icon_emoji=self.emoji,
                text='Me he quedado sin palabras, pero Google seguramente sepa la respuesta.',
                attachments=[{
                    'fallback': buttonUrl,
                    'actions': [{'type': 'button', 'text': 'Búscalo :mag:', 'url': buttonUrl, 'style': 'primary'}]
                    }]
                )
        return


    def next_event(self):
        today = datetime.date.today()
        current_month = today.month
        year = today.year
        possible_day = self.calculate_first_friday(year, current_month)
        if today <= possible_day:
            return possible_day
        else:
            next_month = current_month + 1
            if next_month > 12:
                next_month = 1
                year += 1
            return self.calculate_first_friday(year, next_month)
                

    def calculate_first_friday(self, year, month):
        for month_day in range(1, 8):
            possible_day = datetime.date(year, month, month_day)
            if possible_day.weekday() == 4:
                return possible_day
        
                