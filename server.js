const express = require("express");

const app = express();
app.use(express.json({
    limit: '30mb',
}));
app.use(express.urlencoded({
    limit: '30mb',
    extended: true
}));

app.get('/', async (req, res) => {
    res.send("NASA APOD Discord bot is alive!").status(200);
});

const keepAlive = () => {
    app.listen(3000, () => {
        console.log("[SERVER] listening on port #3000");
    });
};

module.exports = keepAlive;