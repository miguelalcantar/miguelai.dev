from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import sys
import pandas as pd
from datetime import datetime
from telegram_bot import telegram_bot_sendtext

abs_path="/home/miguel/Documents/proj/python/scraping/"

def to_datetime(s):

	s = s.replace(',','')
	i = s.find(' ')
	j = s.find(' ', i + 1)
	month = s[i+1:j]

	if month == 'Enero':
		new_month = 'Jan'
	elif month == 'Febrero':
		new_month = 'Feb'
	elif month == 'Marzo':
		new_month = 'Mar'
	elif month =='Abril':
		new_month = 'Apr'
	elif month =='Mayo':
		new_month = 'May'
	elif month =='Junio':
		new_month = 'Jun'
	elif month =='Julio':
		new_month = 'Jul'
	elif month =='Agosto':
		new_month = 'Aug'
	elif month =='Septiembre':
		new_month = 'Sep'
	elif month =='Octubre':
		new_month = 'Oct'
	elif month =='Noviembre':
		new_month = 'Nov'
	else:
		new_month = 'Dec'

	s = s.replace(month,new_month)

	dt = datetime.strptime(s, '%d %b %Y %H:%M')

	return dt
	
	
def scrap_projects(query=None):
	
	# options
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('headless');
	chrome_options.add_argument("--incognito")

	# read csv
	try:
		data = pd.read_csv(f'{abs_path}workana_jobs.csv')
		data = data[data['query'] == query]
	except FileNotFoundError:
		data = pd.DataFrame()

	# web driver
	driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
	# request
	query_string = f'query={query}&' if query else ''	
	driver.get(f"https://www.workana.com/jobs?{query_string}category=it-programming&language=es%2Cen")
	# content
	projects = driver.find_elements_by_xpath("//div[@class='project-item  js-project']")
	skills = driver.find_elements_by_xpath("//div[@class='skills']")

	proj = {
		'query':[],
		'date':[],
		'link':[],
		'title':[],
		'budget':[],
		'skills':[]
	}

	for project in zip(projects,skills):

		# date
		src_code = project[0].get_attribute("outerHTML")
		i = src_code.find('h5 title="') + len('h5 title="')
		j = src_code.find('"',i)
		date = src_code[i:j]
		dt = to_datetime(date)

		if not data.empty:
			if datetime.strptime(data.iloc[0]['date'], '%Y-%m-%d %H:%M:%S') <= dt:
				break

		proj['date'].append(dt)

		# query
		proj['query'].append(query)
		# i += 20
		# link
		i = src_code.find('a href',j) + 8
		j = src_code.find('"',i)
		link = f'https://www.workana.com{src_code[i:j]}/'
		proj['link'].append(link)
		# title
		i = src_code.find('title',j) + 7
		j = src_code.find('"',i + 1)
		title = src_code[i:j]
		proj['title'].append(title)
		# budget
		i = src_code.find('USD')
		j = src_code.find('<',i)
		budget = src_code[i:j]
		proj['budget'].append(budget)
		# skills
		skills = project[1].text
		proj['skills'].append(skills)

		# send notification
		send_notification = f'[New Project]({link})\n{date}\n{budget}'
		telegram_bot_sendtext(send_notification)


	data_proj = pd.DataFrame.from_dict(proj)

	# writing
	if data.empty:
		data_proj.to_csv(f'{abs_path}workana_jobs.csv', index=False)
	else:
		frames = [data_proj,data]
		new_data = pd.concat(frames)
		new_data.to_csv(f'{abs_path}workana_jobs.csv', index=False)

	# making sure of closing chrome (?)
	driver.close()
	driver.quit()

if __name__ == '__main__':

	if len(sys.argv) > 1:
		scrap_projects(sys.argv[1])
	else:
		scrap_projects()