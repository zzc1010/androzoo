from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from subprocess import Popen, PIPE
import time, os, sys
import codecs

DEBUG = True

sys.stdout = codecs.getwriter('utf8')(sys.stdout)

def flushPrint(txt):
    print txt
    sys.stdout.flush()

# selenium driver
browser = webdriver.Firefox()

i = 1
has_reach = False
while True:
    # search
    url = 'https://www.androidrank.org/android-most-popular-google-play-apps?start=%d&category=all&sort=4&price=all' % i
    if DEBUG:
        print url
    browser.get(url)

    # wait to load
    time.sleep(1)

    # get value
    tdnodelist = browser.find_elements_by_xpath("//td[@style='text-align:left;']")
    for tdnode in tdnodelist:
        pkglink = tdnode.find_element_by_tag_name("a")
        ratingtd = tdnode.find_element_by_xpath("following-sibling::*") \
                         .find_element_by_xpath("following-sibling::*")
        installtd = ratingtd.find_element_by_xpath("following-sibling::*")

        pkgsplit = pkglink.get_attribute("href").split("/")
        if DEBUG:
            print pkgsplit
        pkgname = pkgsplit[5]
        ratingnum = ratingtd.text
        installnum = installtd.text

        if 'M' not in installnum:
            has_reach = True
            break
        txt = '%s\t%s\t%s' % (pkgname, ratingnum, installnum)
        flushPrint(txt)

    if has_reach:
        break

    i = i + 20

browser.quit()
