# -*- coding: UTF-8 -*-
import requests

def run():
    path = 'product.wav'
    wav = open(path, 'rb')

    headers = {
        'Authorization': 'Bearer RJJUXHI2B3JSACNLVWTBHOKZDCE46M5D',
        'content-type': 'audio/wav'
    }

    r = requests.post('https://api.wit.ai/speech?v=20160511', headers=headers,
                                 data=wav);
    
    print(r.json()['_text'])
    return r.json()['_text']
