import requests
import shutil
from bs4 import BeautifulSoup
import os


class NasaApod:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.3"
        }
        self.url = "https://apod.nasa.gov/apod/"

    def collect_info(self):
        response = requests.get(self.url, headers=self.headers)
        data = response.content
        soup = BeautifulSoup(data, "html.parser")

        date = (
            soup.select_one("body > center:nth-child(1) > p:nth-child(2)")
            .text.strip()
            .split("\n")[-1]
        )
        title = soup.select_one(
            "body > center:nth-child(2) > b:nth-child(1)"
        ).text.strip()
        credit = soup.select_one("body > center:nth-child(2) > a")
        name = credit.text.strip()
        credit_link = credit["href"]
        # content = soup.select_one("body > p:nth-child(3)").text.strip()

        image = soup.select_one("img")
        filename = f"apod-{date}.jpg"

        if os.path.exists(filename):
            return date, title, name, credit_link, filename, True

        status = self.download_image(self.url + image["src"], filename)
        # print(f"{date=}\n\n{title=}\n\n{credit=}\n\n{content=}")
        return date, title, name, credit_link, filename, status

    def download_image(self, image_url, filename):
        r = requests.get(image_url, stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True
            with open(filename, "wb") as f:
                shutil.copyfileobj(r.raw, f)
            return True
        else:
            print("Couldn't load image!")
            return False
