import MySQLdb
import hashlib
import os


class Database:
    def __init__(self):
        print('Conetando no MySQL...')

        self.db = MySQLdb.connect(
            host="localhost",
            user="root",
            password="",
            database="seg1"
        )

        with open(f'database/dml.sql') as ddl:
            ddl_sql = ddl.read()

        self.cursor = self.db.cursor()

        try:
            self.cursor.execute('select * from users')
            print('Conectando na base de dados criada anteriormente...')
        except MySQLdb.ProgrammingError:
            print('Criando base de dados...')
            self.cursor.execute(ddl_sql)

    def create(self, email, password):
        password = self.create_password(password)
        try:
            self.cursor.execute('INSERT INTO users (email, password) VALUES (%s, %s)', (email, password,))
            self.db.commit()
            return True
        except MySQLdb.IntegrityError:
            return False

    def create_password(self, password, salt=os.urandom(16)):
        password = bytes(password, encoding='utf8')
        hash = hashlib.scrypt(password, salt=salt, n=1024, r=8, p=1)
        value = salt.hex() + hash.hex()
        return value

    def login(self, email, password):
        self.cursor.execute('SELECT password from users where email=%s', (email,))
        try:
            fetch_password = self.cursor.fetchone()[0]
        except TypeError:
            return False
        if fetch_password is None:
            return False
        salt = bytes.fromhex(fetch_password[:32])
        compare_pass = self.create_password(password, salt)
        is_same_pass = compare_pass == fetch_password
        return is_same_pass

    def create_session(self, email):
        id = os.urandom(16).hex()
        self.cursor.execute('SELECT email from sessions where id=%s', (id,))
        while self.cursor.fetchone() is not None:
            id = os.urandom(16).hex()
            self.cursor.execute('SELECT email from sessions where id=%s', (id,))

        self.cursor.execute('INSERT INTO sessions (id, email) VALUES (%s, %s)', (id, email,))
        self.db.commit()
        return id

    def is_valid_session(self, session):
        self.cursor.execute('SELECT email from sessions where id=%s', (session,))
        try:
            fetch_id = self.cursor.fetchone()[0]
            return True
        except TypeError:
            return False

    def close_session(self, session):
        status = self.is_valid_session(session)
        if status:
            self.cursor.execute('DELETE FROM sessions where id=%s', (session,))
            self.db.commit()

    def get_email(self, session):
        self.cursor.execute('SELECT email from sessions where id=%s', (session,))
        try:
            email = self.cursor.fetchone()[0]
            return email
        except TypeError:
            return ''
