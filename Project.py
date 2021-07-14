#!/usr/bin/env python
# coding: utf-8

# Project Aim is to help our developers understand what type of apps are likely to attract more users on Google Play and the App Store. To do this, we'll need to collect and analyze data about mobile apps available on Google Play and the App Store.

# In[ ]:





# In[1]:


from csv import reader


# # Creating Dataset 

# In[2]:


open_AppleStore = open('AppleStore.csv')
open_playstore = open('googleplaystore.csv')
appleStore = list(reader(open_AppleStore))
playStore = list(reader(open_playstore))


# # Create  explore_data() function 

# In[3]:


#explore data function will help us to explore our new dataset's
def explore_data(dataset,header=True):
    if header:
        for i in dataset:
            print(i)
            print('\n')
    else:
        for i in dataset[1:]:
            print(i)
            print('\n') 


# # Use explore_data() function to explore dataset 

# In[4]:


#here we are exploring only 6 rows(in appleStore)
explore_data(appleStore[0:6],header=True)


# In[5]:


#here we are exploring only 6 rows(in playStore)
explore_data(playStore[0:6],header=True)


# # Data Cleaning and Deal with missing data 

# In[6]:


playStoreLength = playStore[0]
playStoreLength


# In[7]:


for i in playStore[1:]:
    if len(i) != len(playStoreLength):
        print(i)
        print('\n')
        print(playStore.index(i))


# ####  Deleting index number 10473 from playstore

# In[8]:


del playStore[10473]


# #### Find duplicate values

# In[9]:


uniq_values = []
duplicate_values = []
for i in playStore[1:]:
    if i in uniq_values:
        duplicate_values.append(i)
    else:
        uniq_values.append(i)          


# In[10]:


len(uniq_values)


# In[11]:


len(duplicate_values)


# In[12]:


for i in duplicate_values:
    if i[0] == 'Instagram':
        print(i)


# #### we won't remove the duplicates randomly. we will keep the data that have higher number of review 

# In[13]:


reviews_max = {}
for i in playStore[1:]:
    name = i[0]
    n_review = float(i[3])
    if name in reviews_max and n_review > reviews_max[name]:
        reviews_max[name] = n_review
    elif name not in reviews_max:
        reviews_max[name] = n_review


# In[14]:


len(reviews_max)


# ####  Use the dictionary we created above to remove the duplicate rows

# In[15]:


#we will store new clean data here
android_clean = []

#just to store app names
already_added = []

for i in playStore[1:]:
    name = i[0]
    n_reviews = float(i[3])
    if n_reviews == reviews_max[name] and name not in already_added:
        android_clean.append(i)
        already_added.append(name)


# In[16]:


len(android_clean)


# # Remove Non-English Apps 

#  We're not interested in keeping these apps, so we'll remove them. One way to do this is to remove each app with a name containing a symbol that isn't commonly used in English text — English text usually includes letters from the English alphabet, numbers composed of digits from 0 to 9, punctuation marks (., !, ?, ;), and other symbols (+, *, /).
#  
# Each character we use in a string has a corresponding number associated with it. For instance, the corresponding number for character 'a' is 97, character 'A' is 65, and character '爱' is 29,233. We can get the corresponding number of each character using the ord() built-in function.
# 
# 

# In[17]:


def checkEnglishString(data):
    n_nonEnglish = 0
    for i in data:
        check = ord(i)
        if check > 127 and n_nonEnglish >= 3:
            return False
        elif check > 127:
            n_nonEnglish += 1
    return True   


################################--NOTE--#####################################
##If the input string has more than three characters that fall outside the ASCII range (0 - 127), then the function should return False


# ####  Checking by giving some input inside function

# In[18]:


checkEnglishString('Instagram')


# In[19]:


checkEnglishString('Docs To Go™ Free Office Suite')


# In[20]:


checkEnglishString('爱奇艺PPS -《欢乐颂2》电视剧热播')


# In[21]:


checkEnglishString('Instachat 😜')


# The numbers corresponding to the characters we commonly use in an English text are all in the range 0 to 127, according to the ASCII (American Standard Code for Information Interchange) system. Based on this number range, we can build a function that detects whether a character belongs to the set of common English characters or not. If the number is equal to or less than 127, then the character belongs to the set of common English characters.
# 
# If an app name contains a character that is greater than 127, then it probably means that the app has a non-English name.

# In[22]:


