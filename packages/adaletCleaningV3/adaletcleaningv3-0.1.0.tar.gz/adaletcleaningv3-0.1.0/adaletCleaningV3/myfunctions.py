import re
#import string
import json
from adaletCleaningV3 import utils



def convertTRChars(text):

    with open("adaletCleaningV3/resources/trCharToReplace.json", "r", encoding="utf-8") as file:
        TRCHARTOREPLACE = json.load(file)

    try:
        if isinstance(text, str):
            # Iterate over all key-value pairs in dictionary
            for key, value in TRCHARTOREPLACE.items():
                # Replace key character with value character in string
                text = text.replace(key, value)
    except Exception as e:
        print("Error: ", e)
    
    return text
 

def lowercase(text):

    try:
        if isinstance(text, str):
            text = utils.turkish_lower(text)
         
    except Exception as e:
        print("Error: ", e)

    return text


def removeCityDistrictNames(text):
    
    _, _, cityDistrictNames = utils.getCityDistrictNames()  
        
    try:
        if isinstance(text, str):
            text = utils.turkish_lower(text)
            text = ' '.join(word for word in text.split() if word not in cityDistrictNames)
    except Exception as e:
        print("Error: ", e)

    return text


def removePunctuations(text):
    # string.punctuations characters are : !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    #PUNCTUATIONS = string.punctuation
    with open("adaletCleaningV3/resources/punctuations.txt", "r", encoding="utf-8") as file:
        PUNCTUATIONS = file.read()

    try:
        if isinstance(text, str):
            text = text.translate(str.maketrans(PUNCTUATIONS, ' ' * len(PUNCTUATIONS)))
    except Exception as e:
        print("Error: ", e)

    return text


def keepCharacters(text, keepNumber):

    with open("adaletCleaningV3/resources/cleaningParams.txt", "r", encoding="utf-8") as file:
        partOfFile = file.read()

        charactersToKeepStart = partOfFile.find("<CHARACTERS_TO_KEEP>") + len("<CHARACTERS_TO_KEEP>")
        charactersToKeepEnd = partOfFile.find("</CHARACTERS_TO_KEEP>")
        charactersAndNumbersToKeepStart = partOfFile.find("<CHARACTERSANDNUMBERS_TO_KEEP>") + len("<CHARACTERSANDNUMBERS_TO_KEEP>")
        charactersAndNumbersToKeepEnd = partOfFile.find("</CHARACTERSANDNUMBERS_TO_KEEP>")

        characterTokens = partOfFile[charactersToKeepStart:charactersToKeepEnd]
        CHARACTERSTOKEEP = re.compile(r'[{}]'.format(characterTokens))
        characterAndNumbersTokens = partOfFile[charactersAndNumbersToKeepStart:charactersAndNumbersToKeepEnd]
        CHARACTERSANDNUMBERSTOKEEP = re.compile(r'[{}]'.format(characterAndNumbersTokens))

    try:
        if isinstance(text, str):
            if keepNumber:
                pattern = re.compile(CHARACTERSANDNUMBERSTOKEEP)
            else:
                pattern = re.compile(CHARACTERSTOKEEP)
            text = re.sub(pattern, ' ', text)
    except Exception as e:
        print("Error: ", e)

    return text


def removeSpecialCharacters(text):

    with open("adaletCleaningV3/resources/cleaningParams.txt", "r", encoding="utf-8") as file:
        partOfFile = file.read()
        specialCharactersStart = partOfFile.find("<SPECIAL_CHARACTERS>") + len("<SPECIAL_CHARACTERS>")
        specialCharactersEnd = partOfFile.find("</SPECIAL_CHARACTERS>")
        specialCharacters = partOfFile[specialCharactersStart:specialCharactersEnd]
        SPECIALCHARACTERS = re.compile(r'[{}]'.format(specialCharacters))

    try:
        if isinstance(text, str):
            pattern = re.compile(SPECIALCHARACTERS)
            text = re.sub(pattern, ' ', text)
    except Exception as e:
        print("Error: ", e)

    return text


def removeStopwords(text):

    with open(("adaletCleaningV3/resources/stopwords.txt"), "r", encoding="utf-8") as file:
        STOPWORDS = file.read().split("\n")

    try:
        if isinstance(text, str):
            text = utils.turkish_lower(text)
            text = ' '.join(word for word in text.split() if word not in STOPWORDS)
    except Exception as e:
        print("Error: ", e)

    return text
        

def removeSingleCharacters(text):

    try:
        if isinstance(text, str):
            text = ' '.join([w for w in text.split() if len(w) > 1])
    except Exception as e:
        print("Error: ", e)

    return text


