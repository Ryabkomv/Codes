import telebot
import requests
import random
from telebot import types
import psycopg2

def establish_connection():
    dbSession       = psycopg2.connect("dbname='postgres' user='postgres' password='postgres'");
    dbCursor = dbSession.cursor();
    return dbSession, dbCursor


def close_connection(dbSession, dbCursor):
    dbCursor.close()
    dbSession.close()

bot = telebot.TeleBot('1312476531:AAFebX-ubG1cCShIgO6UOlMmPVXh08hvMy8')

S = requests.Session()

try:
    s = 'Monstr'
    dbSession, dbCursor = establish_connection()
    sqlSelect = """UPDATE topics SET username=%s, valid=%s, userid=%s WHERE id=%s"""
#    sqlSelect = """INSERT INTO topics values(%s, %s, %s, %s, %s, %s)"""
    #            print(sqlSelect, [call.from_user.first_name, 'false', call.from_user.id, call.data])
    dbCursor.execute(sqlSelect, ['Maxx', 'false', '124576', '79']);
    dbSession.commit()
    close_connection(dbSession, dbCursor)

except:
    print('error')