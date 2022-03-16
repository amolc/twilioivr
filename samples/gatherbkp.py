from flask import Flask, request 
from twilio.twiml.voice_response import VoiceResponse,Pay, Say,Gather
import json
import requests as req

app = Flask(__name__)





@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Respond to incoming phone calls with a menu of options"""
    # Start our TwiML response
    resp = VoiceResponse()

    # Start our <Gather> verb
    gather = Gather(finishOnKey="#", action='/confirmshipping')
    gather.say('Please press one for shipping  , ,,,,,, ,,,,   ,,,,, ',voice="alice", language="en-GB")
    gather.say('Please press two for Customs duties or Charge back  , ,,,,,, ,,,,   ,,,,, ',voice="alice", language="en-GB")
    gather.say('Please press three for Subscription  , ,,,,,, ,,,,   ,,,,, ',voice="alice", language="en-GB")
    gather.say('Please press four for anything else  , ,,,,,, ,,,,   ,,,,, ',voice="alice", language="en-GB")
    resp.pause()
    resp.append(gather)
    resp.redirect('/voice')
    return str(resp)


@app.route('/shipping', methods=['GET', 'POST'])
def confirmshipping():
    """Processes results from the <Gather> prompt in /voice"""
    # Start our TwiML response
    resp = VoiceResponse()

    # If Twilio's request to our app included already gathered digits,
    # process them
    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']
        print("choice"+choice)
        resp.say('Thank you',voice="alice", language="en-GB" ) 
        # <Say> a different message depending on the caller's choice
        if choice == 1 : 
            gather = Gather(finishOnKey="#", action='/confirmshipping')
            gather.say('Please provbide your shipping number followed by a pound sign.       , ,,,,,, ,,,,   ,,,,, ',voice="alice", language="en-GB")
            resp.append(gather)
        elif  choice == 2 : 
            gather = Gather(finishOnKey="#", action='/confirmcustomcharges')
            gather.say('Please provbide your shipping number to know the custom charges.       , ,,,,,, ,,,,   ,,,,, ',voice="alice", language="en-GB")
            resp.append(gather)
        elif choice == 3 : 
            gather = Gather(finishOnKey="#", action='/confirmsubscription')
            gather.say('Please provbide your invoice number followed by a pound sign.       , ,,,,,, ,,,,   ,,,,, ',voice="alice", language="en-GB")
            resp.append(gather)

        elif choice == 4 : 
            gather = Gather(finishOnKey="#", action='/others')
            gather.say('Please wait while we transfer your call.       , ,,,,,, ,,,,   ,,,,, ',voice="alice", language="en-GB")
            resp.append(gather)
   
        else  :
            gather = Gather(finishOnKey="#", action='/voice')
            gather.pause(length=1)
            gather.say('Please select an option',voice="alice", language="en-GB" ) 
            resp.append(gather)
            
    # If the user didn't choose 1 or 2 (or anything), send them back to /voice
    return str(resp)







@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Respond to incoming phone calls with a menu of options"""
    # Start our TwiML response
    resp = VoiceResponse()

    # Start our <Gather> verb
    gather = Gather(finishOnKey="#", action='/confirmshipping')
    gather.say('Please provbide your shipping number followed by a pound sign.       , ,,,,,, ,,,,   ,,,,, ',voice="alice", language="en-GB")
    resp.append(gather)
    # If the user doesn't select an option, redirect them into a loop
    resp.redirect('/voice')
    return str(resp)


@app.route('/confirmshipping', methods=['GET', 'POST'])
def confirmshipping():
    """Processes results from the <Gather> prompt in /voice"""
    # Start our TwiML response
    resp = VoiceResponse()

    # If Twilio's request to our app included already gathered digits,
    # process them
    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']
        print("choice"+choice)
        resp.say('Thank you',voice="alice", language="en-GB" ) 
        # <Say> a different message depending on the caller's choice
        if len(choice) >= 5 : 
            resp.say('Please wait while we fetch the results',voice="alice", language="en-GB" ) 
            resp.pause(length=1)
            resp.redirect('/getshippingdetails?id='+choice)
        else :
            gather = Gather(finishOnKey="#", action='/voice')
            gather.pause(length=1)
            gather.say('Oh No, please give us your shipping number',voice="alice", language="en-GB" ) 
            resp.append(gather)
            
    # If the user didn't choose 1 or 2 (or anything), send them back to /voice
    
    return str(resp)
    

