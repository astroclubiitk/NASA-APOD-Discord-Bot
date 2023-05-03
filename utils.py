import requests

introduction = "Hello there! I'm your NASA APOD bot. I fetch information from NASA APOD site [https://apod.nasa.gov/apod/], where each day a different image or photograph of our universe is featured, along with a brief explanation written by a professional astronomer."

help_content = "Use **$APOD** followed by"

def check_validity(url):
    response = requests.get(
        url,
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.3"
        }
    )
    if "was not found on this server" in str(response.content):
        return False
    return True