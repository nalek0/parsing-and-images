from PIL import Image, ImageDraw 
from random import randint
import math
import requests
import time

class Color:
	def __init__(self, red, green, blue):
		self.red 	= red
		self.green 	= green
		self.blue 	= blue

	def distance_to(self, other):
		return math.sqrt((self.red - other.red)**2 + (self.green - other.green)**2 + (self.blue - other.blue)**2) 

	def random_color():
		return Color(randint(0, 255), randint(0, 255), randint(0, 255))

class Art:
	def __init__(self, filepath):

		self.filepath = filepath

	def get_pixels(self):
		image = Image.open(self.filepath) 
		width 	= image.size[0]
		height 	= image.size[1]
		
		pix = image.load()

		pixels = []
		for x in range(width):
			for y in range(height):
				pixels.append(Color(pix[x, y][0], pix[x, y][1], pix[x, y][2]))

		return pixels

	def get_resized_art(self, size):
		img = Image.open(self.filepath)
		img.thumbnail(size, Image.ANTIALIAS)
		img.save("0.jpg", "JPEG")

		return Art("0.jpg")

	#Methods:

	def kmeans(pixels, k):
		base_points = []
		for i in range(k):
			base_points.append(Color.random_color())

		for i in range(20):
			# Creating groups of nearest
			nearest = []
			for i in range(k):
				nearest.append([])

			for pixel in pixels:
				nearest_color = 0
				for i in range(k):
					if (pixel.distance_to(base_points[nearest_color]) > pixel.distance_to(base_points[i])):
						nearest_color = i

				nearest[nearest_color].append(pixel)

			# Creating new "centers of mass" of the groups of nearest, that we found before 
			new_centers = []
			for i in range(k):
				if (len(nearest[i]) == 0):
					new_centers.append(Color.random_color())
				else:
					sum_r = 0
					sum_g = 0
					sum_b = 0
					for col in nearest[i]:
						sum_r += col.red
						sum_g += col.green
						sum_b += col.blue

					new_centers.append(Color(
						sum_r // len(nearest[i]),
						sum_g // len(nearest[i]), 
						sum_b // len(nearest[i])))

			base_points = new_centers

		return base_points

	def load_art(url, filepath):
		r = requests.get(url)


		if (r.status_code >= 200 and r.status_code <= 209):
			with open(filepath, 'wb') as img:
				img.write(r.content)
		else:
			print(f"Error code: { r.status_code } with text: { r.text }")