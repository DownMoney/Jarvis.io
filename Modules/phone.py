from twilio.rest import TwilioRestClient
 
# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "ACae6263a1dcef4949ada05656374769c0"
auth_token  = "0b088e5560cf97f7fe847ff32d4185a5"
client = TwilioRestClient(account_sid, auth_token)

def sendMessage(message, number):
	client.sms.messages.create(body=message,
	    to=number,    # Replace with your phone number
	    from_="+441143599292") # Replace with your Twilio number