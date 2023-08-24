# Segurança da Informação

## Como executar?

1. Instale o Python e MySQL
2. Instale os pacotes (de preferência em um virtualenv): 

```
pip install mysqlclient jinja2
```

3. Edite as suas configurações em `database.py`

```
host="localhost",
user="root",
password="",
database="seg1"
```

4. Execute `python3 server.py`
5. Entre no site no navegador `http://127.0.0.1:8080`
