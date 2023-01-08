# TRADE VIA TRADINGVIEW EMAIL ALERT
Python Code to Trade Via TradingView Email ALERTS

Please follow the youtube video : 

STEPS TO GO THROUGH:

Make sure you have a GMAIL account with APP PASSWORD and have activated IMAP service. 

APP PASSWORD  DETAILS INFO: https://support.google.com/accounts/answer/185833?hl=en

IMAP DETAILS INFO: https://support.google.com/mail/answer/7126229?hl=en#zippy=

Replace your EMAIL and APP-PASSWORD in document_details.py file.

Must have a TRADING VIEW account with same GMAIL ID.

Prepare a JSON type ALERT string with prefix and pstfox string.

e.g. <prefix_string>{'strategy':'<your_strategy_name>','ticker':'{{ticker}}','price':{{close}},'action':'{{strategy.order.action}}'}<postfix_string>

According to main.py the ALERT message string should be,

#TVALERT#{'strategy':'Supertrend_10_3','ticker':'{{ticker}}','price':{{close}},'action':'{{strategy.order.action}}'}#TVALERT#

Create an alert with any strategy and paste the prepared ALERT string in the message section.

You can modify the above format according to your need or can directly mention in PINE Script alert method. 

Make sure you have python installed or else you can make a quick go with Googlecolab, https://colab.research.google.com/

Install the requirenets from requirements.txt file.

Run the main.py file. 

Once done Terminate the LOOP with CTRL+C.
