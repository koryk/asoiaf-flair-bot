import praw
import re
import string
import urllib
import time
import ConfigParser
from pprint import pprint
from pprint import pformat
import flair_response

try:
    import badwords
    naughty = badwords.naughty
    spoiler = badwords.spoiler
except ImportError:
    naughty = []
    spoiler = []


try:
    import flairs
    flairs = flairs.flairs
except ImportError:
    flairs = []

moderators = []
subreddit = 'testasoiaf'
config = ConfigParser.ConfigParser()
config.read("./config.ini")
subreddit = config.get("user","subreddit") 
creds = {'user': config.get("user","username"), 'passwd': config.get("user","passwd")}
user_agent = "asoiaf post bot"

def isModerator(user):
    global moderators
    if (not moderators):
        moderators = r.get_moderators(subreddit)
    return user in moderators

def crawlMessages():
    for msg in r.get_unread(limit=None):
        msg.mark_as_read()
        if (isModerator(msg.author)):
            if (handeModMessage(msg)):
                r.send_message(msg.author, "Moderator Override Success " + msg.subject, flair_response.moderatorSuccess, None)
            else:
                r.send_message(msg.author, "Moderator Override Failure " + msg.subject ,flair_response.moderatorFailure, None)
        else:
            handleMessage(msg)

def handeModMessage(msg):
    print "handling mod message"
    title = msg.subject.split()
    if (len(title) < 2):
        #changing personal flair?
        return handleMessage(msg)
    user = title[0]
    shield = title[1]
    flair = flairs.get(shield, None)
    title = msg.body
    if (shield.lower() == 'clear'):
        clearFlair(user)
    elif (flair is None):
        return False
    else:
        r.send_message(user, "Shield and Title Changed Successfully!", flair_response.successFlairReply  , None)
        return changeFlair(flair, title, user)

def handleMessage(msg):
    shield = msg.subject.lower()
    title = msg.body
    user = msg.author
    flair = flairs.get(shield, None)
    if (shield.lower() == "clear"):
        clearFlair(user)
        pprint("Clear the flair for %s" % (user))
    elif (flair is None):
        pprint("Flair isn't recognized %s - %s - %s" % (user, title, shield))
        r.send_message(msg.author, "Flair and Title Not Updated -- Unrecognized Shield Name", flair_response.noShieldFlairReply , None)
    elif (len(title) > 40):
        message = pformat("Flair is too long %s - %s -%s" % (user, title, shield))
        r.send_message(msg.author, "Flair and Title Not Updated -- Flair is too long", flair_response.tooLongFlairReply , None)
    elif (hasBadWord(title,naughty)):
        pprint("Flair is naughty %s - %s - %s" % (user, title, shield))
        r.send_message(msg.author, "Flair and Title Not Updated -- Rule Violation", flair_response.naughtyFlairReply , None)
    elif (isCaps(title)):
        pprint("Flair is caps %s - %s - %s" % (user, title, shield))
        r.send_message(msg.author, "Flair and Title Not Updated -- Rule Violation", flair_response.allCapsFlairReply  , None)
    elif (hasBadWord(title, spoiler)):
        #send mod message
        r.send_message(msg.author, "Flair and Title Waiting for approval -- Possible Spoiler", flair_response.spoilerFlairReply , None)
        r.send_message('dipotassium', "Flair needs approval", flair_response.approvalFlairReply.format(user, title, "http://www.reddit.com/message/compose?to="+urllib.quote(creds['user'])+"&subject="+urllib.quote(user.name+" "+msg.subject)+"&message="+urllib.quote(title))))
        pprint("Flair is spoiler %s - %s - %s" % (user, title, shield))
    else:
        r.send_message(msg.author, "Shield and Title Changed Successfully!", flair_response.successFlairReply  , None)
        print changeFlair(flair, title, user)

def clearFlair(user):
    changeFlair('','',user)

def changeFlair(flair, title, user):
    r.set_flair(subreddit,user,title,flair)
    return pformat("Changed flair %s - %s - %s" % (user, title, flair))

def isCaps(phrase):
    return phrase == phrase.upper() and phrase != phrase.lower()

def hasBadWord(phrase, wordList):
    strip_unicode = re.compile("[-. !@#%&=,/'\";:~`\$\^\*\(\)\+\[\]\{\}\|\?\<\>]")
    transPhrase = strip_unicode.sub('', phrase).lower()

    for badWord in wordList:
        transBadWord = strip_unicode.sub('', badWord).lower()

        if -1 != string.find(transPhrase,transBadWord):
            # Badword Found 
            pprint("Found the word \"%s\" in \"%s\"" % (badWord, phrase))
            return True

    return False

#connect to reddit
r = praw.Reddit(user_agent=user_agent)
r.login(creds['user'],creds['passwd'])
print r.is_logged_in()
reddit = r.get_subreddit(subreddit)
crawlMessages()
