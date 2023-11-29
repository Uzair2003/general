# URL Shortner Using Cuttly
# Uzair

import requests

# Function to shorten a URL using Cuttly
def shorten_url(full_url, custom_name):

    api_key = "89e6ba1ef5d2abf9fb166a1ed151791ae8bd0" 
    base_url = "https://cutt.ly/api/api.php"

    # Payload for the API request
    payload = {
        "key": api_key,
        "short": full_url,
        "name": custom_name
    }

    try:
        response = requests.get(base_url, params=payload)
        # Raise an error for bad HTTP status codes   
        response.raise_for_status() 

        data = response.json()
        url_status = data["url"]["status"]

        # Check if URL shortening was successful
        # Status 7 indicates successful URL shortening
        if url_status == 7:  
            title = data["url"]["title"]
            short_link = data["url"]["shortLink"]
            return f"Title: {title}\nShortened Link: {short_link}"
        else:
            return f"Error: Unable to shorten URL. Status code: {url_status}"

    except requests.RequestException as e:
        return f"Error: An exception occurred - {e}"

# Main function to drive the program
def main():
    user_url = input("Enter a URL to shorten: ")
    custom_name = input("Enter a custom name for the shortened URL (leave blank for a random name): ")

    shortened_url = shorten_url(user_url, custom_name)
    print(shortened_url)

if __name__ == "__main__":
    main()
