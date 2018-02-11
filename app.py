import os
import sys
import pprint
import json
import webhoseio

from bw_clients import *
from flask import Flask, request, render_template
from quick_deploy import *

app = Flask(__name__)

def po(o):
    """
    Prints things to console much more nicely than the default print
    """
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(o)

# Global variable for app name
bw_application_id = ''

# Trims text if it is too long; Useful for future development that includes some texts of articles
def trim_text(str):
    length = len([c for c in s if c.isdigit()])
    if length > 150:
        str = str[0:151]

# Web crawler that finds information on news articles
webhoseio.config(token="99ea9e40-d0a0-4407-9c0a-2b9b94144549")
query_params = {
    "q": "language:english performance_score:>0 (title:\"Hurricane\" OR title:\"State of Emergency\" OR title:\"Earthquake\" ) (site_type:news -buzzfeed.com -nhl.com -espn.com -gamespot.com ) thread.title:(-thread.title:game -thread.title:GOP -thread.title:democrat -thread.title:prostitute -thread.title:sex -thread.title:court)",
	"sort": "crawled"
}
output = webhoseio.query("filterWebContent", query_params)
# title of news articles
t1 = output['posts'][0]['title']
t2 = output['posts'][1]['title']
t3 = output['posts'][2]['title']
t4 = output['posts'][3]['title']
t5 = output['posts'][4]['title']

 # Print the text of the first post

@app.route('/', methods=['POST'])
def handle_message():

    """
    Setup a callback handler for POST message events, keep in mind that if you
    have this setup in a BXML (for voice) app, that this should be GET as well
    """
    
    callback_event = request.get_json()
    po(callback_event)
    event_type = callback_event['eventType']

    # if someone submits a text
    if event_type == 'sms':
        your_message = messaging_api.send_message( from_ = callback_event['to'],
                                  to = callback_event['from'],
                                  text = 'Recent Reports: '+ '\n' + '\n1: ' + t1 
                                  + '\n' + '\n2: ' + t2 + '\n' + '\n3: ' + t3
                                  + '\n' + '\n4: ' + t4 + '\n' + '\n5: ' + t5  + '\n\n' 
                                  + 'Do you want to help solve pressing issues by chipping in some spare change?')
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    # if someone submits multimedia back
    elif event_type == 'mms':
        messaging_api.send_message( from_ = callback_event['to'],
                                  to = callback_event['from'],
                                  text = 'Thank you for submitting your artwork. ',
                                  media = 'https://snag.gy/HOtwVm.jpg')
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    else:
        # Ignore everything else
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

# Automatically runs Flask so you don't have to use "FLASK_APP run" on the command line
if __name__=="__main__":
    app.run(debug=True) 
