from flask import Flask, request 
from twilio.twiml.voice_response import Dial,VoiceResponse,Pay, Say,Gather
import json
import requests as req

app = Flask(__name__)




@app.route("/english", methods=['GET', 'POST'])
def english():
    """Respond to incoming phone calls with a menu of options"""
    # Start our TwiML response
    resp = VoiceResponse()
    resp.pause(2)
    resp.say('Thank you for calling Zion Shipping phone payment system')
    resp.pause(2)
    # Start our <Gather> verb
    gather = Gather(timeout=10, num_digits=1, action='/selectoptions_lang')
    gather.say('Please press one for english ')
    gather.pause(1)
    gather.say('Por   ,,,,favor presione ,,,,dos para español',voice="Polly.Conchita", language="es-ES")
    gather.pause(1)
    gather.say('Veuillez appuyer,,,, sur trois ,,,,pour le français',voice="Polly.Celine", language="fr-FR")
    gather.pause(1)
    resp.append(gather)
    return str(resp)


@app.route('/selectoptions_lang', methods=['GET', 'POST'])
def selectoptions_lang():
    """Processes results from the <Gather> prompt in /voice"""
    # Start our TwiML response
    resp = VoiceResponse()

    # If Twilio's request to our app included already gathered digits,
    # process them
    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']
        print("choice"+choice)
         
        # <Say> a different message depending on the caller's choice

        if int(choice) == 1 : 
            resp.redirect('/start_english')
        elif int(choice) == 2 : 
            resp.redirect('/start_spanish')
        elif int(choice) == 3 :
            resp.redirect('/start_french')
        else : 
             resp.redirect('/english')
       
    # If the user didn't choose 1 or 2 (or anything), send them back to /voice
    return str(resp)





@app.route("/start_english", methods=['GET', 'POST'])
def start_english():
    """Respond to incoming phone calls with a menu of options"""
    # Start our TwiML response
    resp = VoiceResponse()

    # Start our <Gather> verb
    gather = Gather(timeout=5, num_digits=1, action='/selectoptions')
    gather.say('Please press one for shipping  , ,,,,,, ,,,,   ,,,,, ')
    gather.pause(2)
    gather.say('Please press two for Customs duties or Charge back  , ,,,,,, ,,,,   ,,,,, ')
    gather.pause(2)
    gather.say('Please press three to schedule a pickup and pay for it! ')
    gather.pause(2)
    gather.say('Please press four for connecting with a customer representative  , ,,,,,, ,,,,   ,,,,, ')
    resp.pause()
    resp.append(gather)
    resp.redirect('/voice')
    return str(resp)


@app.route('/selectoptions', methods=['GET', 'POST'])
def selectoptions():
    """Processes results from the <Gather> prompt in /voice"""
    # Start our TwiML response
    resp = VoiceResponse()

    # If Twilio's request to our app included already gathered digits,
    # process them
    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']
        print("choice"+choice)
       
        # <Say> a different message depending on the caller's choice

        if int(choice) == 1 : 
            resp.pause(3)
            print("option "+choice)
            gather = Gather(finishOnKey="#", action='/confirmshipping', timeout=5)
            gather.say('Please provide your shipping number followed by a pound sign.')
            resp.append(gather)
        elif int(choice) == 2 : 
            resp.pause(3)
            print("option "+choice)
            gather = Gather(finishOnKey="#", action='/confirmcustomcharges')
            gather.say('Please       provide        your        shipping       number      to     know      the     custom charges.  ')
            resp.append(gather)
        elif int(choice) == 3 :
            resp.pause(3) 
            print("option "+choice)
            gather = Gather(finishOnKey="#", action='/confirmpickup')
            gather.say('Please provide your account number or phone number followed by a pound sign. ')
            resp.append(gather)

        elif int(choice) == 4 : 
            print("option "+choice)
            resp.pause(3)
            gather = Gather(finishOnKey="#", action='/others')
            gather.say('Please wait while we transfer your call.  ')
            resp.append(gather)
   
        else :
            gather = Gather(finishOnKey="#", action='/voice')
            gather.pause(length=1)
            gather.say('Please select an option' ) 
            resp.append(gather)
            
    # If the user didn't choose 1 or 2 (or anything), send them back to /voice
    return str(resp)




##### - Step 1 -- Shipping ####

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
        resp.say('Thank you',voice="alice", language="en" ) 
        # <Say> a different message depending on the caller's choice
        if len(choice) >= 5 : 
            resp.say('Please wait while we fetch the results',voice="alice", language="en" ) 
            resp.pause(length=3)
            resp.redirect('/getshippingdetails?id='+choice)
    else :
        gather = Gather(finishOnKey="#", action='/confirmshipping', timeout=5)
        gather.say('Please provide your shipping number followed by a pound sign.',voice="alice",language="en")
        resp.pause(3)
        resp.append(gather)
            
    # If the user didn't choose 1 or 2 (or anything), send them back to /voice
    
    return str(resp)


##### - Step 1 - Custom Charges  ####

