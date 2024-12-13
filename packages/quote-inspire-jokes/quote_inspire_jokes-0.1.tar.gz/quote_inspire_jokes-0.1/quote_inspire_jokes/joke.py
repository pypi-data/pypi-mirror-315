import requests

def get_joke():
    url = "https://v2.jokeapi.dev/joke/Any?type=single"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        joke = data.get('joke', 'No joke found.')
        return joke
    else:
        return "Error fetching joke"