#!/usr/bin/env python
# encoding:utf-8

import threading
import requests
import sys

screenLock = threading.Semaphore(value=1)

class ColorPrinter:
    @staticmethod
    def print_red_text(content):
        print "\033[1;31;40m %s \033[0m" % (content),
    @staticmethod
    def print_green_text(content):
        print "\033[1;32;40m %s \033[0m" % (content),
    @staticmethod
    def print_blue_text(content):
        print "\033[1;34;40m %s \033[0m" % (content),


def check(url, timeout):
    try:
        if timeout <= 0:
            timeout = 20
        response = requests.head(url,timeout = timeout)
        code = response.status_code
        screenLock.acquire()
        if code == 200:
            ColorPrinter.print_green_text("[ " + str(code) + " ]")
            print "Checking : " + url
            if "404" in response.text:
                ColorPrinter.print_blue_text(url + "\tMaybe every page same!")
        elif code == 404 or code == 405:
            pass
            # ColorPrinter.print_red_text("[ " + str(code) + " ]")
            # print "Checking : " + url
        else:
            ColorPrinter.print_blue_text("[ " + str(code) + " ]")
            print "Checking : " + url
    except Exception as e:
        screenLock.acquire()
        print e
    finally:
        screenLock.release()

class myThread (threading.Thread):
    url = ""
    def __init__(self, url, timeout):
        threading.Thread.__init__(self)
        self.url = url
        self.timeout = timeout
    def run(self):
        check(self.url, self.timeout)


def urlFormater(url):
    if (not url.startswith("http://")) and (not url.startswith("https://")):
        url = "http://" + url
    if not url.endswith("/"):
        url += "/"
    return url


def help(name):
    print "Usage : "
    print "        python %s [URL] [ThreadNumbers] [Timeout]" % (name)
    print "Example : "
    print "        python %s http://127.0.0.1/ 2 5" % (name)
    print "Tips : "
    print "        2 - 3 threadNumber is recommended."
    print "        5 second timeout is recommended.(You can also use a decimal to set the timeout.)"
    print "        If you have any questions, please contact <wangyihanger@gmail.com>"

def main():
    if len(sys.argv) != 4:
        help(sys.argv[0])
        exit(1)

    website = urlFormater(sys.argv[1])
    threadNumber = int(sys.argv[2])
    timeout = float(sys.argv[3])
    colorPrinter = ColorPrinter()
    if timeout == 0:
        print "[-] Your timeout can not be equal with 0!"
        help(sys.argv[0])
        exit(1)
    if not colorPrinter :
        exit(1)
    listFile = open('list.txt', 'r')
    threads = []
    for i in listFile:
        i = i.replace("\n","")
        i = i.replace("\r","")
        if "?" in i:
            fileFile = open('file.txt', 'r')
            for j in fileFile:
                j = j.replace("\n","")
                j = j.replace("\r","")
                temp = i.replace("?",j)
                threads.append(myThread(website + temp, timeout))
        else:
            threads.append(myThread(website + i, timeout))

    for thread in threads:
        thread.start()
        while True:
            if (len(threading.enumerate()) < threadNumber):
                break

if __name__ == "__main__":
    main()
