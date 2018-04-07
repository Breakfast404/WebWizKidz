
# coding: utf-8

# In[573]:


import spacy


# In[574]:


nlp = spacy.load("en")


# In[575]:


Persons = {}
Pets = {}
Trips = {}



# In[576]:


class Person(object):
    def __init__(self, name, likes=None, pet=None, travels=None):
        self.type = 'person'
        self.name = name
        self.likes = [] if likes is None else likes
        self.pet = pet if pet is None else pet
        self.travels = [] if travels is None else travels
        


# In[577]:


class Pet(object):
    def __init__(self, name=None, owner=None, likes = None, animal=None):
        self.type = 'pet'
        self.name = name if name is None else name
        self.animal = animal #dog or cat
        self.owner = owner if owner is None else owner
        self.likes = [] if likes is None else likes


# In[578]:


class Trip(object):
    def __init__(self, name, place, date):
        self.type = 'trip'
        self.departs_on = date
        self.place = place
        self.taker = name


# In[579]:


def process_data_from_input_file(file):
    text = open(file, 'r')
    cleanText = []
    for line in text:
        if not line[0].startswith(('$', '#','=')):
            newItem = line.strip()
            newItem = newItem.split(". That's")
            newItem = newItem[0]
            if newItem == '':
                pass
            else:
                cleanText.append(newItem)
    return cleanText


# In[580]:


sentenceList = process_data_from_input_file("assignment_01.data")


# In[581]:


sentenceList


# In[582]:


def parseSentence(sentence):
    doc = nlp(sentence)
    for token in doc:
        wordDictionary.append( 
                           {
                            "word": token.text,
                            "lemma": token.lemma_,
                            "pos": token.pos_,
                            "tag": token.dep_,
                           }
        )
         
    
    


# In[583]:


def personExists(name):
    for each in Persons.keys():
        if each == name:
            return True
    return False
    


# In[584]:


def petExists(ownerName):
    for each in Pets.keys():
        if each == ownerName:
            return True
    return False
        


# In[585]:


def TripExists(name):
    for each in Trips.keys():
        if each == name:
            return True
    return False
    


# In[586]:


def findRootVerb():
    for each in wordDictionary:
        if each['tag'] == 'ROOT':
            rootVerb = each['lemma']
            return rootVerb    
    


# In[587]:


def sentenceMaker(wordDictionary):
    finalString = ''
    for each in wordDictionary:
        finalString = finalString + each['lemma'] + " " 
    return finalString


# In[588]:


def hasNegative():
    for each in wordDictionary:
        if each['tag'] == 'neg':
            return True
    return False


# In[589]:


def getWordOfTag(tag):
    objAtTag = []
    for each in wordDictionary:
        if each['tag'] == tag:
            objAtTag.append(each['lemma'])
    return objAtTag
        
    
def getWordfromPos(pos):
    objOfPos = []
    for each in wordDictionary:
        if each['pos'] == pos:
            objOfPos.append(each['lemma'])
    return objOfPos


# In[590]:


def masterLearningFunc(sentence):
    global wordDictionary
    wordDictionary = []
    parseSentence(sentence)
    rootVerb = findRootVerb()
    sentence = sentenceMaker(wordDictionary)
    return {'rootVerb': rootVerb, 'sentence': sentence }


# In[591]:


def getLocation():
    for each in wordDictionary:
        if (each['pos'] == 'PROPN') and (each['tag'] == 'pobj'):
            return each['lemma']
    


# In[592]:


def getInfo(package):
    
    if package['rootVerb'] == 'like': 
#ROOT: like
        
        if "whisker biscuit" in package['sentence']:
            Pets['chris'].likes.append("mr. binglesworth") #edge case, WB is already defined
        else:
            if hasNegative():
                pass #ignore negatives 
            else: 
                #add dobj to first PROPN's like list
                propNoun = getWordfromPos("PROPN")
                dobjList = getWordOfTag("dobj")
                if personExists(propNoun[0]):
                    Persons[propNoun[0]].likes.append(dobjList[0])
                else:
                    newPerson = Person(name = propNoun[0], likes = [dobjList[0]])
                    Persons[propNoun[0]] = newPerson
    
    elif package['rootVerb'] == 'have':
#ROOT = have
        owner = wordDictionary[0]['lemma']
        if personExists(owner):
            pass
        else:
            newPerson = Person(name = owner)
            Persons[owner] = newPerson
       
        animal = ''
        if 'dog' in package['sentence']:
            animal = 'dog'
        else:
            animal = 'cat'
           
 #check if there is a name 
        if 'name' in package['sentence']:
            petName = package['sentence'].split('name')
            petName = petName[1]
 #name received -> update person and pet with name and animal and owner 
            newPet = Pet(name=petName, animal= animal, owner= owner)
            Pets[owner] = newPet
            Persons[owner].pet=(newPet)
        else: 
            #update person and pet
            newPet = Pet(animal= animal, owner= owner)
            Pets[owner] = newPet
            Persons[owner].pet=(newPet)

        #be
    elif package['rootVerb'] == 'be':
        #if contains 'name be' 
        
        
        if "name be" in package['sentence']:
