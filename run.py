# Credits to: Liz Petrov in her article https://makezine.com/projects/sms-bot/
# libraries
from flask import Flask, request
from twilio.twiml.messaging_response import Message, MessagingResponse

# set up Flask to connect this code to the local host, which will
# later be connected to the internet through Ngrok
app = Flask(__name__)

def getReply(message):

    # Make the message lower case and without spaces on the end for easier handling
    message = message.lower().strip()
    # This is the variable where we will store our response
    answer = ""

    # if keyword "weather" is in the message
    if "weather" in message:
        answer = "get the weather using a weather API"

    # is the keyword "wiki" in the message? Ex: "wiki donald trump"
    elif "wiki" in message:
        answer = "get a response from the Wikipedia API"

    # if the keyword is "donate"
    elif "donate" in message:
        answer = "get some donations from a site"

    # the message contains no keyword. Display a help prompt to identify possible
    # commands
    else:
        answer = "\n Welcome! These are the commands you may use: \nWIKI \"wikipedia request\"\nWEATHER \"place\"\nDONATE \"make a donation\"\n"

    # Twilio can not send messages over 1600 characters in one message. Wikipedia
    # summaries may have way more than this.
    # So shortening is required (1500 chars is a good bet):
    if len(answer) > 1500:
        answer = answer[0:1500] + "..."

    # return the formulated answer
    return answer
    
# Main method. When a POST request is sent to our local host through Ngrok,
# this code will run. The Twilio service # sends the POST request - we will set this up on the Twilio website. So when # a message is sent over SMS to our Twilio number, this code will run
@app.route('/', methods=['POST'])
def sms():
    # Get the text in the message sent
    message_body = request.form['Body']

    # Create a Twilio response object to be able to send a reply back (as per         # Twilio docs)
    resp = MessagingResponse()

    # Send the message body to the getReply message, where
    # we will query the String and formulate a response
    replyText = getReply(message_body)

	# Text back our response!
    resp.message('Hi\n\n' + replyText )
    return str(resp)

# when you run the code through terminal, this will allow Flask to work
if __name__ == '__main__':
    app.run()

# Removes keyword from searching functions
def removeHead(fromThis, removeThis):
    if fromThis.endswith(removeThis):
        fromThis = fromThis[:-len(removeThis)].strip()
    elif fromThis.startswith(removeThis):
        fromThis = fromThis[len(removeThis):].strip()

    return fromThis
