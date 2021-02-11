# help-erick-phd
Esse repo é um help para meu irmão para pegar dados do IBGE referentes a consumo de energia


# Crie seu virtualenv
Navegue até o diretório onde baixou o projeto e digite:

```virtualenv --python=${PYTHON_PATH}/python3.7 help-erick```

1. Para descobrir o path do python para usar no comando acima, digite: 

```which python```

ou no windows:

```
python
>>> import os
>>> import sys
>>> os.path.dirname(sys.executable)
```


### Recomendações:

* Recomendo aqui que seja instalado pelo menos o [python3.7](https://www.python.org/downloads/release/python-370/)

* Para instalar o virtualenv siga [essas instruções](https://pypi.org/project/virtualenv)

continuando...

2. Depois para ativá-lo: 
```source help-erick/bin/activate```

3. Instale as dependências: 
```pip install -r requirements.txt```


# Rodando o projeto 
1. Preencha o arquivo source.csv
2. ```python process.py```
3. O arquivo *output.csv* será gerado

# Links Uteis
municipios - IBGE
https://www.ibge.gov.br/explica/codigos-dos-municipios.php

conjuntos
https://www2.aneel.gov.br/aplicacoes_liferay/srd/indqual/dspConjunto.cfm?ano=2010&estado=SP&municipio=3507209


indicadores
https://www2.aneel.gov.br/aplicacoes_liferay/srd/indqual/dspIndicadores.cfm?municipio=3507209&conjunto=12165&ano=2010&estado=SP

Usando virtualenv no pycharm
https://ruddra.com/using-intellijidea-within-an-exisiting-virtualenv/

Instalando o virtualenv no windows
https://fernandofreitasalves.com/tutorial-virtualenv-para-iniciantes-windows/
