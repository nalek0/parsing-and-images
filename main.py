import requests
import discord
import json
from pprint import pprint

class Parser:
	def get_author_avatar(username):

		pass

	def get_author_works(username, offset = 0, limit = 24):
		
		pass

	def get_author_posts(username, offset = 0, limit = 24):
		
		pass

	def get_post_image_url(post):

		pass

	def load_image(image_url, filename):
		r = requests.get(image_url)

		if (r.status_code >= 200 and r.status_code <= 209):
			with open(filename, 'wb') as img:
				img.write(r.content)
			return True
		else:
			return False

class DeviantartParser(Parser):
	def get_author_avatar(username):
		info = DeviantartParser.get_author_posts()
		if (len(info) == 0):
			return None
		else:
			return info[0]['deviation']['author']['usericon']

	def get_author_works(username, offset = 0, limit = 24):
		all_folder 	= "true"
		mode 		= "newest"
		r = requests.get(f"https://www.deviantart.com/_napi/da-user-profile/api/gallery/contents?username={username}&offset={str(offset)}&limit={str(limit)}&all_folder={all_folder}&mode={mode}")

		if (r.status_code >= 200 and r.status_code <= 209):
			return json.loads(r.text)
		else:
			with open("error.html", 'w') as err_f:
				err_f.write(r.text)

			return None

	def get_author_posts(username, offset = 0, limit = 24):

		return DeviantartParser.get_author_works(username, offset, limit)['results']

	def get_post_image_url(post):
		fullview = list(filter(lambda type: type['t'] == "fullview", post['deviation']['media']['types']))
		
		if (len(fullview) == 0):
			return None
		else:
			fullview = fullview[0]

			image_url = post['deviation']['media']['baseUri'] + '/' + fullview['c'].replace("<prettyName>", post['deviation']['media']['prettyName']) + '?token=' + post['deviation']['media']['token'][0]

			return image_url