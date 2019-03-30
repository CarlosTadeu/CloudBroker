import requests
import json
import sys

#PROV_URL = 'http://127.0.0.1:5000/'
PROV_URL = 'https://cloudbroker-1fdfa.appspot.com/'

class Provedor:
    def __init__(self):
        self.quantidade = 0
        self.recurso = {}

    def menu(self):
        while True:
            print('1. Consultar e usar recurso')
            print('2. Liberar recurso')
            print('3. Sair')
            opc = int(input())

            if opc == 1:
                response = self.buscar()

                if (not response):
                    print('\n--> Recurso não encontradado.\n')
                else:
                    print('\n--> Recurso encontrado.\n')
                    print(json.dumps(response, indent=4))

                    uso = str(input('Deseja usar este recurso? [s/n]\n'))
                    if (uso == 's'):
                        response = self.postRequest(response, PROV_URL + 'use')
                        print('\n--> Voce esta usando o recurso '+ response['vm_id'] +'.\n')

            if opc == 2:
                response = self.liberar()

                if (not response):
                    print('\n--> Recurso não encontrado em uso.\n')
                else:
                    print('\n--> Recurso liberado.\n')

            if opc == 3:
                return 0

    def buscar(self):
        recursos = {
            'vcpu': '',
            'ram': '',
            'hd': ''
        }
        recursos['vcpu'] = str(input('Quantidade de vCPUs: '))
        recursos['ram'] = str(input('Quantidade de memoria RAM (em GB): '))
        recursos['hd'] = str(input('Quantidade de disco (HD, em GB): '))

        return self.postRequest(recursos, PROV_URL + 'search')

    def liberar(self):
        recurso = {
            'vm_id': ''
        }
        recurso['vm_id'] = str(input('Digite o ID da máquina virtual que deseja liberar: '))

        return self.postRequest(recurso, PROV_URL + 'release')

    def postRequest(self, data, url):
        headers = {'Content-Type': 'application/json', }
        post = requests.post(url=url, data=json.dumps(data), headers=headers)

        return post.json()


if __name__ == '__main__':
    p = Provedor()
    p.menu()