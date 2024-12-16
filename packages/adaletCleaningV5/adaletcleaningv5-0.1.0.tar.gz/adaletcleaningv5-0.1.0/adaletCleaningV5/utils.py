import re
from itertools import chain
import xml.etree.ElementTree as elemTree


def encodeTextToArray(text, commonwords, fullTextSearch=False):

    encodeText = []
    indexArr = []
    if commonwords is not None:
        # encodeText = [1 if word in commonwords else 0 for word in text.split(' ')]
        for idx, word in enumerate(text.split(' ')):
            isExists = 0
            if word in commonwords:       
                isExists = 1
            else:
                for commonword in commonwords:   
                    # if commonword in word
                    if fullTextSearch:
                        if commonword in word:
                            isExists = 1
                            break
                    else:
                        # if word starting with commonword
                        pattern = f"^{commonword}"
                        if re.match(pattern, word):
                            isExists = 1
                            break
            encodeText.append(isExists)

        # assign initial values of -1
        startIdx = -1
        endIdx = -1
        # condition that array has reached at last, if exists then continue to append
        encodeText.append(-1)
        for idx, code in enumerate(encodeText):
            if code > 0:
                if startIdx == -1:
                    startIdx = idx
                endIdx = idx
            else:
                if endIdx > startIdx:
                    indexArr.append([startIdx,endIdx])
                startIdx = -1
                endIdx = -1

    return encodeText, indexArr


def removeElements(text, indices):
    # merge arrays in a list which contains only removable elements
    totalIdx = [list(range(arr[0], arr[1]+1)) for arr in indices]
    totalIdx = list(chain.from_iterable(totalIdx))
    # Reversing Indices List
    indicesList = sorted(totalIdx, reverse=True)
    # Traversing in the indices list
    for indx in indicesList:
        # checking whether the corresponding iterator index is less than the list length
        if indx < len(text):
            # removing element by index
            text.pop(indx)
    return text


def consonantConsecutiveList(word, count):
    consonant_list = re.split(r"[aeıiou]+", word, flags=re.I)
    return [y for y in consonant_list if len(y) > count]


def vowelConsecutiveList(word, count):
    consonant_list = re.split(r"[bcdfghjklmnprstvyz]+", word, flags=re.I)
    return [y for y in consonant_list if len(y) > count]


def turkish_lower(text):
    text = text.replace("T.C.", " tc ")
    text = re.sub(r'İ', 'i', text)
    text = re.sub(r'I', 'ı', text)
    text = text.lower()
    return text


def turkish_upper(text):
    text = re.sub(r'i', 'İ', text)
    text = text.upper()
    return text




