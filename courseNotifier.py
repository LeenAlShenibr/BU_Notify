'''
A simple script that notifies the user when
a seat becomes available in a specific course.

The MIT License (MIT)

Copyright (c) 2014 Leen AlShenibr, Tara Tayba

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

'''



from bs4 import BeautifulSoup
import urllib2
import sys
import smtplib
import time
import threading
import getpass


#GLOBAL VARIABLES
args = {}
t = None




################################################################################
## NOTIFICATION MODULES
################################################################################


def send_notifications(search, number, email, password):

    server = smtplib.SMTP( "smtp.gmail.com", 587 )
    server.starttls()
    server.login( email, password )

    number = number + '@mms.att.net'

    msg = "A seat is avaiable in %s" %search

    server.sendmail( 'Seat avaiable', number, msg )

    if (email != ''):
        server.sendmail( 'Seat avaiable', email, msg )

    print "Sent notifications!"





################################################################################
## URL CONSTRUCTOR & HTML PARSER
################################################################################


def seat_available(search, url):

    print"Seats avaiable called"

    #Open URL
    response = urllib2.urlopen(url)

    #Read HTML file
    html = response.read()


    #Initlize parsing library, with the html file
    soup = BeautifulSoup(html)


    #Parse to get tables that we want.
    resultList = soup.findAll(name='tr', limit=16)

    #Get rid of the first table, and some unnecceary lines from the second
    resultList = resultList[9:]

    #First nine elements can be ignored
    #Class name stored in index: 2, course title: 4, seats left:12
    for e in resultList:

        result = e.findAll(text=True)#Get text from inner list

        if len(result) > 13 and len(result[2]) > 3:

            result[2] = result[2].replace(u'\xa0', u' ')


            if result[2] == search:#Check if its the correct course

                print "Course found..."
                print "Course is " + result[2]
                print "Checking if there are seats avaiable..."
                print "#Seats = " + result[12]

                if int(result[12]) > 0:#Check if there are seats avaiable
                    print"Seat found."
                    response.close()
                    return True

    response.close()

    return False

def construct_url(year,semester, college,
                  department, course, section):

    base_url = 'https://www.bu.edu/link/bin/uiscgi_studentlink.pl/' +\
               '1395464387?ModuleName=univschr.pl&SearchOptionDesc=' +\
               'Class+Number&SearchOptionCd=S'

    #Note: Fix semester names for summer sessions
    #BU adds a number indicating the semester to the year arguement
    specialNumber = {"Summer1":1, "Summer2":2, "Fall": 3, "Spring": 4}

    semesterString = semester[0].upper() + semester[1:].lower()

    semester = '&ViewSem='+ (semester + "+" + year)#First letter upper case


    #Must be in this format 20133, or 20144, the last digit is the semester.
    year = int(year)
    year = '&KeySem=%d%d'%(year , specialNumber[semesterString])

    college = '&College=' + college.upper() #all uppercase

    department = '&Dept='+ department.upper()

    course = '&Course='+ course

    section = '&Section=' + section.upper()

    url = base_url + year + semester + college + department + course + section

    print "URL is:\n %s \n\n" % url

    return url





################################################################################
## LOOPING MODULES
################################################################################

def loop(url, search, phoneNumber, email, password, **extras):

    if (seat_available(search, url) == True):
        print "There are seats avaiable!"
        send_notifications(search,phoneNumber, email, password)
        return True
    print "No seats found"
    return False



def runUntilFound():

    global args

    if (loop(**args)):
        return True
    else:
        global t
        t = threading.Timer(60, runUntilFound)
        t.start()





################################################################################
## SETUP
################################################################################


def setUpArgs(arg):
    global args

    args['semester'] = arg[1]
    args['year'] = arg[2]
    args['college'] = arg[3]
    args['department'] = arg[4]
    args['course'] = arg[5]
    args['section'] = arg[6]

    args['phoneNumber'] = arg[7]
    args['email'] = arg[8]



def getUserInput():
    global args

    print("Please provide the following information about your course: ")
    args['semester'] = raw_input("Semester: ")
    args['year'] = raw_input("Year: ")
    args['college'] = raw_input("College: ")
    args['department'] = raw_input("Department: ")
    args['course'] = raw_input('Course Number: ')
    args['section'] = raw_input("Section: ")

    print("Please provide your phone number, email, and password")

    args['phoneNumber'] = raw_input("Phone Number: ")
    args['email'] = raw_input("Email: ")



def main():

    global args

    n = 120 #Number of seconds

    arg = sys.argv

    if len(arg) > 1:
        setUpArgs(arg)
    else:
        getUserInput()

    args['password'] = getpass.getpass()


    #Construct URL and Search string
    #===========================================================================
    url = construct_url(args['year'], args['semester'], args['college'],\
                        args['department'], args['course'], args['section'])


    search = args['college'].upper()+ ' ' + args['department'].upper() +\
             args['course'] + ' ' + args['section'].upper()

    print "Search string is " + search

    args['url'] = url
    args['search'] = search


    #===========================================================================

    runUntilFound()


if  __name__ =='__main__':
    main()
