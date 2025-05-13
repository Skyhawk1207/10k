# ------  Necessary Libraries -------

import os
import mysql.connector as mycon
from sys import exit
from time import sleep
import curses as cs

# ------------- Importing ends. ---------------


# -------------------------------- Defining all functions ----------------------------------


#only for development

#def dev():
#	cursor = dbStuff.cursorCreate()
#	x = input("	Do you want to drop the database? (0/1) - ")
#	if x == "0" :
#		cursor.execute("DROP DATABASE IF EXISTS 10k;")
#		cursor.execute("commit;")


#For clearing the screen
def clear():
	if os.name == 'nt':
		 os.system('cls')
	else:
		 os.system('clear')

#Properly Closing the Program
def close():
	dbStuff.conn.close()
	print('\n   Keep heading towards the Ten Thousand!')
	print('   Bye.')
	exit()

# Opening page
def opening():
	clear()
	print('\n\n\n\n\t\t\t\tTen Thousand Hours to Mastery')
	print('\t\t\t*********************************************\n\n')
	print('   What would you like to do?\n')
	print('''\t\t 1. Enter hours spent today.
		 2. Start tracking hours spent.
		 3. Show your progress towards mastery.
		 4. Settings.
		 0. Exit.\n''')

	i=0
	while(i<1):
		userinput = input('   Select an option! - ')
		print()

		if userinput == "1":
			hourOrMin()
		elif userinput == "2":
			timerStart()
		elif userinput == "3":
			progressBar()
			break
		elif userinput == "4":
			settings()
			break
		elif userinput == "0":
			close()
		else:
			print("   I didn't get that. Please try again.")
			sleep(0.7)
			opening()

#Settings tab
def settings():
	clear()
	print("\n\n\n\t\t\t\tWelcome to settings!")
	print("\t\t\t   ******************************")
	print("\n\n     1. Change weekly/monthly/yearly goal\n" \
        	  '     2. Change inital hours\n'\
        	  '     3. Delete hours spent from total\n'\
        	  '     4. Change name of skill\n'\
        	  '     5. Clear all data\n'\
        	  '     6. Privacy and Security\n'\
        	  '     7. Previous Menu\n'\
        	  '     0. Quit')
	c = 0
	while c < 1:
		settingsinput = input('   Select an option! - ')
		if settingsinput == '1':
			dbStuff.changeGoals()
		elif settingsinput == "2":
			dbStuff.changeInitial()
		elif settingsinput == "3":
			dbStuff.deleteHours()
		elif settingsinput == "4":
			dbStuff.changeSkill()
		elif settingsinput == '5':
			dbStuff.purge()
		elif settingsinput == "6":
			privacyMenu()
		elif settingsinput == '7':
			opening()
		elif settingsinput == '0':
			close()
		else:
			print("   I didn't get that!")
			sleep(0.7)
			settings()


#Privacy menu from settings
def privacyMenu():
	clear()
	print("\n\n\n\t\t\t\tPrivacy and Security Settings")
	print("\t\t\t     "+"*"*35)
	print("\n\n     1. Change Username"\
	"\n     2. Change Password"\
	"\n     3. Previous Menu"\
	"\n     0. Exit")

	while True:
		privacyinput = input("\n\n     Select an option! - ")
		if privacyinput == "1":
			dbStuff.changeUser()
		if privacyinput == "2":
			dbStuff.changePassword()
		if privacyinput == "3":
			settings()
		if privacyinput == "0":
			close()
#Input in Hour or minutes
def hourOrMin():
	clear()
	print("\n\n\n\t\t\t\tEnter your progress!")
	print("\t\t\t   ******************************")
	print('\n\n     1. Enter time spent in Hours\n' \
		'     2. Enter time spent in Minutes\n'\
		'     9. Go to Previous Menu\n'\
		'     0. Exit\n')
	timeOption = input('     Select an option! - ')
	enterhours(timeOption)

#Entering Hours functions
def enterhours(timeOption):

	if timeOption == "1" :
		temphours = int(input('\n     Enter time spent in hours- '))
	elif timeOption == "2" :
		temphours = int(input('\n     Enter time spent in minutes- ')) / 60
		temphours = round(temphours,3)
	elif timeOption == "9" :
		opening()
	elif timeOption == "0" :
		close()
	else :
		print("\n     I didn't get that.")
		sleep(0.7)
		hourOrMin()
	x = 0
	while x == 0:
		choice = input('\n     Confirm '+ str(temphours)+ ' hours? (y/n) - ')
		if choice.upper() == 'Y':
			dbStuff.insertHours(temphours)
			break
		elif choice.upper() == 'N':
			enterhours(timeOption)
			continue
		else:
			print("\n     I didn't get that!")
			continue


