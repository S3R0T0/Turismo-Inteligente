import spacy,re
from django.db import connection
from spacy.matcher import Matcher

nlp = spacy.load("Models/ner_model")
nlp_request = spacy.load("Models/request_ner")
nlp_residencia = spacy.load("Models/residencia_ner")
nlp_info_v2 = spacy.load("Models/info_v2_ner")
nlp_year = spacy.load("Models/year_ner")
nlp_mod = spacy.load("Models/mod_ner")
nlp_aero = spacy.load("Models/aereo_ner")
nlp_place_v3 = spacy.load("Models/place_v3_ner")

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
    request = [[requests_.label_,re.findall(r'\d+', requests_.text)] for requests_ in nlp_request(text).ents if len(requests_)]
    residencia = [[requests_.label_,requests_.text] for requests_ in nlp_residencia(text).ents if requests_.label_ != "year"]
    place = [[requests_.label_,requests_.text] for requests_ in nlp_place_v3(text).ents]
    aero = [[requests_.label_,requests_.text] for requests_ in nlp_aero(text).ents]
    info = [[requests_.label_,requests_.text] for requests_ in nlp_info_v2(text).ents]
    mod = [[requests_.label_,requests_.text] for requests_ in nlp_mod(text).ents]
    year = [re.findall(r'\d+', requests_.text)[0] for requests_ in nlp_year(text).ents]

    #year = [requests_.label_ for requests_ in nlp_people(text).ents if requests_.label_ == "year"]
    return {"Request": request,
            "Residencia": residencia,
            "Place": place,
            "aereo":aero,
            "mod" : mod,
            "People": info,
            "Year":year}

def process(text):
    breakDown = analize(text)
    toQuery   = queryFy(breakDown)
    result    = query(toQuery[0])

    print(toQuery[1])

    if len(breakDown["Request"]) and breakDown["Request"][0][0] == "graphRequest":
        return {"Response":createGraph(result),"Action":"Graph","Label":toQuery[1]}
    else:
        return {"Response": createList(result),"Action":"List"}


def query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()

def queryFy(nlpRequest):
    listSize = 10
    infoTable = "visitantes"
    year = nlpRequest["Year"] or [2023]
    order = "DESC"
    extranjeros = ""
    aereopuerto = ""
    residente = ""
    label = "#De Personas "

    print(nlpRequest)

    if len(nlpRequest["People"]) and nlpRequest["People"][0][0] == "info extranjeros":
        extranjeros = "and extranjero = 1"
        label = "#De Extranjeros "
    elif len(nlpRequest["People"]) and nlpRequest["People"][0][0] == "info dominicanos":
        extranjeros = "and extranjero = 0"
        label = "#De Dominicanos "

    if len(nlpRequest["Residencia"]) and nlpRequest["Residencia"][0][0] == "residencia negativa":
        extranjeros = "and residente = 0"
        label += "no residentes"
    elif len(nlpRequest["Residencia"]) and nlpRequest["Residencia"][0][0] == "residencia positiva":
        extranjeros = "and residente = 1"
        label += "residentes"

    if len(nlpRequest["mod"]) and nlpRequest["mod"][0][0] == "mod negativo":
        order = "ASC"

    if len(nlpRequest["aereo"]):
        aereopuerto = nlpRequest["aereo"][0][0]
        if nlpRequest["Year"] == "":
            year = ""
        else:
            year = f"and Y = {year[0]}"
        query_txt = f"select * from {infoTable} where aereopuerto = {aereopuerto} {year} {extranjeros} {residente} ORDER BY total {order};"

        print(query_txt)
        #input()
        return [query_txt,label]

    else:
        query_txt = f"select sum(personas) as total, aereopuerto from {infoTable} where Y = {year[0]} {extranjeros} {residente} group by aereopuerto ORDER BY total {order};"
        print(query_txt)
        #input()
        return [query_txt,label]

def createList(data):
    response = ""
    for i,item in enumerate(data):
        response += f"{i+1} {item[1]}: {item[0]}\n"
    return response

def createGraph(data):
    columns = []
    datas   = []
    for item in data:
        columns.append(item[1])
        datas.append(int(item[0]))
    return [columns,datas]