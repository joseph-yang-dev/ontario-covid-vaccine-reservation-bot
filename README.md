# Overview 
This is a crawler robot program used to scan Canada Ontario provincal COVID-19 Vaccine revervation system, obtain the most recent available slot for the people who are ellegible for Ontario's vaccination program. Hope this small program gives people to relief to the threat of COVID-19 and a healthy, happy life. 

Note that this program uses regular and legal web interface to access the reservation system and simulates normal browsing behaviors. However, if you have found your expected reservation, please stop running it to give out access bandwidth to others. 

# Prereq
This program is only tested in a Windows environment. To run this program, you need to install following softwares:
- Chrome browser: https://www.google.com/intl/en_ca/chrome/
- Chrome driver: https://chromedriver.chromium.org/downloads
- python 3.x: https://www.python.org/downloads/
- python selenum: https://selenium-python.readthedocs.io/installation.html


# Usage
Type -h parameter only will be able obtain all parameter references:
```
python3 vaccine-scanner.py -h
usage: vaccine-scanner.py [-h] [-d] [-r] -n {1,2,3} -c HCN -v VCODE -s SCN -b DOB -p POSTAL [-e EMAIL] [-m CELLPHONE] [-r50] [-r100] [-r200] [-r500]

Ontario vaccine reservation bots.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Turn on debug mode.
  -r, --reschedule      Reschedule existing reservation. Ignore this option if you do NOT have any active reservation (reserved but not completed). In another word, if you are looking for a new vaccine reservation, IGNORE this option.
  -n {1,2,3}, --number-of-doses {1,2,3}
                        The does sequence number.
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
python3 vaccine-scanner.py -n 3 -c 1234-567-890 -v AB -s LV1234567 -b 1980-01-02 -p M1N-2J3 -r50
```

Note that:
1. This program is only helping you to scan the system for any availablity with the specific range, however, will NOT reserve the spot for you. In order to complete the reservation, you have to complete the booking by:
  > - take over the pop-up chrome browser window, quickly complete the rest of reservation process. 
  > - open a new browser to start the reservation process from scratch. 
2. This scanner can skip the York Region restriction for all Ontarian people to book all vaccine appointment in the entire Ontario province. 

# Expected result
After running the program for a few minutes, a scan result as following example can be harvested from the standard output:
```
Summary:
INFO:root:>> (HKPR - Lindsay Exhibition (Jan. 31 - Feb. 4)): 1 - 1 time slots available. For Thursday, February 3, 2022
INFO:root:>> (TPHU - Scarborough Town Centre, Near entrance 2 (Jan 20 - Feb 19) Ages 12+): 1 - 1 time slots available. For Wednesday, February 16, 2022
INFO:root:>> (HKPR - Lindsay Exhibition (Jan. 17 - 23)): 7 - 35 time slots available. For Monday, January 17, 2022
INFO:root:>> (HKPR - Fenelon Falls Community Centre (Jan. 25 & 26)): 2 - 7 time slots available. For Tuesday, January 25, 2022
INFO:root:>> (HKPR - Fenelon Falls Community Centre (Feb. 1 & 2)): 2 - 19 time slots available. For Tuesday, February 1, 2022
INFO:root:>> (HKPR - Fenelon Falls Community Centre (Jan. 18 & 19)): 2 - 44 time slots available. For Tuesday, January 18, 2022
INFO:root:>> (HKPR - Cobourg Community Centre (Jan. 31 - Feb 4)): 4 - 8 time slots available. For Tuesday, February 1, 2022
INFO:root:>> (HKPR - Cobourg Community Centre (Jan. 10 - 16)): 4 - 32 time slots available. For Thursday, January 13, 2022
INFO:root:>> (HKPR - Cobourg Community Centre (Jan. 17 - 23)): 7 - 73 time slots available. For Monday, January 17, 2022
INFO:root:>> (PPHU - Healthy Planet Arena (Jan.10-14)): 1 - 9 time slots available. For Friday, January 14, 2022
INFO:root:>> (PPHU - Healthy Planet Arena (Jan.17-21)): 5 - 94 time slots available. For Monday, January 17, 2022
```

You can open a new browser follow the offical reservation procedure locate the selected. 

# Disclaimer
This program was created for the need to fight the COVID-19 Omicorn variant. Heard too much news of people suffering when looking for a vaccination opportunity. If this program offends any people or violates any regulation, please open a ticket in https://github.com/joseph-yang-dev/ontario-covid-vaccine-reservation-bot/issues. It will be taken down with no time. 

This code was just created for instant needs and educational. No warranty, use on your own risk. And the creator does NOT take any responsibility from any consequence of usage. However, still welcome to open an issue ticket here to let us know your opinion and improvement suggestion.

God bless everybody and good luck!

Boxing Day of 2021.