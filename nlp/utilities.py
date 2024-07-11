import spacy,re
from django.db import connection
from spacy.matcher import Matcher

nlp = spacy.load("Models/ner_model")
nlp_request = spacy.load("Models/Request_NER_3")
nlp_residencia = spacy.load("Models/residencia_ner")
nlp_info_v2 = spacy.load("Models/info_v2_ner")
nlp_year = spacy.load("Models/year_ner")
nlp_mod = spacy.load("Models/mod_ner")
nlp_aero = spacy.load("Models/aereo_ner")
nlp_place_v3 = spacy.load("Models/place_v3_ner")
nlp_gastos = spacy.load("Models/gastos_NER")

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
    request = [[requests_.label_,requests_.text] for requests_ in nlp_request(text).ents if len(requests_)]
    residencia = [[requests_.label_,requests_.text] for requests_ in nlp_residencia(text).ents if requests_.label_ != "year"]
    place = [[requests_.label_,requests_.text] for requests_ in nlp_place_v3(text).ents]
    aero = [[requests_.label_,requests_.text] for requests_ in nlp_aero(text).ents]
    info = [[requests_.label_,requests_.text] for requests_ in nlp_info_v2(text).ents]
    mod = [[requests_.label_,requests_.text] for requests_ in nlp_mod(text).ents]
    year = [re.findall(r'\d+', requests_.text)[0] for requests_ in nlp_year(text).ents]
    gastos = [[requests_.label_,re.findall(r'\d+', requests_.text)] for requests_ in nlp_request(text).ents if len(requests_)]

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
    year      = 2023

    if len(breakDown["Year"]):
        year = breakDown["Year"][0]

    print(breakDown)

    acttions = list()

    if len(breakDown["Request"]) and breakDown["Request"][0][0] == "R_Graph":
        acttions.append({"Response":createGraph(result,year),"Action":"Graph","Label":toQuery[1],"year":year})
    if len(breakDown["Request"]) and breakDown["Request"][0][0] == "R_Lista":
        acttions.append({"Response": createList(result,year),"Action":"List","year":year})

    return acttions

def query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()

def queryFy(nlpRequest):
    listSize = 20
    infoTable = "visitantes"
    year = nlpRequest["Year"] or [2023]
    order = "DESC"
    extranjeros = ""
    aereopuerto = ""
    residente = ""
    label = "#De Personas "

    #print(nlpRequest)

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
        aereopuerto = "("
        for i in nlpRequest["aereo"]:
            print(i[0])
            aereopuerto += f"'{i[0]}',"
        aereopuerto = aereopuerto[:-1] + ")"
        if len(nlpRequest["Year"]) == 0 or nlpRequest["Year"][0] == "":
            year = ""
        else:
            year = f"and Y = {year[0]}"
        query_txt = f"select sum(personas),Y,aereopuerto from {infoTable} where aereopuerto in {aereopuerto} {year} {extranjeros} {residente} GROUP BY aereopuerto, Y ORDER BY aereopuerto,Y {order};"
        #print(query_txt)
        return [query_txt,label]

    else:
        query_txt = f"select sum(personas) as total, aereopuerto from {infoTable} where Y = {year[0]} {extranjeros} {residente} group by aereopuerto ORDER BY total {order};"
        #print(query_txt)
        return [query_txt,label]

def createList(data,year):
    response = f"Datos del año {year}\n"
    last = ""
    offset = 0
    for i,item in enumerate(data):
        if {item[2]} != last:
            response += "\nEn " + item[2] + "\n"
            offset = i
        response += f"{item[1]}: {item[0]}\n"
        last = {item[2]}
    return response

def createGraph(data,year):
    datas   = {}
    # provincia 2, year 1, data 0
    for item in data:
        if not (item[2] in datas):
            datas[item[2]] = []
        print([int(item[0]),item[1]])
        datas[item[2]].append([int(item[0]),item[1]])

    print(datas)
    return datas