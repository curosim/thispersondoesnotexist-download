import urllib.request
import time
from random import uniform
from multiprocessing.dummy import Pool as ThreadPool
import requests
import glob
import os
import hashlib

def file_hash(filepath):
	""" Generate MD5 Hash of an file.
	"""
	with open(filepath, 'rb') as f:
		return hashlib.md5(f.read()).hexdigest()

def remove_duplicates():
	""" Remove duplicate images.
	"""
	hashes = []
	for jpgfile in glob.iglob(os.path.join('./images/', "*.jpg")):
		md5_hash = file_hash(jpgfile)
		if md5_hash in hashes: os.remove(jpgfile)
		else: hashes.append(md5_hash)
	return hashes

def download_image(i):
	""" Download image from thispersondoesnotexist.com
	"""
	time.sleep(uniform(0.1,2))
	print("Downloading Image: {0}".format(i))
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
	try:
		response = requests.get('https://thispersondoesnotexist.com/image', headers=headers)
		if response.status_code == 200:
			img_path = "images/face_{0}.jpg".format(i)
			with open(img_path, 'wb') as f:
				f.write(response.content)
	except: pass

def banner():
	print("  __________  ____  _   ________   ____                      __                __")
	print(" /_  __/ __ \\/ __ \\/ | / / ____/  / __ \\____ _      ______  / /___  ____ _____/ /")
	print("  / / / /_/ / / / /  |/ / __/    / / / / __ \\ | /| / / __ \\/ / __ \\/ __ `/ __  / ")
	print(" / / / ____/ /_/ / /|  / /___   / /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /  ")
	print("/_/ /_/   /_____/_/ |_/_____/  /_____/\\____/|__/|__/_/ /_/_/\\____/\\__,_/\\__,_/   ")
	print("                                                                                 ")
	print("Version: 1.0 - Author: @curosim")


def main():

	#change to maximum number of images needed
	number_of_images = int(input("[*] Enter number of images: "))

	# Download images with multiple threads
	pool = ThreadPool(5)
	results = pool.map(download_image, range(0, number_of_images))
	pool.close()
	pool.join()

	print("[*] {0} images downloaded".format(number_of_images))
	print("[*] Removing duplicates now")
	hashes = remove_duplicates()
	print("[!] Found {0} unique images, {1} duplicates removed".format(len(hashes), number_of_images-len(hashes)))
	print("[*] Execution finished")

main()