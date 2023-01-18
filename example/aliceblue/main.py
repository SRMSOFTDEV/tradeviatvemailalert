# Importing libraries
import imaplib, email, html2text, re
from pprint import pprint
from email.policy import default
from itertools import chain
from datetime import datetime, timedelta
from pytz import timezone
from dateutil import parser as date_parser
from pya3 import *

# User Definded .py files
import document_details

# Email Credentials
user = document_details.email_id
password = document_details.email_password

# Initializations
imap_url = 'imap.gmail.com'
receiver_email = 'noreply@tradingview.com'
alert_prefix = '#TVALERT#'
alert_postfix = '#TVALERT#'
my_timezone = 'Asia/Kolkata'
since_date = datetime.now(timezone(my_timezone)).date().strftime("%d-%b-%Y") # Convert to DD-MMM-YYYY format


# Connect to Broker
alice = Aliceblue(user_id=document_details.username,api_key=document_details.api_key)
print("The SESSION ID : ",alice.get_session_id()) # Get Session ID
# Download NSE Mastercontract
alice.get_contract_master("NSE")
# Mention Quantity
quantity = 1

############################################ user_defined_functions STARTS ############################################
def write_log(text):
    f = open("tradelogs.log", 'a')           # 'a' will append to an existing file if it exists
    f.write("{}\n".format(str(datetime .now())+" | "+text))  # write the text to the logfile and move to next

def filter_alert_from_msg_body(body_str): 
    global alert_prefix, alert_postfix
    result = re.search(alert_prefix+'(.*)'+alert_postfix, body_str)
    res = result.group(1)
    return res

def email2Text(rfc822mail):
        # parse the message
        msg_data = email.message_from_bytes(rfc822mail, policy=default)
        
        mail_value = {}

        # Get From, Date, Subject
        mail_value["from"] = header_decode(msg_data.get('From'))
        mail_value["date"] = header_decode(msg_data.get('Date'))
        mail_value["subject"] = header_decode(msg_data.get('Subject'))
        
        #print( mail_value["date"] )
        #print( mail_value["from"] )
        #print( mail_value["subject"] )

        # Get Body
        #print("--- body ---")
        mail_value["body"] = ""
        if msg_data.is_multipart():
            for part in msg_data.walk():
                #print("--- part ---")
                ddd = msg2bodyText(part)
                if ddd is not None:
                    mail_value["body"] = mail_value["body"] + ddd
        else:
            #print("--- single ---")
            ddd = msg2bodyText(msg_data)
            mail_value["body"] = ddd

        return mail_value

#
# get body text from a message (EmailMessage instance)
#
def msg2bodyText(msg):
    ct = msg.get_content_type()
    cc = msg.get_content_charset() # charset in Content-Type header
    cte = msg.get("Content-Transfer-Encoding")
    print("part: " + str(ct) + " " + str(cc) + " : " + str(cte))

    # skip non-text part/msg
    if msg.get_content_maintype() != "text":
        return None

    # get text
    ddd = msg.get_content()

    # html to text
    if msg.get_content_subtype() == "html":
        try:
            ddd = html2text.html2text(ddd)
        except:
            print("error in html2text")

    return ddd


def header_decode(header):
    hdr = ""
    for text, encoding in email.header.decode_header(header):
        if isinstance(text, bytes):
            text = text.decode(encoding or "us-ascii")
        hdr += text
    return hdr

def search_string(criteria):
    c = list(map(lambda t: (t[0], '"'+str(t[1])+'"'), criteria.items()))
    return '(%s)' % ' '.join(chain(*c))
    # Produce search string in IMAP format:
    #   e.g. (FROM "me@gmail.com" SUBJECT "abcde" BODY "123456789" UID 9999:*)

def num_byte_str_to_numlist(numbystr):
    return [int(s) for s in numbystr.split()]

def custom_order(i,q,b_or_s = "BUY"):
    b_or_s = b_or_s.upper()
    od = alice.place_order(transaction_type = TransactionType.Sell if b_or_s == 'SELL' else TransactionType.Buy,
                     instrument = i,
                     quantity = q,
                     order_type = OrderType.Market,
                     product_type = ProductType.Intraday,
                     price = 0.0,
                     trigger_price = None,
                     stop_loss = None,
                     square_off = None,
                     trailing_sl = None,
                     is_amo = False,
                     order_tag='order1')
    return od

############################################ user_defined_functions ENDS ############################################

# Mail Filtering Criterias
criteria = {
    'FROM': receiver_email,
    'SINCE': since_date,
    # 'SUBJECT': strategy_tag,
}

loop = 1
loop_start_time = datetime.now(timezone(my_timezone))
# loop_start_time = datetime.now(timezone(my_timezone)) - timedelta(minutes=10)
print("LOOP START TIME: ", loop_start_time)
try:
    while True:
        print(f"********LOOP-{loop}********")
        #LOGIN GMAIL
        con = imaplib.IMAP4_SSL(imap_url) # this is done to make SSL connection with GMAIL
        con.login(user, password) # logging the user in
        con.select('INBOX') # calling function to check for email under this label

        # Obtain unique ids'(UID) of the UNSEEN filtered mails 
        result, data = con.uid('search',('UNSEEN'), search_string(criteria))
        print("Mail Filter Status : ",result)
        # Convert the byte string inside the list to interger list of ids
        uids = num_byte_str_to_numlist(data[0])
        uids.sort() # It is not necessary, but written just to ensure the list items are in ascending order
        
        if len(uids) > 0:
            print("UID List for New EMAIL ALERTS:", uids)
            for uid in uids:
                # Fetch the details of a perticular UID
                res, dat = con.uid('FETCH', str(uid), '(RFC822)')
                # print(dat)
                # Convert byte data to text data
                one_msg_det = email2Text(dat[0][1])
                # retive msg datetime from one msg details
                if 'date' in one_msg_det:
                    msg_dt = date_parser.parse(one_msg_det['date']).astimezone(timezone(my_timezone))

                    # Only Considered the ALERTS that are recived after the loop_start_time
                    if msg_dt >= loop_start_time:
                        # retive msg body from one msg details
                        if 'body' in one_msg_det:
                            body_str = one_msg_det['body']
                            alert_msg = filter_alert_from_msg_body(body_str)
                            # print(alert_msg)
                            # Convert String to dict
                            try:
                                alert_dict = eval(alert_msg)
                            except:
                                alert_dict = {}
                            print(alert_dict)
                            if len(alert_dict) > 0:
                                write_log(str(alert_dict))
                                print(f"-------Use ORDER-API of your preferred Broker to FIRE A {alert_dict['action'].upper()} ORDER FOR {alert_dict['ticker']}-------")
                                """API BUY/SELL Code Start"""
                                ins = alice.get_instrument_by_symbol(symbol=alert_dict['ticker'],exchange=alert_dict['exchange'])
                                print(ins)
                                oder_var = custom_order(i=ins,q=quantity,b_or_s=alert_dict['action'])
                                print(oder_var)
                                """API BUY/SELL Code End"""
                    else:
                        print(f"Ignoring UNSEEN EMAIL(before loop starting) with UID : {uid}")
        else:
            print("Wating for new EMAIL ALERT(s).")

        # close the mailbox
        con.close()
        #logout GMAIL
        con.logout()
        
        loop += 1 #Increment the loop counter
except KeyboardInterrupt:
    print("The program is terminated with CTRL+C")