@app.route('/confirmcustomcharges', methods=['GET', 'POST'])
def confirmcustomcharges():
    """Processes results from the <Gather> prompt in /voice"""
    # Start our TwiML response
    resp = VoiceResponse()

    # If Twilio's request to our app included already gathered digits,
    # process them
    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']
        print("choice"+choice)
        resp.say('Thank you',voice="alice", language="en" ) 
        # <Say> a different message depending on the caller's choice
        if len(choice) >= 5 : 
            resp.say('Please wait while we fetch the results',voice="alice", language="en" ) 
            resp.pause(length=1)
            resp.redirect('/getcustomdetails?id='+choice)
        else :
            gather = Gather(finishOnKey="#", action='/confirmcustomcharges', timeout=5)
            gather.say('Please provide your shipping number followed by a pound sign.',voice="alice",language="en")
            resp.pause(3)
            resp.append(gather)
            
    # If the user didn't choose 1 or 2 (or anything), send them back to /voice
    
    return str(resp)



##### - Step 1 - Others  ####

@app.route('/others', methods=['GET', 'POST'])
def others():
    """Processes results from the <Gather> prompt in /voice"""
    # Start our TwiML response
    resp = VoiceResponse()
    dial = Dial()
    dial.number('415-123-4567', send_digits='1000')
    resp.append(dial)
    resp.hangup()
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
        resp.say(msg3,voice="alice", language="en")
        resp.redirect('/confirmshipping')


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
        resp.say(msg,voice="alice", language="en")
        resp.say(msg1,voice="alice", language="en")
        shipmentamountunit = shipmentamount.split()
        shipmentamountunit[0]
        url = '/payment?shippingnumber=' + shippingid + '&pay=' + shipmentamountunit[0]
        gather = Gather(num_digits=1, action=url)
        gather.say(msg3,voice="alice", language="en" ) 
        resp.append(gather)


    return str(resp)



@app.route('/getcustomdetails', methods=['GET', 'POST'])
def getcustomdetails():
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
        resp.say(msg3,voice="alice", language="en")
        resp.redirect('/confirmshipping')


    else:
        print('else shipped_by',shipped_by) # Printing response
        print('shipped_for',shipped_for) # Printing response
        print('shipping_cost',shipping_cost) # Printing response
        print('shipped_from',shipped_from) # Printing response
        shippername = shipped_by
        deliverto = shipped_for
        shipmentamount  = shipping_cost
        msg = 'This shipment is sent by' + shippername +' and will deliver to ' + deliverto
        msg1 = 'There is a total balance of ' + shipmentamount + ', for custom charges would you like to process to your payment now '
        msg3 = 'Please press one to accept or two to cancel'
        resp.say(msg,voice="alice", language="en")
        resp.say(msg1,voice="alice", language="en")
        shipmentamountunit = shipmentamount.split()
        shipmentamountunit[0]
        url = '/payment?shippingnumber=' + shippingid + '&pay=' + shipmentamountunit[0]
        gather = Gather(num_digits=1, action=url)
        gather.say(msg3,voice="alice", language="en" ) 
        resp.append(gather)

    return str(resp)


##### - Step 3 - Pickup  ####

@app.route('/confirmpickup', methods=['GET', 'POST'])
def confirmpickup():
    """Processes results from the <Gather> prompt in /voice"""
    # Start our TwiML response
    resp = VoiceResponse()

    # If Twilio's request to our app included already gathered digits,
    # process them
    if 'Digits' in request.values:
        # Get which digit the caller chose
        invoiceid  = request.values['Digits']
        print("invoiceid"+invoiceid)
        # <Say> a different message depending on the caller's choice
        if len(invoiceid) >= 5 : 
            resp.say('Please wait while we fetch the results') 
            resp.pause(length=1)
            resp.redirect('/getpickupdetails?shippingid='+invoiceid)
        else :
            gather = Gather(finishOnKey="#", action='/confirmpickup', timeout=5)
            gather.say('Please provide your account number or phone number followed by a pound sign.')
            resp.pause(3)
            resp.append(gather)
            
    # If the user didn't choose 1 or 2 (or anything), send them back to /voice
    
    return str(resp)

  

@app.route('/getpickupdetails', methods=['GET', 'POST'])
def getpickupdetails():
    resp = VoiceResponse()
    shippingid = request.args['shippingid']
    print(shippingid)
    # url = 'http://dev.zionshipping.com/shipping_details/' + shippingid 
    # print(url)
    # shipping_response = req.get(url)
    # data_dict = shipping_response.json()
    # print(data_dict)
    # shipped_by = data_dict.get(shipped_by,"0")

    shippingid = "12"
    shipping_address = '3725 Lake Worth Rd, Palm Springs, FL 33461, United'

    # try: 
    #     shipped_by = data_dict['shipped_by']
    #     shipped_for = data_dict['shipped_for']
    #     shipping_cost = data_dict['shipping_cost']
    #     shipped_from = data_dict['shipped_from']
    # except:
    #     shipped_by = "0"

    if shippingid == "0":
        print("No info found")
        msg1 = 'Your invoice number or phone number is not found ,please try again'
        resp.say(msg1,voice="alice", language="en")
        resp.redirect('/confirmpickup')

    else:
        print('shippingid ',shippingid) # Printing response
        print('shipping_address',shipping_address) # Printing response
       
        msg1 = 'I see your pickup address is ' + shipping_address +' ,'
        msg2 = 'would you like to schedule the pickup using this address?' 
        msg3 =  'Please press one, to confirm or two,'
        msg4 = ' '
        msg5 = 'if you need to schedule the pickup in a different address.'
        url = '/confirmtiming?shippingid='+ shippingid 
        gather = Gather(num_digits=1, action=url,timeout=20)
        gather.say(msg1) 
        gather.pause(1)
        gather.say(msg2) 
        gather.pause(1)
        gather.say(msg3) 
        gather.say(msg4) 
        gather.pause(1)
        gather.say(msg5) 
        resp.append(gather)


    return str(resp)



