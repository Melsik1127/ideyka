# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import telebot
from telebot import apihelper
from telebot import types
from time import sleep


a = ''
end = False
end3 = False
end2 = False
d = ''
box = []
rd = []
proxies = { 'http': 'socks5://127.0.0.1:9099', 'https': 'socks5://127.0.0.1:9099' }
TOKEN = '1148670597:AAFgWuli1WK4l0XiTXL4jTn_tH-3abU5jXU'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item = types.InlineKeyboardButton("Проверить картину на наличие", callback_data='one')
    item_2 = types.InlineKeyboardButton("Купить картину(ы)", callback_data='two')
    item_3 = types.InlineKeyboardButton("Посмотреть все доступные картины", callback_data='three')
    markup.add(item, item_2, item_3)
    a = ''
    end = False
    end2 = False
    d = ''
    box = []
    rd = []
    bot.send_message(message.chat.id, 'Выберите, что вам нужно:', reply_markup=markup)

@bot.message_handler(commands=['pocess'], func=lambda message: True)
def pocess(message):
    bot.send_message(message.chat.id, 'Введите номер картины')
    
        

 
@bot.message_handler(commands=['all_pocess'])
def all_pocess(message):
    global rd
    bot.send_message(message.chat.id, 'Сейчас мы проверим все картины в наличии...')
    bot.send_message(message.chat.id, 'Мы вас оповестим когда закончим поиск (он может занять до 8 минут)')
    driver = webdriver.Chrome('chromedriver')
    ad = []
    rd = []
    for n in range(1,5):
        
        
        if n == 1:
            driver.get('https://ideyka.com.ua/hobby/kartiny-po-nomeram/4050-sm/')
        else:
            driver.get('https://ideyka.com.ua/hobby/kartiny-po-nomeram/4050-sm/page-' + str(n))
        driver.set_window_size(1366,686)
        sleep(2)
        al = driver.find_elements_by_css_selector('a')
        for i in range(0, len(al)):
            if 'Картина по номерам' in al[i].text:
                ad.append(al[i].get_attribute('href'))
        print(len(ad))   
    for n in range(1,5):
        
        
        if n == 1:
            driver.get('https://ideyka.com.ua/hobby/kartiny-po-nomeram/4040-sm/')
        else:
            driver.get('https://ideyka.com.ua/hobby/kartiny-po-nomeram/4040-sm/page-' + str(n))
        driver.set_window_size(1366,686)
        sleep(2)
        al = driver.find_elements_by_css_selector('a')
        for i in range(0, len(al)):
            if 'Картина по номерам' in al[i].text:
                ad.append(al[i].get_attribute('href'))
        print(len(ad))     
    for i in range(0, len(ad)):
        driver.get(ad[i])
        sleep(2)
        try:
            nal = driver.find_element_by_xpath('//*[@id="page"]/section/div/div[2]/div[1]/div/div[3]/div/div[2]/b/span')
            f = driver.find_element_by_class_name('sku')
            rd.append(f.text)
        except:
            try:
                nal = driver.find_element_by_xpath('//*[@id="page"]/section /div/div[2]/div[1]/div/div[3]/div/div[2]/b/span')
                f = driver.find_element_by_class_name('sku')
                f.text = str.replace(f.text,"арт.", "")
                rd.append(f.text)
            except:
                print('not found')
    print(rd)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item = types.InlineKeyboardButton("Посмотреть", callback_data='see')
    
        
    markup.add(item)
                    
    bot.send_message(message.chat.id, 'Поиск завершен', reply_markup=markup) 
    driver.quit()
            
@bot.message_handler(commands=['see'])
def see(message):
    global rd
    md = ' '.join(map(str, rd))
    bot.send_message(message.chat.id, 'В наличии сейчас: '  + md)
    sleep(2)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item = types.InlineKeyboardButton("Главное меню", callback_data='menu')
    
        
    markup.add(item)
                    
    bot.send_message(message.chat.id, 'Нажмите чтобы перейти к меню', reply_markup=markup)

