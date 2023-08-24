# Segurança da Informação

## Como executar?

1. Instale o Python e MySQL
2. Instale os pacotes (de preferência em um virtualenv): 

```
pip install mysqlclient jinja2
```

Observações sobre os pacotes usados

```
'http.server', 'http.cookies', 'datetime', 'urllib', 'os' e 'hashlib' são batteries included da linguagem

'mysqlclient' indispensável para conectar a linguagem ao MySQL

'jinja2' facilita a inserção de mensagens como 'Conta criada com sucesso!', que poderia ser feito sem o pacote, porém considerei um tempo gasto em vão: foco na lógica de login com métodos http, sem utilizar frameworks
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
