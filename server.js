const express = require("express");
const multer = require("multer");
const cors = require("cors");
const fs = require("fs");
const { exec } = require("child_process");

const app = express();

app.use(cors());

const upload = multer({
    dest: "uploads/"
});

app.get("/", (req, res) => {
    res.send("Whisper API Running");
});

app.post("/transcribe", upload.single("audio"), (req, res) => {

    if (!req.file) {
        return res.status(400).send("No file uploaded");
    }

    const input = req.file.path;

    const cmd = `./whisper.cpp/build/bin/whisper-cli \
-m ./whisper.cpp/models/ggml-medium.bin \
-f ${input} \
-oj`;

    console.log(cmd);

    exec(cmd, (error, stdout, stderr) => {

        console.log("STDOUT:");
        console.log(stdout);

        console.log("STDERR:");
        console.log(stderr);

        if (error) {
            console.log(error);
            return res.status(500).send(error.toString());
        }

        const jsonFile = input + ".json";

        console.log("Looking for:", jsonFile);

        if (!fs.existsSync(jsonFile)) {

            return res.status(500).json({
                error: "JSON not generated",
                stdout,
                stderr
            });

        }

        const json = fs.readFileSync(jsonFile, "utf8");

        res.setHeader("Content-Type", "application/json");

        res.send(json);

    });

});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {

    console.log("Server running on " + PORT);

});