def removeUnusedWords(text):

    with open("adaletCleaningV3/resources/adaletUnusedWords.txt", "r", encoding="utf-8") as file:
        ADALETUNUSEDWORDS = file.read().split("\n")

    try:
        if isinstance(text, str):
            text = utils.turkish_lower(text)
            text = ' '.join(word for word in text.split() if word not in ADALETUNUSEDWORDS)
    except Exception as e:
        print("Error: ", e)

    return text


def removeCommonWords(text):

    with open("adaletCleaningV3/resources/adaletCommonWords.txt", "r", encoding="utf-8") as file:
        ADALETCOMMONWORDS = file.read().split("\n")

    try:
        if isinstance(text, str):
            text = utils.turkish_lower(text)
            encodeText, indices = utils.encodeTextToArray(text, ADALETCOMMONWORDS, fullTextSearch=True)
            resolvedText = text.split(' ')
            if len(resolvedText):
                resolvedText = utils.removeElements(resolvedText, indices)
                text = ' '.join(resolvedText)
    except Exception as e:
        print("Error: ", e)

    return text


def removeConsecutiveConsonants(text):

    try:
        if isinstance(text, str):
            result = []
            for word in text.strip().split(" "):
                if isinstance(word, str):
                    # if there are more than 3 consecutive consonants for a text
                    if len(utils.consonantConsecutiveList(word, 3)) == 0:
                        result.append(word)
            if len(result) > 0:
                text = ' '.join(result)
    except Exception as e:
        print("Error: ", e)

    return text


def removeConsecutiveVowels(text):
    try:
        if isinstance(text, str):
            result = []
            for word in text.strip().split(" "):
                if isinstance(word, str):
                    # if there are more than 2 consecutive vowels for a text
                    if len(utils.vowelConsecutiveList(word, 2)) == 0:
                        result.append(word)
            if len(result) > 0:
                text = ' '.join(result)
    except Exception as e:
        print("Error: ", e)

    return text


def cleanSpaces(text):

    try:
        # return str(rawText).replace("\'", "").replace('"', "").replace("\t", "").replace("\n", "")
        if isinstance(text, str):
            #text = re.sub(r'\s+', ' ', text).strip()
            text = re.sub(r'\s+', ' ', text).replace("'", " ").replace('"', " ").strip()
    except Exception as e:
        print("Error: ", e)

    return text


def replaceAbbreviations(text):

    with open("adaletCleaningV3/resources/abbreviations.json", "r", encoding="utf-8") as file:
        ABBREVIATIONS = json.load(file)
    try:
        if isinstance(text, str): 
            text = utils.turkish_lower(text) 
            for abbr, full_form in ABBREVIATIONS.items():
                text = re.sub(r'\b{}\b'.format(re.escape(abbr)), full_form, text)
         
    except Exception as e:
        print("Error: ", e)

    return text


#: if requested allowCharacters params, then merge all unwanted punctuations and finally remove allowedchars from them
def allowOnlySpecificCharacters(text, isSpecialCharacters):

    with open("adaletCleaningV3/resources/cleaningParams.txt", "r", encoding="utf-8") as file:
        partOfFile = file.read()
        specialCharactersStart = partOfFile.find("<SPECIAL_CHARACTERS>") + len("<SPECIAL_CHARACTERS>")
        specialCharactersEnd = partOfFile.find("</SPECIAL_CHARACTERS>")
        specialCharacters = partOfFile[specialCharactersStart:specialCharactersEnd]
        SPECIALCHARACTERS = re.compile(r'[{}]'.format(specialCharacters))
    with open("adaletCleaningV3/resources/punctuations.txt", "r") as file:
        PUNCTUATIONS = file.read()
    with open("adaletCleaningV3/resources/allowedChars.txt", "r") as file:
        ALLOWEDCHARS = file.read()

    try:
        if isinstance(text, str):
            charactersForReplace = PUNCTUATIONS
            if isSpecialCharacters:
                charactersForReplace += SPECIALCHARACTERS.pattern
            if len(ALLOWEDCHARS.strip()) > 0:
                uniqueCharacters = ''.join(set(charactersForReplace) - set(ALLOWEDCHARS))
            else:
                uniqueCharacters = ''.join(set(charactersForReplace))
            if isinstance(text, str):
                text = text.translate(str.maketrans(uniqueCharacters, ' ' * len(uniqueCharacters)))
    except Exception as e:
        print("Error: ", e)

    return text



def text_normalizer(text):
    text = cleanSpaces(text)
    text = lowercase(text)
    text = removePunctuations(text)
    text = removeSpecialCharacters(text)
    text = removeCommonWords(text)
    text = removeCityDistrictNames(text)
    text = removeStopwords(text)
    text = removeUnusedWords(text)
    text = convertTRChars(text)
    text = keepCharacters(text, False)
    text = replaceAbbreviations(text)
    text = removeSingleCharacters(text)
    text = removeConsecutiveConsonants(text)
    text = removeConsecutiveVowels(text)
    
    return text


