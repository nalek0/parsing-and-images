# Bot images parser
### This bot will parse deviantart, artsation and pixiv

## `parser.py`:
```
class Image:
	parameters:
		url(String)
		format(String)
	methods:
		download(self, filename = "image")
```		
```
class Author:
	parameters:
		name(String)
		url(String)
		avatar(String)
		platform(...Parser)
```
```
class Post:
	parameters:
		author(Author)
		image(Image)
		title(String)
		description(String)
		url(String)
```
```
class ...Parser:
	methods:
		load_picture(post)
			returns Image
		get_posts(username, page)
			returns List[Post]
		get_author(username)
			returns Author
```

## `kmeans.py`:
```
class Color:
	parameters:
		red(Integer)
		green(Integer)
		blue(Integer)
	methods:
		distance_to(self, other)
			need for k-means problem
		random_color()
```
```
class Art:
	parameters:
		filepath(String)
	methods:
		get_pixels(self)
			returns List[Color]
		get_resized_art(self)
			returns Art
		kmeans(pixels, k)
			returns List[Color]
```