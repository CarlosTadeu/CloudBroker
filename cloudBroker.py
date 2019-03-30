from flask import Flask, request, jsonify
from bson import json_util
import bson
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB('db.json')
User = Query()

vm_id = 0

PROV_URL = 'http://127.0.0.1:5000/'
@app.route('/')
def main():
    return db

@app.route('/provedor/cadastrar/<provider_id>',methods=['POST'])
def init_provedor(provider_id):
    global vm_id
    data = request.get_json()
    db.insert(
        {
            'vm_id': str(vm_id),
            'provider_id': provider_id,
            'vcpu': data['vcpu'],
            'ram': data['ram'],
            'hd': data['hd'],
            'preco': data['preco'],
            'usando': 'false'
        })

    vm_id = vm_id + 1
    return jsonify({'Ok': True})

@app.route('/search',methods=['POST'])
def search_vm():
    data = request.get_json()
    provider = []
    busca = db.search((User.vcpu == data['vcpu']) &
                      (User.ram == data['ram']) &
                      (User.hd == data['hd']) &
                      (User.usando == 'false'))

    if (busca):
        min_price = int(busca[0]['preco'])
        provider = busca[0]
        for item in busca:
            if (int(item['preco']) < min_price):
                min_price = int(item['preco'])
                provider = item

    return bson.json_util.dumps(provider)

@app.route('/release',methods=['POST'])
def release_vm():
    data = request.get_json()
    busca = []
    busca = db.search((User.vm_id == data['vm_id']) &
                      (User.usando == 'true'))

    db.update({'usando': 'false'}, User.vm_id == data['vm_id'])

    return bson.json_util.dumps(busca)

@app.route('/use',methods=['POST'])
def use_vm():
    data = request.get_json()
    db.update({'usando': 'true'}, User.vm_id == data['vm_id'])
    data['usando'] = 'true'

    return bson.json_util.dumps(data)