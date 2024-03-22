import telebot
import requests
import random
from telebot import types
import psycopg2
from time import time


def establish_connection():
    dbSession       = psycopg2.connect("dbname='postgres' user='postgres' password='postgres'");
    dbCursor = dbSession.cursor();
    return dbSession, dbCursor


def close_connection(dbSession, dbCursor):
    dbCursor.close()
    dbSession.close()
#393476363:AAGMEGMhCS2oCwxUJtAJxxWP4_GA1kfgvbc
bot = telebot.TeleBot('1312476531:AAFebX-ubG1cCShIgO6UOlMmPVXh08hvMy8')

S = requests.Session()


def get_topics(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    keyboard = []
    keyboard1 = []
    dbSession, dbCursor = establish_connection()
    res=[]
    try:
        sqlSelect = "select * from topics where userid=" +str(message.from_user.id) +" and valid ='false'"
#        print(str(message.from_user.id))
#        print(sqlSelect)
        dbCursor.execute(sqlSelect)
        res = dbCursor.fetchall()
#        print(res)
        
    except:
        close_connection(dbSession, dbCursor)
        bot.send_message(message.chat.id, "Something went wrong, try again", reply_markup=markup)
#    print(res)    
    if (res !=[]):
        close_connection(dbSession, dbCursor)
        start_message(message)
    else:
        
        try:
            sqlSelect = "select * from topics";
            dbCursor.execute(sqlSelect);
            categories = dbCursor.fetchall();
            
            for row in categories:
    #            print(row[1])
                if (row[3]):
    #                print(row[0])
                    keyboard1.append(types.InlineKeyboardButton(row[0], callback_data=str(row[4])))
                else:
                    keyboard1.append(types.InlineKeyboardButton("**selected**" +row[0], callback_data='busy'))
                    
                keyboard.append(keyboard1)
                keyboard1=[]
            close_connection(dbSession, dbCursor)
            markup = types.InlineKeyboardMarkup(keyboard)
            bot.send_message(message.chat.id, "Select the topic", reply_markup=markup)
        except:
            close_connection(dbSession, dbCursor)
            bot.send_message(message.chat.id, "Something went wrong, try again", reply_markup=markup)
    
        

def view_results(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    keyboard = []
    keyboard1 = []
    dbSession, dbCursor = establish_connection()
    try:
        sqlSelect = "select * from topics where valid=false";
        dbCursor.execute(sqlSelect);
        res = dbCursor.fetchall();
#        print(res)
        if res !=[]:       
            for row in res:
                s = str(row[1]) +": "+str(row[0])
                keyboard1.append(types.InlineKeyboardButton(s, callback_data='none'))
                keyboard.append(keyboard1)
                keyboard1=[]
            msg = "Chosen topics are:"
        else:
            msg = "There are no chosen topics yet, be the first one."
        close_connection(dbSession, dbCursor)
        markup = types.InlineKeyboardMarkup(keyboard)
        bot.send_message(message.chat.id, msg, reply_markup=markup)
    except:
        close_connection(dbSession, dbCursor)
        bot.send_message(message.chat.id, "Something went wrong, try again", reply_markup=markup)

    

def show_details(message):
    dbSession, dbCursor = establish_connection()
    res=[]
    
    try:
        sqlSelect = "select * from topics where userid="+str(message.from_user.id)
#        print(sqlSelect)
        dbCursor.execute(sqlSelect);
        res = dbCursor.fetchall();
#        print(res[0])

        close_connection(dbSession, dbCursor)
        bot.send_message(message.chat.id, res[0][2],  parse_mode='html')
    except:
        close_connection(dbSession, dbCursor)
        bot.send_message(message.chat.id, "Something went wrong, try again", parse_mode='html')

    
    
    
def change_topic(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    try:
            dbSession, dbCursor = establish_connection()
            sqlSelect = """update topics set (username, valid, userid)= (%s, %s, %s) where userid=%s"""
#            print(sqlSelect, ['true', 'null',  message.from_user.id])
            dbCursor.execute(sqlSelect, ['None', 'true', 0, message.from_user.id]);
            dbSession.commit()
            close_connection(dbSession, dbCursor)
            start_message(message)
#        ", user='"+str(call.from_user.first_name)+
    except:
        close_connection(dbSession, dbCursor)
        print( "Something went wrong, try again")
        

    
    
    
@bot.message_handler(commands=['help'])
def help_message(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('Start the joney')
    
    markup.add(itembtn1)
    
    bot.send_message(message.chat.id, "You may select the topic and make seminar to educate SAIT-Russia Team members.", reply_markup=markup)


@bot.message_handler(commands=['start'])
def start_message(message):
    print(message.from_user.is_bot)
    markup = types.ReplyKeyboardMarkup(row_width=1)
    res=[]
    if  message.from_user.is_bot:
        sqlSelect = "select * from topics where userid=" +str(message.chat.id) +" and valid ='false'"
    else:
        sqlSelect = "select * from topics where userid=" +str(message.from_user.id) +" and valid ='false'"
        
    
        
    
    try:
        dbSession, dbCursor = establish_connection()
#        sqlSelect = "select * from topics where userid=" +str(message.from_user.id) +" and valid ='false'"
    #        print(str(message.from_user.id))
    #        print(sqlSelect)
        dbCursor.execute(sqlSelect)
        res = dbCursor.fetchall()
    #        print(res)
        close_connection(dbSession, dbCursor)
                
    #        ", user='"+str(call.from_user.first_name)+
    except:
        print( "Something went wrong, try again")
            
    
       
    if res !=[]:
        itembtn2 = types.KeyboardButton('View results')
        itembtn3 = types.KeyboardButton('Change my topic')
        itembtn4 = types.KeyboardButton('Details about selected topic')
        markup.add(itembtn2, itembtn3,itembtn4)
        bot.send_message(message.chat.id, "You are assigned to topic: "+res[0][0] +". You may still change it.", reply_markup=markup)
    else:
        itembtn1 = types.KeyboardButton('Select topic')
        itembtn2 = types.KeyboardButton('View results')
        markup.add(itembtn1, itembtn2)
        bot.send_message(message.chat.id, "You may select the topic and make seminar to educate SAIT-Russia Team members.", reply_markup=markup)
        
        
        
    
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == "busy":
            bot.send_message(call.message.chat.id, "This topic is already selected", parse_mode='html')
        else:
            res =[]
            sqlSelect = "select * from topics where userid=" +str(call.from_user.id) +" and valid ='false'"
            try:
                dbSession, dbCursor = establish_connection()
        #        sqlSelect = "select * from topics where userid=" +str(message.from_user.id) +" and valid ='false'"
            #        print(str(message.from_user.id))
            #        print(sqlSelect)
                dbCursor.execute(sqlSelect)
                res = dbCursor.fetchall()
            #        print(res)
                close_connection(dbSession, dbCursor)
                    
        #        ", user='"+str(call.from_user.first_name)+
            except:
                close_connection(dbSession, dbCursor)
                print( "Something went wrong, try again")
    #        print(call.message)
            if res ==[]:
                try:
                    dbSession, dbCursor = establish_connection()
                    sqlSelect = """update topics set (username, valid, userid)= (%s, %s, %s) where id=%s"""
        #            print(sqlSelect, [call.from_user.first_name, 'false', call.from_user.id, call.data])
                    dbCursor.execute(sqlSelect, [call.from_user.first_name, 'false', call.from_user.id, call.data]);
                    dbSession.commit()
                    close_connection(dbSession, dbCursor)
                    start_message(call.message)
        #        ", user='"+str(call.from_user.first_name)+
                except:
                    close_connection(dbSession, dbCursor)
                    print( "Something went wrong, try again")
     
#   bot.send_message(call.message.chat.id, "Good job", parse_mode='html')
  
    
            
@bot.message_handler(func=lambda message: True)
def echo_all(message):
   
#    print(message)
    if (message.text == 'Start the joney'):
        start_message(message)
        

    elif (message.text == 'Select topic'):
        get_topics(message)
    elif (message.text == 'View results'):
         view_results(message)  
    elif (message.text == 'Change my topic'):   
         change_topic(message)
    elif (message.text == 'Details about selected topic'):  
         show_details(message)
#         bot.send_message(message.chat.id, "Больше не будет")

try:   
    bot.polling()
except Exception as e:
    print('sleep')
#    logger.error(e)

    time.sleep(15)