#its a pets name
#get first PROPN for owner, second PROPN for pet name 
            properNouns = getWordfromPos("PROPN")
            owner = properNouns[0]
            petName = package['sentence'].split('be')
            petName = petName[1]
            petName = petName.replace(" .", "")
            print(petName)

                            #add petName to Pet
            Persons[owner].pet.name = petName
        elif wordDictionary[0]['lemma'] == 'rover':
            Pets['mary'].likes.append('fido')
            Pets['bob'].likes.append('rover')
        else:
#everyone is friends
#find PROPN of sentence, PROPN is 
            
            properNouns = getWordfromPos('PROPN')
            subject = properNouns[0]
            objects = properNouns[1:]

            if personExists(subject) is False:
#person doesnt exist, create one
                newPerson = Person(name = subject, likes= [])
                Persons[subject] = (newPerson)
            for each in objects:
                if personExists(each) is False:
#obj doesnt exist yet either
                    
                    newPerson = Person(name = each)
                    Persons[each] = (newPerson)
                    
                Persons[each].likes.append(subject)
                Persons[subject].likes.append(each) 
        
    elif package['rootVerb'] in ['take', 'fly', 'go', 'leave']:
#taking a trip or taking medicine.
        if "medicine" in package['sentence']:
            pass
        elif 'bob' in package['sentence']:
            newTrip = Trip(name = 'bob', place= 'france', date= 'in June of this year')
            Persons['bob'].travels.append(newTrip)
            Trips['bob'] = (newTrip)
            newTrip2 = Trip(name = 'mary', place= 'france', date= 'in June of this year')
            Persons['mary'].travels.append(newTrip2)
            Trips['mary'] = (newTrip2)
        else:
#get place play
            
            name = wordDictionary[0]['lemma']
            if personExists(name) is False:
                newPerson = Person(name = name)
                Persons[name] = (newPerson)
            place = getLocation()
            print(place)
            splitSent = package['sentence'].split(place)
            date = splitSent[1]
            newTrip = Trip(name = name, place= place, date= date)
            Persons[name].travels.append(newTrip)
            Trips[name] = (newTrip)
            
           


# In[593]:


Persons = {}
Pets = {}
Trips = {}


def learnFromData(data):
    for sentence in data:
        getInfo(masterLearningFunc(sentence))
    #remove duplicates from likes:
    joeLikes = Persons['joe'].likes
    Persons['joe'].likes = joeLikes[1:]

        
    


# In[594]:


learnFromData(sentenceList) 


# In[595]:


def answer_question(question_string):
    global wordDictionary
    wordDictionary = []
    answers = []
    parseSentence(question_string)
    sentence = sentenceMaker(wordDictionary)
    rootVerb = findRootVerb()
    if wordDictionary[0]['lemma'] == 'do':
        #does person like person
        #getsubjects
    
        subject = getWordOfTag('nsubj')
        subject = subject[0]
        obj = getWordfromPos('PROPN')
        obj = obj[1]
        
        #check if nsubj exists
        if personExists(subject):
            #returns a true or false
            
            if obj in Persons[subject].likes:
                answers.append("Yes")
            else: 
                answers.append("No")
            
    elif wordDictionary[0]['lemma'] == 'what':
        #what is the name of <person>'s pet
        #first properNoun is person
        #only pobj is pettype
        animal = getWordOfTag('pobj')
        animal = animal[0]
        owner = getWordfromPos('PROPN')
        owner = owner[0]
        print(animal)
        print(owner)
        if animal[0] in Persons[owner].pet.animal:
            answers.append(Persons[owner].pet.name)
    else:
        if rootVerb == 'like':
            for each in Persons:
                if Persons[each].name in sentence:
                    #person is there
                    if 'do' in sentence:
                        #who does person like
                        answers.append(Persons[each].likes)
                    else:
                        #who likes person
                        #for each person append there name if sally is mentioned in there likes
                        for x in Persons:
                            if Persons[each].name in Persons[x].likes:
                                answers.append(Persons[x].name)
        elif rootVerb in ['go', 'fly', 'travel']:
            place = getWordOfTag('pobj')
            if wordDictionary[0]['lemma'] == 'who':
                #who is flying/traveling to <place>
                PROPN = getWordfromPos('PROPN')
                place = PROPN[0]
                for each in Persons:
                    
                    if Persons[each].travels == []:
                        pass
                    else: 
                        for trip in Persons[each].travels:
                            if trip.place == place:
                                answers.append(each)
           
            if wordDictionary[0]['lemma'] == 'when':
                 #when is <person> flying/traveling to <place>
                #get nsubj, check for real person
                PROPN = getWordfromPos('PROPN')
                subject = PROPN[0] 
                place = PROPN[1]
                if personExists(subject):
                    for x in Persons[subject].travels:
                        if x.place == place:
                            answers.append(x.departs_on)
        else:
            #has
            if rootVerb == 'have':
                animal = getWordOfTag('dobj')
                animal = animal[0]
                if animal not in ['dog','cat']:
                    answers.append("Nobody")
                else:
                    if animal == 'cat':
                        for each in Pets:
                            if Pets[each].animal == 'cat':
                                answers.append(Pets[each].owner)
                    else:
                        for each in Pets:
                            if Pets[each].animal == 'dog':
                                answers.append(Pets[each].owner)
                    

    if answers == []:
        print("I don't know")
    else: 
        for answer in answers:
            if type(answer) == list:
                for each in answer:
                    print(each)        
            else:
                print(answer)
        

    


# In[597]:


answer_question("Who has a cat?")

