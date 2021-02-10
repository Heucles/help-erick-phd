from lxml import etree
from lxml.html import fromstring

class MunicipioData:
    def __init__(self, conjuntoNome, dec, fec, dicAnual, dicTrim,
                 dicMensal, ficAnual, ficTrim, ficMensal, dmicMensal,
                 dicriInterrupcao, tipo):

        # tr class = res
        self.conjuntoNome = conjuntoNome  # td 0
        self.dec = dec  # td 1
        self.fec = fec  # td 2
        self.dicAnual = dicAnual  # td 3
        self.dicTrim = dicTrim  # td 4
        self.dicMensal = dicMensal  # td 5
        self.ficAnual = ficAnual  # td 6
        self.ficTrim = ficTrim  # td 7
        self.ficMensal = ficMensal  # td 8
        self.dmicMensal = dmicMensal  # td 9
        self.dicriInterrupcao = dicriInterrupcao  # td 10
        self.tipo = tipo

    
def parseIntoMunicipioData(markupRawData):
    # checka se o dado veio em branco
    if (markupRawData != ''):

        # converte o dado em html
        html = fromstring(markupRawData)

        #procura o elemento onde estão as repostas
        tables = html.find_class('res')

        response = list()

        # isso ficou feio mas como esse codigo não vai ser usado depois e vai ter que ficar mexendo, vou deixar assim
        #tem duas respostas, urbano e não urbano então vem as duas
        for i in range(0,2):
            td = tables[i]

            #pega os tipos 
            tipos = html.xpath('//*[self::span]')

            municipioData = MunicipioData(
            td[0].text_content().strip(),
            td[1].text_content(),
            td[2].text_content(),
            td[3].text_content(),
            td[4].text_content(),
            td[5].text_content(),
            td[6].text_content(),
            td[7].text_content(),
            td[8].text_content(),
            td[9].text_content(),
            td[10].text_content(),
            tipos[i].text
            )

            response.append(municipioData)
    
    return response
