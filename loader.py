#!/usr/bin/env python



import re

from robobrowser import RoboBrowser

from bs4 import BeautifulSoup

import requests

from robobrowser.forms.form import Form

import pycurl

from urllib.parse import urlencode

import dryscrape



browser = RoboBrowser(history=True, parser='html.parser')

print("enter the anime you want to download")

inp = input()

anime = inp.split(" ")

ur = ""

for x in anime:

	ur = ur+x+"%"

url = "http://www1.gogoanime.tv//search.html?keyword="+ur

print(url)

browser.open(url)

anchors = browser.get_links(inp)

links=[]

titles=[]

for x in anchors:

	links.append(x['href'])

	titles.append(x['title'])



print("enter the no. of anime you want to download")

i = 1

for t in titles:

	print(str(i)+"> "+t)

	i+=1



base_url = "http://www1.gogoanime.tv"

selec = int(input())


browser.follow_link(anchors[selec-1])



base_title = titles[selec-1]

selected = titles[selec-1].split(" ")

inter = ""

for s in selected:

	inter=inter+s.lower()+"-"

selected = inter[0:len(inter)-1]

print(selected)

z = browser.parsed

z = str(z)

soup = BeautifulSoup(z , 'html.parser')



movie_id = soup.find_all("input" , class_="movie_id")

default_ep = soup.find_all("input" , class_="default_ep")

a = soup.find_all("a" ,class_="active")

movie_id=movie_id[0]

default_ep=default_ep[0]

a=a[0]

movie_id=movie_id['value']

default_ep=default_ep['value']

ep_start=a['ep_start']

ep_end=a['ep_end']

print(movie_id + " " + default_ep + " " + ep_start + " " + ep_end)

url = base_url + '/load-list-episode?ep_start='+ep_start+'&ep_end='+ep_end+'&id='+movie_id+'&default_ep='+default_ep 

r = requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')

episodes = soup.find_all("a")

print(episodes)

no_of_episodes = len(episodes)

print(no_of_episodes)

print('enter starting and ending episode')

inp =input()

inp = inp.split(' ')

stend = [int(x.strip()) for x in inp]




for num in range(no_of_episodes-int(stend[0]),no_of_episodes-int(stend[1])-1,-1):

	print(num)

	link=((episodes[num])['href'])

	url = base_url+link

	url = re.sub('[\s+]', '', url)

	print(url)

	browser.open(url)

	soup = BeautifulSoup(str(browser.parsed),'html.parser')

	dl = soup.find_all("div" ,class_="download-anime")

	soup = BeautifulSoup(str(dl[0]),'html.parser')

	dl = soup.find_all("a")

	browser.follow_link(dl[0])

	soup = BeautifulSoup(str(browser.parsed),'html.parser')

	mirror_link = soup.find_all("div" ,class_="mirror_link")

	lin = []

	source = []

	for x in mirror_link:

		sap = BeautifulSoup(str(x),'html.parser')

		tag = str(sap.find("h6").string)

		if(tag == "Mirror Link"):

			sp = BeautifulSoup(str(x),'html.parser')

			anchs = sp.find_all("a")

			for y in anchs:

				lin.append(y['href'])

				source.append(y.string)

	l = len(lin)

	dl = l-1

	for x in range(l-1,-1,-1):

		if(source[x] == "Download mp4upload"):

			dl = x

			break

		elif(source[x] == "Download openload"):

			dl = x

			break

		else:

			print("Sorry no script supported download link found")



	dlselected = lin[dl]

	browser.open(dlselected)

	filename = base_title + str(no_of_episodes-num)+".mp4"




	if(source[dl] == "Download mp4upload"):

		print('Downloading from mp4upload')

		form = browser.get_forms()

		num = 0

		i = 0

		for f in form:

			if(f['op'].value=="download2"):

				num = i

			i+=1

		form = form[num]

		data = {'op' : form['op'].value, 'id' : form['id'].value, 'rand' : form['rand'].value, 'referer' : form['referer'].value,	'method_free' : form['method_free'].value,	'method_premium' : form['method_premium'].value}

		c = pycurl.Curl()

		c.setopt(c.URL, dlselected)

		postfields = urlencode(data)

		c.setopt(c.POSTFIELDS, postfields)

		fp= open(filename, "wb")

		c.setopt(c.WRITEDATA, fp)

		c.setopt(c.FOLLOWLOCATION, True)

		print("starting download,happy waiting..")

		c.perform()

		fp.close()

		c.close()

		fp= open(filename, "r")

		try:

			fi=fp.read()

			sipa = BeautifulSoup(fi, 'html.parser')

			if(sipa.find('h1').string == '404 Not Found'):

				for x in range(l-1,-1,-1):

					if(source[x] == "Download openload"):

						dl = x

						break

				print(str(dl))

				print('couldn;t download form mp4upload')

			else:

				continue

		except UnicodeDecodeError:

			continue

	if(source[dl] == "Download openload"):

		print('Downloading from openload')

		dlselected = lin[dl]

		dry = dryscrape.Session()

		dry.set_attribute('auto_load__images', False)

		dry.set_attribute('javascript_can_open_windows', False)

		dry.visit(dlselected)

		r = dry.body()

		#print(r)

		sip = BeautifulSoup(r,'html.parser')

		downloadlinkis = sip.find('span', id='streamurl')

		print(downloadlinkis)

		downloadlinkis = downloadlinkis.string

		downloadlinkis = "https://openload.co/stream/"+downloadlinkis

		c = pycurl.Curl()

		c.setopt(c.URL, downloadlinkis)

		fp= open(filename, "wb")

		c.setopt(c.WRITEDATA, fp)

		#range metter 1 megabyte is 1048576 byte just for knowladge

		#c.setopt(c.RANGE, '5242880-52428800') 

		c.setopt(c.FOLLOWLOCATION, True)

		print("starting download,happy waiting..")

		c.perform()

		fp.close()

		c.close()