def getCityDistrictNames():


    cityNames = ["Adana","Adıyaman","Afyonkarahisar","Ağrı","Amasya","Ankara","Antalya","Artvin","Aydın","Balıkesir","Bilecik","Bingöl","Bitlis",
                 "Bolu","Burdur","Bursa","Çanakkale","Çankırı","Çorum","Denizli","Diyarbakır","Edirne","Elazığ","Erzincan","Erzurum","Eskişehir",
                 "Gaziantep","Giresun","Gümüşhane","Hakkari","Hatay","Isparta","Mersin","İstanbul","İzmir","Kars","Kastamonu","Kayseri",
                 "Kırklareli","Kırşehir","Kocaeli","Konya","Kütahya","Malatya","Manisa","Kahramanmaraş","Mardin","Muğla","Muş","Nevşehir","Niğde",
                 "Ordu","Rize","Sakarya","Samsun","Siirt","Sinop","Sivas","Tekirdağ","Tokat","Trabzon","Tunceli","Şanlıurfa","Uşak","Van",
                 "Yozgat","Zonguldak","Aksaray","Bayburt","Karaman","Kırıkkale","Batman","Şırnak","Bartın","Ardahan","Iğdır","Yalova","Karabük",
                 "Kilis","Osmaniye","Düzce"]
    districtNames = [
            "Seyhan","Ceyhan","Feke","Karaisalı","Karataş","Kozan","Pozantı","Saimbeyli","Tufanbeyli","Yumurtalık","Yüreğir","Aladağ","İmamoğlu","Sarıçam","Çukurova",
            "Adıyaman Merkez","Besni","Çelikhan","Gerger","Gölbaşı","Kahta","Samsat","Sincik","Tut",
            "Afyonkarahisar Merkez","Bolvadin","Çay","Dazkırı","Dinar","Emirdağ","İhsaniye","Sandıklı","Sinanpaşa","Sultandağı","Şuhut","Başmakçı","Bayat","İscehisar","Çobanlar","Evciler","Hocalar","Kızılören",
            "Ağrı Merkez","Diyadin","Doğubayazıt","Eleşkirt","Hamur","Patnos","Taşlıçay","Tutak",
            "Amasya Merkez","Göynücek","Gümüşhacıköy","Merzifon","Suluova","Taşova","Hamamözü",
            "Altındağ","Ayaş","Bala","Beypazarı","Çamlıdere","Çankaya","Çubuk","Elmadağ","Güdül","Haymana","Kalecik","Kızılcahamam","Nallıhan","Polatlı","Şereflikoçhisar","Yenimahalle","Gölbaşı","Keçiören","Mamak","Sincan","Kazan","Akyurt","Etimesgut","Evren","Pursaklar",
            "Akseki","Alanya","Elmalı","Finike","Gazipaşa","Gündoğmuş","Kaş","Korkuteli","Kumluca","Manavgat","Serik","Demre","İbradı","Kemer","Aksu","Döşemealtı","Kepez","Konyaaltı","Muratpaşa",
            "Ardanuç","Arhavi","Artvin Merkez","Borçka","Hopa","Şavşat","Yusufeli","Murgul",
            "Bozdoğan","Çine","Germencik","Karacasu","Koçarlı","Kuşadası","Kuyucak","Nazilli","Söke","Sultanhisar","Yenipazar","Buharkent","İncirliova","Karpuzlu","Köşk","Didim","Efeler",
            "Ayvalık","Balya","Bandırma","Bigadiç","Burhaniye","Dursunbey","Edremit","Erdek","Gönen","Havran","İvrindi","Kepsut","Manyas","Savaştepe","Sındırgı","Susurluk","Marmara","Gömeç","Altıeylül","Karesi",
            "Bilecik Merkez","Bozüyük","Gölpazarı","Osmaneli","Pazaryeri","Söğüt","Yenipazar","İnhisar",
            "Bingöl Merkez","Genç","Karlıova","Kiğı","Solhan","Adaklı","Yayladere","Yedisu",
            "Adilcevaz","Ahlat","Bitlis Merkez","Hizan","Mutki","Tatvan","Güroymak",
            "Bolu Merkez","Gerede","Göynük","Kıbrıscık","Mengen","Mudurnu","Seben","Dörtdivan","Yeniçağa",
            "Ağlasun","Bucak","Burdur Merkez","Gölhisar","Tefenni","Yeşilova","Karamanlı","Kemer","Altınyayla","Çavdır","Çeltikçi",
            "Gemlik","İnegöl","İznik","Karacabey","Keles","Mudanya","Mustafakemalpaşa","Orhaneli","Orhangazi","Yenişehir","Büyükorhan","Harmancık","Nilüfer","Osmangazi","Yıldırım","Gürsu","Kestel",
            "Ayvacık","Bayramiç","Biga","Bozcaada","Çan","Çanakkale Merkez","Eceabat","Ezine","Gelibolu","Gökçeada","Lapseki","Yenice",
            "Çankırı Merkez","Çerkeş","Eldivan","Ilgaz","Kurşunlu","Orta","Şabanözü","Yapraklı","Atkaracalar","Kızılırmak","Bayramören","Korgun",
            "Alaca","Bayat","Çorum Merkez","İskilip","Kargı","Mecitözü","Ortaköy","Osmancık","Sungurlu","Boğazkale","Uğurludağ","Dodurga","Laçin","Oğuzlar",
            "Acıpayam","Buldan","Çal","Çameli","Çardak","Çivril","Güney","Kale","Sarayköy","Tavas","Babadağ","Bekilli","Honaz","Serinhisar","Pamukkale","Baklan","Beyağaç","Bozkurt","Merkezefendi",
            "Bismil","Çermik","Çınar","Çüngüş","Dicle","Ergani","Hani","Hazro","Kulp","Lice","Silvan","Eğil","Kocaköy","Bağlar","Kayapınar","Sur","Yenişehir",
            "Edirne Merkez","Enez","Havsa","İpsala","Keşan","Lalapaşa","Meriç","Uzunköprü","Süloğlu",
            "Ağın","Baskil","Elazığ Merkez","Karakoçan","Keban","Maden","Palu","Sivrice","Arıcak","Kovancılar","Alacakaya",
            "Çayırlı","Erzincan Merkez","İliç","Kemah","Kemaliye","Refahiye","Tercan","Üzümlü","Otlukbeli",
            "Aşkale","Çat","Hınıs","Horasan","İspir","Karayazı","Narman","Oltu","Olur","Pasinler","Şenkaya","Tekman","Tortum","Karaçoban","Uzundere","Pazaryolu","Aziziye","Köprüköy","Palandöken","Yakutiye",
            "Çifteler","Mahmudiye","Mihalıççık","Sarıcakaya","Seyitgazi","Sivrihisar","Alpu","Beylikova","İnönü","Günyüzü","Han","Mihalgazi","Odunpazarı","Tepebaşı",
            "Araban","İslahiye","Nizip","Oğuzeli","Yavuzeli","Şahinbey","Şehitkamil","Karkamış","Nurdağı",
            "Alucra","Bulancak","Dereli","Espiye","Eynesil","Giresun Merkez","Görele","Keşap","Şebinkarahisar","Tirebolu","Piraziz","Yağlıdere","Çamoluk","Çanakçı","Doğankent","Güce",
            "Gümüşhane Merkez","Kelkit","Şiran","Torul","Köse","Kürtün",
            "Çukurca","Hakkari Merkez","Şemdinli","Yüksekova",
            "Altınözü","Dörtyol","Hassa","İskenderun","Kırıkhan","Reyhanlı","Samandağ","Yayladağı","Erzin","Belen","Kumlu","Antakya","Arsuz","Defne","Payas",
            "Atabey","Eğirdir","Gelendost","Isparta Merkez","Keçiborlu","Senirkent","Sütçüler","Şarkikaraağaç","Uluborlu","Yalvaç","Aksu","Gönen","Yenişarbademli",
            "Anamur","Erdemli","Gülnar","Mut","Silifke","Tarsus","Aydıncık","Bozyazı","Çamlıyayla","Akdeniz","Mezitli","Toroslar","Yenişehir",
            "Adalar","Bakırköy","Beşiktaş","Beykoz","Beyoğlu","Çatalca","Eyüp","Fatih","Gaziosmanpaşa","Kadıköy","Kartal","Sarıyer","Silivri","Şile","Şişli","Üsküdar","Zeytinburnu","Büyükçekmece","Kağıthane","Küçükçekmece","Pendik","Ümraniye","Bayrampaşa","Avcılar","Bağcılar","Bahçelievler","Güngören","Maltepe","Sultanbeyli","Tuzla","Esenler","Arnavutköy","Ataşehir","Başakşehir","Beylikdüzü","Çekmeköy","Esenyurt","Sancaktepe","Sultangazi",
            "Aliağa","Bayındır","Bergama","Bornova","Çeşme","Dikili","Foça","Karaburun","Karşıyaka","Kemalpaşa","Kınık","Kiraz","Menemen","Ödemiş","Seferihisar","Selçuk","Tire","Torbalı","Urla","Beydağ","Buca","Konak","Menderes","Balçova","Çiğli","Gaziemir","Narlıdere","Güzelbahçe","Bayraklı","Karabağlar",
            "Arpaçay","Digor","Kağızman","Kars Merkez","Sarıkamış","Selim","Susuz","Akyaka",
            "Abana","Araç","Azdavay","Bozkurt","Cide","Çatalzeytin","Daday","Devrekani","İnebolu","Kastamonu Merkez","Küre","Taşköprü","Tosya","İhsangazi","Pınarbaşı","Şenpazar","Ağlı","Doğanyurt","Hanönü","Seydiler",
            "Bünyan","Develi","Felahiye","İncesu","Pınarbaşı","Sarıoğlan","Sarız","Tomarza","Yahyalı","Yeşilhisar","Akkışla","Talas","Kocasinan","Melikgazi","Hacılar","Özvatan",
            "Babaeski","Demirköy","Kırklareli Merkez","Kofçaz","Lüleburgaz","Pehlivanköy","Pınarhisar","Vize",
            "Çiçekdağı","Kaman","Kırşehir Merkez","Mucur","Akpınar","Akçakent","Boztepe",
            "Gebze","Gölcük","Kandıra","Karamürsel","Körfez","Derince","Başiskele","Çayırova","Darıca","Dilovası","İzmit","Kartepe",
            "Akşehir","Beyşehir","Bozkır","Cihanbeyli","Çumra","Doğanhisar","Ereğli","Hadim","Ilgın","Kadınhanı","Karapınar","Kulu","Sarayönü","Seydişehir","Yunak","Akören","Altınekin","Derebucak","Hüyük","Karatay","Meram","Selçuklu","Taşkent","Ahırlı","Çeltik","Derbent","Emirgazi","Güneysınır","Halkapınar","Tuzlukçu","Yalıhüyük",
            "Altıntaş","Domaniç","Emet","Gediz","Kütahya Merkez","Simav","Tavşanlı","Aslanapa","Dumlupınar","Hisarcık","Şaphane","Çavdarhisar","Pazarlar",
            "Akçadağ","Arapgir","Arguvan","Darende","Doğanşehir","Hekimhan","Pütürge","Yeşilyurt","Battalgazi","Doğanyol","Kale","Kuluncak","Yazıhan",
            "Akhisar","Alaşehir","Demirci","Gördes","Kırkağaç","Kula","Salihli","Sarıgöl","Saruhanlı","Selendi","Soma","Turgutlu","Ahmetli","Gölmarmara","Köprübaşı","Şehzadeler","Yunusemre",
            "Afşin","Andırın","Elbistan","Göksun","Pazarcık","Türkoğlu","Çağlayancerit","Ekinözü","Nurhak","Dulkadiroğlu","Onikişubat",
            "Derik","Kızıltepe","Mazıdağı","Midyat","Nusaybin","Ömerli","Savur","Dargeçit","Yeşilli","Artuklu",
            "Bodrum","Datça","Fethiye","Köyceğiz","Marmaris","Milas","Ula","Yatağan","Dalaman","Ortaca","Kavaklıdere","Menteşe","Seydikemer",
            "Bulanık","Malazgirt","Muş Merkez","Varto","Hasköy","Korkut",
            "Avanos","Derinkuyu","Gülşehir","Hacıbektaş","Kozaklı","Nevşehir Merkez","Ürgüp","Acıgöl",
            "Bor","Çamardı","Niğde Merkez","Ulukışla","Altunhisar","Çiftlik",
            "Akkuş","Aybastı","Fatsa","Gölköy","Korgan","Kumru","Mesudiye","Perşembe","Ulubey","Ünye","Gülyalı","Gürgentepe","Çamaş","Çatalpınar","Çaybaşı","İkizce","Kabadüz","Kabataş","Altınordu",
            "Ardeşen","Çamlıhemşin","Çayeli","Fındıklı","İkizdere","Kalkandere","Pazar","Rize Merkez","Güneysu","Derepazarı","Hemşin","İyidere",
            "Akyazı","Geyve","Hendek","Karasu","Kaynarca","Sapanca","Kocaali","Pamukova","Taraklı","Ferizli","Karapürçek","Söğütlü","Adapazarı","Arifiye","Erenler","Serdivan",
            "Alaçam","Bafra","Çarşamba","Havza","Kavak","Ladik","Terme","Vezirköprü","Asarcık","19 Mayıs","Salıpazarı","Tekkeköy","Ayvacık","Yakakent","Atakum","Canik","İlkadım",
            "Baykan","Eruh","Kurtalan","Pervari","Siirt Merkez","Şirvan","Tillo",
            "Ayancık","Boyabat","Durağan","Erfelek","Gerze","Sinop Merkez","Türkeli","Dikmen","Saraydüzü",
            "Divriği","Gemerek","Gürün","Hafik","İmranlı","Kangal","Koyulhisar","Sivas Merkez","Suşehri","Şarkışla","Yıldızeli","Zara","Akıncılar","Altınyayla","Doğanşar","Gölova","Ulaş",
            "Çerkezköy","Çorlu","Hayrabolu","Malkara","Muratlı","Saray","Şarköy","Marmaraereğlisi","Ergene","Kapaklı","Süleymanpaşa",
            "Almus","Artova","Erbaa","Niksar","Reşadiye","Tokat Merkez","Turhal","Zile","Pazar","Yeşilyurt","Başçiftlik","Sulusaray",
            "Akçaabat","Araklı","Arsin","Çaykara","Maçka","Of","Sürmene","Tonya","Vakfıkebir","Yomra","Beşikdüzü","Şalpazarı","Çarşıbaşı","Dernekpazarı","Düzköy","Hayrat","Köprübaşı","Ortahisar",
            "Çemişgezek","Hozat","Mazgirt","Nazımiye","Ovacık","Pertek","Pülümür","Tunceli Merkez",
            "Akçakale","Birecik","Bozova","Ceylanpınar","Halfeti","Hilvan","Siverek","Suruç","Viranşehir","Harran","Eyyübiye","Haliliye","Karaköprü",
            "Banaz","Eşme","Karahallı","Sivaslı","Ulubey","Uşak Merkez",
            "Başkale","Çatak","Erciş","Gevaş","Gürpınar","Muradiye","Özalp","Bahçesaray","Çaldıran","Edremit","Saray","İpekyolu","Tuşba",
            "Akdağmadeni","Boğazlıyan","Çayıralan","Çekerek","Sarıkaya","Sorgun","Şefaatli","Yerköy","Yozgat Merkez","Aydıncık","Çandır","Kadışehri","Saraykent","Yenifakılı",
            "Çaycuma","Devrek","Ereğli","Zonguldak Merkez","Alaplı","Gökçebey","Kilimli","Kozlu",
            "Aksaray Merkez","Ortaköy","Ağaçören","Güzelyurt","Sarıyahşi","Eskil","Gülağaç",
            "Bayburt Merkez","Aydıntepe","Demirözü",
            "Ermenek","Karaman Merkez","Ayrancı","Kazımkarabekir","Başyayla","Sarıveliler",
            "Delice","Keskin","Kırıkkale Merkez","Sulakyurt","Bahşili","Balışeyh","Çelebi","Karakeçili","Yahşihan",
            "Batman Merkez","Beşiri","Gercüş","Kozluk","Sason","Hasankeyf",
            "Beytüşşebap","Cizre","İdil","Silopi","Şırnak Merkez","Uludere","Güçlükonak",
            "Bartın Merkez","Kurucaşile","Ulus","Amasra",
            "Ardahan Merkez","Çıldır","Göle","Hanak","Posof","Damal",
            "Aralık","Iğdır Merkez","Tuzluca","Karakoyunlu",
            "Yalova Merkez","Altınova","Armutlu","Çınarcık","Çiftlikköy","Termal",
            "Eflani","Eskipazar","Karabük Merkez","Ovacık","Safranbolu","Yenice",
            "Kilis Merkez","Elbeyli","Musabeyli","Polateli",
            "Bahçe","Kadirli","Osmaniye Merkez","Düziçi","Hasanbeyli","Sumbas","Toprakkale",
            "Akçakoca","Düzce Merkez","Yığılca","Cumayeri","Gölyaka","Çilimli","Gümüşova","Kaynaşlı"]
    
    cityNames = [turkish_lower(city) for city in cityNames]
    districtNames = [turkish_lower(district) for district in districtNames]

    cityDistrictNames = list(set(cityNames)) + list(set(districtNames))

    return list(set(cityDistrictNames))

