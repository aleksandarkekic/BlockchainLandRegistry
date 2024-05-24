import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from rsaKey import Encrypt
import json


def run():
    #we read all json data from 'blockchain.json' file

    with open("blockchain.json", 'r') as file:
        blockchain_data = json.load(file)


    chain = blockchain_data['chain']

    #for every block in the chain we print following informations
    #we are using data_decrypt() method to decrypt data from the block

    for block in chain:
        print("Index:", block['index'])
        print("Timestamp:", block['timestamp'])
        print("Proof:", block['proof'])
        print("Previous Hash:", block['previous_hash'])
        if  len(block['data']) ==0:
            print(block['data'])
        else:
            print("Data:", data_decrypt(block['data']))
        print("\n")

def data_decrypt(data):
    #this method is used for decryption information
    #first we need to do b64decode and then decryption with private key
    # return result is string with information about land registry
    string_vr=str(data)
    #print(type(string_vr))
    parts = string_vr.split(", ")
    surface_area = parts[0].split(":")[1].strip()
    sale_price = parts[1].split(":")[1].strip()
    previous_owner = parts[2].split(":")[1].strip()
    current_owner = parts[3].split(":")[1].strip()
    contract_date = parts[4].split(":")[1].strip()
    address = parts[5].split(":")[1].strip()
    surface_area_decrypt = Encrypt.decryption(base64.b64decode(surface_area.encode('utf-8')[2:-1]))
    sale_price_decrypt = Encrypt.decryption(base64.b64decode(sale_price.encode('utf-8')[2:-1]))
    previous_owner_decrypt = Encrypt.decryption(base64.b64decode(previous_owner.encode('utf-8')[2:-1]))
    current_owner_decrypt = Encrypt.decryption(base64.b64decode(current_owner.encode('utf-8')[2:-1]))
    contract_date_decrypt = Encrypt.decryption(base64.b64decode(contract_date.encode('utf-8')[2:-1]))
    address_decrypt = Encrypt.decryption(base64.b64decode(address.encode('utf-8')[2:-1]))
    result = f"surface_area: {surface_area_decrypt}, sale_price: {sale_price_decrypt}, previous_owner: {previous_owner_decrypt}, current_owner: {current_owner_decrypt}, contract_date: {contract_date_decrypt}, address: {address_decrypt}"
    return result

if __name__ == '__main__':
    flag = True
    while flag:
        print("\n==================================")
        print("=== Read File ================ [1]")
        print("=== Exit ===================== [2]")
        print("==================================\n")

        option = input("Enter option number: ")

        if option.__eq__("1"):
            priv_key=""
            print("Input private key: \n ")

            while True:
                line = input()
                if not line:
                    break
                priv_key += line + '\n'

            with open("private_key.pem", 'r') as file:
                private_key_read = file.read()
            print(private_key_read.replace('\n', ' '))
            print(priv_key.replace('\n', ' '))
            if private_key_read.replace('\n', ' ') == priv_key.replace('\n', ' '):
                run()

        elif option.__eq__("2"):
            flag = False

