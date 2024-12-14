import os, sys
sys.path.insert(0, os.path.abspath('src'))
from jellyfaas import *

API_KEY = os.getenv('JELLYFAAS_API_KEY')
if not API_KEY:
    raise Exception('No API KEY')


client = AIClient(AIConfig(API_KEY))

file = open('test/campaign-compressed.pdf', mode='rb')
client.upload(file, 'frogidol')