@bot.message_handler(commands=['buy'],func=lambda message: True)
def buy(message):
    sleep(0.5)
    global box
    markup = types.InlineKeyboardMarkup(row_width=1)
    item = types.InlineKeyboardButton("Добавить картину в корзину", callback_data='add')
    item_2 = types.InlineKeyboardButton("Купить", callback_data='buy')
    item_4 = types.InlineKeyboardButton("Назад", callback_data='menu')
    item_3 = types.InlineKeyboardButton("Посмотреть корзину", callback_data="bin")
    item_5 = types.InlineKeyboardButton("Очистить корзину", callback_data="clear")
    

    markup.add(item, item_3, item_5,item_2, item_4)
                        
    bot.send_message(message.chat.id,'В вашей корзине сейчас ' + str(len(box)) + ' картин' , reply_markup=markup)  

@bot.message_handler(content_types=['text'])
def text(message):
    global end2,end3, end
    if end3 == True:
        if end2 == False:
            a = message.text

            bot.send_message(message.chat.id, 'Проверяем ' + a)
            driver = webdriver.Chrome('chromedriver')
            driver.get('https://ideyka.com.ua/hobby/')
            driver.set_window_size(1366,686)
            sleep(2)
            find = driver.find_element_by_class_name('form-control')
            find.click()
            find.send_keys(a)
            sleep(2)
            try:
                vis = driver.find_element_by_xpath('//*[@id="search-dropdown"]/li[2]/a/div/div[2]')
                vis.click()
                sleep(5)
                image_name = driver.find_element_by_xpath('//*[@id="page"]/section/div/div[2]/div[1]/div/div[1]/div/h1')
                m = image_name.text
                m = str.replace(m,"Картины по номерам", "")
                try:
                    nal = driver.find_element_by_xpath('//*[@id="page"]/section/div/div[2]/div[1]/div/div[3]/div/div[2]/b/span')
                    bot.send_message(message.chat.id, 'Картина ' + m + ' | в наличии' )
                except:
                    try:
                        nal = driver.find_element_by_xpath('//*[@id="page"]/section /div/div[2]/div[1]/div/div[3]/div/div[2]/b/span')
                        bot.send_message(message.chat.id, 'Картина ' + m + ' | в наличии, заканчивается' )
                    except:
                        bot.send_message(message.chat.id, 'Картина ' + m + ' | не в наличии' )
                driver.quit()
                sleep(5)    
                markup = types.InlineKeyboardMarkup(row_width=1)
                item = types.InlineKeyboardButton("Проверить картину на наличие", callback_data='one')
                item_2 = types.InlineKeyboardButton("Купить картину(ы)", callback_data='two')
                item_3 = types.InlineKeyboardButton("Посмотреть все доступные картины", callback_data='three')
                markup.add(item, item_2, item_3)
                                
                bot.send_message(message.chat.id, 'Что дальше?', reply_markup=markup) 
            except:
                markup = types.InlineKeyboardMarkup(row_width=1)
                item = types.InlineKeyboardButton("Проверить картину на наличие", callback_data='one')
                item_2 = types.InlineKeyboardButton("Купить картину(ы)", callback_data='two')
                item_3 = types.InlineKeyboardButton("Посмотреть все доступные картины", callback_data='three')
                markup.add(item, item_2, item_3)
                                
                bot.send_message(message.chat.id, 'Ошибка, картины под таким номером не существует', reply_markup=markup)
                driver.quit()
                end3 = False
        if end2 == True:
            global box
            print(end)
            if end == False:
                if message.text in box:
                    bot.send_message(message.chat.id, 'Данная картина уже в корзине!')
                    end3 = False  
                else:
                    box.append(message.text)
                    bot.send_message(message.chat.id, 'Картина ' + message.text + ' добавлена к корзину')
                    end3 = False  
                buy(message)
            if end == True:
                try:
                    driver = webdriver.Chrome('chromedriver')
                    comment = message.text
                    bot.send_message(message.chat.id, 'Ожидайте, мы оповестим вас, когда закажем картину(ы)')
                    driver.get('https://ideyka.com.ua')
                    driver.set_window_size(1366, 666)
                    l_name = 'kartina.karantina@gmail.com'
                    l_pass = '0000'
                    sleep(5)
                    login = driver.find_element_by_class_name('popup_auth')
                    login.click()
                    log = driver.find_element_by_class_name('mail_login')
                    log.click()
                    log.send_keys(l_name)
                    pas = driver.find_element_by_name('password')
                    pas.click()
                    pas.send_keys(l_pass)
                    pas_butt = driver.find_element_by_xpath('//*[@id="button_login"]')
                    pas_butt.click()
                    sleep(5)
                    
                    if len(box) == 1:
                        find = driver.find_element_by_class_name('form-control')
                        find.click()
                        find.send_keys(box[0])
                        sleep(5)
                        vis = driver.find_element_by_xpath('//*[@id="search-dropdown"]/li[2]/a/div/div[2]')
                        vis.click()
                        sleep(5)
                        b = driver.find_element_by_id('button-cart')
                        b.click()
                        sleep(7)
                        butt = driver.find_element_by_xpath('//*[@id="cart"]/div/div/table/tfoot/tr/td/a[2]')
                        butt.click()
                        sleep(6)
                        comm = driver.find_element_by_id('comment')
                        comm.click()
                        comm.send_keys(comment)
                        butt_confirm = driver.find_element_by_xpath('//*[@id="simplecheckout_button_confirm"]')
                        butt_confirm.click()
                        sleep(10)
                        driver.get('https://ideyka.com.ua/index.php?route=checkout/success')
                        sleep(3)
                        yes = driver.find_element_by_xpath('//*[@id="content"]/div[3]/div[3]/div/a')
                        yes.click()
                        sleep(2)
                        user = driver.find_element_by_xpath('//*[@id="top-menu"]/div/div[1]/div/div[2]/a[1]')
                        user.click()
                        sleep(2)
                        my_z = driver.find_element_by_xpath('//*[@id="column-right"]/div[1]/div[2]/ul/li[5]/a')
                        my_z.click()
                        sleep(2)
                        numb = driver.find_elements_by_class_name('order-id')

        
                        bot.send_message(message.chat.id, 'Заказ успешно готов!')
                        bot.send_message(message.chat.id, 'Номер вашего заказа: \n' + numb[0].text)
                        driver.quit()
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item = types.InlineKeyboardButton("Проверить картину на наличие", callback_data='one')
                        item_2 = types.InlineKeyboardButton("Купить картину(ы)", callback_data='two')
                        item_3 = types.InlineKeyboardButton("Посмотреть все доступные картины", callback_data='three')
                        markup.add(item, item_2, item_3)
                        end3 = False
                        bot.send_message(message.chat.id, 'Что дальше?', reply_markup=markup) 
                
                    if len(box) > 1:
                        for i in range(0,len(box)):
                            find = driver.find_element_by_class_name('form-control')
                            find.click()
                            find.send_keys(box[i])
                            sleep(5)
                            vis = driver.find_element_by_xpath('//*[@id="search-dropdown"]/li[2]/a/div/div[2]')
                            vis.click()
                            sleep(5)
                            b = driver.find_element_by_id('button-cart')
                            b.click()
                            sleep(5)
                            butt = driver.find_element_by_xpath('//*[@id="popupcart"]/div[1]/a')
                            butt.click()
                            sleep(5)
                            if i == (len(box)-1):
                                l = driver.find_element_by_xpath('//*[@id="page"]/header/div/div[1]/div/div[3]/a')
                                l.click()
                                sleep(5)
                                comm = driver.find_element_by_id('comment')
                                comm.click()
                                comm.send_keys(comment)
                                sleep(2)
                                butt_confirm = driver.find_element_by_xpath('//*[@id="simplecheckout_button_confirm"]')
                                butt_confirm.click()
                                sleep(10)
                                driver.get('https://ideyka.com.ua/index.php?route=checkout/success')
                                sleep(3)
                                yes = driver.find_element_by_xpath('//*[@id="content"]/div[3]/div[3]/div/a')
                                yes.click()
                                sleep(2)
                                user = driver.find_element_by_xpath('//*[@id="top-menu"]/div/div[1]/div/div[2]/a[1]')
                                user.click()
                                sleep(2)
                                my_z = driver.find_element_by_xpath('//*[@id="column-right"]/div[1]/div[2]/ul/li[5]/a')
                                my_z.click()
                                sleep(2)
                                numb = driver.find_elements_by_class_name('order-id')

                                end3 = False    
                                bot.send_message(message.chat.id, 'Заказ успешно готов!')
                                bot.send_message(message.chat.id, 'Номер вашего заказа: \n' + numb[0].text)
                                driver.quit()
                                markup = types.InlineKeyboardMarkup(row_width=1)
                                item = types.InlineKeyboardButton("Проверить картину на наличие", callback_data='one')
                                item_2 = types.InlineKeyboardButton("Купить картину(ы)", callback_data='two')
                                item_3 = types.InlineKeyboardButton("Посмотреть все доступные картины", callback_data='three')
                                markup.add(item, item_2, item_3)
                                bot.send_message(message.chat.id, 'Что дальше?', reply_markup=markup)



                except Exception as e:
                    print(repr(e))
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item = types.InlineKeyboardButton("Главное меню", callback_data='menu')
                    bot.send_message(message.chat.id, 'Непонятная ошибка( . Попробуйте заказать заново')
                    markup.add(item)
                    bot.send_message(message.chat.id, 'Вы точно добавили картину, которая в наличии?', reply_markup=markup)
                    del(box)
                    box = []
                    end3 = False
                
        
                
