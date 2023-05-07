const { MessageEmbed } = require("discord.js");
const { APOD_COLOR } = require("../config.js");

const returnHelp = async (message) => {
    const helpEmbed = new MessageEmbed()
        .setColor(APOD_COLOR)
        .setTitle("NASA APOD Help")
        .setDescription("Hello there! I'm your NASA APOD bot. I fetch information from NASA APOD site [https://apod.nasa.gov/apod/], where each day a different image or photograph of our universe is featured, along with a brief explanation written by a professional astronomer.")
        .setFields(
            { name: "**help**", value: "To open this menu" },
            { name: "**dd/mm/uu**", value: "To show the APOD at that day (January 1, 2015 onwards)" }
        );

    await message.reply({
        embeds: [helpEmbed]
    });
}

module.exports = returnHelp;