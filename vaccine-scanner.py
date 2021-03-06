from selenium import webdriver, common
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import logging
import os
import argparse

vc=[]
vcList=[]

_key_provider="vc"
_key_vacant_days_count="vcCnt"
_key_slot_text="slotText"
_key_slot_start_text="slotStartText"

browser=None
r="25"
lCount=1
dose=None
hcn=None
vcode=None
scn=None
dob=None
postal=None
email=None
cellphone=None

isReschedule=False
delayInterval=3

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

def summary():
  global lCount
  vcs=[]
  for j in range(len(vc)):
    if vcList[j][_key_vacant_days_count] > 0:
      vcs.append(vcList[j])
  print("###################################################################################################")
  if len(vcs)>0:
    print("Summary: ")
    for vc1 in vcs:
      print(">> {}: {} - {}. {}".format(
        vc1[_key_provider], 
        vc1[_key_vacant_days_count], 
        vc1[_key_slot_text], 
        vc1[_key_slot_start_text]
      ))
  else:
    print("!!! NO VACCINE AVAILABLE FOR NOW, try again later or enlarge the searching range !!!")
  print("###################################################################################################")
  lCount -= 1
  if lCount <= 0:
    quit()

  logging.info("Rescan .... ")
  vc.clear()
  vcList.clear()
  time.sleep(10)

# initialize
def init():
  global r, lCount, hcn, dose, vcode, scn, dob, postal, email, cellphone, browser, isReschedule, delayInterval
  parser = argparse.ArgumentParser(description='Ontario vaccine reservation finder.')
  parser.add_argument("-d", "--debug", dest='isDebug', action='store_true', help="Turn on debug mode.")
  parser.add_argument("-x", "--headless", dest='isHeadless', action='store_true', help="Headless execution. Used only for dockerize or running without browser pops.")
  parser.add_argument("--result-only", dest='isResultOnly', action='store_true', help="Only display results.")
  parser.add_argument("-r", "--reschedule", dest="isReschedule", action='store_true', help="Reschedule existing reservation. Ignore this option if you do NOT have any active reservation (reserved but not completed). In another word, if you are looking for a new vaccine reservation, IGNORE this option.")
  parser.add_argument("-n", "--number-of-doses", type=str, dest="dose", action="store", default="1", choices=["1", "2", "3"], help="The does sequence number.", required=True)
  parser.add_argument("-l", "--number-of-loops", type=int, dest="loopCount", action="store", default="1", help="How many times to scan the reservations.")
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
  parser.add_argument("-w", "--delay-interval", type=int, dest="delayInterval", action="store", default="3", help="Delay interval in seconds between navigating pages. Increse this value can help to avoid crashing during reservation site busy. Default: 3")
  args = parser.parse_args()
  
  if args.isDebug:
    logging.basicConfig(level=logging.DEBUG)
  elif args.isResultOnly:
    logging.basicConfig(level=logging.ERROR)
  else:  
    logging.basicConfig(level=logging.INFO)
  
  if args.r != None:
    r=args.r

  if args.delayInterval != None:
    delayInterval=args.delayInterval  


  if args.isReschedule:
    isReschedule=True
  
  lCount=args.loopCount
  
  dose=args.dose
  hcn=args.hcn
  vcode=args.vcode
  scn=args.scn
  dob=args.dob
  postal=args.postal
  email=args.email
  cellphone=args.cellphone

  options = webdriver.ChromeOptions()
  options.add_experimental_option('excludeSwitches', ['enable-logging'])
  if args.isHeadless:
    options.add_argument("--no-sandbox")
    options.add_argument('--headless')
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-dev-shm-usage")
  browser=webdriver.Chrome(options=options)
  browser.get("https://covid19.ontariohealth.ca/")
  browser.implicitly_wait(10)

