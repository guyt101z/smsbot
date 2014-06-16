smsbot
======

XMPP / Jabber bot written in python 2 allowing contacts to send you sms on your free mobile number.

To use this bot you need a XMPP account, and a free mobile subscription.
You also need to activate the "Notifications par SMS" option in your account.

Then anybody can add the bot as a XMPP contact, and each message sent to the bot will be sent to you as a sms.

Install
=======

That bot runs using python2 and the following libraries:
 - urllib2
 - threading
 - jabberbot (available from http://thp.io/2007/python-jabberbot/)

Use
===

First, give to the following parameters the proper values:
 - username: The username of the XMPP account your bot will use
 - password: The password of the bot's XMPP account
 - smsUser: The username of your free mobile account
 - smsPass: The pass available on the "Notifications par SMS" webpage
 - waitingTime: The time (in seconds) each user should wait before sending you two sms (default is 5 minutes)

