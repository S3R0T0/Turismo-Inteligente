import spacy,re
from django.db import connection
from spacy.matcher import Matcher

nlp = spacy.load("Models/ner_model")
nlp_request = spacy.load("Models/request_ner")
nlp_residencia = spacy.load("Models/residencia_ner")
nlp_info_v2 = spacy.load("Models/info_v2_ner")
nlp_year = spacy.load("Models/year_ner")
nlp_mod = spacy.load("Models/mod_ner")

nlp_place = spacy.load("Models/place_ner")

#nlp_people = spacy.load("Models/people_ner")




"""paisPatterns = [[{"TEXT": {"REGEX": "(?=.*pais)|(?=.*isla)"}}],
                [{"TEXT": {"REGEX": "(?=.*republica)|(?=.*dominicana)"}, "OP": "+"}],
                [{"TEXT": {"REGEX": "(?i)rd"}, "OP": "+"}]]

provPatterns = [[{"TEXT": {"REGEX": "(?=.*punta)|(?=.*cana)"}, "OP": "+"}]]

sitiosPatterns = [
    [{"TEXT": {"REGEX": "(?=.*playa)|(?=.*playas)|(?=.*hotel)|(?=.*hotels)|(?=.*sitio)|(?=.*sitios)"}, "OP": "+"}]]

requestPatter = [[{"POS": "NUM"}, {"TEXT": {"REGEX": "(?=.*mas)|(?=.*menos)"}, "OP": "*"},
                  {"TEXT": {"REGEX": "(?=.*mejores)|(?=.*mejor)|(?=.*peores)|(?=.*peor)|(?=.*popular)|(?=.*populares)"},
                   "OP": "*"}],
                 [{"TEXT": {"REGEX": "(?=.*lista)|(?=.*listas)|(?=.*top)|(?=.*tops)"}}],
                 [{"TEXT": {"REGEX": "(?=.*grafico)|(?=.*graficos)|(?=.*visual)|(?=.*visualizacion)"}}]]

turista = [[{"TEXT": {"REGEX": "(?=.*turista)|(?=.*turistas)|(?=.*inmigrantes)|(?=.*inmigrante)"}}]]

nacionalidad = [[{"ENT_TYPE": "LOC", "OP": "+"}]]

matcher = Matcher(nlp.vocab)
matcher.add("elPais", paisPatterns, greedy="LONGEST")
matcher.add("provincia", provPatterns, greedy="LONGEST")
matcher.add("sitios", sitiosPatterns, greedy="LONGEST")
matcher.add("request", requestPatter, greedy="LONGEST")
matcher.add("turista", turista, greedy="LONGEST")
matcher.add("nacionalidad", nacionalidad, greedy="LONGEST")"""


def analize(text):
    request = [[requests_.label_,re.findall(r'\d+', requests_.text)[0]] for requests_ in nlp_request(text).ents]
    residencia = [[requests_.label_,requests_.text] for requests_ in nlp_residencia(text).ents if requests_.label_ != "year"]
    place = [[requests_.label_,requests_.text] for requests_ in nlp_place(text).ents]
    info = [[requests_.label_,requests_.text] for requests_ in nlp_info_v2(text).ents]
    mod = [[requests_.label_,requests_.text] for requests_ in nlp_mod(text).ents]
    year = [re.findall(r'\d+', requests_.text)[0] for requests_ in nlp_year(text).ents]

    #year = [requests_.label_ for requests_ in nlp_people(text).ents if requests_.label_ == "year"]
    return {"Request": request,
            "mod" : mod,
            "People": info,
            "Residencia":residencia,
            "Place": place,
            "Year":year}

def process(text):
    breakDown = analize(text)
    print(breakDown)
    doc = nlp(text)
    request = []

    return None
'''
    doc = nlp(text)
    matches = matcher(doc)
    matches.sort(key=lambda x: x[1])

    elementos = []

    last = ""
    for i in matches:
        if nlp.vocab[i[0]].text == "request" and not (last == "request"):
            elementos.append(
                {"request": [doc[i[1]:i[2]].text], "sitios": [], "provincias": [], "nacionalidad": [], "elPais": [],
                 "turista": []})
        else:
            for e in elementos:
                e[nlp.vocab[i[0]].text].append(doc[i[1]:i[2]].text)
        last = nlp.vocab[i[0]].text
    return "elementos"'''



def query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()

def listTop(nlpRequest):
    listSize = 10
    year = 2023
    month = ""
    extranjeros = ""
    infoTable = "visitantes"
    result = query(f"select sum(personas) as total,aereopuerto from {infoTable} where Y = {year} {month} {extranjeros} group by aereopuerto order by total desc")
    nlpResponse = "Aqui la cantidad de visitantes en los aereopuertos princiaples:\n"
    for index,item in enumerate(result):
        nlpResponse += f"\n{index+1}. {item[1].title()} con {int(item[0])} visitantes"
    return nlpResponse

def createGraph(nlpRequest):
    table = "visitantes"
    year = ""
    queryMsg = f"select * from {table} where Y = 2000"
    result = query(queryMsg)
    for index, item in enumerate(result):
       pass
       #print(item)
    return "a"