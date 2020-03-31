import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from requests.compat import quote_plus
from . import models


BASE_CRAIGLIST_URL ='https://colombia.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):
	return render(request, 'base.html')

def new_search(request):
	search = request.POST.get('search')
	models.Search.objects.create(search=search) 
	#print(quote_plus(search))
	final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
	response = requests.get(final_url)
	data = response.text
	#print(data)
	soup = BeautifulSoup(data, features='html.parser')


	post_listings = soup.find_all('li', {'class':'result-row'})
	

	final_postings = []

	for post in post_listings:  
		post_titles = post.find(class_='result-title').text
		post_url = post.find('a').get('href')

		if post.find(class_='result-price'):
			post_price = post.find(class_='result-price').text
		else:
			post_price = 'N/A'

		if post.find(class_='result-image').get('data-ids'):
			post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1] #split by column will act the sam way than '1:' // index by 1 to get only data-id
			post_image_url = BASE_IMAGE_URL.format(post_image_id)
			#print(post_image_url)
			#print(post_image_id)
		else:
			post_image_url = 'https://craigslist.org/images/peace.jpg'


		final_postings.append((post_titles, post_url, post_price, post_image_url))

	

	stuff_for_frontend = {
		'search': search,
		'final_postings': final_postings,
	}
	
	return render(request, 'craigjuan_list/new_search.html', stuff_for_frontend)