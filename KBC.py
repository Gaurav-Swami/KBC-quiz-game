import PySimpleGUI as sg
import mysql.connector as c
import prettytable as pt
import pyttsx3
from pygame import mixer
from random import choice


def gen_questions():
	con = c.connect (host='localhost',
					 user='root',
					 password = 'root',
					 database = 'KBC')
	cursor = con.cursor()
	query ="select * from Questions"
	cursor.execute(query)
	data = cursor.fetchall()
	con.commit()
	con.close()
	cursor.close()   
	return data


def highscores():
	con = c.connect (host='localhost',
					 user='root',
					 password = 'root',
					 database = 'KBC')
	cursor = con.cursor()
	cursor.execute("SELECT rank() over(Order by Winning_Amount desc) as 'Rank',Name,Standard,Winning_Amount,Date FROM highscores limit 10")
	mytable = pt.from_db_cursor(cursor)
	con.close()
	cursor.close()

	sg.theme('DarkPurple6')
	layout = [[sg.Push(),sg.Text('x',size = (0,0), enable_events = True,key = '-CLOSE-',font = 'Calibri')],
			   [sg.Text(mytable, font = 'Consolas',text_color = '#FFCC00')]]
	window = sg.Window("highscores",layout,no_titlebar = True)
	while True:
		event, values = window.read()

		if event == sg.WIN_CLOSED or event == '-CLOSE-':
			break
	window.close()


def create_songs():
	mixer.init()
	song1 = mixer.Sound(r'Sounds\kbc_opening.mp3')
	song2 = mixer.Sound(r'Sounds\kbc_timer.mp3')
	song3 = mixer.Sound(r'Sounds\kbc_question.mp3')
	return song1,song2,song3


def create_fwindow():
	global player_name,standard_name
	class_list = ['Class-9th',
				  'Class-10th',
				  'Class-11th',
				  'Class-12th', 
				  'Graduate',
				  'Post Graduate']
	
	song1.play()
	sg.theme('black')

	

	frame = [
			[sg.InputText(default_text='Enter your name :', 
						  text_color = ('#FFCC00'), 
				      	  pad = (10,0), 
				      	  size = (45,5), 
				          key = '-NAME-'),
				      
			 sg.DropDown(class_list,
			 			 default_value = 'Class 12th', 
			 			 text_color = '#FFCC00', 
			 			 size = (23,5),
			 			 key = '-STANDARD-')]]
	layout = [
			 [sg.Image('Logos\\AB.png',pad = (0,0))],
			 [sg.Frame('Enter your details : ',frame, size = (525,54))],
			 
			 [sg.Button(
			 		'HIGHSCORES',
			 		key = '-HIGHSCORES-',
			 		button_color = ('#FFCC00','#3A0E4B'),
			 		size = (13,1),font = 'Young 15'),
			 sg.Text(
			 		'   Welcome to Kaun Banega Codepati, Grab your Hotseat now!   ',
			 	 	text_color = ('#FFCC00'),
			 	  	font = 'Young 14',
			 	  	pad = (0,15)
			 	  	),
			 sg.Button(
			 		'START',
			 		key = '-START-',
			 		button_color = ('#FFCC00','#3A0E4B'),
			 		size = (13,1),font = 'Young 15')
			 		]]
	window =  sg.Window(
						"FWINDOW",layout,	
						element_justification = 'centre',
						no_titlebar = True
						)
	while True:
		event, values = window.read()


		if event == '-START-':
			if len(values['-NAME-']) > 17:
				mixer.pause()
				window.close()
				P_N = values['-NAME-']
				standard_name = values['-STANDARD-']
				player_name = P_N[17:]
				create_mwindow()
			else:
				window['-NAME-'].update(text_color = '#C32200')
				continue
			
			break

		
		if event == '-HIGHSCORES-': # to be deleted
			highscores()

		if event == sg.WIN_CLOSED:
			break
	
	window.close()


def fifty(data,window):
	o_list = ['A','B','C','D']
	o_list.remove(data[i][6])
	element = choice(o_list)
	o_list.remove(element)
	window[o_list[0]].update('')
	window[o_list[1]].update('')


