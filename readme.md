# Segurança da Informação

## Como executar?

1. Instale o Python e MySQL
2. Instale os pacotes (de preferência em um virtualenv): 

```
pip install mysqlclient jinja2
```

```
'http.server', 'http.cookies', 'datetime', 'urllib', 'os' e 'hashlib' são batteries included da linguagem

'mysqlclient' indispensável para se conectar no MySQL

'jinja2' facilita a inserção de mensagens como 'Conta criada com sucesso!', que poderia ser feito sem o pacote, porém considerei que seria um tempo gasto desnecessário pois o foco é na lógica de login.
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
