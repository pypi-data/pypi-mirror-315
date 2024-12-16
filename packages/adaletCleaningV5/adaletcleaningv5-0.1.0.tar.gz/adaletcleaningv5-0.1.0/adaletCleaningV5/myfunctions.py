import re
#import string
import json
from adaletCleaningV5 import utils

TRCHARTOREPLACE = {
    "Â": "a",
    "â": "a",
    "ş": "s",
    "ğ": "g",
    "ü": "u",
    "ç": "c",
    "ö": "o",
    "ı": "ı",
    "Ş": "S",
    "Ğ": "G",
    "Ç": "C",
    "Ü": "U",
    "Ö": "O",
    "İ": "I"
}

PUNCTUATIONS = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    # string.punctuations characters are : !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    #PUNCTUATIONS = string.punctuation

CHARACTERSTOKEEP = re.compile(r'[{}]'.format("^a-zA-ZçığöşüÇĞİÖŞÜ"))

CHARACTERSANDNUMBERSTOKEEP = re.compile(r'[{}]'.format("^a-zA-Z0-9çığöşüÇĞİÖŞÜ"))

SPECIALCHARACTERS = re.compile(r'[{}]'.format("»«—”"))


STOPWORDS = [
    "acaba", "ama", "ancak", "arada", "aslında", "ayrıca", "bana", "bazı", "belki", "ben", "benden", "beni", "benim", "beri", "bile", "birçok", 
    "biri", "birkaç", "birkez", "birşey", "birşeyi", "biz", "bize", "bizden", "bizi", "bizim", "böyle", "böylece", "bu", "buna", "bunda", 
    "bundan", "bunlar", "bunları", "bunların", "bunu", "bunun", "burada", "çok", "çünkü", "da", "daha", "dahi", "de", "defa", "değil", "diğer", 
    "diye", "dolayı", "dolayısıyla", "eğer", "en", "gibi", "göre", "halen", "hangi", "hatta", "hem", "henüz", "hep", "hepsi", "her", "herhangi", 
    "herkesin", "hiç", "hiçbir", "için", "ile", "ilgili", "ise", "işte", "itibaren", "itibariyle", "kadar", "karşın", "kendi", "kendilerine", 
    "kendini", "kendisi", "kendisine", "kendisini", "kez", "ki", "kim", "kimden", "kime", "kimi", "kimse", "mu", "mü", "mı", "nasıl", "ne", 
    "neden", "nedenle", "nerde", "nerede", "nereye", "niye", "niçin", "o", "ona", "ondan", "onlar", "onlardan", "onları", "onların", "onu", 
    "onun", "oysa", "öyle", "pek", "rağmen", "sadece", "sanki", "sen", "senden", "seni", "senin", "siz", "sizden", "sizi", "sizin", "şey", 
    "şeyden", "şeyi", "şeyler", "şöyle", "şu", "şuna", "şunda", "şundan", "şunları", "şunu", "tarafından", "tüm", "üzere", "ve", "veya", "ya", 
    "yani", "yerine", "yine", "yoksa", "zaten", "mi", "onlari", "acep", "adeta", "artık", "aynen", "az", "bari", "bazen", "başka", "biraz", 
    "bütün", "dahil", "daima", "dair", "dayanarak", "fakat", "halbuki", "hani", "hele", "herkes", "iken", "ila", "ilk", "illa", "iyi", "iyice", 
    "kanımca", "kere", "keşke", "kısaca", "lakin", "madem", "meğer", "nitekim", "sonra", "veyahut", "yahut", "şayet", "şimdi", "gerek", "hakeza", 
    "hoş", "kah", "keza", "mademki", "mamafih", "meğerki", "meğerse", "netekim", "neyse", "oysaki", "velev", "velhasıl", "velhasılıkelam", 
    "yalnız", "yok", "zira", "adamakıllı", "bilcümle", "binaen", "binaenaleyh", "birazdan", "birden", "birdenbire", "birlikte", "bitevi", 
    "biteviye", "bittabi", "bizatihi", "bizce", "bizcileyin", "bizzat", "buracıkta", "buradan", "büsbütün", "çoğu", "çoğun", "çoğunca", 
    "çoğunlukla", "dahilen", "demin", "demincek", "deminden", "derhal", "derken", "elbet", "elbette", "enikonu", "epey", "epeyce", "epeyi", 
    "esasen", "esnasında", "etraflı", "gibilerden", "gibisinden", "halihazırda", "haliyle", "hasılı", "hulasaten", "illaki", "itibarıyla", 
    "iyicene", "kala", "külliyen", "nazaran", "nedeniyle", "nedense", "nerden", "nerdeyse", "nereden", "neredeyse", "neye", "neyi", "nice", 
    "nihayet", "nihayetinde", "onca", "önce", "önceden", "önceleri", "öncelikle", "oracık", "oracıkta", "orada", "oradan", "oranca", "oranla", 
    "oraya", "peyderpey", "sahiden", "sonradan", "sonraları", "sonunda", "şuncacık", "şuracıkta", "tabii", "tam", "tamam", "tamamen", "tamamıyla", 
    "tek", "vasıtasıyla", "doğru", "gelgelelim", "gırla", "hasebiyle", "zarfında", "öbür", "başkası", "beriki", "birbiri", "birçoğu", "birileri", 
    "birisi", "birkaçı", "bizimki", "burası", "diğeri", "filanca", "hangisi", "hiçbiri", "kaçı", "kaynak", "kimisi", "kimsecik", "kimsecikler", 
    "neresi", "öbürkü", "öbürü", "onda", "öteki", "ötekisi", "sana", "şunlar", "şunun", "şuracık", "şurası", "nın", "nin", "nun", "nün", "ın", 
    "in", "un", "ün"]

