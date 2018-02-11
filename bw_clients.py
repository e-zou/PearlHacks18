import os
import sys
from bandwidth import messaging, voice, account

# Grab environment variables.
user_id = os.environ.get('BANDWIDTH_USER_ID', 'u-nwcurdyok7qjclpn5fbbjry')
token = os.environ.get('BANDWIDTH_API_TOKEN', 't-pzipqox45zoxsz77q44doha')
secret = os.environ.get('BANDWIDTH_API_SECRET', 'xd5pkk7wux3m45qdcen4avpugkdwf3h72s2tgmq')

# Make sure the evn variables are set
if not all((user_id, token, secret)):
    print('Please make sure you have set your user_id, token, and secret as environment variables')
    sys.exit();

# Works best if you include each of these individually
messaging_api = messaging.Client(user_id, token, secret)
voice_api = voice.Client(user_id, token, secret)
account_api = account.Client(user_id, token, secret)

app_name = 'bandwidth-python-quickstart'

call_path = '/inbound-voice-callbacks'
message_path = '/inbound-message-callbacks'