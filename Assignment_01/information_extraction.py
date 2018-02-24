
# coding: utf-8

# In[4]:


import spacy


# In[5]:


nlp = spacy.load('en')
persons = []
pets = []
trips = []


# In[6]:


#Takes file 
def process_data_from_input_file(file):
    text = open(file, 'r')
    cleanText = []
    for line in text:
        if not line[0].startswith(('$', '#','=')):
            cleanText.append(line.strip())
    return cleanText
        


# In[7]:


cleanText = process_data_from_input_file('assignment_01.data')
cleanText


# In[8]:


class Person(object):
    def __init__(self, name, likes=None, has=None, travels=None):
        
        self.name = name
        self.likes = [] if likes is None else likes
        self.has = [] if has is None else has
        self.travels = [] if travels is None else travels



# In[9]:


class Pet(object):
    def __init__(self, pet_type, name=None, owner):
        self.name = name
        self.type = pet_type
        self.owner = owner


# In[10]:


class Trip(object):
    def __init__(self):
        self.departs_on = None
        self.departs_to = None
        self.taker = None


# In[13]:


def max_similarity(string):
    string.strip('who')
    string.strip('what')
    string.strip('is')
    string.strip('when')
    string.strip('has')
    string.strip('does')
    doc1 = nlp(string)
    max_score = 0.1
    best_match = ''
    for each in cleanText:
        if max_score < doc1.similarity(nlp(each)):
            max_score = doc1.similarity(nlp(each))
            best_match = each
    if best_match = '':
        print("I don't know")
    else: 
        print(best_match)




# In[14]:



###Takes question_string, parses question, returns all possible answers, if no good answer, return 'I don't know"###

def answer_question(question_string):
    max_similarity(question_string)
    
answer_question('Who has a dog named rover')


# In[15]:


def select_person(name):
    for person in persons:
        if person.name == name:
            return person


# In[16]:


def select_pet(name):
    for pet in pets:
        if pet.name == name:
            return pet


# In[17]:


def add_person(name):
    person = select_person(name)

    if person is None:
        new_person = Person(name)
        persons.append(new_person)

        return new_person

    return person


# In[18]:




