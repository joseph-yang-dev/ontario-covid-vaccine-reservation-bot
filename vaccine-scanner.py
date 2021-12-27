from selenium import webdriver, common
from selenium.webdriver.common.by import By
import time
import logging
import os
import argparse

parser = argparse.ArgumentParser(description='Ontario vaccine reservation bots.')
parser.add_argument("-d", "--debug", dest='isDebug', action='store_true', help="Turn on debug mode.")
parser.add_argument("-r", "--reschedule", dest="isReschedule", action='store_true', help="Reschedule existing reservation. Ignore this option if you do NOT have any active reservation (reserved but not completed). In another word, if you are looking for a new vaccine reservation, IGNORE this option.")
parser.add_argument("-n", "--number-of-doses", type=str, dest="dose", action="store", default="1", choices=["1", "2", "3"], help="The does sequence number.", required=True)
# parser.add_argument("-1", "--first-doses", dest="dose", action="store_const", const="1", help="This is for the FIRST dose reservation.")
# parser.add_argument("-2", "--second-doses", dest="dose", action="store_const", const="2", help="This is for the SECOND dose reservation.")
# parser.add_argument("-3", "--third-doses", dest="dose", action="store_const", const="3", help="This is for the THIRD dose reservation.")
parser.add_argument("-c", "-hcn", dest="hcn", action="store", type=str, help="Ontario health card number, in \"xxxx-xxx-xxx\"(10 digits) format.", required=True)
parser.add_argument("-v", "--vcode", dest="vcode", action="store", type=str, help="Ontario health card number verificiation code in \"XX\"(2 alphabet codes).", required=True)
parser.add_argument("-s", "--scn", dest="scn", action="store", type=str, help="Ontario health card security code(can be found in the back) in \"XXNNNNNNN\"(2 alphabet and 7 digits combination).", required=True)
parser.add_argument("-b", "--dob", dest="dob", action="store", type=str, help="Date of birth in \"yyyy-mm-dd\" format.", required=True)
parser.add_argument("-p", "--postal", dest="postal", action="store", type=str, help="Postal code (match to healthcard) in \"A0B-1C3\" format.", required=True)
parser.add_argument("-e", "--email", dest="email", action="store", type=str, help="Email address to receive confimration and notification. Only needed for the fist dose reservation.")
parser.add_argument("-m", "--cellphone", dest="cellphone", action="store", type=str, help="Mobile phone to receive confirmation and notification. Only needed for the fist dose reservation.")

parser.add_argument("-r50", "--in-50-km", dest="r", action="store_const", const="50", help="Search with 50KM range.")
parser.add_argument("-r100", "--in-100-km", dest="r", action="store_const", const="100", help="Search with 100KM range.")
parser.add_argument("-r200", "--in-200-km", dest="r", action="store_const", const="200", help="Search with 200KM range.")
parser.add_argument("-r500", "--in-500-km", dest="r", action="store_const", const="500", help="Search with 500KM range.")

args = parser.parse_args()

if args.isDebug:
  logging.basicConfig(level=logging.DEBUG)
else:  
  logging.basicConfig(level=logging.INFO)


if args.r != None:
  r=args.r
else:
  r="25"

dose=args.dose
hcn=args.hcn
vcode=args.vcode
scn=args.scn
dob=args.dob
postal=args.postal
email=args.email
cellphone=args.cellphone


browser=webdriver.Chrome()
browser.get("https://covid19.ontariohealth.ca/")

#
def wait_for_element_by(e_by, e_key):
  while True:
      try:
        browser.find_element(e_by, e_key)
        logging.debug("Element {} is here.".format(e_key))
        break
      except common.exceptions.NoSuchElementException:
          time.sleep(5)
          logging.debug("Waiting for {} ...".format(e_key))

#
def wait_for_text(txt):
  while True:
    try:
      if txt in browser.page_source:
        break
        logging.debug("Found text \"{}\" in page source.".format(txt))
      else:
        time.sleep(5)
        logging.debug("Waiting for text \"{}\" ...".format(txt))
    except common.exceptions.NoSuchElementException:
      time.sleep(5)
      logging.debug("Waiting for text \"{}\" ...".format(txt))

acptTerm=browser.find_element(By.ID, 'home_acceptTerm1_label')
acptTerm.click()
cntButton=browser.find_element(By.ID, "continue_button")
cntButton.click()

# fill person info
wait_for_element_by(By.ID, 'hcn')
browser.find_element(By.ID, 'hcn').send_keys(hcn)
browser.find_element(By.ID, 'vcode').send_keys(vcode)
browser.find_element(By.ID, 'scn').send_keys(scn)
browser.find_element(By.ID, 'dob').send_keys(dob)
browser.find_element(By.ID, 'postal').send_keys(postal)
browser.find_element(By.ID, 'continue_button').click()

