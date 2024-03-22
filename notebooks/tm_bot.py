import telebot
import requests
import random
from telebot import types
import psycopg2

dbSession       = psycopg2.connect("dbname='postgres' user='postgres' password='postgres'");
dbCursor = dbSession.cursor();


bot = telebot.TeleBot('1312476531:AAFebX-ubG1cCShIgO6UOlMmPVXh08hvMy8')

S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"
#'Technology by type'
cC=['Emerging technologies', 'Category:Biotechnology', 'Category:Electronics', 'Category:Equipment', 'Category:Information appliances', 
        'Category:Nanotechnology‎', 'Category:Sound technology' , 'Category:Scientific equipment', 'Category:Information and communications technology‎', 
        'Quantum technology', 'Microtechnology', 'High tech', 'Electrical engineering technology']
curCat =[]
ifAddCategory = False
ifAddRes = False
BadCat=[]
tech=''
try:
    sqlSelect = "select * from BadCat";
    dbCursor.execute(sqlSelect);
    rows = dbCursor.fetchall();
    for row in rows:

        BadCat.append(row[0]);

except:
    BadCat=[]


NanoCat = []
try:
    sqlSelect = "select * from NanoCat";
    dbCursor.execute(sqlSelect);
    rows = dbCursor.fetchall();
    for row in rows:

        NanoCat.append(row[0]);
except:
      NanoCat = []  
      

      
def getRandomCategory(t):
    

    PARAMS = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": t,
        "cmlimit": 500,
        "format": "json"
    }
    
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    return random.choice(DATA['query']['categorymembers'])['title']

def getCategory():
    t=BadCat[0]
    while (t in BadCat):
        t = random.choice(cC)
        while ("Category:" in t):
            
            t = getRandomCategory(t)
            
    return t 
def setTech(t):
    global tech
    tech=t
    
def getTech():
    return tech

def setIfAddCategory(t):
    global ifAddCategory
    ifAddCategory= t

def getIfAddCategory():
    return ifAddCategory    

def setIfAddRes(t):
    global ifAddRes
    ifAddRes= t

def getIfAddRes():
    return ifAddRes  
    
def setCurCat(c):
    global curCat
    curCat = c
  
def getCurCat():
    return curCat

def addBadCat(c):
    global BadCat
    BadCat.append(c)
    sqlInsertRow1  = "INSERT INTO BadCat values('" + c +"')";
    dbCursor.execute(sqlInsertRow1);
    dbSession.commit()
    
def addNanoCat(c):
    global NanoCat
    NanoCat.append(c)
    sqlInsertRow1  = "INSERT INTO NanoCat values('" + c +"')";
    dbCursor.execute(sqlInsertRow1);
    dbSession.commit()
    
def addRes(m,c,t,u):
    sqlInsertRow1  = "INSERT INTO results values('" + t +"','"+c+"','"+ m +" ', '"+ u +" ')";
    dbCursor.execute(sqlInsertRow1);
    dbSession.commit()  
    
def show_result(m):
    sqlSelect = "select * from results";
    dbCursor.execute(sqlSelect);
    rows = dbCursor.fetchall();
    num=0
    try:
        for row in rows:
            
            if (row):
                num=num+1
#                bot.send_message(m.chat.id, "Category " + row[0] + " tecnology " +  row[1])
                bot.send_message(m.chat.id, str(num) + ". "+ row[2])
            else:
                bot.send_message(m.chat.id, 'Пока ничего нету')
            print(row)
    except:
            bot.send_message(m.chat.id, 'Пока ничего нету')
            

