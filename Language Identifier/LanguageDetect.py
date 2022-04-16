# This module implements a regex algorithm to check if words are within
# an English dictionary. If they are not initially we remove unnecessary characters/
# with regex to clean data. Then we check if words are comprised of multiple subwords
# then word is English but not defined by dictionary (slang).


# Leverages a dictionary to check words individually and performs string manipulation otherwise.
import re
#from spylls.hunspell import Dictionary
import enchant
# print(enchant.list_languages())
e = enchant.Dict("en_US")
#m = Dictionary.from_files('malayalan.oxt') Not supported yet
check = e.check("update")

r = open('Language_Detection.csv',"r", encoding = 'cp850') #use 'test.csv'
r.readline()                                               #skip column header



# Words need to be capitalized as in dictionary
def toUpper(string):
    first = string[0].upper()
    return first+string[1:len(string)]

# Check if word is within another word, to check both in dictionary
def checkCombined(word):
    subWord = []

    if(e.check(word.replace('┬á',''))): return True #unicode character remove
    for x in range(len(word)-1):
        if(e.check(word[:x+1])): subWord.append(word[:x+1])
        if(e.check(word[x+1:])): subWord.append(word[x+1:])
    for words in subWord:
        if(word.replace(words, '') in subWord): return True
       
    return False

# Parses words with regex and checks if they are within dictionaryh
def classify(string):
    nonEnglish = []
    actual = (re.sub(r'[!@#$(),\n"%^*?\:;~`0-9\[\]]|(ppt|i\.e\.|)', '', string)).split(" ")
    actual = list(filter(None,actual))
    for items in actual:
        if(items == '' or items == ' '):actual.remove(items)
    if("English" in actual[-1]):
        actual[-1] = actual[-1].replace("English", '')
    size = len(actual)
    isEnglish = 0
    
    # Additional regex subs on words
    # This is for checking words individually if they're english after regex, and substitutions
    for x in actual:
        if(x == '' or x == ' '): continue
        if(e.check(x)):
            # print(x) UNCOMMENT TO SEE WORDS LABELLED AS ENGLISH
            isEnglish += 1
        elif(re.sub('\'|""|\.┬á|\.com|[ÔÇö¤å¤ì¤â╬╣¤é¼├Â├º├®┬á]|\.org|en.mobile.|en\.|\[!A-Z].$','',x) == ''): 
            size-=1
            continue
        elif(e.check(re.sub('\'|""|\.┬á|\.com|[ÔÇö¤å¤ì¤â╬╣¤é¼├Â├º├®┬á]|\.org|en.mobile.|en\.|\[!A-Z].$','',toUpper(x)))): 
            x=re.sub('\'|""|\.┬á|\.com|[ÔÇö¤å¤ì¤â╬╣¤é¼├Â├º├®┬á]|\.org|en.mobile.|en\.|\[!A-Z].$','',toUpper(x))
            
            isEnglish+=1  #check broken quotations   
            
        elif(len(x) > 3 and e.check(x[:-3]) or len(x) > 3 and e.check(x[:-2])): # made up simple sub words + concatination        
            isEnglish += 1
        elif(checkCombined(x)):         
            isEnglish += 1  # made up of sub words             
        else:          
            
            nonEnglish.append(x)
        
    if((isEnglish / size) >= .85): # If sentence is mostly nonEnglish we cannot classify as English sentence
        return True
    #print(nonEnglish) UNCOMMENT TO SEE WORDS LABELLED AS NON ENGLISH
    #print(actual) UNCOMMENT TO SEE SENTENCES LABELLED AS NON ENGLISH
    
    return False

wrong = 0

#1425 English for Range, Checking English Sentences Only from dataset
for x in range(1000):
    colNames = r.readline().replace('\n','').split('",')
    if(len(colNames) == 2): classified = classify(colNames[0])
    elif(len(colNames) == 3): classified = classify(colNames[1])
    if(not classified): wrong += 1
    

# Accuracy of Sentences identified as English, correspondent to range argument above
print((1000 - wrong) / 1000)







