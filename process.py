import requests
from lxml import etree
import numpy as np
import pandas as pd

from municipio_data import MunicipioData, parseIntoMunicipioData

# pega os conjuntos que tem para aquele municipio em um determinado ano
def getConjuntosAvailableForMunicipioByAno(estado, municipioCode, ano):
    url = 'https://www2.aneel.gov.br/aplicacoes_liferay/srd/indqual/dspConjunto.cfm?ano=' + ano + '&estado=' + estado + '&municipio=' + municipioCode
    response = requests.get(url)
    data = response.text
    tree = etree.fromstring(data)

    conjuntos = []

    for leaf in tree:
        # o que queremos é o valor que esta dentro da tag
        if (leaf.attrib['value'] != '0'):
            conjuntos.append(leaf.attrib['value'])

    return conjuntos

# pega os dados de fato para o municipio em um determninado ano
def getMarkupDataFromMunicipioByConjuntoAndAno(estado, municipioCode, ano, conjuntoCode):
    url = 'https://www2.aneel.gov.br/aplicacoes_liferay/srd/indqual/dspIndicadores.cfm?municipio=' + municipioCode + '&conjunto=' + conjuntoCode + '&ano=' + ano + '&estado=' + estado
    response = requests.get(url)
    data = response.text
    return data

# lendo parametros de entrada
entries = np.genfromtxt('source.csv',
                      delimiter=';',
                      dtype='|U30,<U30,U10,<U4',
                      skip_header=1)


# abre arquivo de output onde colocaremos as respostas
with open('output.csv', 'w+') as f:
    header = True
    columns = [
        'municipio', 'municipioCode', 'estado', 'ano', 'conjuntoNome',
        'conjunto', 'dec', 'fec', 'dicAnual', 'dicTrim', 'dicMensal',
        'ficAnual', 'ficTrim', 'ficMensal', 'dmicMensal',
        'dicriInterrupcao', 'tipo'
    ]

    # itera na quantidade de entradas que foram passadas no arquivo source.csv
    for i in range(len(entries)):
        print('############ COMEÇANDO A PEGAR DADOS ##############')
        print('Municipio:', str(entries[i][0]))
        print('Estado:', str(entries[i][2]))

        paramEstado = str(entries[i][2])
        paramMunicipio = str(entries[i][0])
        paramMunicipioCode = str(entries[i][1])
        paramAno = entries[i][3]

        conjuntos = getConjuntosAvailableForMunicipioByAno(paramEstado, paramMunicipioCode, paramAno)

        print('------- RECUPERADOS CONJUNTOS ----------')
        print('------- COLETANDO OS DADOS PARA CADA CONJUNTO NO ANO DE: '+paramAno+'----------')
        for i in range(len(conjuntos) - 1):
            
            print('******* '+ str(i+1) + ' de ' + str(len(conjuntos)) + ' ****** CONJUNTO: ' + conjuntos[i] + ' ******')

            # pega o html que vem no portalzinho do IBGE la
            municipioMarkupData = getMarkupDataFromMunicipioByConjuntoAndAno(paramEstado, paramMunicipioCode,
                                    paramAno, conjuntos[i])

            # converte esse html em um objeto
            municipioData = parseIntoMunicipioData(municipioMarkupData)

            # converte o objeto em um csv, sempre tem 2 no retorno do metodo getMarkupDataFromMunicipioByConjuntoAndAno porque 
            # tem o "urbano" e o "não urbano"
            municipioDataCsvPrepared = pd.DataFrame(
                [[
                    paramMunicipio, paramMunicipioCode, paramEstado, paramAno,
                    municipioData[0].conjuntoNome, conjuntos[i],
                    municipioData[0].dec, municipioData[0].fec,
                    municipioData[0].dicAnual, municipioData[0].dicTrim,
                    municipioData[0].dicMensal, municipioData[0].ficAnual,
                    municipioData[0].ficTrim, municipioData[0].ficMensal,
                    municipioData[0].dmicMensal,
                    municipioData[0].dicriInterrupcao, municipioData[0].tipo
                ],
                [
                    paramMunicipio, paramMunicipioCode, paramEstado, paramAno,
                    municipioData[1].conjuntoNome, conjuntos[i],
                    municipioData[1].dec, municipioData[1].fec,
                    municipioData[1].dicAnual, municipioData[1].dicTrim,
                    municipioData[1].dicMensal, municipioData[1].ficAnual,
                    municipioData[1].ficTrim, municipioData[1].ficMensal,
                    municipioData[1].dmicMensal,
                    municipioData[1].dicriInterrupcao, municipioData[1].tipo
                ]],
                columns=[
                    'municipio', 'municipioCode', 'estado', 'ano',
                    'conjuntoNome', 'conjunto', 'dec', 'fec', 'dicAnual',
                    'dicTrim', 'dicMensal', 'ficAnual', 'ficTrim', 'ficMensal',
                    'dmicMensal', 'dicriInterrupcao', 'tipo'
                ])

            municipioDataCsvPrepared = municipioDataCsvPrepared[columns]
            mode = 'w' if header else 'a'
            municipioDataCsvPrepared.to_csv(path_or_buf=f,
                        mode=mode,
                        header=header,
                        index=False,
                        sep='|')
            header = False

        print('############ TERMINADO ##############')

f.close()