@bot.message_handler(commands=['help'])
def help_message(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('Добавить технологию')
    itembtn2 = types.KeyboardButton('Попробовать свои силы')
    itembtn3 = types.KeyboardButton('Посмотреть идеи')
    itembtn4 = types.KeyboardButton('Как это работает')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    
    bot.send_message(message.chat.id, "You may /start adventure. There you will get random Category from Wiki, read its description if needed. You are suggested to match this Category with one of our integrated technologies. If you have an idea, submit the description. If suggested category from Wiki is not relevant, you may mark it as bad to avoid it in the future for everybody. Also you can add more OUR integrated technologies to provide more choices for the adventure.", reply_markup=markup)


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('Добавить технологию')
    itembtn2 = types.KeyboardButton('Попробовать свои силы')
    itembtn3 = types.KeyboardButton('Посмотреть идеи')
    itembtn4 = types.KeyboardButton('Как это работает')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    
    bot.send_message(message.chat.id, "Choose option:", reply_markup=markup)
    
    
@bot.message_handler(commands=['get'])
def get_category(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('Плохая категория')
    itembtn2 = types.KeyboardButton('Другая категория')
    itembtn3 = types.KeyboardButton('Добавить технологию')
    itembtn4 = types.KeyboardButton('Добавить идею')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

    try:
        setCurCat(getCategory())
        setTech(random.choice(NanoCat))
        bot.send_message(message.chat.id, "Ваша категория: <b>" +  getCurCat() + "</b>. Попробуйте объеденить с <b>" + getTech() + "</b> ну или с чем то еще. Ниже подробная информация по категории, если желаете.", parse_mode='html')
    
        PARAMS = {
                  "action": "query",
                  "titles": getCurCat(),
                  "prop": "info",
                  "inprop" : "url",
                  "format": "json"
                 }

        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()
        
        bot.send_message(message.chat.id, DATA['query']['pages'][list(DATA['query']['pages'].keys())[0]]['fullurl'], reply_markup=markup)
    except:
        
         bot.send_message(message.chat.id, "Что-то пошло не так, попробуем еще раз?",  reply_markup=markup)
         start_message(message)
         

def add_category(message):
    markup = types.ForceReply(selective=False)
    setIfAddCategory(True)
    bot.send_message(message.chat.id, "Добавьте что-то про нанофотонику с чем будем комбинировать категории", reply_markup=markup) 
    
@bot.message_handler(commands=['stats'])    
def get_Stats(message):
    res ={}
    sqlSelect = "select usr from results";
    dbCursor.execute(sqlSelect);
    rows = dbCursor.fetchall();
    print(rows)
    try:
        for row in rows:
            print(row[0])
            if (row[0] in res):
                res[row[0]] +=1
            else:
                res.update({row[0]:1})
#               
    except:
            bot.send_message(message.chat.id, 'Пока ничего нету')
    for i in res:
        print(i + "- <b>" + str(res[i]) + "</b>")
        bot.send_message(message.chat.id, i + " - <b>" + str(res[i]) + "</b>", parse_mode='html')  
    
def add_result(message):
    markup = types.ForceReply(selective=False)
    setIfAddRes(True)
    bot.send_message(message.chat.id, "Добавьте что-то для " + getCurCat()+" и " + getTech(), reply_markup=markup)
    
@bot.message_handler(func=lambda message: True)
def echo_all(message):
   
    print(message.from_user.first_name)
    if (message.text == 'Добавить технологию'):
        add_category(message)
        

    elif (message.text == 'Попробовать свои силы'):
        get_category(message)
    elif (message.text == 'Как это работает'):
         help_message(message)  
    elif (message.text == 'Плохая категория'):   
         addBadCat(getCurCat())
         bot.send_message(message.chat.id, "Больше не будет")
         get_category(message)
    elif (message.text == 'Другая категория'):   
         get_category(message)    
    elif (message.text == 'Добавить идею'):   
         add_result(message) 
    elif (message.text == 'Посмотреть идеи'):   
         show_result(message)
    elif (getIfAddCategory()):
         setIfAddCategory(False)
         addNanoCat(message.text)
         bot.send_message(message.chat.id, "Спасибо "+message.from_user.first_name)
         start_message(message)
    elif (getIfAddRes()):
         setIfAddRes(False)
         addRes(message.text, getCurCat(), getTech(), message.from_user.first_name)
         bot.send_message(message.chat.id, "Отлично!")
         start_message(message)
           
   
bot.polling()