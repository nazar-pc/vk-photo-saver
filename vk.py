#!/usr/bin/env python
# -*- coding: utf-8 -*-


import urllib, urllib2, json, requests, time, os

vk_token = "ваш токен"
donload_dir = u"/home/username/Изображения/%s/"

def main():
  album_list("идентификатор пользователя")

def album_list(user_id):
	d = {"owner_id":user_id}
	response = vkMethod("photos.getAlbums", d)
	for album in response["response"]:
		print album["title"]
		dir_name = donload_dir % album["title"]
		if create_dir(dir_name):
			print u"Создан каталог %s" % dir_name
		
		album_id = album["aid"]
		photo_list(album_id,user_id, dir_name)
		print

def photo_list(album_id, user_id, dir_name):
	d = {"album_id":album_id, "owner_id":user_id}
	response = vkMethod("photos.get", d)
	for photo in response["response"]:
		if photo.has_key("src_xxxbig"):
			url = photo["src_xxxbig"]
		elif photo.has_key("src_xxbig"):
			url = photo["src_xxbig"]
		elif photo.has_key("src_xbig"):
			url = photo["src_xbig"]
		elif photo.has_key("src_big"):
			url = photo["src_big"]
		else:
			url = photo["src"]
		
		photo_id = photo["pid"]
		download_photo(url, dir_name, photo_id, photo["text"])
		print

def create_dir(dir_name):
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)
		return True
	else:
		return False

def download_photo(url, dir_name, photo_id, text):
	print u"Загружаю фото %s" % url
	photo = urllib.urlopen(url).read()
	album_title = dir_name.rsplit('/')[-2]
	save_name = "%s%s_%s.jpg" % (dir_name, album_title, photo_id)
	f = open(save_name, "wb")
	f.write(photo)
	print u"Сохранено %s" % save_name
	if text:
		f = open("%s.txt" % save_name, "wb")
		f.write(text.encode('utf-8'))
		print u"Сохранено описание %s.txt" % save_name
	f.close()

def vkMethod(method, d={}):
	print "Запрос к API"
	url = 'https://api.vk.com/method/%s' % (method)
	d.update({'access_token': vk_token})
	#print d
	print
	response = json.loads(requests.post(url, d).content)
	if 'error' in response:
		print 'VK API error: %s' % (response['error']['error_msg'])
	else:
		print "Ответ получен"
	return response

if __name__ == "__main__":
	main()
