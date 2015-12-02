# Rede Sustentabilidade API v2

## Dependências

* Python 3.4.3
* Muffin Framework

## Configuração

```
pyvenv .
source bin/activate
pip install -r requirements.txt
```

## Comando disponíveis

* subir servidor

```
DATABASE_URL=postgresql://user:@127.0.0.1/rs-api muffin api run --bind=0.0.0.0:5000
```

* sincronizar filiados a partir de uma planilha com E-mail e Nome

```
DATABASE_URL=postgresql://user:@127.0.0.1/rs-api muffin api process_csv_from_file ~/arquivo-com-coluna-E-mail-Nome.csv
```

## Testes

```
DATABASE_URL=postgresql://user:@127.0.0.1/rs-api-tests py.test -xs api/tests.py
```
