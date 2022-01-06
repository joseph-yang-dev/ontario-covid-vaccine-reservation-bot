# Overview 
This is a crawler robot program used to scan Canada Ontario provincal COVID-19 Vaccine revervation system(https://covid19.ontariohealth.ca/), obtain the most recent available slot for the people who are ellegible for Ontario's vaccination program. Hope this small program gives people to relief to the threat of COVID-19 and a healthy, happy life. 

Note that this program uses regular and legal web interface to access the reservation system and simulates normal browsing behaviors. However, if you have found your expected reservation, please stop running it to give out access bandwidth to others. 

# Prerequisite
## Interactively
This program is only tested in a Windows environment. To run this program, you need to install following softwares:
- Chrome browser: https://www.google.com/intl/en_ca/chrome/
- Chrome driver: https://chromedriver.chromium.org/downloads
- python 3.x: https://www.python.org/downloads/
- python selenium module: https://selenium-python.readthedocs.io/installation.html

## Silently
This program is also dockerized. All you need is a docker engine capable of running x86 Linux docker images. No additional dependent software is required to run this program silently.

# Usage
## Interactively
This program can be run as a normal python application. Using -h parameter only will be able obtain all parameter references:
```
$ python3 vaccine-scanner.py -h
usage: vaccine-scanner.py [-h] [-d] [-r] -n {1,2,3} [-l LOOPCOUNT] -c HCN -v VCODE -s SCN -b DOB -p POSTAL [-e EMAIL] [-m CELLPHONE] [-r50] [-r100] [-r200] [-r500]

Ontario vaccine reservation finder.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Turn on debug mode.
  -r, --reschedule      Reschedule existing reservation. Ignore this option if you do NOT have any active reservation (reserved but not completed). In another word, if
                        you are looking for a new vaccine reservation, IGNORE this option.
  -n {1,2,3}, --number-of-doses {1,2,3}
                        The does sequence number.
  -l LOOPCOUNT, --number-of-loops LOOPCOUNT
                        How many times to scan the reservations.
  -c HCN, -hcn HCN      Ontario health card number, in "xxxx-xxx-xxx"(10 digits) format.
  -v VCODE, --vcode VCODE
                        Ontario health card number verificiation code in "XX"(2 alphabet codes).
  -s SCN, --scn SCN     Ontario health card security code(can be found in the back) in "XXNNNNNNN"(2 alphabet and 7 digits combination).
  -b DOB, --dob DOB     Date of birth in "yyyy-mm-dd" format.
  -p POSTAL, --postal POSTAL
                        Postal code (match to healthcard) in "A0B-1C3" format.
  -e EMAIL, --email EMAIL
                        Email address to receive confimration and notification. Only needed for the fist dose reservation.
  -m CELLPHONE, --cellphone CELLPHONE
                        Mobile phone to receive confirmation and notification. Only needed for the fist dose reservation.
  -r50, --in-50-km      Search with 50KM range.
  -r100, --in-100-km    Search with 100KM range.
  -r200, --in-200-km    Search with 200KM range.
  -r500, --in-500-km    Search with 500KM range.
  ```


If passing in proper parameters and values as following example, a chrome browser window will pop and simulate all regular reservation process on behalf of the provide health card owner.

```
$ python3 vaccine-scanner.py -n 3 -c 1234-567-890 -v AB -s LV1234567 -b 1980-01-02 -p M1N-2J3 -r50
```


Note that:
1. This program is only helping you to scan the system for any availablity with the specific range, however, will NOT reserve the spot for you. In order to complete the reservation, you have to complete the booking by taking over the pop-up chrome browser window, quickly complete the rest of reservation process. 
2. This scanner can skip the York Region restriction for all Ontarian people to book all vaccine appointment in the entire Ontario province. 

## Silently in a docker container
To run this program in a docker container, following command can be issued:
```
docker run --shm-size="4g" quay.io/joseph_yang_dev/ontario-vaccine-finder <parameters>
```

Note:
1. The parameters in the command is 100% the same as those used in the interactive approach. Same result as interactive mode is returned in silent mode.
2. **--shm-size="4g"** is needed, since the chrome engine consumes a lot of memory. You can adjust a better value according to your machine configuration.
3. In silent mode, there will be no browser pops up. Hence, you need to open a browser to complete the reservation process after.

Also, only passing **-h** can return all required parameters:
```
# docker run -it --shm-size="4g" quay.io/joseph_yang_dev/ontario-vaccine-finder -h
usage: vaccine-scanner.py [-h] [-d] [-x] [-r] -n {1,2,3} [-l LOOPCOUNT] -c HCN -v VCODE -s SCN -b DOB -p POSTAL [-e EMAIL] [-m CELLPHONE] [-r50] [-r100] [-r200] [-r500]

Ontario vaccine reservation finder.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Turn on debug mode.
  -x, --headless        Headless execution. Used only for dockerize or running without browser pops.
  -r, --reschedule      Reschedule existing reservation. Ignore this option if you do NOT have any active reservation (reserved but not completed). In another word, if you are looking for a new vaccine reservation, IGNORE this option.
  -n {1,2,3}, --number-of-doses {1,2,3}
                        The does sequence number.
  -l LOOPCOUNT, --number-of-loops LOOPCOUNT
                        How many times to scan the reservations.
  -c HCN, -hcn HCN      Ontario health card number, in "xxxx-xxx-xxx"(10 digits) format.
  -v VCODE, --vcode VCODE
                        Ontario health card number verificiation code in "XX"(2 alphabet codes).
  -s SCN, --scn SCN     Ontario health card security code(can be found in the back) in "XXNNNNNNN"(2 alphabet and 7 digits combination).
  -b DOB, --dob DOB     Date of birth in "yyyy-mm-dd" format.
  -p POSTAL, --postal POSTAL
                        Postal code (match to healthcard) in "A0B-1C3" format.
  -e EMAIL, --email EMAIL
                        Email address to receive confimration and notification. Only needed for the fist dose reservation.
  -m CELLPHONE, --cellphone CELLPHONE
                        Mobile phone to receive confirmation and notification. Only needed for the fist dose reservation.
  -r50, --in-50-km      Search with 50KM range.
  -r100, --in-100-km    Search with 100KM range.
  -r200, --in-200-km    Search with 200KM range.
  -r500, --in-500-km    Search with 500KM range.
```
# Expected result
After running the program for a few minutes, a scan result as following example can be harvested from the standard output:
```
###################################################################################################
Summary:
>> (HKPR - Lindsay Exhibition (Jan. 24 - 28)): 1 - 1 time slots available. For Wednesday, January 26, 2022
>> (HKPR - Lindsay Exhibition (Jan. 10 - 16)): 1 - 1 time slots available. For Thursday, January 13, 2022
>> (HKPR - Lindsay Exhibition (Jan. 17 - 23)): 6 - 50 time slots available. For Tuesday, January 18, 2022
>> (HKPR - Fenelon Falls Community Centre (Jan. 25 & 26)): 2 - 1 time slots available. For Tuesday, January 25, 2022
>> (MGH-Shoppers World Danforth (Dec 27 - Jan 2)): 1 - 1 time slots available. For Sunday, January 2, 2022
>> (SMDHU-Holly Recreation Centre, Community Room (Jan 15-20)): 1 - 1 time slots available. For Tuesday, January 18, 2022
>> (SMDHU - 29 Sperling Drive Covid-19 Immunization Clinic (Jan 2-Feb 3)): 2 - 1 time slots available. For Monday, January 10, 2022
>> (TPHU - Woodbine Mall, Inside Hudson's Bay (Jan 20 - Feb 19) Ages 12+): 1 - 1 time slots available. For Tuesday, February 8, 2022
>> (HKPR - Lindsay Exhibition (Jan. 2 - 9)): 1 - 1 time slots available. For Sunday, January 9, 2022
>> (HKPR - Fenelon Falls Community Centre (Feb. 1 & 2)): 2 - 19 time slots available. For Tuesday, February 1, 2022
>> (HKPR - Fenelon Falls Community Centre (Jan. 18 & 19)): 2 - 36 time slots available. For Tuesday, January 18, 2022
>> (HKPR - Fenelon Falls Community Centre (Jan 11 & 12)): 1 - 1 time slots available. For Tuesday, January 11, 2022
###################################################################################################
```

When the program finish running, the scanning browser stay active. You can continue the rest of the reservation by using the scanning browser, all personal information is the same as those in the command line parameters.

# Troubleshooting

For Mac user, if found following errors:
```
Error: “chromedriver” cannot be opened because the developer cannot be verified. Unable to launch the chrome browser
```
Then you need to follow https://stackoverflow.com/questions/60362018/macos-catalinav-10-15-3-error-chromedriver-cannot-be-opened-because-the-de to configure chromedriver installation in your Mac OS.

# Disclaimer
This program was created for the need to fight the COVID-19 Omicorn variant. Heard too much news of people suffering when looking for a vaccination opportunity. If this program offends any people or violates any regulation, please open a ticket in https://github.com/joseph-yang-dev/ontario-covid-vaccine-reservation-bot/issues. It will be taken down with no time. 

This code was just created for instant needs and educational. No warranty, use on your own risk. And the creator does NOT take any responsibility from any consequence of usage. However, still welcome to open an issue ticket here to let us know your opinion and improvement suggestion.

God bless everybody and good luck!

**Boxing Day of 2021.**