@bot.message_handler(commands=['add'])
def add(message):
    global box
    sleep(0.5)
    bot.send_message(message.chat.id, 'Введите номер(id) картины')
        
                

@bot.message_handler(commands=['bin'])
def b_bin(message):
    global box
    if len(box) != 0:
        bot.send_message(message.chat.id, 'В вашей корзине:')
        box_export = ' '.join(map(str, box))
        bot.send_message(message.chat.id, box_export)
        buy(message)
    if len(box) == 0:
        bot.send_message(message.chat.id, 'Ваша корзина пуста!')
        buy(message)
@bot.message_handler(commands=['create'])
def create(message):
    global box, end, end3
    if len(box) != 0:
        bot.send_message(message.chat.id, 'Введите комментарий')
        end = True
        end3 = True
    else:
        bot.send_message(message.chat.id, 'Ваша корзина пуста!')
        buy(message)
        
@bot.message_handler(commads=['clean'])
def clear(message):
    global box
    del(box)
    box = []
    bot.send_message(message.chat.id, 'Корзина успешно очистилась!')
    buy(message)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global end2, end3
    try:
        if call.message:
            if call.data == 'one':
                end2 = False
                end = False
                end3 = True
                pocess(call.message)
            elif call.data == 'three':
                all_pocess(call.message)
            elif call.data == 'menu':
                start(call.message)
            elif call.data == 'see':
                see(call.message)
            elif call.data == 'two':
                end3 = True
                end2 = True
                buy(call.message)
            elif call.data == 'add':
                add(call.message)
                end2 = True
                end3 = True
            elif call.data == 'bin':
                b_bin(call.message)
                end2 = True
                end3 = True
            elif call.data == 'buy':
                create(call.message)
            elif call.data == 'clear':
                clear(call.message)


    except Exception as e:
        print(repr(e))

bot.polling()