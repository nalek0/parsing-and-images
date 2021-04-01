from pprint import pprint
import requests
import json
from bs4 import BeautifulSoup as bs4

class Image:
	def __init__(self, **kwargs):
		self.url 	= None if not 'url' in kwargs else kwargs['url']
		self.format = "" if not 'url' in kwargs else kwargs['format']

	def download(self, filename = "image"):
		r = requests.get(self.url)


		if (r.status_code >= 200 and r.status_code <= 209):
			with open(filename + "." + self.format, 'wb') as img:
				img.write(r.content)
		else:
			print(f"Error code: { r.status_code }")
			print(r.text)
			print(self.url)

	def __repr__(self):
		return f"<Image { self.url }>"

class Author:
	def __init__(self, **kwargs):
		self.name 		= None if not 'name' in kwargs else kwargs['name']
		self.url 		= None if not 'url' in kwargs else kwargs['url']
		self.avatar 	= None if not 'avatar' in kwargs else kwargs['avatar']
		self.platform 	= None if not 'platform' in kwargs else kwargs['platform']

	def __repr__(self):
		return f"<Author { self.name }>"

class Post:
	def __init__(self, author, image, **kwargs):
		self.author 		= author
		self.image 			= image
		self.title 			= None if not 'title' in kwargs else kwargs['title']
		self.description 	= None if not 'description' in kwargs else kwargs['description']
		self.url 			= None if not 'url' in kwargs else kwargs['url']

	def __repr__(self):
		return f"<Post image: { self.image }, author: { self.author }>"


class DeviantartParser:
	def get_posts(username, page):
		offset 		= (page - 1) * 24
		limit 		= 24
		all_folder 	= "true"
		mode 		= "newest"
		r = requests.get(f"https://www.deviantart.com/_napi/da-user-profile/api/gallery/contents?username={username}&offset={str(offset)}&limit={str(limit)}&all_folder={all_folder}&mode={mode}")

		if (r.status_code >= 200 and r.status_code <= 209):
			results = json.loads(r.text)['results']
			posts 	= []
			for result in results:
				if ('c' in list(filter(lambda type: type['t'] == "fullview", result['deviation']['media']['types']))[0]):
					image_url = result['deviation']['media']['baseUri'] + '/' + list(filter(lambda type: type['t'] == "fullview", result['deviation']['media']['types']))[0]['c'].replace("<prettyName>", result['deviation']['media']['prettyName']) + '?token=' + result['deviation']['media']['token'][0]
				else:
					image_url = result['deviation']['media']['baseUri'] + '?token=' + result['deviation']['media']['token'][-1]

				posts.append(
					Post(
						Author(
							name 		= result['deviation']['author']['username'],
							url 		= f"https://www.deviantart.com/{ username }",
							avatar 		= result['deviation']['author']['usericon'],
							platform	= "Deviantart"),
						Image(
							url 		= image_url,
							format 		= result['deviation']['media']['baseUri'].split('.')[-1]),

						title 			= result['deviation']['title'],
						url 			= result['deviation']['url'] 
					)
				)
			return posts
		else:
			return None

	def get_author(username):
		offset 		= 1
		limit 		= 1
		all_folder 	= "true"
		mode 		= "newest"
		r = requests.get(f"https://www.deviantart.com/_napi/da-user-profile/api/gallery/contents?username={username}&offset={str(offset)}&limit={str(limit)}&all_folder={all_folder}&mode={mode}")

		if (r.status_code >= 200 and r.status_code <= 209):
			results = json.loads(r.text)['results']
			posts 	= []
			if len(results) > 0:
				result = results[0]
						
				return Author(
					name 		= result['deviation']['author']['username'],
					url 		= f"https://www.deviantart.com/{ username }",
					avatar 		= result['deviation']['author']['usericon'],
					platform	= "Deviantart")
			else:
				return None
		else:
			return None

class ArtstationParser:
	def get_posts(username, page):
		author = ArtstationParser.get_author(username)

		r = requests.get(f"https://www.artstation.com/users/{username}/projects.json?page={str(page)}")

		if (r.status_code >= 200 and r.status_code <= 209):
			results = json.loads(r.text)['data']
			posts 	= []
			for result in results:
				chunks = result['cover']['thumb_url'].split('/')
				if (len(chunks) == 12):
					chunks[10] = 'large'
				else:
					chunks[11] = 'large'
					chunks = chunks[:10] + chunks[11:]

				image_url = "/".join(chunks)

				posts.append(
					Post(
						author,
						Image(
							url 		= image_url,
							format 		= result['cover']['thumb_url'].split('?')[-2].split('.')[-1]),

						title 			= result['title'],
						description 	= result['description'],
						url 			= result['permalink'] 
					)
				)
			return posts
		else:
			return None

	def get_author(username):
		r = requests.get("https://www.artstation.com/aenamiart")
		lines = r.text.split('\n')
		line_with_info = list(filter(lambda l: l.find("cache.put") != -1, lines))[0]
		info = line_with_info[line_with_info.find("{"):(line_with_info.rfind("}") + 1)].replace("\\", "")
		info = json.loads(info)

		return Author(
			name 		= info['full_name'],
			url 		= info['permalink'],
			avatar 		= info['large_avatar_url'],
			platform	= "Artstation")


# for post in DeviantartParser.get_posts('yuumei', 1):
# 	post.image.download("yuumei_images/" + post.title)
# 	print(f"Downloaded { post.title }  with post_url: { post.url }")
for post in ArtstationParser.get_posts('aenamiart', 1):
	post.image.download("aenamiart_images/" + post.title.replace("|", "~"))
	print("Downloaded" + post.title + "image")


# https://cdna.artstation.com/p/assets/images/images/033/957/502/large/alena-aenami-night-1k.jpg?1611017729
# https://cdna.artstation.com/p/assets/images/images/033/957/502/20210118185529/large/alena-aenami-night-1k.jpg?1611017729