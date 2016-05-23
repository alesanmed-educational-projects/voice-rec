# -*- coding: UTF-8 -*-
import requests
import json

def run():
	path = 'product.wav'
	wav = open(path, 'rb')

	headers = {
		'Authorization': 'Bearer UPRL3H64PZKCVAJF4Z7PG5VFXLWPMCZM',
		'content-type': 'audio/wav'
	}

	r = requests.post('https://api.wit.ai/speech?v=20160511', headers=headers,
								 data=wav);

	return r.json()['_text']
