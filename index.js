const { Client, Intents } = require("discord.js")

const returnHelp = require("./messages/help.js");
const returnInfo = require("./messages/info.js");
const returnError = require("./messages/error.js");
const checkValidity = require("./helpers/checkValidity.js");
const keepAlive = require("./server.js");

const { APOD_CHANNEL_ID, APOD_TOKEN, APOD_PREFIX, APOD_URL } = require("./config.js")

const client = new Client({
    intents: [
        Intents.FLAGS.GUILDS,
        Intents.FLAGS.GUILD_MESSAGES
    ]
});

client.on("ready", () => {
    console.log(`[DISCORD] ${client.user.tag} is ready!`)
    client.user.setPresence({
        status: 'online',
        activities: [{
            name: '$APOD help',
            type: 'PLAYING',
        }]
    });
    setInterval(() => {
        // Redundancy if the server restarts, to prevent duplicates
        const now = new Date();
        if (now.getHours() === 9 && now.getMinutes() === 7){
            const channel = client.channels.cache.get(APOD_CHANNEL_ID);
            if (channel){
                returnInfo(APOD_URL)
                    .then((reply) => {
                        channel.send(reply.replyMessage);
                        channel.send(reply.linkURL);
                    })
                    .catch(error => {
                        console.log(error);
                    });
            } else {
                console.log(`[DISCORD][ERROR] Unable to find channel with channel ID: ${APOD_CHANNEL_ID}`);
            }
        }
        return;
    }, 60000);
})

client.on("message", async (message)=> {
    if (!message.content.startsWith(APOD_PREFIX) || message.author.bot){
        return;
    }

    const [P, command, ...rawArgs] = message.content
        .trim()
        .toLowerCase()
        .substring(APOD_PREFIX.length)
        .split(/\s+/);
    
    if (command == "help"){
        await returnHelp(message);
    } else if (command.split("/").length == 3){
        const date_nums = command.split("/");
        if (date_nums[0].length == 1)
            date_nums[0] = "0" + date_nums[0];
        if (date_nums[1].length == 1)
            date_nums[1] = "0" + date_nums[1];
        date_nums[2] = parseInt(date_nums[2]%100).toString();
        if (parseInt(date_nums[2]) < 15){
            await returnError(message);
            return;
        }

        const targetURL = APOD_URL + `ap${date_nums[2]}${date_nums[1]}${date_nums[0]}.html`;
        const isUrlValid = await checkValidity(targetURL);
        if (!isUrlValid){
            await returnError(message);
            return;
        }

        const reply = await returnInfo(targetURL);
        await message.reply(reply.replyMessage);
        message.channel.send(reply.linkURL);
    }
});

keepAlive();
client.login(APOD_TOKEN);