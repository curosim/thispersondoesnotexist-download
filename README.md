# Thispersondoesnotexist.com Download
Automated download of faces from <a href="https://thispersondoesnotexist.com" target="_blank">Thispersondoesnotexist.com</a>

### Description:
Downloads a certain amount of images from thispersondoesnotexist.com and stores them in a folder (./images/).
After downloading, it will remove any duplicates so we only have unique images.

### Usage:
```
python tpdne-download.py
```
The script is interactive, simply start it and enter the number of images to download.


### About the speed:
While the script uses multiprocessing for the requests, it's designed to not work particularly fast.
The reason for that is based on how thispersondoesnotexist.com works - it generates a new image based on time and not on requests.
So if we work with 20 threads, it will just download the same image multiple times, which would be removed by the duplicate checker anyway.