@app.route('/getshippingdetails', methods=['GET', 'POST'])
def getshippingdetails():
    resp = VoiceResponse()
    shippingid = request.args['id']
    print(shippingid)
    url = 'http://dev.zionshipping.com/shipping_details/' + shippingid 
    print(url)
    shipping_response = req.get(url)
    data_dict = shipping_response.json()
    print(data_dict)
    # shipped_by = data_dict.get(shipped_by,"0")
    try: 
        shipped_by = data_dict['shipped_by']
        shipped_for = data_dict['shipped_for']
        shipping_cost = data_dict['shipping_cost']
        shipped_from = data_dict['shipped_from']
    except:
        shipped_by = "0"

    if shipped_by == "0":
        print("No info found")
        msg3 = 'Your shipping id is incorrect,please try again'
        resp.say(msg3,voice="alice", language="en-GB")
        resp.redirect('/voice')


    else:
        print('else shipped_by',shipped_by) # Printing response
        print('shipped_for',shipped_for) # Printing response
        print('shipping_cost',shipping_cost) # Printing response
        print('shipped_from',shipped_from) # Printing response
        shippername = shipped_by
        deliverto = shipped_for
        shipmentamount  = shipping_cost
        msg = 'This shipment is sent by' + shippername +' and will deliver to ' + deliverto
        msg1 = 'There is a total balance of ' + shipmentamount + ', would you like to process to your payment now '
        msg3 = 'Please press one to accept or two to cancel'
        resp.say(msg,voice="alice", language="en-GB")
        resp.say(msg1,voice="alice", language="en-GB")
        shipmentamountunit = shipmentamount.split()
        shipmentamountunit[0]
        url = '/payment?shippingnumber=' + shippingid + '&pay=' + shipmentamountunit[0]
        gather = Gather(num_digits=1, action=url)
        gather.say(msg3,voice="alice", language="en-GB" ) 
        resp.append(gather)


    return str(resp)


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    resp = VoiceResponse()
    print('paymentmethod')
    shippingid = request.args['shippingnumber'] or 0
    amount = request.args['pay'] or 0    
    print('shippingid',shippingid)
    print('amount',amount)
    resp.say('Calling Twilio Pay')
    resp.pause(1)
    # resp.pay(charge_amount=amount,action='https://champagne-greyhound-2717.twil.io/stripepay')
    url = '/confirmpayment?shippingnumber='+ shippingid
    resp.pay(payment_connector='Stripe_Connector' , charge_amount=amount,action=url,description=shippingid)
    return str(resp)


@app.route('/confirmpayment', methods=['GET','POST'])
def confirmpayment():
    resp = VoiceResponse()
    multi_dict = request.form
    PaymentConfirmationCode = multi_dict['PaymentConfirmationCode']
    Result = multi_dict['Result']
    PaymentError = multi_dict['PaymentError']
    PaymentToken = multi_dict['PaymentToken']
    print(PaymentConfirmationCode)
    print(Result)
    print(PaymentError)
    print(PaymentToken)
    shippingid = request.args['shippingnumber'] or 0
    print("shippingidcallback",shippingid)
    
    if len(PaymentError) > 0 : 
        resp.say('Your transaction is not success, please wait while I am tranfering you to an Agent')
    else : 
        resp.say('Your transaction is completed successfuly. We have send you the confirmation to your phone and the invoice to your email.')
        resp.say('If you have any question please feel free to contact us back at any time. We appreciate your business. Good bye!')
        resp.hangup()
    return str(resp)



@app.route('/test', methods=['GET','POST'])
def test():
    resp = VoiceResponse()
    shippingid = request.args['id']
    url = 'http://dev.zionshipping.com/shipping_details/' + shippingid 
    shipping_response = req.get(url)
    shipped_by = 0
    data_dict =   shipping_response.json()
    print(data_dict)
    # shipped_by = data_dict.get(shipped_by,"0")
    try: 
        shipped_by = data_dict['shipped_by']
        shipped_for = data_dict['shipped_for']
        shipping_cost = data_dict['shipping_cost']
        shipped_from = data_dict['shipped_from']
    except:
        shipped_by = "0"

    if shipped_by == "0":
        print("No info found")
    else:
        print('else shipped_by',shipped_by) # Printing response
        print('shipped_for',shipped_for) # Printing response
        print('shipping_cost',shipping_cost) # Printing response
        print('shipped_from',shipped_from) # Printing response



    resp.say('Your transaction is  success')
    return str(resp)
    
    





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000,debug=True)