const { MessageEmbed } = require("discord.js");
const { APOD_COLOR } = require("../config.js");

const returnError = async (message) => {
    const errorEmbed = new MessageEmbed()
        .setColor(APOD_COLOR)
        .setTitle("Scrape Error")
        .setDescription("The date doesn't seem to be in the specified format of **dd/mm/yy**. Please check again.");

    await message.reply({
        embeds: [errorEmbed]
    });
}

module.exports = returnError;