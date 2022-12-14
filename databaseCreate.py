import sqlite3

#teste111azxza
connection = sqlite3.connect('banco.db')
cursor = connection.cursor()


cria_tabela = "CREATE TABLE IF NOT EXISTS hoteis (hotel_id text PRYMARY KEY,\
     nome text, estrelas real, diaria real, cidade text )"

cria_hotel = "INSERT INTO hoteis VALUES ('alpha', 'alphahotel', 4.3, 344.22, 'Sao Paulo')"

cursor.execute(cria_tabela)
cursor.execute(cria_hotel)

connection.commit()
connection.close()
