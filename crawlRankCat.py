from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from subprocess import Popen, PIPE
import time, os, sys
import codecs

DEBUG = False
CATDUMP = 'GPlay_Category.txt'

sys.stdout = codecs.getwriter('utf8')(sys.stdout)

def flushPrint(txt):
    print txt
    sys.stdout.flush()

# read category list
catlist = []
f = open(CATDUMP, 'r')
for line in f:
    cat = line.rstrip('\n')
    catlist.append(cat)
if f:
    f.close()
if DEBUG:
    print catlist

#Read finished list
finishedList = []
if os.path.exists("group/Finished.txt"):
    f = open("group/Finished.txt", 'r')
    for line in f:
        finishedCat = line.rstrip()
        finishedList.append(finishedCat)
    if f:
        f.close()

# selenium driver
browser = webdriver.Firefox()

# loop category list
for cat in catlist:
    if cat in finishedList:
        continue
    catFile = open("group/"+cat+".txt",'w+')
    i = 1
    has_reach = False
    while True:
        # search
        #https://www.androidrank.org/android-most-popular-google-play-apps?start=321&category=all&sort=4&price=all
	if i>500:
	    break
        url = 'https://www.androidrank.org/android-most-popular-google-play-apps?category=%s&start=%d&sort=4&price=all&hl=en' % (cat, i)
        if DEBUG:
            print url
        browser.get(url)

        # wait to load
        time.sleep(5)

        # get value
        try:
            tdnodelist = browser.find_elements_by_xpath("//td[@style='text-align:left;']")
            for tdnode in tdnodelist:
                pkglink = tdnode.find_element_by_tag_name("a")
                ratingtd = tdnode.find_element_by_xpath("following-sibling::*") \
                    .find_element_by_xpath("following-sibling::*")
                installtd = ratingtd.find_element_by_xpath("following-sibling::*")

                pkgsplit = pkglink.get_attribute("href").split("/")
                if DEBUG:
                    print pkgsplit
                pkgname = pkgsplit[5]#[0:len(pkgsplit[5])-6]
                ratingnum = ratingtd.text
                installnum = installtd.text

                if 'M' not in installnum:
                    has_reach = True
                    break
                txt = '%s\t%s\t%s\t%s' % (pkgname, cat, ratingnum, installnum)
                flushPrint(txt)
                catFile.write(txt+"\n")

            if has_reach:
                break

            i = i + 20
        except:
            break
    if catFile:
        catFile.close()
    with open("group\Finished.txt", "a") as finishedFile:
        finishedFile.write(cat+"\n")
    if finishedFile:
        finishedFile.close()

browser.quit()
