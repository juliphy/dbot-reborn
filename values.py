
# Не трогати це!
length = 12 # Розмір ID
users = {}

class User:
    def __init__(self):
        self.name = None
        self.birthdate = None
        self.firstname = None
        self.url_face = None
        self.url_sign = None
        self.id = None
        self.passport_id = None
        self.chatID = None
        self.kpp_id = None


    def json(self):
        return {"name":self.name, "birthdate": self.birthdate, "firstname": self.firstname, "urlFace": self.url_face, "urlSign": self.url_sign, "chatID":self.chatID, "passport_id": self.passport_id, "kpp_id": self.kpp_id, "id": self.id }


# Можна трогати це!
token = "6480118641:AAGi-rJwYAj0tE2rqwnEJ4uiaS8kEw-Oqa0" # Ваш токен бота
img_api_key = "d2f5768f8798f57a63d32ddd6a4e9f8e"
server_url = 'https://xnet-server.onrender.com' # IP чи URL-адреса вашого xnet-server
client_url = 'https://juliphy.github.io/project-x' # URL-адреса вашого project-x



