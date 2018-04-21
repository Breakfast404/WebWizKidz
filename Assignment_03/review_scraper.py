
# coding: utf-8

# In[597]:


from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import random
import numpy as np
import time
import pandas as pd
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.corpus import sentiwordnet as swn
import matplotlib.pyplot as plt


# In[266]:


Reviews = {}


# In[267]:


pageUrl = 'https://www.amazon.com/RockBirds-Flashlights-Bright-Aluminum-Flashlight/product-reviews/B00X61AJYM/ref=cm_cr_arp_d_paging_btm_1?sortBy=recent&pageNumber=1&reviewerType=avp_only_reviews&formatType=all_formats'


# In[268]:


driver = webdriver.Chrome(executable_path='./chromedriver')


# In[269]:


authors = []
ratings = []
titles = []
texts = []
dates = []


# #### Used to check length of every list to make sure dataframe can be made 

# In[ ]:


print(len(authors))
print(len(ratings2))
print(len(titles))
print(len(texts))
print(len(cleanText))
print(len(dates))
print(len(pos_ScoreOfText))
print(len(neg_ScoreOfText))
print(len(pos_ScoreOfTitle))
print(len(neg_ScoreOfTitle))
print(len(goodWordsInSent))
print(len(badWordsInSent))
print(len(isGuest))
print(len(lengthOfText))
print(len(wordsInAuthor))


# ### Page Scraper. -Takes Review Text, Title, Author Name, Date, and Rating

# In[271]:


def pageQuery():

    driver.get(pageUrl)
    n = 0
    running = True
    #wait
    time.sleep(5)
    #wait-finished
    while n <= 1300:

        wrapper = driver.find_element_by_id('cm_cr-review_list')
        elements = wrapper.find_elements_by_css_selector("div[data-hook='review']")
        for each in elements:
            title = 'null'
            author = 'null'
            date = 'null'
            text = 'null'
            rating = 'null'
            title = each.find_element_by_css_selector("a[data-hook='review-title']").text
            titles.append(title)

            author = each.find_element_by_css_selector("a[data-hook='review-author']").text
            authors.append(author)

            date = each.find_element_by_css_selector("span[data-hook='review-date']").text
            date = date.replace('on ', "")
            dates.append(date)

            

            text = each.find_element_by_css_selector("span[data-hook='review-body']").text
            texts.append(text)

            element = each.find_element_by_css_selector('a[class="a-link-normal"]').get_attribute("title")
            rating = element.replace(' out of 5 starts', '')
            ratings.append(rating)
            
            n+=1
            
            if n % 100 == 0: 
                print(str(n) + "Reviews Collected")
            
        nextPage()
        time.sleep(5)
        
    print('Finished')


# #### Switches to the next page of amazon reviews

# In[272]:


def nextPage():

        element = driver.find_element_by_css_selector("li[class='a-last']")
        nextButton = element.find_element_by_css_selector("a")
        nextButton.click()


# In[273]:


pageQuery()


# #### Most extra factors that are extracted defined in one place. Some are defined in their respective for loops

# In[633]:


#extra factors
isGuest = []
lengthOfText = []
wordsInText = []
lengthOfAuthor = []
wordsInAuthor = []




# ##### Checks if user name is Amazon Customer. I figured this might be a good indicator that a review might be fake because they are not displaying a username.

# In[634]:


for each in authors:
    if each == "Amazon Customer":
        isGuest.append(1)
    else:
        isGuest.append(0)
        
    numOfWords = each.count(' ') + 1
    lengthOfString = len(each)
    lengthOfAuthor.append(lengthOfString)
    wordsInAuthor.append(numOfWords)
    
for each in texts:
    wordsInText.append(each.count(' ') + 1)
    lengthOfText.append(len(each))
    
    


# In[276]:


cleanText = []


# ##### Removes stopwords and puntuation as well as pronouns and creates a list.

# In[ ]:


nlp = spacy.load("en")

cachedStopWords = stopwords.words("english")

for sentence in texts:
    doc = nlp(sentence)
    newSentence = []
    for token in doc:
        if token.text in cachedStopWords:
            pass
        elif token.is_punct:
            pass
        elif token.pos_ == 'PRON':
            pass
        elif token.lemma_ == '-PRON-':
            pass
        else:
            newSentence += [token.lemma_]
            
            
    cleanText.append(newSentence)
        
cleanText    
    


# ##### common positive and negative words in reviews. This is used to make a scoreOfText feature for both positive and negative review

# In[1187]:


#make a list of positive words
#check if text contains a positive word
goodWords = ['awesome', 'excellent', 'solid', 'perfect', 'good', 'love', 'better', 'easy', 'great', 'powerful', 'inexpensive', 'amazing', 'happy', 'terrific']


