# TRADE VIA TRADINGVIEW EMAIL ALERT
Python Code to Trade Via TradingView Email ALERTS

STEPS TO GO THROUGH:

Make sure you have a GMAIL account with APP PASSWORD and have activated IMAP service. 

Must have a TRADING VIEW account with same GMAIL ID.

Prepare a JSON type ALERT string with prefix and pstfox string.

e.g. <prefix_string>{'strategy':'<your_strategy_name>','ticker':'{{ticker}}','price':{{close}},'action':'{{strategy.order.action}}'}<postfix_string>

According to main.py the ALERT message string can be 

You can modify the above format according to your need or can directly mention in PINE Script. 
