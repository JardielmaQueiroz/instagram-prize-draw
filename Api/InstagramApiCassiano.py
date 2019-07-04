from datetime import datetime, timedelta
import time
import json
from random import randint
from InstagramAPI import InstagramAPI


class InstagramApiCustom(InstagramAPI):

    def __init__(self, username, password):
        super().__init__(username, password)
        self.user_id = 0
        self.id_media = 0
        self.two_factor = False

    def login(self, force=False):
        if (not self.isLoggedIn or force):
            if (self.two_factor or self.SendRequest('si/fetch_headers/?challenge_type=signup&guid=' + self.generateUUID(False), None, True)):

                data = {'phone_id': self.generateUUID(True),
                        '_csrftoken': self.LastResponse.cookies['csrftoken'],
                        'username': self.username,
                        'guid': self.uuid,
                        'device_id': self.device_id,
                        'password': self.password,
                        'login_attempt_count': '0'}

                if (self.two_factor or self.SendRequest('accounts/login/', self.generateSignature(json.dumps(data)), True)):
                    self.isLoggedIn = True
                    self.username_id = self.LastJson["logged_in_user"]["pk"]
                    self.rank_token = "%s_%s" % (self.username_id, self.uuid)
                    self.token = self.LastResponse.cookies["csrftoken"]
                    return True

    def login_account(self):
        self.login()
        response = self.LastJson
        if response['status'] == 'fail':
            if "two_factor_required" in list(response.keys()):
                code = input("Insira o código enviado via SMS: ")
                self.send_two_factor_code(code)
                response = self.LastJson
                if response['status'] == 'ok':
                    return True
                elif response['status'] == 'fail':
                    return False
        else:
            return True

    def send_two_factor_code(self, code):
        data = {
            "verification_code": code,
            "_csrftoken": self.LastResponse.cookies['csrftoken'],
            "two_factor_identifier": self.LastJson['two_factor_info']['two_factor_identifier'],
            "username": self.username,
            "guid": self.uuid,
            "device_id": self.device_id,
            "_uuid": self.uuid
        }
        self.two_factor = self.SendRequest(
            'accounts/two_factor_login/', self.generateSignature(json.dumps(data)), True)
        self.login()

    def find_user_id(self, profile):
        # PROCURANDO O PERFIL DA PROMOCAO
        self.searchUsername(profile)
        response = self.LastJson  # PEGANDO A RESPOSTA
        # CASO STATUS DA RESPOSTA SEJA FAIL NÃO FOI POSSIVEL FAZER O LOGIN
        if response['status'] == 'fail':
            return False
        else:
            self.user_id = response['user']['pk']
            return True

    def search_photo(self, photo):
        find = False
        max_id = ''
        while not find:
            # PEGANDO UMA QUANTIDADE DE FOTOS DO PERFIL
            self.getUserFeed(self.user_id, max_id)
            # GUARDANDO ESSA LISTA DE FOTOS
            feed_user = self.LastJson['items']

            for date in feed_user:  # VARRENDO A LISTA FOTO POR FOTO
                # VERIFICANDO SE O CODIGO DA FOTO É O MESMO FORNECIDO PELO USUARIO
                if date['code'] == photo:
                    self.id_media = date['pk']  # GUARDANDO ESSE CÓDIGO
                    return True  # RETORNO TRUE POIS ACHEI

            if not find:  # CASO NAO TENHA ACHADO AINDA
                # PEGO O TAMANHO DA LISTA DE FOTOS RECEBIDA
                size_vet = len(feed_user)
                if size_vet != 0:  # VERIFICO SE O TAMANHO NÃO É ZERO, POIS POSSO TER PEGO JÁ TODAS AS FOTOS DO PERFIL
                    # PEGO O ID DA ULTIMA FOTO DA LISTA
                    max_id = feed_user[size_vet - 1]['id']
                else:
                    return False  # RETORNO FALSO CASO NAO TENHA ENCONTRADO

    def do_comment(self, text):
        # COMENTO O TEXTO ENVIADO NA FOTO ESPECIFICA
        self.comment(self.id_media, text)
        status = self.LastJson['status']  # PEGO O RESULTADO DO COMENTARIO
        if status == 'ok':  # VERIFICO SE FOI COMENTADO
            return True  # RETORNO TRUE SE SIM
        else:
            return False  # RETORNO FALSE SE NÃO
    
    # override
    def SendRequest(self, endpoint, post=None, login=False):
        verify = False  # don't show request warning

        if (not self.isLoggedIn and not login):
            raise Exception("Not logged in!\n")

        self.s.headers.update({'Connection': 'close',
                               'Accept': '*/*',
                               'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                               'Cookie2': '$Version=1',
                               'Accept-Language': 'en-US',
                               'User-Agent': self.USER_AGENT})

        while True:
            try:
                if (post is not None):
                    response = self.s.post(self.API_URL + endpoint, data=post, verify=verify)
                else:
                    response = self.s.get(self.API_URL + endpoint, verify=verify)
                break
            except Exception as e:
                print('Except on SendRequest (wait 60 sec and resend): ' + str(e))
                time.sleep(60)
        try:
            self.LastResponse = response
            self.LastJson = json.loads(response.text)
        except:
            pass

        if response.status_code == 200:
            return True
        elif (response.status_code == 500):
            response.raise_for_status()
            return False
        elif (response.status_code == 400) and ("two_factor_required" in self.LastJson) and (self.LastJson["two_factor_required"] == True):
            return False
        elif (response.status_code == 400) and ("error_type" in self.LastJson) and (self.LastJson['error_type'] == 'sms_code_validation_code_invalid'):
            print("Error: %s" % self.LastJson['message'])
            return False
        else:
            return False