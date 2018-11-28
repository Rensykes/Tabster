import os
from bs4 import BeautifulSoup
import requests
import re
import json


class Finder(object):
	def __init__(self, url):
		#connect to the url
		website = requests.get(url)
		#read html as text 
		html = website.text
		soup = BeautifulSoup(website.text, 'html.parser')
		script = soup.find('script', text=re.compile('window\.UGAPP\.store\.page'))
		json_text = re.search(r'^\s*window\.UGAPP\.store\.page\s*=\s*({.*?})\s*;\s*$',
					  script.string, flags=re.DOTALL | re.MULTILINE).group(1)
		data = json.loads(json_text)


		self.title = self.get_title(data)
		self.artist = self.get_artist(data)
		self.typology = self.get_typology(data)
		self.tuning = self.get_tuning(data)

	def get_title(self, json):
		try:
			title = json.get('data').get('tab').get('song_name')
		except AttributeError:  
			print('Cannot find TITLE')
			title = None
		return title

	def get_artist(self, json):
		try:
			artist = json.get('data').get('tab').get('artist_name')
		except AttributeError:  
			print('Cannot find ARTIST')
			artist = None
		return artist	

	def get_typology(self, json):
		try:
			typology = json.get('data').get('tab').get('type')
		except AttributeError:  
			print('Cannot find TYPOLOGY')
			typology = None
		return typology  

	def get_tuning(self, json):
		try:
			tuning = json.get('data').get('tab_view').get('meta').get('tuning').get('name')
		except AttributeError:  
			print('Cannot find TUNING')
			tuning = None
		return tuning


