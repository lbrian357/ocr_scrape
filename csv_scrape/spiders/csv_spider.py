import scrapy
import csv
import re

#import for tesseracter function
from PIL import Image
import PIL
import pytesseract

#import for url request and save img
import urllib.request
from bs4 import BeautifulSoup
import urllib.parse


"""
with open('/home/brian/Downloads/Sample_of_100_ocr.csv', 'r+t') as f:
    reader = csv.reader(f)
    for row in reader:
        for i in row:
            print(i)

def multiple_replace(dict, text):
    regex = re.compile(r'(http:\/\/www\.lespagesmaghreb\.com.+?)(?:,|\s)')
"""

#takes img and returns text
def img_to_txt ( img_location ):
    try:
        basewidth = 600
        img = Image.open( img_location )
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize( (basewidth,hsize), PIL.Image.ANTIALIAS)
        img.save( img_location )
        return(pytesseract.image_to_string(Image.open( img_location )))
    except:
        return 'NO IMAGE FOUND'
        print('NO IMAGE FOUND')

def multiple_replace(dict, text): 

    """ Replace in 'text' all occurences of any key in the given
        dictionary by its corresponding value.  Returns the new tring.""" 

    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text)

def scrape_job():
    f = open('/home/brian/Documents/csv_scrape/csv_scrape/spiders/output.csv', 'r+t')
    text = f.read()
    f.close()
    pattern = re.compile(r'(http:\/\/www\.lespagesmaghreb\.com.+?)(?:,|\s)')
#   count = 0
    scraps = {}
    try:
        for link in re.findall(pattern, text):
#           count += 1
            print('.', end='')

            urllib.request.urlretrieve(link, "/home/brian/Documents/csv_scrape/csv_scrape/spiders/image.png")


            scraps[link] = img_to_txt("/home/brian/Documents/csv_scrape/csv_scrape/spiders/image.png")
#           print(count)

        #open file to write output csv
#       fi = open("/home/brian/Documents/csv_scrape/csv_scrape/spiders/output.csv", "w")
        f = open('/home/brian/Documents/csv_scrape/csv_scrape/spiders/output.csv', 'r+t')
        print(multiple_replace(scraps, text),file=f)
    except:
        #open file to write output csv
#       fi = open("/home/brian/Documents/csv_scrape/csv_scrape/spiders/output.csv", "w")
        f = open('/home/brian/Documents/csv_scrape/csv_scrape/spiders/output.csv', 'r+t')
        print(multiple_replace(scraps, text),file=f)
        print('exception raised')
        print(link)

condition = True
while condition == True:
    fil = open('/home/brian/Documents/csv_scrape/csv_scrape/spiders/output.csv', 'r+t')
    fil_text = fil.read()
    pat = re.compile(r'(http:\/\/www\.lespagesmaghreb\.com.+?)(?:,|\s)')
    
    if len(re.findall(pat, fil_text)) > 0:
        print('Scrapes left: ' + str(len(re.findall(pat, fil_text))))
        scrape_job()
    else:
        condition = False