PlayStore = []
for i in android_clean:
    if checkEnglishString(i[0]) == True:
         PlayStore.append(i)
AppleStore = []
for i in appleStore:
    if checkEnglishString(i[1]) == True:
         AppleStore.append(i)            


# In[23]:


AppleStore


# **So far in the data cleaning process, we've done the following:**
# 
# **-->Removed inaccurate data**
# 
# **-->Removed duplicate app entries**
# 
# **-->Removed non-English apps**

# we only build apps that are free to download and install, and our main source of revenue consists of in-app ads. Our datasets contain both free and non-free apps; we'll need to isolate only the free apps for our analysis. 

# In[24]:


len(AppleStore)


# In[25]:


len(PlayStore)


# #### AppleStore Free Apps 

# In[26]:


#the index number of column about app price in AppleStore is "5"
appleStoreFree = []
appleStoreNotFree = []
for i in AppleStore[1:]:
    if i[4] == "0.0" or i[4] == "0":
        appleStoreFree.append(i)
    else:
        appleStoreNotFree.append(i)


# In[27]:


len(appleStoreFree)


# #### PlayStore Free Apps 

# In[28]:


#the index number of column about app price in PlayStore is "7"
playStoreFree = []
playStoreNotFree = []
for i in PlayStore:
    if i[7] == "0":
        playStoreFree.append(i)
    else:
        playStoreNotFree.append(i)


# In[29]:


len(playStoreFree)


# our goal is to determine the kinds of apps that are likely to attract more users because the number of people using our apps affect our revenue.
# 
# To minimize risks and overhead, our validation strategy for an app idea has three steps:
# 
# 1.Build a minimal Android version of the app, and add it to Google Play.
# 2.If the app has a good response from users, we develop it further.
# 3.If the app is profitable after six months, we build an iOS version of the app   and add it to the App Store.

# # Generate Frequency tables to determine common genres for each market

# In[30]:


def freq_table(dataset,index):
    appgenres = {}
    for i in dataset:
        genres = i[index]
        if genres in appgenres:
            appgenres[genres] += 1
        else:
            appgenres[genres] = 1
    return appgenres      


# In[31]:


def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# In[32]:


#Playstore
display_table(playStoreFree,9)


# In[33]:


#Applestore
display_table(appleStoreFree,11)


# In[34]:


appleStoreGenre = freq_table(appleStoreFree,11)
playStoreGenre = freq_table(playStoreFree,9)


# In[35]:


for i in appleStoreGenre:
    for j in playStoreGenre:
        if i == j:  
            print(f'''                           **{j}**                  
                  PlayStore= {playStoreGenre[j]} | AppleStore= {appleStoreGenre[i]}\n\n''')


# The frequency tables we analyzed on the previous screen showed us that apps designed for fun dominate the App Store, while Google Play shows a more balanced landscape of both practical and fun apps. Now, we'd like to determine the kind of apps with the most users.
# 
# One way to find out what genres are the most popular (have the most users) is to calculate the average number of installs for each app genre. For the Google Play data set, we can find this information in the Installs column, but this information is missing for the App Store data set. As a workaround, we'll take the total number of user ratings as a proxy, which we can find in the rating_count_tot app.

# In[36]:


for i in playStoreGenre:
    total = 0
    len_genre = 0
    for j in playStoreFree:
                genre_app = j[9]
                if genre_app == i:
                    user_rating = float(j[2])
                    total += user_rating
                    len_genre += 1
    if total != 'nan':
        avg_rating = total/len_genre
        print(i,":",avg_rating)


# After analyze the result app profile recommendation for PlayStore 
# 
# **1.Puzzle,Education**
# 
# **2.Entertainment,Creativity**
# 
# **3.Racing,Pretend Play**

# In[42]:


for i in appleStoreGenre:
    total = 0
    len_genre = 0
    for j in appleStoreFree:
                genre_app = j[11]
                if genre_app == i:
                    user_rating = float(j[7])
                    total += user_rating
                    len_genre += 1
 
    avg_rating = total/len_genre
    print(i,':',avg_rating)


# After analyze the result app profile recommendation for AppleStore 
# 
# **1.Catalogs**
# 
# **2.Games**
# 
# **3.Business** 

# ## In this project, I went through a complete data science workflow:
# 
# **I started by clarifying the goal of our project.**
# 
# **I collected relevant data.**
# 
# **I cleaned the data to prepare it for analysis.**
# 
# **I analyzed the cleaned data.**

# In[ ]:




