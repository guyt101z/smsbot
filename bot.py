from jabberbot import JabberBot, botcmd
import urllib2
from threading import Timer

class SystemInfoJabberBot(JabberBot):

    def __init__(self, username, password, smsUser, smsPass, waitingTime):
        JabberBot.__init__(self, username, password)
        self.blocked = []
        self.smsUser = smsUser
        self.smsPass = smsPass
        self.waitingTime = waitingTime

    def getAuthor(self, mess):
        """
        Returns the author of a xmpp message
        """
        author = self.get_sender_username(mess).encode('utf8', 'replace')
        return author

    def sendSMS(self, smsUser, smsPass, smsMsg):
        """
        Sends a sms to the specified free mobile user
        @param smsUser: username for the free mobile account
        @param smsPass: password for the free mobile sms notification option
        @param smsMsg: message to send
        @return Error description if the message could not be sent, "Messageg sent :)" otherwise
        """
        try:
            urllib2.urlopen("https://smsapi.free-mobile.fr/sendmsg?user=" + smsUser + "&pass=" + smsPass + "&msg=" + smsMsg)
        except Exception,e:
            errorCode = e.code
            if errorCode == 400:
                return "This error should not have happened. This bot was launched with an invalid set of parameters."
            if errorCode == 402:
                return "Too much sms have been sent in a short period of time. Please try again later."
            if errorCode == 403:
                return "Service is not available, sorry."
            if errorCode == 500:
                return "Error on Free mobile side. Please try again later."

        return "Message sent :)"


    def unblock(self, author):
        """
        Remove a user from the blocked list
        @param author: user to remove from the bloked list
        """
        self.blocked.remove(author)

    def block(self, author, time):
        """
        Add a user to the blocked list for a limited amount of time
        @param author: user to add to the blocked list
        @param time: time before the user is removed from the blocked list (in seconds)
        """
        self.blocked.append(author)
        Timer(time,self.unblock,[author]).start()



    def unknown_command(self, mess, cmd, args):
        """
        Default handler of all messages.
        Sends the message by SMS if the user is in the blocked list, do not do anything otherwise
        @return: Validation message if the SMS has been sent, error message otherwise
        """

        author = self.getAuthor(mess)
        if author in self.blocked:
            nbMinutes = round(self.waitingTime / 60)
            return "Please wait at least " + nbMinutes + " minutes between each message."

        smsMsg = author + ": " + mess.getBody().encode('utf8', 'replace')
        self.block(author, self.waitingTime)
        return self.sendSMS(self.smsUser, self.smsPass, smsMsg)

 

######
# The following parameters should be modified before launching that bot
######
username = "bot@foo.bar" # Bot XMPP account
password = "toto" # Bot XMPP password
smsUser = "xxxxxx" # Free mobile account number
smsPass = "tata" # Free mobile account password
waitingTime = 300 # Time to wait between each text from a same person (in seconds)

bot = SystemInfoJabberBot(username,password, smsUser, smsPass, waitingTime)
bot.serve_forever()
