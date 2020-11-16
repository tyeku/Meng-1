

import re
import random
from mic import Mic


WORDS=["Sports", "Equipment"]

def isValid(text):
    return bool(re.search(r'\bsports equipment\b',text,re.IGNORECASE))

def handle(text, mic, profile):
    message_1 = "Is it for you or someone else?"
    Option_1= ["me", "myself", "my self"]
    mic.say(message_1)
    response= mic.activeListen()

Question_1= ["What is the first thing you want to do with it?",
"Who do you want to show it to first?"]

Question_2= ["What do you want to say when you offer it?",
"How does this contribute to your relationship?"]

for word in Option_1:
    result = re.search(word, response.lower())
    result2= re.search("someone", response.lower())
    result3= re.search("somebody", response.lower())
    if result2 or result3:
        #mic.say(random.choice(Question_2))
        print random.choice(Question_2)
        break
    else:
        if result: #basically saying if true. If it wasnt result would return None
            #mic.say(random.choice(Question_1))
            print random.choice(Question_1)
            break
        else:
            if word== "me":
                continue
            else:
                if word=="myself":
                    continue
                else:
                    #mic.say(random.choice(Question_2))
                    print random.choice(Question_2)

#Testing
#if result!=None:
#    print result.group()
#else:
#    print "None"

"""
result = re.search(Option_1[0], response.lower())
if result: #basically saying if True. If it wasn't result would return None
    mic.say(random.choice(Question_1))
    break
elif:
    result= re.search(Option_1[1], response.lower())
    if result:
    mic.say(random.choice(Question_1))
    break
else:
    mic.say(random.choice(Question_2))
    print result.group()
    """
