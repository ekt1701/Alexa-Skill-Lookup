from __future__ import print_function
import urllib2
import urllib
import csv
import re

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "getDateIntent":
        return getDate(intent, session)
    elif intent_name == "getInfoIntent":
        return getInfo(intent, session)
    elif intent_name == "getSkillNameIntent":
        return getSkillName(intent, session)
    elif intent_name == "getAuthorIntent":
        return getAuthor(intent, session)
    elif intent_name == "getDescriptionIntent":
        return getDescription(intent, session)
    elif intent_name == "getInvocationIntent":
        return getInvocation(intent, session)
    elif intent_name == "getWhenUpdatedIntent":
        return getWhenUpdated(intent, session)
    elif intent_name == "getNumberSkillsIntent":
        return getNumberSkills(intent, session)
    elif intent_name == "AMAZON.YesIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.NoIntent":
        return handle_session_end_request()
    elif intent_name == "AMAZON.HelpIntent":
        return get_help()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        return get_welcome_response()


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    session_attributes = {}
    card_title = "ASK Intro"

    speech_output = "Welcome to ALexa Skills Lookup, what do you want to look up?"
    reprompt_text = "You can say Find Skill named cave, What skill did James write, Tell me about space, Get the skills released yesterday, How many skills are there, When was the list updated, Describe the skill mind maze, How do I launch cave"
    should_end_session = False
    return build_response_without_card(session_attributes, build_speechlet_response_without_card(
        card_title, speech_output, reprompt_text, should_end_session))

def get_help():
    session_attributes = {}
    card_title = "Help"
    speech_output = "You can say Find Skill named cave, What skill did James write, Tell me about space, Get the skills released yesterday, How many skills are there, When was the list updated, Describe the skill mind maze, How do I launch cave"
    reprompt_text = "What do you want to look up?"
    should_end_session = False
    return build_response_without_card(session_attributes, build_speechlet_response_without_card(
        card_title, speech_output, reprompt_text, should_end_session))


def getDate(intent, session):
    session_attributes = {}
    card_title = "When skills updated"
    datelookup = intent['slots']['Date']['value'].lower()
    mydate = str(datelookup)
    url = 'https://github.com/dale3h/alexa-skills-list/raw/master/skills.csv'
    response = urllib2.urlopen(url)
    cr = csv.reader(response)
    titles = []
    for row in cr:
        if mydate in row[8]:
            titles.append(row[0])
    newskills = '. '.join(titles)

    if newskills == "":
        text = "There were no skills released on " + mydate
    else:
        text = "Here are the skills released on " + mydate + " " + str(newskills)

    speech_output = text + ". What else do you want to lookup?"
    reprompt_text = "Can you repeat your request"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def getWhenUpdated(intent, session):
    session_attributes = {}
    card_title = "when updated"
    url = "https://github.com/dale3h/alexa-skills-list/blob/master/skills.csv"
    file = urllib.urlopen(url)
    text = file.read()

    datelocation = 'datetime="(.+?)Z'
    datepattern = re.compile(datelocation)
    date = re.findall(datepattern,text)
    temp = str(date)
    reldate = temp.split("T")

    speech_output = "The csv file was updated on " + str(reldate[0]) + ". What else do you want to lookup?"
    reprompt_text = "Can you repeat your request"
    should_end_session = False
    return build_response_without_card(session_attributes, build_speechlet_response_without_card(
        card_title, speech_output, reprompt_text, should_end_session))

def getNumberSkills(intent, session):
    session_attributes = {}
    card_title = "How many skills"
    url = 'https://github.com/dale3h/alexa-skills-list/raw/master/skills.csv'
    response = urllib2.urlopen(url)
    cr = csv.reader(response)
    data = []
    count = 0
    for row in cr:
        count = int(count) + 1
    count = count - 1
    number = str(count)
    text = "Currently, there are " + str(number) + " skills"
    speech_output = text + ". What else do you want to lookup?"
    reprompt_text = "Can you repeat your request"
    should_end_session = False
    return build_response_without_card(session_attributes, build_speechlet_response_without_card(
        card_title, speech_output, reprompt_text, should_end_session))