# In[1188]:


#make a list of negative words
badWords = ['poor', 'trash', 'garbage', 'broken', 'broke','terrible', 'bad', 'defective', 'dropped', 'drop', 'disappointed', 'faulty', 'miss', 'waste', 'weak', 'stopped', 'mediocre','cheaply','junk', 'china','hate',]
#check if text contains a positive word


# In[429]:


#extra all adjectives
#combine into string with str(word)+".a.01"
#store pos_score()  
#store neg_score() and add to df
pos_ScoreOfText = []
neg_ScoreOfText = []
n = 0

for sentence in texts:
    if n % 100 == 0:
        print(n)
    doc = nlp(sentence)
    AdjInSent = []
    totalPos = 0
    totalNeg = 0
    for token in doc:
        if token.text in cachedStopWords:
            pass
        elif token.is_punct:
            pass
        elif token.pos_ == 'PRON':
            pass
        elif token.lemma_ == '-PRON-':
            pass
        else:
            if token.pos_ == 'ADJ':
                try:
                    breakdown = swn.senti_synset(str(token.lemma_)+'.a.01')
                    AdjInSent.append(breakdown)
                except:
                    pass
    for each in AdjInSent:
        totalPos = totalPos + each.pos_score()
        totalNeg = totalNeg + each.neg_score()
    pos_ScoreOfText.append(totalPos)
    neg_ScoreOfText.append(totalNeg)
    n += 1
        
   
                      


# ### Count how many good words /bad words the review contains. Could be a useful feature

# In[434]:


#extra all adjectives
#combine into string with str(word)+".a.01"
#store pos_score()  
#store neg_score() and add to df
pos_ScoreOfTitle = []
neg_ScoreOfTitle = []
n = 0

for sentence in titles:
    if n % 100 == 0:
        print(n)
    doc = nlp(sentence)
    AdjInSent = []
    totalPos = 0
    totalNeg = 0
    for token in doc:
        if token.text in cachedStopWords:
            pass
        elif token.is_punct:
            pass
        elif token.pos_ == 'PRON':
            pass
        elif token.lemma_ == '-PRON-':
            pass
        else:
            if token.pos_ == 'ADJ':
                try:
                    breakdown = swn.senti_synset(str(token.lemma_)+'.a.01')
                    AdjInSent.append(breakdown)
                except:
                    pass
    for each in AdjInSent:
        totalPos = totalPos + each.pos_score()
        totalNeg = totalNeg + each.neg_score()
    pos_ScoreOfTitle.append(totalPos)
    neg_ScoreOfTitle.append(totalNeg)
    n += 1
        
   
                      


# In[ ]:


remove_words= ['is','baby', 'pack', 'personal', 'using', 'extension', 'changed', 'today', 've', 'kong', 'wider']
newText = [] 
for sentence in texts:
    for each in sentence:
        if each in remove_words:
            sentence = sentence.replace(each, '')
    newText.append(sentence)


# #### Removes 'out of 5 stars' from ratings and converts string to float then an integer.

# In[498]:


ratings2 = []
for each in ratings:
    score = each.replace(' out of 5 stars', '')
    ratings2.append(int(float(score)))
    
    


# In[ ]:


newText = []
keep_types = {'NOUN', 'PROPN', 'ADJ', 'VERB'}

for sentence in texts:
    
    doc = nlp(sentence)
    
    keep_tokens_string = ' '.join([t.text for t in doc if t.pos_ in keep_types])
    newText.append(keep_tokens_string)


# In[ ]:


from nltk.tokenize import word_tokenize
cleanTitle = []
cleanTitle = [word_tokenize(x) for x in titles]


# In[1123]:


data = {'Date': dates, 'Author': authors, 'Title': titles, 'Rating': ratings2, 'Clean Title': cleanTitle, 'Text': newText,'Is Guest': isGuest, 'Review Length (char)': lengthOfText, 'Words in Review': wordsInText, 'Author Name Length': lengthOfAuthor, 'Words In Author Name': wordsInAuthor, 'Cleaned Text': cleanText, 'Positive Sentiment Score of Text': pos_ScoreOfText, 'Negative Sentiment Score of Text': neg_ScoreOfText,'Positive Sentiment Score of Title': pos_ScoreOfTitle,'Negative Sentiment Score of Title': neg_ScoreOfTitle, 'SentimentWords': SentiWords}


# In[1189]:


df = pd.DataFrame(data=data)


# In[1125]:


df.to_csv('outputdata.csv')
df.to_json('reviews.json')