def option_space (a,b,c,d):
	A = ' '*(18-(len(a)))
	B=  ' '*(18-(len(b)))
	C = ' '*(18-(len(c)))
	D = ' '*(18-(len(d)))
	return A, B,C, D


def timer():
	layout =[[sg.Text()]]
	window = sg.Window("Gamer",layout)
	while True:
	    event, values = window.read()
	    
	    if event == sg.WIN_CLOSED:
	        break

	window.close()


def phone_friend(data,i):
	if data[i][6] == 'A':
		ans = data[i][2]	
		answer = 'The correct answer is A; ' + ans

	elif data[i][6] == 'B':
		ans = data[i][3]	
		answer = 'The correct answer is B; '+ ans
	
	elif data[i][6] == 'C':
		ans = data[i][4]	
		answer = 'The correct answer is ' + data[i][6] +'; '+ ans
	
	else:
		ans = data[i][5]	
		answer = 'The correct answer is ' + data[i][6] +'; '+ ans
	
	

	text_speech = pyttsx3.init()
	text_speech.say(answer)
	text_speech.runAndWait()


def aud_pole(data):
	if data[i][6] == 'A':
		a_v = 50
		b_v = 15
		c_v = 30
		d_v = 5
	elif data[i][6] == 'B':
		b_v = 64
		a_v = 6
		c_v = 20
		d_v = 10
	elif data[i][6] == 'C':
		c_v = 70
		b_v = 9
		a_v = 20
		d_v = 1
	elif data[i][6] == 'D':
		a_v = 35
		b_v = 20
		c_v = 5
		d_v = 40
	sg.theme('DarkPurple6')
	layout = [[sg.Push(),sg.Text('x',size = (0,0), enable_events = True,key = '-CLOSE-',font = 'Calibri')],
	    [sg.ProgressBar(100,size = (10,20),orientation = 'v',key = 'a',style = 'vista',bar_color = ('#BAA75C','#070725')),
	     sg.ProgressBar(100,size = (10,20),orientation = 'v',key = 'b',style = 'vista',bar_color = ('#BAA75C','#070725')),
	     sg.ProgressBar(100,size = (10,20),orientation = 'v',key = 'c',style = 'vista',bar_color = ('#BAA75C','#070725')),
	     sg.ProgressBar(100,size = (10,20),orientation = 'v',key = 'd',style = 'vista',bar_color = ('#BAA75C','#070725'))],
	    [sg.Text(' A'), sg.Text('B'), sg.Text('C'), sg.Text('D')]
	]
	awindow = sg.Window("Gamer",layout,no_titlebar = True,location = (650,230))
	while True:
		event, values = awindow.read(timeout = 1)
		awindow['a'].UpdateBar(a_v)
		awindow['b'].UpdateBar(b_v)
		awindow['c'].UpdateBar(c_v)
		awindow['d'].UpdateBar(d_v)
		if event == sg.WIN_CLOSED or event == '-CLOSE-':
			break
	awindow.close()


def create_lwindow(i):
	global win_amt
	mixer.pause()
	sg.theme('Black')
	win_list = [1000,2000,3000,5000,10000,20000,40000,80000,160000,320000,640000,1250000,2500000,5000000,70000000,0]
	win_amt = win_list[i-1]
	player_data()
	
	layout = [
	[	sg.Text ('Congratulations, your winning amount is Ruppees - ' + str(win_amt),
			   	  text_color = '#FFCC00',
	  		   	  font = 'Arial')],
		[sg.Button('QUIT', key = '-QUIT-', size = (13,1),button_color = ('#FFCC00','#3A0E4B'))]
	]
	
	window = sg.Window("Gamer",layout,no_titlebar = True )
	while True:
	    event, values = window.read()                                                                                 
	    if event == '-QUIT-':
	        break
	window.close() 