def getInfo(intent, session):
    session_attributes = {}
    card_title = "get info"
    namelookup = intent['slots']['Info']['value'].lower()
    name = str(namelookup)
    url = 'https://github.com/dale3h/alexa-skills-list/raw/master/skills.csv'
    response = urllib2.urlopen(url)
    cr = csv.reader(response)
    data = []
    infotitle = ""
    for row in cr:
        infotitle = row[0]
        if name in infotitle.lower():
            temp = row[8]
            reldate = temp.split(" ")

            info = row[0] + " written by " + row[2] + ". The description is " + row[3] + ". It has rating of " + row[4] + ".  The number of reviews is " + row[5] + ". It was released on " + reldate[0] + ". Say " + row[9] + " to launch the skill."
            data.append(info)
    allinfo = '. '.join(data)
    if allinfo == "":
        text = "I'm sorry could not find that information"
    else:
        text = str(allinfo)
        replace = {
                "\\n" : " "
                }
        text = multiple_replace(replace, text)
    speech_output = str(text) + ". What else do you want to lookup?"
    reprompt_text = "Can you repeat your request"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def getSkillName(intent, session):
    session_attributes = {}
    card_title = "get info"
    namelookup = intent['slots']['Name']['value'].lower()
    name = str(namelookup)
    url = 'https://github.com/dale3h/alexa-skills-list/raw/master/skills.csv'
    response = urllib2.urlopen(url)
    cr = csv.reader(response)
    data = []
    skillname = ""
    for row in cr:
        skillname = row[0]
        if name in skillname.lower():
            data.append(row[0])
    nameskills = '. '.join(data)
    if nameskills == "":
        text = "There are no skills with the name " + name
    else:
        text = "Here are the skills with the name " + name + ". " + nameskills
    speech_output = str(text) + ". What else do you want to lookup?"
    reprompt_text = "Can you repeat your request"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def getAuthor(intent, session):
    session_attributes = {}
    card_title = "get info"
    namelookup = intent['slots']['Author']['value'].lower()
    author = str(namelookup)
    url = 'https://github.com/dale3h/alexa-skills-list/raw/master/skills.csv'
    response = urllib2.urlopen(url)
    cr = csv.reader(response)
    data = []
    authorname = ""
    for row in cr:
        authorname = row[2]
        if author in authorname.lower():
            skillsbyauthor = row[2] + ":" + row[0]
            data.append(skillsbyauthor)
    authorskills = '. '.join(data)
    if authorskills == "":
        text = "There were no skills by " + author
    else:
        text = "Here are the skills released by " + author + " " + authorskills
    speech_output = str(text) + ". What else do you want to lookup?"
    reprompt_text = "Can you repeat your request"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def getDescription(intent, session):
    session_attributes = {}
    card_title = "get info"
    namelookup = intent['slots']['Description']['value'].lower()
    name = str(namelookup)
    url = 'https://github.com/dale3h/alexa-skills-list/raw/master/skills.csv'
    response = urllib2.urlopen(url)
    cr = csv.reader(response)
    data = []
    infotitle = ""
    for row in cr:
        infotitle = row[0]
        if name in infotitle.lower():
            temp = row[8]
            reldate = temp.split(" ")

            info = row[0] + ". The description is " + row[3] + ". "
            data.append(info)
    allinfo = '. '.join(data)
    if allinfo == "":
        text = "I'm sorry could not find that information"
    else:
        text = allinfo
        replace = {
                "\\n" : " "
                }
        text = multiple_replace(replace, text)
    speech_output = str(text) + ". What else do you want to lookup?"
    reprompt_text = "Can you repeat your request"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def getInvocation(intent, session):
    session_attributes = {}
    card_title = "get info"
    namelookup = intent['slots']['Invocation']['value'].lower()
    name = str(namelookup)
    url = 'https://github.com/dale3h/alexa-skills-list/raw/master/skills.csv'
    response = urllib2.urlopen(url)
    cr = csv.reader(response)
    data = []
    invoke = ""
    for row in cr:
        invoke = row[9]
        if name in invoke.lower():
            saying = row[9]
            data.append(saying)
    invocation = '. '.join(data)
    if invocation == "":
        text = "I'm sorry could not find that information"
    else:
        text = "For the skill " + name + ". Say " + invocation
    speech_output = str(text) + ". What else do you want to lookup?"
    reprompt_text = "Can you repeat your request"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



def multiple_replace(dict, text):
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text)

def handle_session_end_request():
    card_title = "Session Ended"
    should_end_session = True
    speech_output = "Thank you for using Alexa Skills Lookup."
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_speechlet_response_without_card(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
       'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
def build_response_without_card(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
