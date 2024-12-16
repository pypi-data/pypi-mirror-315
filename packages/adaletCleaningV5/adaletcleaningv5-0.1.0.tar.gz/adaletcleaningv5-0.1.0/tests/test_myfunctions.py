from adaletCleaningV5 import myfunctions



def test_convertTRChars():
    text = "İstanbul güzel bir şehir"
    expected = "Istanbul guzel bir sehir"
    print(myfunctions.convertTRChars(text))
    assert myfunctions.convertTRChars(text) == expected

def test_lowercase():
    text = "T.C. KÜÇÜK HARFLERE ÇEVİR"
    expected = " tc  küçük harflere çevir"
    print(myfunctions.lowercase(text))
    assert myfunctions.lowercase(text) == expected

def test_removeCityDistrictNames():

    text = "İstanbul Kadıköy güzel bir yer"
    expected = "güzel bir yer"
    print(myfunctions.removeCityDistrictNames(text))
    assert myfunctions.removeCityDistrictNames(text) == expected

def test_removePunctuations():

    text = "Merhaba, dünya! Nasıl?"
    expected = "Merhaba  dünya  Nasıl "
    print(myfunctions.removePunctuations(text))
    assert myfunctions.removePunctuations(text) == expected

def test_keepCharacters():
    text = "abc&%123 xyz"
    expected = "abc      xyz"
    print(myfunctions.keepCharacters(text, False))
    print(myfunctions.keepCharacters(text, True))
    assert myfunctions.keepCharacters(text, keepNumber=False) == expected
    assert myfunctions.keepCharacters(text, True) == "abc  123 xyz"

def test_removeSpecialCharacters():
 
    text = "«test»—data”"
    expected = " test  data "
    print(myfunctions.removeSpecialCharacters(text))
    assert myfunctions.removeSpecialCharacters(text) == expected

def test_removeStopwords():

    text = "Bu test   cümlesi ile deneme"
    expected = "test cümlesi deneme"
    print(myfunctions.removeStopwords(text))
    assert myfunctions.removeStopwords(text) == expected

def test_removeSingleCharacters():
    text = "a test cümlesi b c d"
    expected = "test cümlesi"
    print(myfunctions.removeSingleCharacters(text))
    assert myfunctions.removeSingleCharacters(text) == expected

def test_removeUnusedWords():

    text = "imzalıdır bu örnek bir metindir"
    expected = "bu örnek bir metindir"
    print(myfunctions.removeUnusedWords(text))
    assert myfunctions.removeUnusedWords(text) == expected

def test_removeCommonWords():

    text = "Bu Ticaret hukuk test"
    expected = "bu test"
    print(myfunctions.removeCommonWords(text))
    assert myfunctions.removeCommonWords(text) == expected

def test_removeConsecutiveConsonants():
    text = "bcdc kfg güzel"
    expected = "kfg güzel"
    print(myfunctions.removeConsecutiveConsonants(text))
    assert myfunctions.removeConsecutiveConsonants(text) == expected

def test_removeConsecutiveVowels():
    text = "aai aa güzel"
    expected = "aa güzel"
    print(myfunctions.removeConsecutiveVowels(text))
    assert myfunctions.removeConsecutiveVowels(text) == expected

def test_cleanSpaces():
    text = "  Bu  bir    test.  "
    expected = "Bu bir test."
    print(myfunctions.cleanSpaces(text))
    assert myfunctions.cleanSpaces(text) == expected

def test_replaceAbbreviations():

    text = "Av. Ahmet ve inş"
    expected = "avukat. ahmet ve inşaat"
    print(myfunctions.replaceAbbreviations(text))
    assert myfunctions.replaceAbbreviations(text) == expected

def test_allowOnlySpecificCharacters():
    
    text = "abc@!10 x.yz"
    expected = "abc  10 x.yz"
    print(myfunctions.allowOnlySpecificCharacters(text, True))
    assert myfunctions.allowOnlySpecificCharacters(text, isSpecialCharacters=True) == expected

def test_text_normalizer():

    text = "T.C. Av. Mehmet Kadıköy'den10 İstanbul'a geçti."
    expected = "tc avukat mehmet den gecti"
    print(myfunctions.text_normalizer(text))
    assert myfunctions.text_normalizer(text) == expected

if __name__ == "__main__":
    test_convertTRChars()
    test_lowercase()
    test_removeCityDistrictNames()
    test_removePunctuations()
    test_keepCharacters()
    test_removeSpecialCharacters()
    test_removeStopwords()
    test_removeSingleCharacters()
    test_removeUnusedWords()
    test_removeCommonWords()
    test_removeConsecutiveConsonants()
    test_removeConsecutiveVowels()
    test_cleanSpaces()
    test_replaceAbbreviations()
    test_allowOnlySpecificCharacters()
    test_text_normalizer()
    print("Tüm testler başarıyla geçti!")