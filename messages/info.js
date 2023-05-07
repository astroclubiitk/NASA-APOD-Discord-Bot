const axios = require("axios");
const cheerio = require("cheerio");

const { APOD_URL } = require("../config.js");

const returnInfo = async (url) => {
    try {
        const { data } = await axios.get(url);
        const $ = cheerio.load(data);

        const response = {
            date: "",
            title: "",
            explanation: "",
            name: "",
            creditLink: "",
            tomorrowsPicture: "TBA",
            linkURL: "",
            mediaType: ""
        };

        const dateContainer = $("center").find("p").eq(1).text().trim().split("\n");
        response.date = dateContainer[dateContainer.length - 1];

        const secondCenterTag = $("center").eq(1);
        response.title = secondCenterTag.find("b").first().text().trim();
        response.name = secondCenterTag.find("a").first().text().trim();
        response.creditLink = secondCenterTag.find("a").first().attr("href").trim();
        response.explanation = $("body").find("center").next("p").text().trim().split("\n").join(" ").split("  ").join(" ").split("Explanation: ").join("").trim().split(" Tomorrow's picture")[0].trim();

        const splitArr = $("body").text().split("Tomorrow's picture:");
        if (splitArr.length > 1){
            response.tomorrowsPicture = splitArr[1].split("<")[0].trim();
        }

        if ($("img").length > 0){
            response.linkURL = APOD_URL + $("img").attr("src");
            response.mediaType = "Image";
        } else if ($("iframe").length > 0){
            response.linkURL = $("iframe").attr("src").split("?")[0];
            response.mediaType = "Video";
        }

        const replyMessage = `
        **Astronomy Picture of the Day - NASA** :camera_with_flash: [https://apod.nasa.gov/apod/astropix.html]
**Date** - ${response.date}
**Title** - ${response.title}
**${response.mediaType} Credits** - ${response.name} [${response.creditLink}]
**Explanation** - ${response.explanation}
**Tomorrow's picture** - ${response.tomorrowsPicture.charAt(0).toUpperCase() + response.tomorrowsPicture.slice(1)}
        `
        return {
            replyMessage: replyMessage,
            linkURL: response.linkURL
        };
    } catch (error){
        console.log("[AXIOS][ERROR]");
        console.log(error);
    }
};

module.exports = returnInfo;