def create_mwindow():
	song3.play()
	data = gen_questions()
	sg.theme('black')
	sg.set_options(font = 'Arial 15',button_element_size = (30,2))
	button_size = (25,2)
	button_color = ('#FFCC00','#3A0E4B')
	text_color = ('#FFCC00')
	con_fifty = 1
	con_aud = 1
	con_phone = 1
	global i
	i = 0
	A_Space,B_Space,C_Space,D_Space = option_space(data[i][2],data[i][3],data[i][4],data[i][5]) 
	image_pad = (100,0)
	frame = [			
	[sg.Button('A. '+ data[i][2]+ A_Space,key = 'A',expand_x = True, button_color = button_color, size = (button_size), pad = (5,5),font = 'Consolas 15'),
	 sg.Button('B. '+ data[i][3]+ B_Space,key = 'B',expand_x = True, button_color = button_color, size = (button_size),font = 'Consolas 15')],
	[sg.Button('C. '+ data[i][4]+ C_Space,key = 'C',expand_x = True, button_color = button_color, size = (button_size), pad = (5,5),font = 'Consolas 15'),
	 sg.Button('D. '+ data[i][5]+ D_Space,key = 'D',expand_x = True, button_color = button_color ,size = (button_size),font = 'Consolas 15')]
	]
	control_col = sg.Column([
	[sg.Image(r'Logos\50-50.png',pad = image_pad,key = '-50-',enable_events = True),
	 sg.Image(r'Logos\audiencePole.png',expand_x = True,key = '-AP-',enable_events = True),
	 sg.Image('Logos\phoneAFriend.png',pad = image_pad,key = '-PF-',enable_events = True)],
	[sg.Image('Logos\center4.png',expand_x = True)],
	[sg.Text(str(i+1) + '. ' + data[i][1],key = '-QUE1-', pad = (74,0), expand_x = True )],
	[sg.Text(key = '-QUE2-',pad = (98,0))],
	[sg.Text()],
	[sg.Frame(' Options : ', frame,pad = (70,0),element_justification = 'centre')]
	])
	image_col = sg.Column([[sg.Image("Wins\\picture0.png",pad=(0,9), expand_x = True,key = '-MONEY-')]])
	layout =[[control_col,image_col]]
	window = sg.Window("Kaun Banega Codepati",layout)
	while True:
		
		event, values = window.read()
		
		if event in ['A','B','C','D']:
			if event == data[i][6]:
				mixer.pause()
				if i == 14:
					create_lwindow(i+1)
					break
				else:
					i=i+1
					song3.play()

					print (i)
					
					if len(data[i][1])>58 :
						if data[i][1][57] != ' ':
							window['-QUE1-'].update(str(i+1) + '. ' + data[i][1][0:57] + '-')
							window['-QUE2-'].update(data[i][1][57:])
						else:
							window['-QUE1-'].update(str(i+1) + '. ' + data[i][1][0:58])
							window['-QUE2-'].update(data[i][1][58:])
					else:
						window['-QUE1-'].update(str(i+1) + '. ' + data[i][1])
						window['-QUE2-'].update('')
					A_Space,B_Space,C_Space,D_Space = option_space(data[i][2],data[i][3],data[i][4],data[i][5]) 
					window['A'].update('A. '+ data[i][2] +  A_Space)
					window['B'].update('B. '+ data[i][3] +  B_Space)
					window['C'].update('C. '+ data[i][4] +  C_Space)
					window['D'].update('D. '+ data[i][5] +  D_Space)
					window['-MONEY-'].update('Wins\\picture' + str(i) + '.png') 
			else:
				window[event].update(button_color = '#8B0101')
				window[data[i][6]].update(button_color = 'Green')
				print (data[i][6])
				create_lwindow(i)
				break
		if event == '-50-':
			if con_fifty == 1:
				fifty(data,window)
				con_fifty -= 1
				window[event].update('Logos\\50-50-X.png')                        																													
		if event == '-AP-':
			if con_aud == 1:
				window[event].update('Logos\\audiencePoleX.png')                        																													
				aud_pole(data)
				con_aud -= 1 
		if event == '-PF-':
			if con_phone == 1:
				con_phone -= 1
				window[event].update('Logos\\phoneAFriendX.png')
				phone_friend(data,i)
		
		if event == sg.WIN_CLOSED:
			break
	window.close()


def player_data():
	global player_name, standard_name

	con = c.connect (host='localhost',
					 user='root',
					 password = 'root',
					 database = 'KBC')
	cursor = con.cursor()
	query ="insert into highscores values('{}','{}',{},curdate())".format(player_name,standard_name,win_amt)
	cursor.execute(query)
	con.commit()
	con.close()
	cursor.close()



song1,song2,song3 = create_songs()
create_fwindow()










