@app.route('/confirmtiming', methods=['GET', 'POST'])
def confirmtiming():
    resp = VoiceResponse()
    shippingid = request.args['shippingid'] or 0
     
    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice  = request.values['Digits']
        # <Say> a different message depending on the caller's choice
        if int(choice) == 1 : 
            url = "/confirmdate?shippingid="+shippingid
            gather = Gather(numDigits='8',finishOnKey="#",action=url, timeout=10)
            gather.say('Please provide your pickup date follow by the pound key.')
            gather.say('Please put 2 digit for the month, 2 digit for the day and 4 digit for the year. As an example: For (May twelve twenty twenty two), please type  (zero, five,,, one, two,,, two, zero, two, two)')
            gather.pause(3)
            resp.append(gather)

        elif int(choice) == 2 :
            resp.say('Please wait while we transfer your call to an agent' )
            resp.redirect('/others')
        else :
            gather = Gather(action='/confirmtiming', timeout=5)
            gather.say('Please provide your choice.')
            resp.pause(3)
            resp.append(gather)
    return str(resp)


@app.route('/confirmdate', methods=['GET', 'POST'])
def confirmdate():
    resp = VoiceResponse()
    shippingid = request.args['shippingid'] or 0
    if 'Digits' in request.values:
        # Get which digit the caller chose
        pickupdate = request.values['Digits']
        # <Say> a different message depending on the caller's choice
      
        if len(pickupdate) > 5 : 
            url = '/confirmpickuptime?pickupdate='+pickupdate+'&shippingid='+shippingid
            gather = Gather(numDigits='1',action=url, timeout=10)
            gather.say('Do you want your pickup to be schedule in the morning from Nine AM to twelve PM or in the afternoon from twelve PM to five PM?')
            gather.say('Please, press one for morning pickup OR two for afternon pickup.')      
            resp.append(gather)
        else :
            gather = Gather(action='/confirmtiming', timeout=20)
            gather.say('Please provide your pickup date properly')
            resp.pause(3)
            resp.append(gather)
    return str(resp)


@app.route('/confirmpickuptime', methods=['GET', 'POST'])
def confirmpickuptime():
    resp = VoiceResponse()
    shippingid = request.args['shippingid']
    pickupdate = request.args['pickupdate']

    if 'Digits' in request.values:
        # Get which digit the caller chose
        pickuptime = request.values['Digits']
        # <Say> a different message depending on the caller's choice
        
        if int(pickuptime) == 1 or int(pickuptime) == 2  : 
            url = '/confirmpickuppayment?shippingid=' + shippingid+'&pickupdate='+pickupdate +'&pickuptime='+pickuptime
            gather = Gather(numDigits='1',action=url, timeout=5)
            gather.say('Theres a  $20 fee for the pickup would you like to pay now?')
            gather.say('Please press one to confirm and press two to cancel.')      
            resp.append(gather)
        else :
            gather = Gather(action='/confirmtiming', timeout=5)
            gather.say('Please provide your pickup date properly')
            resp.pause(3)
            resp.append(gather)
    return str(resp)


@app.route('/confirmpickuppayment', methods=['GET', 'POST'])
def confirmpickuppayment():
    resp = VoiceResponse()
    shippingid = request.args['shippingid']
    shipmentamount = 20.00
    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']
        # <Say> a different message depending on the caller's choice
        if int(choice) == 1   : 
            url = '/payment?shippingid='+str(shippingid)+'&pay='+str(shipmentamount)
            print(url)
            resp.say('Please wait while we connect to our payment system')
            
            resp.redirect(url)
        else :
            resp.say("Thank you")
            resp.pause(3)
            resp.hangup()
    return str(resp)




@app.route('/payment', methods=['GET', 'POST'])
def payment():
    resp = VoiceResponse()
    print('paymentmethod')
    shippingid = request.args['shippingid'] or 0
    amount = request.args['pay'] or 0    
    print('shippingid',shippingid)
    print('amount',amount)
    resp.say('Twilio Pay')
    resp.pause(1)
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

        url = 'http://dev.zionshipping.com/paymentsuccess/' + shippingid 
        print(url)
        shipping_response = req.get(url)
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