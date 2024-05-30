import spacy
from spacy.matcher import Matcher

nlp = spacy.load("es_core_news_lg")
doc = nlp("dame los 10 mas populares en un grafico hoteles y playas de santo domingo")

paisPatterns = [[{"TEXT": {"REGEX": "(?=.*pais)|(?=.*isla)"}}],
                [{"TEXT": {"REGEX": "(?=.*republica)|(?=.*dominicana)"}, "OP": "+"}],
                [{"TEXT": {"REGEX": "(?i)rd"}, "OP": "+"}]]

provPatterns = [[{"TEXT": {"REGEX": "(?=.*punta)|(?=.*cana)"}, "OP": "+"}]]

sitiosPatterns = [
    [{"TEXT": {"REGEX": "(?=.*playa)|(?=.*playas)|(?=.*hotel)|(?=.*hotels)|(?=.*sitio)|(?=.*sitios)"}, "OP": "+"}]]

requestPatter = [[{"POS": "NUM"}, {"TEXT": {"REGEX": "(?=.*mas)|(?=.*menos)"}, "OP": "*"},
                  {"TEXT": {"REGEX": "(?=.*mejores)|(?=.*mejor)|(?=.*peores)|(?=.*peor)|(?=.*popular)|(?=.*populares)"},
                   "OP": "+"}],
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
matcher.add("nacionalidad", nacionalidad, greedy="LONGEST")


def process():
    matches = matcher(doc)
    matches.sort(key=lambda x: x[1])

    elementos = []

    last = ""
    print("AAA")
    for i in matches:
        if nlp.vocab[i[0]].text == "request" and not (last == "request"):
            elementos.append({"request": [doc[i[1]:i[2]].text], "sitios": [], "provincias": [], "nacionalidad": []})
        else:
            for e in elementos:
                e[nlp.vocab[i[0]].text].append(doc[i[1]:i[2]].text)
        last = nlp.vocab[i[0]].text

    return elementos

