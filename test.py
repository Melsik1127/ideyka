# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import telebot
from telebot import apihelper
from telebot import types
from time import sleep


driver = webdriver.Chrome('chromedriver')
# переменные
box = []
end = False
rd = []
a = ''

TOKEN = '1148670597:AAFgWuli1WK4l0XiTXL4jTn_tH-3abU5jXU'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    item1 = types.KeyboardButton("Оформить заказ")
    item2 = types.KeyboardButton("Очистить корзину")
    item3 = types.KeyboardButton("Показать все наличие")
 
    markup.add(item1, item2, item3)
 
    bot.send_message(message.chat.id, "Введи номер товара".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=markup)

# заказ
@bot.message_handler(commands=['buy'])
def buy(message):
	global box, end
	if len(box) != 0:
		bot.send_message(message.chat.id, 'В корзине сейчас:')
		for i in range(0,len(box)):
			bot.send_message(message.chat.id, box[i])

		bot.send_message(message.chat.id, 'Введите данные получателя одним сообщением')
		end = True
	if len(box) == 0:
		bot.send_message(message.chat.id, 'Наберите товар в корзину')
# очистить корзину
@bot.message_handler(commands=['clear'])
def clear(message):
	global box
	box = []
	bot.send_message(message.chat.id, 'Корзина успешно очистилась!')

# посмотреть все товары в наличии
@bot.message_handler(commands=['all_pocces'])
def all_pocces(message):
	global rd
	bot.send_message(message.chat.id, 'Сейчас мы проверим все картины в наличии...')
	bot.send_message(message.chat.id, 'Мы вас оповестим когда закончим поиск (он может занять до 8 минут)')
	
	ad = []
	rd = []
	for n in range(1,2):
		
		
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
	for n in range(1,2):
		
		
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



# проверка на слова
@bot.message_handler(content_types=['text'])
def text(message):
	global a, end
	if message.text == 'Оформить заказ':
		buy(message)
	elif message.text == 'Очистить корзину':
		clear(message)
	elif message.text == 'Показать все наличие':
		all_pocces(message)
	elif end == False:
		a = message.text
		bot.send_message(message.chat.id, 'Проверяем ' + a)
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
				bot.send_message(message.chat.id, 'Картина ' + m)
				bot.send_message(message.chat.id, 'В наличии💃')
				markup2 = types.InlineKeyboardMarkup(row_width=1)
				item5 = types.InlineKeyboardButton("Добавить в корзину", callback_data='add')
				markup2.add(item5)
				bot.send_message(message.chat.id, 'Вы можете добавить эту картину в корзину', reply_markup=markup2)
			except:
				try:
					nal = driver.find_element_by_xpath('//*[@id="page"]/section /div/div[2]/div[1]/div/div[3]/div/div[2]/b/span')
					bot.send_message(message.chat.id, 'Картина ' + m)
					bot.send_message(message.chat.id, 'В наличии💃')
					markup2 = types.InlineKeyboardMarkup(row_width=1)
					item5 = types.InlineKeyboardButton("Добавить в корзину", callback_data='add')
					markup2.add(item5)
					bot.send_message(message.chat.id, 'Вы можете добавить эту картину в корзину', reply_markup=markup2)
                    
				except:
					bot.send_message(message.chat.id, 'Картина ' + m)
					bot.send_message(message.chat.id, 'Не в наличии🤷‍♀️')
			driver.quit()
		except:
			bot.send_message(message.chat.id, 'Такого номера не существует 🤔')
			driver.quit()
	elif end == True:
		global box
		comment = message.text
		bot.send_message(message.chat.id, 'Ваш заказ обрабатывается')
		try:
			comment = message.text
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
				sleep(2)
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
					
				bot.send_message(message.chat.id, 'Номер вашего заказа: \n' + numb[0].text)
				bot.send_message(message.chat.id, 'Товары:')
				for m in range(0,len(box)):
					bot.send_message(message.chat.id, box[m])
				bot.send_message(message.chat.id, 'Комментарий: ' + comment) 
				
				bot.send_message(message.chat.id, 'Спасибо за ваш заказ!')
				driver.quit()
				end = False
		
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

						end = False    
						bot.send_message(message.chat.id, 'Номер вашего заказа: \n' + numb[0].text)
						bot.send_message(message.chat.id, 'Товары:')
						for m in range(0,len(box)):
							bot.send_message(message.chat.id, box[m])
						bot.send_message(message.chat.id, 'Комментарий: ' + comment) 
						
						bot.send_message(message.chat.id, 'Спасибо за ваш заказ!')
						driver.quit()
						



		except Exception as e:
			print(repr(e)) 
			bot.send_message(message.chat.id, 'Ошибка. Какой-то из товаров недоступен!')
			del(box)
			box = []
			end = False
			driver.quit()
		del box
		box = []
		
@bot.message_handler(commands=['add'])
def add(message):
	global box, a
	if a in box:
		bot.send_message(message.chat.id, 'Товар уже в корзине')
	else:
		box.append(a)
		bot.send_message(message.chat.id, 'Товар ' + a + ' добавлен в корзину')

@bot.message_handler(commands=['see'])
def see(message):
	global rd
	md = ' '.join(map(str, rd))
	bot.send_message(message.chat.id, 'В наличии сейчас: '  + md)
	sleep(2)






# кнопки


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:

			if call.data == 'add':
				add(call.message)
			elif call.data == 'see':
				see(call.message)

	except Exception as e:
		print(repr(e))
bot.polling()