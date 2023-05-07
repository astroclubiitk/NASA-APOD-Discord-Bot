const dotenv = require("dotenv");

dotenv.config();

const APOD_COLOR = "#11213f";
const APOD_CHANNEL_ID = process.env.APOD_CHANNEL_ID;
const APOD_PREFIX = "$APOD";
const APOD_TOKEN = process.env.APOD_TOKEN;
const APOD_URL = "https://apod.nasa.gov/apod/"

module.exports = {
    APOD_COLOR,
    APOD_CHANNEL_ID,
    APOD_PREFIX,
    APOD_TOKEN,
    APOD_URL
};