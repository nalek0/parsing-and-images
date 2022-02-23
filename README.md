# Different parsers and k-means algorithm

## Documentation:

### `parser.py`:
```python
class Image:
	parameters:
		url(String)
		format(String)
	methods:
		download(self, filename="image")
```
```python
class Author:
	parameters:
		name(String)
		url(String)
		avatar(String)
		platform(...Parser)
		id(String)
```
```python
class Post:
	parameters:
		author(Author)
		image(Image)
		title(String)
		description(String)
		url(String)
```
```python
class ...Parser:
	methods:
		load_picture(post)
			returns Image
		get_posts(username, page)
			returns List[Post]
		get_author(username)
			returns Author
```

_Available parsers: DeviantartParser, PixivParser_

### `kmeans.py`:
```python
class Color:
	parameters:
		red(Integer)
		green(Integer)
		blue(Integer)
	methods:
		distance_to(self, other) # need for k-means problem
		random_color()
```
```python
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