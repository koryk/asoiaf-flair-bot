import praw
import re
import string
import urllib
import time
import ConfigParser
import shutil
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
approved_flair = []
config = ConfigParser.ConfigParser()
config.read("./config.ini")
subreddit = config.get("user","subreddit") 
creds = {'user': config.get("user","username"), 'passwd': config.get("user","passwd")}
approved_flair_file = config.get("flair","approved")
user_agent = "asoiaf flair bot"

def pruneFlair(flair):
    flair = flair.lower()
    flair = re.sub(r"\.|,|\!|\?|\'|\"","",flair)
    flair = re.sub(r"\s+"," ",flair)
    return flair

def isApprovedFlair(flair):
    global approved_flair
    if (not approved_flair):
        approved_flair = loadApprovedFlair()
    return pruneFlair(flair) in approved_flair

def loadApprovedFlair():
    global approved_flair
    global approved_flair_file
    if (not approved_flair):
        print "loading approved flair"
        #load flair from file
        if (not approved_flair_file):
            approved_flair_file = './approved_flair.txt'
        with open(approved_flair_file) as old:
            for line in old:
                line = line.replace("\n","")
                approved_flair.append(line)
    return approved_flair

def addApprovedFlair(flair):
    global approved_flair
    global approved_flair_file
    approved_flair = loadApprovedFlair()
    flair = pruneFlair(flair)
    if (flair in approved_flair):
        return
    approved_flair.append(flair)
    temp_flair_file = approved_flair_file + '.tmp'
    with open(approved_flair_file) as old:
        with open(temp_flair_file, 'w') as new:
            for line in old:
                new.write(line)
            new.write(flair+"\n")
    shutil.move(temp_flair_file, approved_flair_file)

def isModerator(user):
    global moderators
    if (not moderators):
        moderators = r.get_moderators(subreddit)
    return user in moderators

def crawlMessages():
    for msg in r.get_unread(limit=None):
        if (isModerator(msg.author) and msg.subject != 'Flair needs approval'):
            if (handeModMessage(msg)):
                addApprovedFlair(msg.body)
                r.send_message(msg.author, "Moderator Override Success " + msg.subject, flair_response.moderatorSuccess, None)
            else:
                r.send_message(msg.author, "Moderator Override Failure " + msg.subject ,flair_response.moderatorFailure, None)
        else:
            handleMessage(msg)
        msg.mark_as_read()

def handeModMessage(msg):
    print "handling mod message"
    title = msg.subject.split()
    if (len(title) < 2):
        #changing personal flair?
        return handleMessage(msg)
    user = title[0]
    shield = title[1].lower()
    flair = flairs.get(shield, None)
    title = msg.body
    if (shield.lower() == 'clear'):
        clearFlair(user)
    elif (flair is None):
        return False
    else:
        if changeFlair(flair, title, user):
            r.send_message(user, "Shield and Title Changed Successfully!", flair_response.successFlairReply  , None)
            return True


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
        pprint("Flair is too long %s - %s -%s" % (user, title, shield))
        r.send_message(msg.author, "Flair and Title Not Updated -- Flair is too long", flair_response.tooLongFlairReply , None)
    elif (isCaps(title)):
        pprint("Flair is caps %s - %s - %s" % (user, title, shield))
        r.send_message(msg.author, "Flair and Title Not Updated -- Rule Violation -- All Caps", flair_response.allCapsFlairReply  , None)
    elif ((hasBadWord(title, spoiler) or hasBadWord(title,naughty)) and not isApprovedFlair(title)):
        r.send_message(msg.author, "Flair and Title Waiting for approval -- Possible Spoiler", flair_response.spoilerFlairReply , None)
        #send mod message
        r.send_message('/r/'+subreddit, "Flair needs approval", flair_response.approvalFlairReply.format(user.name, title, "http://www.reddit.com/message/compose?to="+urllib.quote(creds['user'])+"&subject="+urllib.quote(user.name+" "+msg.subject)+"&message="+urllib.quote(title)))
        pprint("Flair needs approval %s - %s - %s" % (user, title, shield))
    else:
        if changeFlair(flair, title, user.name):
            r.send_message(msg.author, "Shield and Title Changed Successfully!", flair_response.successFlairReply, None)

def clearFlair(user):
    changeFlair('','',user)

def changeFlair(flair, title, user):
    current_flair =  r.get_flair(subreddit, user)
    if (isinstance(flair, dict) and current_flair['flair_css_class'] == flair['css_class'] and current_flair['flair_text'] == title):
        print "Flair already set for " + user + " with the title " + title
        return False
    elif flair == '':
        print "Clearing flair"
        flair = {'css_class':''}
    else:
        print "Setting flair " + flair['css_class'] +  " for " + user + " with the title " + title
    r.set_flair(subreddit,user,title,flair['css_class'])
    return pformat("Changed flair %s - %s - %s" % (user, title, flair['css_class']))

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
