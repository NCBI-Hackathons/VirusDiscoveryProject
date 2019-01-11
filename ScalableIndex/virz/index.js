const express = require('express')
const app = express()
const port = 8000
const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');
const mongo_url = 'mongodb://localhost:27017';
//const mongo_db = 'hackathon'; // smaller db
const mongo_db = 'big_hack';
const q2m = require('query-to-mongo')

app.get('/', function (req, res) {
  res.send(
  `
  <li><a href="/query?meta__bio_project=PRJEB24383">BioProject PRJEB24383</a>
  <li><a href="/query?length=>200">Contig length >300</a>
  <li><a href="/query?length=>200&sample__sacc=NC_005856">Contig length >300 and sample accession NC_005856</a>
  <li><a href="/query?contig=Contig_68060_47.6107">Contig Contig_68060_47.6107</a>
  <li><a href="/query?sample__btax=&quot;10678&quot;">Tax 10678</a>
  <li><a href="/query?meta__scientific_name=/^human gut/&fields=meta__scientific_name,sample__btax">Viral taxa for human gut samples</a>
  <li><a href="/query?meta__center=/OXFORD/&fields=meta__center">Sample from Oxford</a>
  <li><a href="/query?meta__bio_sample=SAMEA728658">BioSample SAMEA728658</a>
  </ul>
  `);
})

app.listen(port, () => console.log(`Example app listening on port ${port}!`))

app.get('/query', function (req, res) {
  var client = new MongoClient(mongo_url);
  client.connect(function(err) {
    assert.equal(null, err);

    const db = client.db(mongo_db);
    console.log("Connected successfully to db", mongo_db);

    // length=>100&sample__sacc=NC_005856
    // { length: { '$gt': 100 }, sample__sacc: 'NC_005856' }
    var qry = q2m(req.query);
    console.log(qry.criteria);
    db.collection('query').find(qry.criteria, qry.options).toArray(
      function(err, docs) {
        if (err) {
          console.log(err)
          res.send(err) 
        }
        else {
          res.send(docs)
        }
      }
    );
  });
})
