
import urllib2
from bs4 import BeautifulSoup
import smtplib
import time
import sys
import traceback

URL="http://chj.tbe.taleo.net/chj05/ats/careers/jobSearch.jsp?org=CSUCHICO&cws=4&org=CSUCHICO"
INTERVAL_PERIOD= 30

def send_mail_trigger(job_counter,new_count) :
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    #Next, log in to the server
    server.login("out.trigger.mailer@gmail.com", "weakpassword")

    #Send the mail
    msg = "#jobtrigger \n" # The /n separates the message from the headers
    msg = msg+"Counter changed from "+str(job_counter)+" to "+str(new_count)+" \n"
    msg = msg+"Check here :  "+ URL +"   for more details"
    server.sendmail("out.trigger.mailer@gmail.com", "praveendareddy@gmail.com", msg)
    server.quit()
    print "done"
    
def url_parser():
    url = URL
    data = urllib2.urlopen(url).read()
    bs = BeautifulSoup(data, 'html.parser')
 

    line = bs.find(lambda tag: tag.name=='br' )
   
    
    
    fname = 'url_parser_.log'
    with open(fname, 'a') as outf:
        outf.write("Time : "+str(time.time())+ " logout : "+str(line)+'\n')

    return int((str(line).split("</")[0]).split("b>")[1])  # return final  int no of entries




def main():
    job_counter = 0
    print("Staring the Main LOOP")
    print("All the exceptions will be caught and reported here")
    while True:
        try :
            while True:
                new_count=url_parser()
                
                if(new_count!=job_counter):
                    print("Job Counter changed, calling Trigger funtion")
                    send_mail_trigger(job_counter,new_count)
                    
                job_counter=new_count
                time.sleep(INTERVAL_PERIOD)
                
        except :
            print "Unexpected error:", sys.exc_info()[0]
            print "Crashed"
            print traceback.format_exc()
        print("Trying Again ")
            

if __name__=="__main__":
    main(
