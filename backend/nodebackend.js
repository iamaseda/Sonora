import crypto from "crypto";

function verifySignature(
  secret /* Secret specified on Cyanite.ai */,
  signature /* Signature sent via the Signature header */,
  body /* raw request body */
) {
  const hmac = crypto.createHmac("sha512", secret);
  hmac.write(body);
  hmac.end();
  const compareSignature = hmac.read().toString("hex");
  if (signature !== compareSignature) {
    throw new Error("Invalid signature");
  }
}

const express = require('express')
const request = require('request');
const axios = require('axios');

app = express();
const PORT = 3000;

app.get('/ls-genres', function(req, res) {
    request('http://127.0.0.1:5000/flask', function (error, response, body) {
        console.error('error:', error); // Print the error
        console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
        console.log('body:', body); // Print the data received
        res.send(body); //Display the response on the website
      });      
});

app.listen(PORT, function (){ 
    console.log('Listening on Port 3000');
});  