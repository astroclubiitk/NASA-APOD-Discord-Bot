const axios = require("axios");
const cheerio = require("cheerio");

const { APOD_URL } = require("../config.js");

const checkValidity = async (url) => {
    try {
        const { data } = await axios.get(url);
        const $ = cheerio.load(data);

        if ($("body").text().split("html was not found on this server").length > 1)
            return false;
        return true;
    } catch (error){
        console.log("[AXIOS][ERROR]");
        console.log(error);
        return false;
    }
};

module.exports = checkValidity;