# navigate in vaccine reservation website
def navigate():
  # accept terms
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
    if isReschedule:
      wait_for_element_by(By.ID, 'fld_booking-home_eligibility_group_noGroup_label')
      browser.find_element(By.ID, 'fld_booking-home_eligibility_group_noGroup_label').click()
      browser.find_element(By.ID, 'submit_label_schedule').click()
    else:
      wait_for_text("COVID-19 vaccine booster dose")
      try:
        wait_for_element_by(By.ID, 'fld_booking-home_isThirdDose_label')
        browser.find_element(By.ID, 'fld_booking-home_isThirdDose_label').click()
      except WebDriverException:
        print("You seem have already reserved previously, switch to reschedule mode.")
      wait_for_element_by(By.ID, 'fld_booking-home_eligibility_group_noGroup_label')
      browser.find_element(By.ID, 'fld_booking-home_eligibility_group_noGroup_label').click()
      browser.find_element(By.ID, 'submit_label_schedule').click()

  else:
    print("Only allow 1st - 3rd dose booking")
    quit()
  
  # enter postal code 
  wait_for_element_by(By.ID, 'location-search-address')
  browser.find_element(By.ID, 'location-search-address').send_keys(postal)
  browser.find_element(By.CLASS_NAME, 'tw-space-y-2').click()
  
  wait_for_text("Select a Vaccination Centre Location")
  
# scan vaccine availability
def scan_vaccination():  
  # change range to 50/100/200
  if r != "25":
    wait_for_element_by(By.ID, "locationSearchDistance-button")
    browser.find_element(By.ID, 'locationSearchDistance-button').click()
    wait_for_element_by(By.ID, r)
    browser.find_element(By.ID, r).click()
    wait_for_text("Select a Vaccination Centre Location")
    time.sleep(2)
  
  # Loop all vaccine providers. 
  # This is a poke & peek process until can not find any more provider, because during navigation the provide list might be changed.
  while True:
    # logging.info("Scanning ...")
    wait_for_text("Select a Vaccination Centre Location")
  
    # Load all paginated results
    while "Load more locations" in browser.page_source:
      for btn in browser.find_elements(By.TAG_NAME, "button"):
        if btn.get_attribute("data-testid") == "load-more-locations-button":
          btn.click()
          time.sleep(5)
          wait_for_text("Select a Vaccination Centre Location")
          break
  
    # wait_for_text("tw-max-w-screen-sm tw-p-6 tw-mx-auto md:tw-px-0 tw-pt-8 tw-prose")
    # Loop all location buttons
    vaccineProviders=browser.find_elements(By.CLASS_NAME, "tw-sr-only")
    entryCount=len(vaccineProviders)
    logging.info("Found {} potentional locations..".format(entryCount))
    for i in range(entryCount):
      vaccineProvider=vaccineProviders[i]
  
      if vaccineProvider.get_attribute("data-testid") == "sr-button-location-name":
        t=vaccineProvider.text
    
        if t in vc:
          if i == entryCount-1:
            print("Ends with found repeat ...")
            summary()
          else:
            continue
          
        else:
          btn=vaccineProvider.find_element(By.XPATH, "..")
          btn.click()
          wait_for_text("Book Appointment")
          wait_for_element_by(By.CLASS_NAME, "day--blocked")
          dates=browser.find_elements(By.CLASS_NAME, "calendar__day")
          cnt=0
          for dateEntry in dates:
            dClass=dateEntry.get_attribute("class")
            if (not "day--blocked" in dClass) and (dClass != "calendar__day day--selected calendar__day--today"):
              cnt+=1
          
          slotTextElements=browser.find_elements(By.CLASS_NAME, "tw-text-lg")
          for slotTextElement in slotTextElements:
            if slotTextElement.tag_name == "h3":
              slotText=slotTextElement.text
  
          slotStartElement=browser.find_element(By.CLASS_NAME, "tw-mb-5")
          slotstartText=slotStartElement.text
          logging.info("+ Discover {}: {} day(s) has {}. {}".format(t, cnt, slotText, slotstartText))
          
          vc.append(t)
          vcList.append({
            _key_provider: t,
            _key_vacant_days_count: cnt,
            _key_slot_text: slotText,
            _key_slot_start_text: slotstartText
          })

          for btn in browser.find_elements(By.TAG_NAME, "button"):
            if btn.get_attribute("data-testid")=="back-button":
              btn.click()
              time.sleep(delayInterval)
              break                            
          # browser.back()
          # time.sleep(5)
  
          if i == entryCount-1:
            logging.debug("Ends with found all location navigated ...")
            summary()
          break
      else:
        if i == entryCount-1:
          logging.debug("Ends with found redirection...")
          summary()

# main process
def main():
  init()
  navigate()
  scan_vaccination()

# entry point  
if __name__ == "__main__":
    main()
