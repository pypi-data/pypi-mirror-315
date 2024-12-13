import requests

def get_inspiration():
    url = "http://api.forismatic.com/api/1.0/"
    params = {
        "method": "getQuote",
        "format": "json",
        "lang": "en"
    }
    response = requests.post(url, data=params)

    if response.status_code == 200:
        data = response.json()
        quote = data.get('quoteText', "No quote available")
        author = data.get('quoteAuthor', "Unknown Author")
        return f'"{quote}" - {author}'
    else:
        return "Error fetching inspiration"