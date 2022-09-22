# URL Shortner Using Cuttly
# Uzair

# pip install requests
import requests 

def shorten_link(full_link, link_name):

    # Link the program to my Cuttly API 
    API_KEY = "89e6ba1ef5d2abf9fb166a1ed151791ae8bd0"
    BASE_URL = "https://cutt.ly/api/api.php"

    payload = {"key": API_KEY, "short": full_link, "name": link_name}
    request = requests.get(BASE_URL, params = payload)
    data = request.json()

    print("\n")

    try:
        title = data["url"]["title"]
        short_link = data["url"]["shortLink"]

        print("\33[32mTitle:\33[0m", title)
        print("\33[32mShortened Link:\33[0m", short_link)

    except:
        status = data["url"]["title"]
        print("Error Status:", status)

link = input("\33[33mEnter A Link: \33[0m")
name = input("\33[33mGive Your Link A Name(Leave Blank For Random Name): \33[0m")
shorten_link(link, name)
