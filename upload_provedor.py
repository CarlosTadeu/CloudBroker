import requests
import json

#PROV_URL = 'http://127.0.0.1:5000/'
PROV_URL = 'https://cloudbroker-1fdfa.appspot.com/'

class Provedor:
    def __init__(self):
        self.quantidade = 0
        self.recurso = {}

    @property
    def menu(self):
        while True:
            print ("1. Divulgar recursos")
            print ("2. Sair")
            opc = int(input())

            if (opc == 1):
                #file = open(sys.argv[1])
                #json_data = json.load(file)
                #print(json_data)
                response = self.divulgar()
                if (response['Ok'] == True):
                    print("\n--> Recurso divulgado com sucesso.\n")
                else:
                    print("\n--> Erro ao divulgar recurso.\n")
            elif (opc == 2):
                return 0

    def divulgar(self):

        provider_id = int(input('Id do provedor: '))

        recursos = {
            'vcpu': '',
            'ram': '',
            'hd': '',
            'preco': ''
        }
        recursos['provider_id'] = provider_id
        recursos['vcpu'] = str(input('Quantidade de vCPUs: '))
        recursos['ram'] = str(input('Quantidade de memoria RAM (em GB): '))
        recursos['hd'] = str(input('Quantidade de disco (HD, em GB): '))
        recursos['preco'] = str(input('Preco do recurso (em R$): '))
        return self.postRequest(recursos, PROV_URL + 'provedor/cadastrar/' + str(provider_id))

    def postRequest(self, data, url):
        headers = {'Content-Type': 'application/json', }
        print(data)
        post = requests.post(url=url, data=json.dumps(data), headers=headers)
        return post.json()


if __name__ == '__main__':
    p = Provedor()
    p.menu