wait_for_element_by(By.ID, 'booking_button')
browser.find_element(By.ID, 'booking_button').click()

if dose =='1':
  # 1st 
  wait_for_element_by(By.ID, 'fld_booking-home_oop_no_label')
  browser.find_element(By.ID, 'fld_booking-home_oop_no_label').click()
  browser.find_element(By.ID, 'submit_label_continue').click()
  
  wait_for_text("You are eligible for a vaccination")
  browser.find_element(By.ID, 'email').send_keys(email)
  browser.find_element(By.ID, 'emailx2').send_keys(email)
  browser.find_element(By.ID, 'mobile').send_keys(cellphone)
  browser.find_element(By.ID, 'schedule_button').click()
elif dose == '2':
  # 2nd
  # You can book your second or booster dose appointment
  wait_for_element_by(By.ID, 'second_dose_button')
  browser.find_element(By.ID, 'second_dose_button').click()
elif dose == '3':
  # 3rd
  wait_for_element_by(By.ID, 'fld_booking-home_eligibility_group_noGroup_label')
  browser.find_element(By.ID, 'fld_booking-home_eligibility_group_noGroup_label').click()
  browser.find_element(By.ID, 'submit_label_schedule').click()
else:
  print("Only allow 1st - 3rd dose booking")

wait_for_element_by(By.ID, 'location-search-address')
browser.find_element(By.ID, 'location-search-address').send_keys('M2J-3A1')
browser.find_element(By.CLASS_NAME, 'tw-space-y-2').click()

wait_for_text("Select a Vaccination Centre Location")

# change range to 50/100/200
if r != "25":
  wait_for_element_by(By.ID, "locationSearchDistance-button")
  browser.find_element(By.ID, 'locationSearchDistance-button').click()
  wait_for_element_by(By.ID, r)
  browser.find_element(By.ID, r).click()
  wait_for_text("Select a Vaccination Centre Location")
  time.sleep(2)

vc=[]
vcList=[]

def summary():
  logging.info("\n\nSummary: ")
  for j in range(len(vc)):
    if vcList[j]["vcCnt"] > 0:
      logging.info(">> {}: {} - {}. {}".format(vc[j], vcList[j]["vcCnt"], vcList[j]["slotText"], vcList[j]["slotStartText"]))
  vc.clear()
  vcList.clear()
  logging.info("\n\nRescan .... ")
  time.sleep(10)

while True:
  logging.info("Scanning ...")
  wait_for_text("Select a Vaccination Centre Location")

  while "Load more locations" in browser.page_source:
    for btn in browser.find_elements(By.TAG_NAME, "button"):
      if btn.get_attribute("data-testid") == "load-more-locations-button":
        btn.click()
        time.sleep(5)
        wait_for_text("Select a Vaccination Centre Location")
        break

  h2=browser.find_elements(By.CLASS_NAME, "tw-sr-only")
  entryCount=len(h2)

  for i in range(entryCount):
    h=h2[i]

    if h.get_attribute("data-testid") == "sr-button-location-name":
      t=h.text
  
      if t in vc:
        if i == entryCount-1:
          summary()
        else:
          continue
        
      else:
        btn=h.find_element(By.XPATH, "..")
        btn.click()
        wait_for_text("Book Appointment")
        wait_for_element_by(By.CLASS_NAME, "day--blocked")
        dates=browser.find_elements(By.CLASS_NAME, "calendar__day")
        cnt=0
        for d1 in dates:
          dClass=d1.get_attribute("class")
          if not "day--blocked" in dClass and dClass != "calendar__day day--selected calendar__day--today":
            cnt+=1
        
        cntElements=browser.find_elements(By.CLASS_NAME, "tw-text-lg")
        for cntElement in cntElements:
          if cntElement.tag_name == "h3":
            slotText=cntElement.text

        slotStart=browser.find_element(By.CLASS_NAME, "tw-mb-5")
        slotstartText=slotStart.text
        logging.info("+ Found {}: {} day(s) has {}. {}".format(t, cnt, slotText, slotstartText))
        
        vc.append(t)
        vcList.append({
          "vc": t,
          "vcCnt": cnt,
          "slotText": slotText,
          "slotStartText": slotstartText
        })
    
        browser.back()
        time.sleep(2)

        if i == entryCount-1:
          summary()
        break
    else:
      if i == entryCount-1:
        summary()


print("The end.")

