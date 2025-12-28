from contextlib import closing
import sqlite3

with sqlite3.Connection('agenda.db') as conexão:
    with closing(conexão.cursor()) as cursor:
        cursor.execute('''create table tipos(id integer primary key autoincrement,
                       descrição text);''')
        cursor.execute('''create table nomes(id integer primary key autoincrement,
                       nome text);''')
        cursor.execute('''create table telefones(id integer primary key autoincrement,
                       id_nome integer, número text,
                       id_tipo integer);''')


