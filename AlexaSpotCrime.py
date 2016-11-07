import logging, requests, json
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


  
   
@ask.launch
def new_program():
    location = "Give me the pincode where you want me to spot crime, and I'll tell you the top dangerous streets in that area and related crime information'"
	#IP2LocObj = IP2Location.IP2Location()
	#IP2LocObj.open("data/IP-COUNTRY-REGION-CITY-LATITUDE-LONGITUDE-ZIPCODE-TIMEZONE-ISP-DOMAIN-NETSPEED-AREACODE-WEATHER-MOBILE-ELEVATION-USAGETYPE-SAMPLE.BIN")
	#rec = IP2LocObj.get_all("19.5.10.1")
    #location = "Do you want to spot crime at {}".format(str(rec.city))
    return question(location)

@ask.intent("locationIntent", convert={'pincode': int})
def checkcrime(pincode):
    
    location = requests.get('https://www.zipcodeapi.com/rest/wDv6MejhOSmYXNvv1zPMun0b8TXsQNRmrmseAMvpESnCFS7HsXuWlv8to5WeSNBk/info.json/{}/degrees'.format(pincode))
    try:
        lat = json.loads(location.text)['lat']
    except:
        statement("I couldn't find the pincode. Please try again'")
        return question(location)
    lng = json.loads(location.text)['lng']
    radius = 0.5
    param ={'lon' : lng, 'lat' : lat, 'radius': radius, 'key': '.' }
    response = requests.get("https://api.spotcrime.com/crimes.json", params = param)
    data = response.json()
    givenList = data["crimes"]
      
    crimeList = []
    addressList = []
    OF = "OF"
    AMPERSAND = "&"
    
    for chunk in givenList:
        if chunk["type"] in crimeList:
            pass
        else:
            crimeList.append(chunk["type"])
            
        fullAddress = chunk["address"]
            
            #print fullAddress
            
        if (OF in fullAddress):
            street1 = fullAddress[fullAddress.index(OF) + 3 :]

            if street1 in addressList:
                pass
            else:
                addressList.append(street1)
        elif (AMPERSAND in fullAddress):
            street2 = fullAddress[:fullAddress.index(AMPERSAND)]
            street3 = fullAddress[fullAddress.index(AMPERSAND)+2:]

            if street2 in addressList:
                pass
            else:
                addressList.append(street2)
                
            if street3 in addressList:
                pass
            else:
                addressList.append(street3)


    icrimecount = [0] * len(crimeList)
    time_crime_slot = [0] * 8 #there are eight different time slots which are fixed 12 am - 3am , 3am - 6am etc etc.
        
    istreetcount = [0]* len(addressList)
        

    for chunk in givenList:
        if chunk["type"] in crimeList:
            icrimecount[crimeList.index(chunk["type"])] +=1

        eventTime = 0
            #12 is the only number in PM in which we don't add 12
            
        event_hour = int(chunk["date"][9:11])*100
        event_min = int(chunk["date"][12:14])

            #print chunk["date"][15:17]
        if ((str(chunk["date"][15:17]) == 'PM') and (int(event_hour) != 1200 )):
            eventTime +=1200
                                        
        if ((str(chunk["date"][15:17]) == 'AM') and (int(event_hour) == 1200 )):
            event_hour = 2400

        eventTime += event_hour + event_min

        value = 300
            #print eventTime
        for i in range(8):
            if (int(eventTime) <= value):
                time_crime_slot[i] += 1
                break
            value += 300
            
        for street in addressList:
            if street in chunk["address"]:
                istreetcount[addressList.index(street)] += 1    

            
        #sorted(range(len(addressList)), key=lambda x: addressList[x])
        #topThree = sorted(range(len(addressList)), key=lambda x: addressList[x])[-3:]

        
        #print icrimecount       
    total_crime = len(givenList)
        #print time_crime_slot

    print addressList
        #print crimeList

    print istreetcount

        #print topThree

    crimeListDict = {}

    for i in range(len(crimeList)):
        crimeListDict[str(crimeList[i])] = icrimecount[i]

    dangerousList = {}
    top = 0
    second = 0
    third = 0
    secondIndex = 0
    thirdIndex = 0
    topIndex = 0
    for i in range(len(istreetcount)):
        if (istreetcount[i] >= top):
            third = second
            second = top
            top = istreetcount[i]
            thirdIndex = secondIndex
            secondIndex = topIndex
            topIndex = i
        elif (istreetcount[i] >= second):
            third = second
            second = istreetcount[i]
            thirdIndex = secondIndex
            secondIndex = i
        elif (istreetcount[i] >= third):
            third = istreetcount[i]
            thirdIndex = i

            

    dangerousList[str(addressList[topIndex])] = istreetcount[topIndex]
    dangerousList[str(addressList[secondIndex])] = istreetcount[secondIndex]
    dangerousList[str(addressList[thirdIndex])] = istreetcount[thirdIndex]        

    print dangerousList
    
    #theList = str(dangerousList.keys)

    dangerous1 = str(dangerousList.keys()[0])
    try:
        dangerous2 = str(dangerousList.keys()[1])
    except:
        dangerous2 = " "
    try:
        dangerous3 = str(dangerousList.keys()[2])
    
    except:
        dangerous3 = " "
    
    dangerous_count1 = str(dangerousList.values()[0])
    try:
        dangerous_count2 = str(dangerousList.values()[1])
    except:
        dangerous_count2 = " "
    try:
        dangerous_count3 = str(dangerousList.values()[3])
    except:
        dangerous_count3 = " "
    return statement("The most dangerous streets in the area are {0},{1},{2},,{3} {4} have been reported,,{5} {6} have been reported, All these crimes were reported in last 24 hours.".format(dangerous1,dangerous2,dangerous3,icrimecount[0],crimeList[0],icrimecount[1],crimeList[1]))
        

if __name__ == '__main__':
    app.run(debug=True)
    
