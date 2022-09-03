const express = require('express');
const puppeteer = require('puppeteer');
const app = express();
const port = 5501;


app.get('/', (req, res) => {
    res.sendFile(__dirname + '/static/project2.html');
  });

  app.get('/search', (req, res) => {
    const searchQuery = request.query.searchquery;

    if(searchQuery != null){
        searchWiki(searchQuery)
            .then(results => {
                //Returns a 200 Status OK with Results JSON back to the client.
                response.status(200);
                response.json(results);
            }); 
    }
    else{
      response.end();
    }
  });

  app.listen(port, () => console.log(`This app is listening on port ${port}`));