ADALETUNUSEDWORDS = [
    "rica", "olunur", "imzalıdır", "com", "gov", "tl", "http", "tr", "wwww"
]

ADALETCOMMONWORDS = [
    "zabıt", "katibi", "anadolu", "cumhuriyet", "savci", "savcı", "büro", "müdürlük", "müdürlüğü", "idare", "vergi", "sulh", "icra", "bölge", 
    "adliye", "daire", "ağır", "ceza", "mahkeme", "asliye", "ticaret", "sulh", "hukuk", "kadastro", "çocuk", "ilk", "derece", "1.", "2.", "3.", 
    "4.", "5.", "6.", "7.", "8.", "9.", "10."
]

ABBREVIATIONS = {
    "av": "avukat",
    "inş": "inşaat",
    "mak": "makina",
    "san": "sanayi",
    "ltd": "limited",
    "şti": "şirketi",
    "şne": "şirketine",
    "mah": "mahallesi",
    "mh": "mahallesi",
    "cad": "caddesi",
    "cd": "caddesi",
    "tckn": "kimlik numarası",
    "tckno": "kimlik numarası",
    "sk": "sokak",
    "sok": "sokak",
    "nöb": "nöbetçi",
    "işl": "işleri"
}

ALLOWEDCHARS = "."


def convertTRChars(text):

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
    
    cityDistrictNames = utils.getCityDistrictNames()  
        
    try:
        if isinstance(text, str):
            text = utils.turkish_lower(text)
            text = ' '.join(word for word in text.split() if word not in cityDistrictNames)
    except Exception as e:
        print("Error: ", e)

    return text


def removePunctuations(text):

    try:
        if isinstance(text, str):
            text = text.translate(str.maketrans(PUNCTUATIONS, ' ' * len(PUNCTUATIONS)))
    except Exception as e:
        print("Error: ", e)

    return text


def keepCharacters(text, keepNumber):

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

    try:
        if isinstance(text, str):
            pattern = re.compile(SPECIALCHARACTERS)
            text = re.sub(pattern, ' ', text)
    except Exception as e:
        print("Error: ", e)

    return text


def removeStopwords(text):

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

    try:
        if isinstance(text, str):
            text = utils.turkish_lower(text)
            text = ' '.join(word for word in text.split() if word not in ADALETUNUSEDWORDS)
    except Exception as e:
        print("Error: ", e)

    return text


def removeCommonWords(text):

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
    text = replaceAbbreviations(text)
    text = convertTRChars(text)
    text = keepCharacters(text, False)
    text = removeSingleCharacters(text)
    text = removeConsecutiveConsonants(text)
    text = removeConsecutiveVowels(text)
    
    return text


