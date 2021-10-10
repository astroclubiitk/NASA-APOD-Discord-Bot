import requests
import urllib.request
import shutil
from bs4 import BeautifulSoup
import os
import re


class NasaApod:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.3"
        }
        self.url = "https://apod.nasa.gov/apod/"

    def collect_info(self):
        response = requests.get(self.url, headers=self.headers)
        print(response.status_code)
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
        content = soup.select_one("body > p:nth-child(3)").text.strip()

        try:
            tomorrows_image = (
                re.search("Tomorrow's picture: (.+?)\n", content).group(1).strip()
            )
        except:
            tomorrows_image = "TBA"

        try:
            image = soup.select_one("img")
            filename = f"apod-{date}.jpg"

            if os.path.exists(filename):
                return date, title, name, credit_link, filename, True
            
            status = self.download_image(self.url + image["src"], filename)

        except:
            video = soup.select_one("iframe")
            filename = f"apod-{date}.mp4"

            if os.path.exists(filename):
                return date, title, name, credit_link, filename, True 
            
            status = self.download_video(video["src"], filename)

        print(f"{date=}\n\n{title=}\n\n{credit=}\n\n{tomorrows_image=}")
        return date, title, name, credit_link, filename, status, tomorrows_image

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

    def download_video(self, url_link, filename):
        try:
            urllib.request.urlretrieve(url_link, filename)
        except:
            print("Couldn't load video!")


dummy = NasaApod()
dummy.collect_info()
