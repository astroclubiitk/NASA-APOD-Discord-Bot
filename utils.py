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
        self.baseurl = "https://apod.nasa.gov/apod/"

    def collect_info(self, vimeo_video_quality):
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
        content = soup.select_one("body > p:nth-child(3)").text.strip()

        try:
            tomorrows_picture = (
                re.search("Tomorrow's picture: (.+?)\n", content).group(1).strip()
            )
        except:
            tomorrows_picture = "TBA"

        try:
            media_type = "Image"
            image = soup.select_one("img")
            filename = f"apod-{date}.jpg"

            if os.path.exists(filename):
                status = True
                is_linkable_video = False
                return (
                    date,
                    title,
                    name,
                    credit_link,
                    filename,
                    status,
                    tomorrows_picture,
                    media_type,
                    is_linkable_video,
                )

            status = self.download_image(self.baseurl + image["src"], filename)

        except:
            media_type = "Video"
            video = soup.select_one("iframe")
            filename = f"apod-{date}.mp4"

            video_url = video["src"].split("?")[0]
            if "youtu" in video_url:
                status = True
                is_linkable_video = True
                return (
                    date,
                    title,
                    name,
                    credit_link,
                    video_url,
                    status,
                    tomorrows_picture,
                    media_type,
                    is_linkable_video,
                )

            if os.path.exists(filename):
                status = True
                is_linkable_video = False
                return (
                    date,
                    title,
                    name,
                    credit_link,
                    filename,
                    status,
                    tomorrows_picture,
                    media_type,
                    is_linkable_video,
                )

            status = self.download_video(video_url, filename, vimeo_video_quality)

            if status == False:
                status = False
                is_linkable_video = True
                return (
                    date,
                    title,
                    name,
                    credit_link,
                    video_url,
                    status,
                    tomorrows_picture,
                    media_type,
                    is_linkable_video,
                )

        # print(f"{date=}\n{title=}\n{credit=}\n{tomorrows_picture=}\n{media_type=}")
        is_linkable_video = False
        return (
            date,
            title,
            name,
            credit_link,
            filename,
            status,
            tomorrows_picture,
            media_type,
            is_linkable_video,
        )

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

    def download_video(self, url_link, filename, vimeo_video_quality):
        if "vimeo" in url_link:
            from vimeo_downloader import Vimeo

            v = Vimeo(url_link, embedded_on=self.url)
            for s in v.streams:
                print(s.quality)
                if s.quality == vimeo_video_quality:
                    s.download(download_directory=".", filename=filename)
                    return True
                else:
                    print("Quality not found")
            return False

        try:
            urllib.request.urlretrieve(self.baseurl + url_link, filename)
        except:
            print("Couldn't load video!")


# dummy = NasaApod()
# dummy.collect_info('360p')
