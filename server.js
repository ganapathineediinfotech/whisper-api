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

app.post("/transcribe", upload.single("audio"), (req, res) => {

    if (!req.file) {
        return res.status(400).send("No file uploaded");
    }

    const input = req.file.path;

    const cmd =
`./whisper.cpp/build/bin/whisper-cli \
-m ./whisper.cpp/models/ggml-medium.bin \
-f ${input} \
-oj`;

    exec(cmd, (error, stdout, stderr) => {

        if (error) {

            console.log(stderr);

            return res.status(500).send(stderr);

        }

        const jsonFile = input + ".json";

        const json = fs.readFileSync(jsonFile);

        res.setHeader("Content-Type","application/json");

        res.send(json);

    });

});

app.listen(3000,()=>{

    console.log("Running on port 3000");

});