#For displaying the progress bar

def progressBar():

	w_prog, w_goal, m_prog, m_goal, y_prog, y_goal, t_prog, skill = dbStuff.getHours()
	screen = curses_main()
	screen.nodelay(True)
	height, width, size = progress_resize(screen)
	cs.noecho()
	cs.curs_set(0)
	screen.clear()
	if size == 1 :
		spaces = 50
		denominator = 2
		start = 42
	elif size == 2 :
		spaces = 20
		denominator = 4
		start = 27
	elif size == 0 :
		screen.addstr("NOT ENOUGH SCREEN SIZE!")


	#Title screen
	title = "Progress Towards Ten Thousand Hours of "+skill
	screen.addstr(3, width - (len(title)//2), title)
	screen.addstr(4,width-(len(title)//2)-3, "*"*(len(title)+6))
	screen.refresh()

	#Weekly Progress

	try :
		w_prog = float(w_prog)
	except:
		w_prog = 0

	try :
		w_goal = float(w_goal)
	except:
		w_goal = 0

	if w_goal == 0 :
		percent = 0
	else :
		percent = round((w_prog/w_goal)*100,3)

	goaltext = "("+str(round(w_prog,3))+"/"+str(w_goal)+" hours)"
	if size in [1,2]:
		screen.addstr(height-6, (width-start-1),"Weekly Progress: |"+" "*spaces+" | ("+format(percent,'.3f')+"%)")
		screen.addstr(height-5, width-(len(goaltext)//2), goaltext)

		if percent>=1:
			for i in range(round(percent/denominator)):
				screen.addstr(height-6, width-(spaces//2) ," "*(i+1), cs.A_STANDOUT)
				screen.refresh()
				sleep(0.015)
				if i>=spaces:
					break

	elif size == 3:
		screen.addstr(height-7, width-9 ,"Weekly Progress: ")
		screen.addstr(height-5, width-6-(len(goaltext)//2), "("+goaltext+" or "+format(percent,'.3f')+"%)")
		screen.addstr(height-6, width-6,"|"+" "*10+" |")

		if percent>=1:
			for i in range(round(percent/10)):
				screen.addstr(height-6,width-5," "*(i+1), cs.A_STANDOUT)
				screen.refresh()
				sleep(0.015)
				if i>=spaces:
					break

	sleep(0.01)

	#Monthly Progress

	try:
		m_prog = float(m_prog)
	except:
		m_prog = 0

	try:
		m_goal = float(m_goal)
	except:
		m_goal = 0

	if m_goal == 0 :
		percent = 0
	else :
		percent = round((m_prog/m_goal)*100,3)

	goaltext = "("+str(round(m_prog,3))+"/"+str(m_goal)+" hours)"
	if size in [1,2]:
		screen.addstr(height-3, (width-start-2),"Monthly Progress: |"+" "*spaces+" | ("+format(percent,'.3f')+"%)")
		screen.addstr(height-2, width-(len(goaltext)//2), goaltext)
		if percent>=1:
			for i in range(round(percent/denominator)):
				screen.addstr(height-3, width-(spaces//2) ," "*(i+1), cs.A_STANDOUT)
				screen.refresh()
				sleep(0.015)
				if i>=spaces:
					break
	elif size == 3:
		screen.addstr(height-3, width-9 ,"Monthly Progress: ")
		screen.addstr(height-1, width-6-(len(goaltext)//2), "("+goaltext+" or "+format(percent,'.3f')+"%)")
		screen.addstr(height-2, width-6,"|"+" "*10+" |")
		if percent>=1:
			for i in range(round(percent/10)):
				screen.addstr(height-2,width-5," "*(i+1), cs.A_STANDOUT)
				screen.refresh()
				sleep(0.015)
				if i>=spaces:
					break
	sleep(0.01)

	#Yearly progress
	try:
		y_prog = float(y_prog)
	except:
		y_prog = 0

	try:
		y_goal = float(y_goal)
	except :
		y_goal = 0

	if y_goal == 0 :
		percent = 0
	else :
		percent = round((y_prog/y_goal)*100,3)

	goaltext = "("+str(round(y_prog,3))+"/"+str(y_goal)+" hours)"
	if size in [1,2]:
		screen.addstr(height, (width-start-1),"Yearly Progress: |"+" "*spaces+" | ("+format(percent,'.3f')+"%)")
		screen.addstr(height+1, width-(len(goaltext)//2), goaltext)
		if percent>=1:
			for i in range(round(percent/denominator)):
				screen.addstr(height, width-(spaces//2) ," "*(i+1), cs.A_STANDOUT)
				screen.refresh()
				sleep(0.015)
				if i>=spaces:
					break
	elif size == 3:
		screen.addstr(height+1, width-9 ,"Yearly Progress: ")
		screen.addstr(height+3, width-6-(len(goaltext)//2), "("+goaltext+" or "+format(percent,'.3f')+"%)")
		screen.addstr(height+2, width-6,"|"+" "*10+" |")
		if percent>=1:
			for i in range(round(percent/10)):
				screen.addstr(height+2,width-5," "*(i+1), cs.A_STANDOUT)
				screen.refresh()
				sleep(0.015)
				if i>=spaces:
					break

	sleep(0.01)

	#Total progress
	if t_prog != '' :
		t_prog = float(t_prog)
	else:
		t_prog = 0

	percent = round((t_prog/10000)*100,3)
	goaltext = "("+str(round(t_prog,3))+"/10000 hours)"
	if size in [1,2]:
		screen.addstr(height+3, (width-start),"Total Progress: |"+" "*spaces+"| ("+format(percent,'.3f')+"%)")
		screen.addstr(height+4, width-(len(goaltext)//2), goaltext)
		if percent>=1:
			for i in range(round(percent/denominator)):
				screen.addstr(height+3, width-(spaces//2) ," "*(i+1), cs.A_STANDOUT)
				screen.refresh()
				sleep(0.015)
				if i>=spaces:
					break
	elif size == 3:
		screen.addstr(height+5, width-8 ,"Total Progress: ")
		screen.addstr(height+7, width-6-(len(goaltext)//2), "("+goaltext+" or "+format(percent,'.3f')+"%)")
		screen.addstr(height+6, width-6,"|"+" "*10+"|")
		if percent>=1:
			for i in range(round(percent/10)):
				screen.addstr(height+6,width-5," "*(i+1), cs.A_STANDOUT)
				screen.refresh()
				sleep(0.015)
				if i>=spaces:
					break

	sleep(0.01)
	screen.addstr(height+ 10, 0, "     Press Enter to Go Back...")

	while True:
		z=screen.getch()
		if z == cs.KEY_ENTER or z in [10,13]:
			curses_end(screen)
			opening()
		z = ""



#----------------- Functions for Timer ---------------------

def timerStart() :

	screen = curses_main()
	y,x = screen.getmaxyx()
	height = y//2
	width = x//2
	hr,mins,sec,timeinhr, height, width = timer(screen, height, width)
	timer_end(screen,hr,mins,sec, timeinhr, height, width)

def timer(screen, height, width):
	mins = 0
	sec = 0
	hr = 0
	ms = 0
	sel_index = 0
	while True:
		sleep(0.1)
		if ms == 9 :
			ms = 0
			if sec == 59 :
				if mins == 59 :
					hr+=1
					mins = 0
				else :
					mins+=1
				sec = 0
			else:
				sec = sec+1
		else :
			ms+=1

		timestr = str(hr).zfill(2)+" hr : "+str(mins).zfill(2)+" mins : "+str(sec).zfill(2)+" sec"

		screen.clear()
		str1 = "You have been practising for :"
		screen.addstr(height-4,width-(len(str1)//2), str1)
		screen.addstr(height,width-(len(timestr)//2), str(timestr), cs.A_BOLD)
		if sel_index == 0 :
			screen.addstr(height+4,width-4," PAUSE ")
			screen.addstr(height+5,width-3," STOP ")
		elif sel_index == 1:
			screen.addstr(height+4,width-4," PAUSE ",cs.A_STANDOUT)
			screen.addstr(height+5,width-3," STOP ")
		elif sel_index == 2:
			screen.addstr(height+4,width-4," PAUSE ")
			screen.addstr(height+5,width-3," STOP ",cs.A_STANDOUT)
		screen.refresh()

		z = screen.getch()
		if  z == cs.KEY_DOWN and sel_index == 0:
			sel_index = 1
			screen.addstr(height+4,width-4," PAUSE ", cs.A_STANDOUT)
			screen.addstr(height+5,width-3," STOP ")
		elif sel_index == 1:
			if z == cs.KEY_UP:
				sel_index = 0
			elif z == cs.KEY_DOWN and sel_index == 1:
				sel_index = 2
			elif z == cs.KEY_ENTER or z in [10,13]:
				screen.nodelay(False)
				screen.clear()
				str1 = "You have been practising for :"
				screen.addstr(height-4,width-(len(str1)//2), str1)
				screen.addstr(height,width-(len(timestr)//2), str(timestr), cs.A_BLINK)
				screen.addstr(height+4,width-4," RESUME ", cs.A_STANDOUT)
				screen.addstr(height+5,width-3," STOP ")
				screen.refresh()

				while True:
                                        z = screen.getch()
                                        if z == cs.KEY_ENTER or z in [10,13]:
                                                screen.nodelay(True)
                                                break
                                        else:
                                                continue


		elif sel_index == 2:
			if z == cs.KEY_UP:
				sel_index = 1
			elif z == cs.KEY_ENTER or z in [10,13]:
				screen.clear()
				screen.nodelay(False)
				timeinhr = round((mins/60)+hr+(sec/3600),3)
				conf = "Press Enter again to confirm "+str(timeinhr)+" hours, or ANY other key to resume timer."
				screen.addstr(height,width-(len(conf)//2),conf)
				screen.refresh()
				conf = screen.getch()

				if conf==cs.KEY_ENTER or conf in [10,13]:
                                         break
				else :
					screen.nodelay(True)

		elif z == cs.KEY_RESIZE:
			sel_index=1
			height,width = curses_resize()

	return hr,mins,sec, timeinhr, height, width

def timer_end(screen, hr,mins,sec, timeinhr, height, width):
	screen.clear()
	str2 = "The time is "+str(hr)+" hours, "+str(mins)+" mins, "+str(sec)+" sec, or "+str(timeinhr)+" hours."
	screen.addstr(height, width - (len(str2)//2), str2)
	screen.addstr(height+2, width - 5, "(Saving..)")
	screen.refresh()
	curses_end(screen)
	dbStuff.insertHours(timeinhr)

#----------------- Functions for Curses ---------------------

def curses_main():
	screen = cs.initscr()
	cs.start_color()
	if cs.has_colors():
		cs.use_default_colors()
	cs.noecho()
	screen.keypad(True)
	cs.curs_set(0)
	screen.nodelay(True)
	return screen

def curses_resize():
	global height
	global width
	y,x = screen.getmaxyx()
	screen.clear()
	cs.resizeterm(y, x)
	height = y//2
	width = x//2
	return height, width

def progress_resize(screen):

	y,x = screen.getmaxyx()
	screen.clear()
	cs.resizeterm(y,x)
	height = y//2
	width = x//2
	while True:
		if width >= 50:
			size = 1
			break
		elif width >= 30  :
			size = 2
			break
		elif width >= 15:
			size = 3
			break
		elif screen.getch() == cs.KEY_RESIZE :
			continue
		else :
			size = 0
			break
	return height, width, size

def curses_end(screen):
	screen.keypad(False)
	cs.curs_set(1)
	cs.echo()
	cs.endwin()

#------------------- Curses Stuff End -------------------------

#Connecting with MySQL Database, and other Database things
class dbStuff:

	y=1
	while y==1:
		try:
			conn = mycon.connect(user = "root", password = "", host = "localhost")
			break
		except :
			if os.name!="nt":
				os.system("sudo service mysql restart")
				continue

	#To create a cursor
	def cursorCreate():
		conn = dbStuff.conn
		cursor = conn.cursor()
		return cursor

	#Opening the needed database
	def dbcon():
		cursor = dbStuff.cursorCreate()
		cursor.execute("Show databases;")
		dbList = cursor.fetchall()

		if ("10k",) not in dbList:
			dbStuff.firstUse()
			dbStuff.initialSettings()
		else:
			cursor.execute("use 10k;")

	#Setting up database and tables for first time users
	def firstUse():
		cursor = dbStuff.cursorCreate()
		cursor.execute("CREATE database 10k;")
		cursor.execute("use 10k;")
		cursor.execute("Create table hours_spent(hours decimal(8,3), entry_date date);")
		cursor.execute("Create table credentials(Name varchar(30), password varchar(100), skill varchar(20));")
		cursor.execute("Create table initial_hours(hours decimal(8,3), initial_date date, m_goal decimal(8,3), w_goal decimal(8,3),"+
				"y_goal decimal(8,3));")

	#For all the initial settings
	def initialSettings():
		clear()
		cursor = dbStuff.cursorCreate()
		print('\n\n\n\n\t\t\t\tTen Thousand Hours to Mastery')
		print('\t\t\t*********************************************\n\n')
		print("     Welcome to Ten Thousand Hours to Mastery!\n\n"\
			"     It's said one truly masters a skill, when they practice it for Ten Thousand Hours."\
			"\n     Let's track the hours you've spent till you reach that Ten Thousasnd!"\
			"\n\n     Before that, please go through a few initial steps.")

		input("\n\n\n\n     Press any key to continue...") #(Just so they have time to read all that intro shit.)
		clear()

		#Getting an username and a password
		print('\n\n\n\n\t\t\t\tTen Thousand Hours to Mastery')
		print('\t\t\t*********************************************\n\n')

		username = input("     Please tell us your name or an alias. - ")
		x=0
		while x==0:
			password = input("\n     Please choose a password. - ")
			confirm  = input("     Please re-enter the password. - ")
			if(password == confirm):
				print("\n     Confirmed!")
				break
			else :
				print("     Sorry your passwords didn't match! Could you enter them again?")
				continue
		print("\n\n     This password will be needed to change settings in the future.")
		input("\n\n\n\n     Press enter to continue...")
		#Getting skill name and initial hours.
		clear()
		print('\n\n\n\n\t\t\t\tTen Thousand Hours to Mastery')
		print('\t\t\t*********************************************\n\n')
		skill = input("\n\n     Hello, " + username +"! What skill or art are you aiming to master? - ")

		while x==0:
			if len(skill)==0:
				print("\n     Sorry, you didn't enter a skill. Could you try again?")
				skill = input("\n     What skill or art are you aiming to master? - ")
				continue
			else:
				break
		skill = skill.capitalize()
		initialTime = input("\n\n     "+skill+"? That's great!\n"\
				"     How many hours have you spent on it till now? (If you're starting your journey now, please enter 0)  -  ")
		if initialTime == "":
			initialTime = "0"
		#Getting monthly and weekly goals
		clear()
		print('\n\n\n\n\t\t\t\tTen Thousand Hours to Mastery')
		print('\t\t\t*********************************************\n\n')
		print("\n\n     Last Step! Setting smaller goals go a long way in achieving the ultimate Ten Thousand."\
			"\n\n     Do you wish to set a Monthly/Weekly goal?")


		print("\n     1. Weekly and  Monthly Goal.\n"\
			"     2. Yearly Goal.\n"\
			"     3. All three. \n"\
			"     0. Skip. \n")

		x=0
		while x==0:
			monOrWeek = input("\n     Please select an option - ")
			monthlyGoal =  "0"
			weeklyGoal =  "0"
			yearlyGoal = "0"
			if monOrWeek == "1":
				while True:
					try:
						print("\n\n     (Please enter 0 if you do not wish to set a goal right now)")
						weeklyGoal = int(input("\n     Set a weekly goal! - "))
						monthlyGoal = int(input("\n\n     Set a monthly goal! - "))
						break
					except:
						print("\n     Something went wrong. Please re-enter your goals. (Enter only numbers)")
						continue
				break
			elif monOrWeek == "2":
				while True:
					try:
						yearlyGoal = int(input("\n\n     Set a yearly goal! - "))
						break
					except:
						print("\n     Something went wrong. Please re-enter your goals. (Enter only numbers)")
						continue
				break 
			elif monOrWeek=="3":
				while True:
					try:
						weeklyGoal = int(input("\n\n     Set a weekly goal! - "))
						monthlyGoal = int(input("\n\n     Set a monthly goal! - "))
						yearlyGoal = int(input("\n\n     Set a yearly goal! - "))
						break
					except:
						print("\n     Something went wrong. Please re-enter your goals. (Enter only numbers)")
						continue
				break
			elif monOrWeek == "0" :
				print("\n\n     Alright! You can come back to this later.")
				break
			else :
				print("\n\n     Sorry, I didn't get that. Please try again.")
				continue
		print("\n\n     Goals have been set! They can be changed anytime in the Settings menu.")

		input("\n\n\n     Press any key to continue...")
		#Entering all the info to a database.
		sqlQuery = 'Insert into credentials values("'+ username + '","' + password +'","'+skill+'");'
		#^^^ The fact that we have to insert varchar in " " is the reason for this whole mess;
		cursor.execute(sqlQuery)

		sqlQuery = "Insert into initial_hours values(" +initialTime+ ", curdate(), " + str(monthlyGoal) + " , " + str(weeklyGoal) +"," + str(yearlyGoal)+");"
		cursor.execute(sqlQuery)
		cursor.execute("commit;")

		#Now some dialogues to end the initialization.
		clear()
		print('\n\n\n\n\t\t\t\tTen Thousand Hours to Mastery')
		print('\t\t\t*********************************************\n\n')

		print("\n\n\n     All done! You can change all of these from the Settings menu. You can start tracking your time now!")
		input("\n     There is no shortcut or easy way to Mastery. It's the reward one gets for their dedication and hard work."\
			"\n     Best of luck!"\
			"\n\n\n\n     Press any key to continue ...")
		opening()

	#Inserting hours, and current date into the database
	def insertHours(hours):
			sqlQuery = "Insert into hours_spent values("+str(hours)+", curdate());"
			cursor = dbStuff.cursorCreate()
			cursor.execute(sqlQuery)
			cursor.execute("commit;")
			print("\n     Hours Added! Another step towards Mastery.")

			choice = input("\n     Do you wish to see your progress? (y/n) - ")
			x=0
			while x==0:
				if choice.upper() == "Y" :
					progressBar()
				elif choice.upper() == "N":
					opening()
				else:
					print("\n     I didn't get that!")
					continue

	#Retrieving hours spent from database. (This will later be used for progress bar and stuff as well)
	def getHours():

			cursor = dbStuff.cursorCreate()
			cursor.execute("Select m_goal from initial_hours;")
			monthGl = str(cursor.fetchall())
			end = monthGl.find(",")-2
			monthGl = monthGl[11:end]

			cursor = dbStuff.cursorCreate()
			cursor.execute("Select w_goal from initial_hours;")
			weekGl = str(cursor.fetchall())
			end = weekGl.find(",")-2
			weekGl = weekGl[11:end]

			cursor.execute("Select skill from credentials;")
			skill = str(cursor.fetchall())
			end = skill.find(",")-1
			skill = skill[3:end]

			cursor.execute("Select hours from initial_hours;")
			initialHr = str(cursor.fetchall())
			start = initialHr.find("'")+1
			end = initialHr.find(",")-2
			initialHr = initialHr[start:end]

			cursor.execute("Select SUM(hours) from hours_spent where MONTH(entry_date)=MONTH(curdate()) and YEAR(entry_date)= YEAR(curdate());")
			monthProg = str(cursor.fetchall())
			start = monthProg.find("'")+1
			end = monthProg.find(",")-2
			monthProg = monthProg[start:end]

			cursor.execute("Select SUM(hours) from hours_spent where WEEK(entry_date)=WEEK(curdate()) and YEAR(entry_date)=YEAR(curdate());")
			weekProg = str(cursor.fetchall())
			start = weekProg.find("'")+1
			end = weekProg.find(",")-2
			weekProg =weekProg[start:end]

			cursor.execute("Select SUM(hours) from hours_spent where YEAR(entry_date)=YEAR(curdate());")
			yearProg = str(cursor.fetchall())
			end = yearProg.find(',')-2
			yearProg = yearProg[11:end]

			cursor.execute("Select y_goal from initial_hours;")
			yearGl = str(cursor.fetchall())
			end = yearGl.find(',')-2
			yearGl = yearGl[11:end]

			cursor.execute("Select SUM(hours) from hours_spent;")
			totalProg = str(cursor.fetchall())
			end = totalProg.find(",")-2
			totalProg = totalProg[11:end]

			if totalProg == '' :
				totalProg = 0

			totalProg = float(totalProg) + float(initialHr)

			return weekProg, weekGl, monthProg, monthGl, yearProg, yearGl, totalProg, skill

	#------------------- ALL SETTINGS MENU RELATED FUNCTIONS ------------
	def purge():
		print('n\n\n\t\t\t\tALERT!!!')
		print("\t\t\t   ******************************")
		print('\n\n     This option will delete all the data you have entered\n'\
			'     This includes the personal information, such as, username and password, as well as all the hours entered.\n'\
			'     You need to input your password for this option...')

		cursor = dbStuff.cursorCreate()
		cursor.execute('use 10k;')
		cursor.execute('select password from credentials;')
		purgedata = cursor.fetchall()

		z = 0
		while z<1:
			purgeinput = input('\n\n   Enter your password! Or leave an empty space to quit! - ')

			if purgedata[0][0] == purgeinput:
				print('\n\n     WARNING - All data will be erased! This action is NOT reversible.')
				finalcon = input('     Are you sure you want to delete all data? y/n -')

				if finalcon.lower() == "y":
					print('\n\n\n\n     Deleting all data!')
					cursor.execute('drop database 10k;')
					clear()
					print("\n\n\n\n     All data has been deleted. Please reopen the program to continue.")
					input("\n\n\n     Press any key to exit..." )
					exit()
				elif finalcon.lower() == 'n':
					print('     Cancelling...')
					opening()
					break

				elif purg1einput == '':
					z = 1
				else:
						print('     Password incorrect!')
						continue

	def changeGoals():
		cursor = dbStuff.cursorCreate()

		cursor.execute("Select w_goal from initial_hours;")
		weekgoal = str(cursor.fetchall())
		end = weekgoal.find(",")-2
		weekgoal = weekgoal[11:end]

		cursor.execute("Select m_goal from initial_hours;")
		monthgoal = str(cursor.fetchall())
		end = monthgoal.find(",")-2
		monthgoal = monthgoal[11:end]

		cursor.execute("Select y_goal from initial_hours;")
		yeargoal = str(cursor.fetchall())
		end = yeargoal.find(",")-2
		yeargoal = yeargoal[11:end]

		print("\n\n     Current weekly goal is: "+weekgoal+" hours. If you do not wish to change it, please enter 0.")
		weekgoal = input("     What's your new weekly goal? - ")

		print("\n\n     Current monthly goal is: "+monthgoal+" hours. If you do not wish to change it, please enter 0.")
		monthgoal = input("     What's your new monthly goal? - ")

		print("\n\n     Current yearly goal is: "+yeargoal+" hours. If you do not wish to change it, please enter 0.")
		yeargoal = input("     What's your new yearly goal? - ")

		while True:
			confirm = input("\n\n     Are you sure you want to update the goals? (y/n) - ")
			if confirm.upper() == "Y":
				if weekgoal != 0:
					query = "Update initial_hours set w_goal = " + weekgoal+ ";"
					cursor.execute(query)
				if monthgoal != 0 :
					query = "Update initial_hours set m_goal = " + monthgoal+ ";"
					cursor.execute(query)
				if yeargoal != 0 :
					query = "Update initial_hours set y_goal = " + yeargoal+ ";"
					cursor.execute(query)
				print("\n\n      Goals Updated!")
				sleep(0.75)
				break
			elif connfirm.upper() == "N" :
				print("\n\n     Cancelling!")
				sleep(0.75)
				break
			else :
				print("\n\n     I didn't get that!")
				continue
		settings()

	def changeInitial():

		cursor = dbStuff.cursorCreate()
		cursor.execute("select hours from initial_hours;")
		initial = str(cursor.fetchall())
		end = initial.find(",")-2
		initial = initial[11:end]

		print("\n\n     The hours you've spent before you began tracking them are " +initial + "hours")
		print("\n     (Enter 0 if you do not wish to change the initial hours)")
		initial = int(input("     How much time (in minutes) have you spent before tracking? - "))
		timeinhrs = round(initial/60,3)

		while True:
			confirm = input("\n\n     Are you sure you want to change initial hours spent to "+str(initial)+"? (y/n) - ")
			if confirm.upper() == "Y":
				if initial != 0 :
					query = "Update initial_hours set hours = " +str(initial)+ ";"
					cursor.execute(query)
					print("\n\n     Initial hours updated!")
				else:
					primt("\n\n     Cancelling!")
				sleep(0.75)
				break
			elif confirm.upper() == "N":
				print("\n\n     Cancelling!")
				sleep(0.75)
				break
			else :
				print("\n\n     I didn't get that!")
				continue
		cursor.execute("commit;")
		settings()

	def deleteHours():
		cursor = dbStuff.cursorCreate()
		print("\n\n     If you do not wish to reduce the total number of hours you've spent so far, enter 0")
		reduce = int(input("\n     How much time (in minutes) do you want to reduce? - "))
		timeinhr = round(reduce/60,3)

		while True:
			confirm = input("\n     Are you sure you want to remove "+str(timeinhr)+" hours from the total? (y/n) - ")
			if confirm.upper() == "Y":
				if reduce != 0 :
					query = "Insert into hours_spent values("+str(0-timeinhr)+", curdate());"
					cursor.execute(query)
					print("\n\n     Removed the hours from total!")
				else :
					print("\n\n      Cancelling!")
				sleep(0.75)
				break
			elif confirm.upper == "N":
				print("\n\n     Cancelling!")
				sleep(0.75)
				break
			else :
				print("\n\n     I didn't get that!")
				continue
		settings()

	def changeUser():
		cursor = dbStuff.cursorCreate()
		print("\n\n    (If you do not wish to change your username, enter 0.)")
		username = input("\n    What's your new username? - ")
		if username == "0":
			print("\n\n     Cancelling!")
			sleep(0.75)
			privacyMenu()		

		while True:
			confirm = input("\n\n     Are you sure you want to change your username to "+username+" ? (y/n) - ")
			if confirm.upper() == "Y":
				query = 'Update credentials set Name="'+username+'";'
				cursor.execute(query)
				cursor.execute("commit;")
				print("\n\n     Username changed!")
				sleep(0.75)
				privacyMenu()
			elif confirm.upper()=="N":
				print("\n\n     Cancelling!")
				sleep(0.75)
				privacyMenu()
			else:
				print("\n\n     I didn't get that!")
				continue
		privacyMenu()

	def changePassword():
		cursor = dbStuff.cursorCreate()
		print("\n\n    (If you do not wish to change your password, enter 0.)")
		query = "Select password from credentials;"
		cursor.execute(query)
		oldPassword = str(cursor.fetchall())
		end = oldPassword.find(',')-1
		oldPassword = oldPassword[3:end]

		while True :
			passconfirm = input("\n\n     Old Password - ")

			if passconfirm == oldPassword :
				while True:
					newPass = input("\n     New Password - ")
					newPassConfirm = input("     Confirm New Password - ")
					if newPass == newPassConfirm :
						query = 'Update credentials set password = "'+newPass+'";'
						if newPass!="0":
							cursor.execute(query)
							cursor.execute("commit;")
							print("\n\n     Password changed!")
							sleep(0.75)
							privacyMenu()
						else:
							print("\n\n     Cancelling!")
							sleep(0.75)
							privacyMenu()
					else:
						print("\n     Passwords did not match! Try again.")
						continue
				break
			else :
				print("\n     The password is incorrect. Please try again.")
				continue

	def changeSkill():
		cursor = dbStuff.cursorCreate()
		query = "Select skill from credentials;"
		cursor.execute(query)
		skill = str(cursor.fetchall())
		end = skill.find(",")-1
		skill = skill[3:end]

		print("\n\n     Your current skill is " +skill+". (If you don't want to change it, please enter 0.)")

		while True:
			skill = input("\n     Enter your new skill! - ")
			if skill !="0":
				while True :
					confirm = input("\n\n     Are you sure you want to change your skill to "+skill+"? (y/n) - ")
					if confirm.upper()=="Y":
						query = 'Update credentials set skill ="'+skill+'";'
						cursor.execute(query)
						cursor.execute("commit;")
						print("\n\n     Skill changed!")
						sleep(0.75)
						privacyMenu()
					elif confirm.upper()=="N":
						print("\n\n     Cancelling!")
						sleep(0.75)
						privacyMenu()
					else:
						print("\n\n     I didn't get that!")
						continue
				break
			elif skill == "0" :
				print("\n\n     Cancelling!")
				sleep(0.75)
				break
			else :
				print("\n\n     I didn't get that!")
				continue
		settings()
# ---------------------------------------- Function Defining ends. -----------------------------------------
# the program begins here
#dev()
dbStuff.dbcon()
opening()
