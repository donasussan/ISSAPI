import requests
import smtplib
import datetime

password_ = "bnsiayfabqvshjwk"
my_lat = 10.3528744

my_long = 76.5120396

#my_position = (my_lat,my_long)
#print("My position is :", my_position)

def iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    #this lat and long gives the lat and long of ISS
    longitude = float(data['iss_position']['longitude'])
    latitude = float(data['iss_position']['latitude'])
    iss_position = (longitude, latitude)
    print("The ISS Position is :", iss_position)


    if my_lat-5 <= latitude < my_lat+5 and my_long-5 <= longitude < my_long+5:
        return True

def is_night():
    #code for finding if its in the night
    parameters = {"lat": my_lat,
                  "lng": my_long,
                  "formatted": 0
                  }
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    sundata = response.json()
    #print(sundata)

    sun_rise = sundata['results']['sunrise']
    sun_set = sundata['results']['sunset']
    #print("sunrise", sun_rise)
    #print("sunset", sun_set)
    sun_rise_hour =int(sun_rise.split("T")[1].split(":")[0])
    sun_set_hour = int(sun_set.split("T")[1].split(":")[0])
    #print("sunrise", sun_rise_hour)
    #print("sunset", sun_set_hour)



    time_now = datetime.datetime.now()
    hour_now = int(time_now.hour)
    print("Hour now", hour_now)
    # notify when the iss position is +5 or -5 degrees near to my position

    if hour_now >= sun_set_hour or hour_now<= sun_rise_hour:
        return True


while True:
    if is_night() and iss_overhead():

        connection = smtplib.SMTP("smtp.gmail.com")
        my_email = "donasussanchacko@gmail.com"
        password = password_
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs="donasussan2000@gmail.com",
        msg="Subject:The International Space Station \n\n Hello! This message is to inform you that the International Space Station is just above your head! ")
        print("ISS IS ABOVE YOU!!")
        connection.close

    else:
        print("ISS not above you")





