import requests

def get_quote():
    url = "https://quote-sender.onrender.com/api/getquote"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        quote_data = data[0]
        quote = quote_data['quote']
        author = quote_data['quoteAuthor']
        return f'"{quote}" - {author}'
    else:
        return "Error fetching quote"