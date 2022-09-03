const { MongoClient } = require('mongodb');
var sw = require('stopword');
var natural = require('natural');
var cont = require('./contractions');

const url = 'mongodb://localhost:27017';
const client = new MongoClient(url);

const dbName = 'Wiki-SE';

async function main() {
  await client.connect();
  console.log('Connected successfully to server');
  const db = client.db(dbName);
  const content = db.collection('Content');
  const Doc_info = db.collection('Doc_info');
    
  return 'done.';
}

main()
  .then(console.log)
  .catch(console.error)
  .finally(() => client.close());



function sort_object(obj) {
    items = Object.keys(obj).map(function(key) {
        return [key, obj[key]];
    });
    items.sort(function(first, second) {
        return second[1] - first[1];
    });
    sorted_obj={}
    $.each(items, function(k, v) {
        use_key = v[0]
        use_value = v[1]
        sorted_obj[use_key] = use_value
    })
    return(sorted_obj)
}


let inputstr = searchQuery;
//remove contractions



inputstr = inputstr.split(/[\n\s()-]/);
//strip newlines and trailing punctuation, remove stop words, convert to lowercase
for(var key in cont.contractions)
{
    if (key == Stemmed)
    {
        Stemmed = cont.contractions[key];
    }
        
}

for (var i = 0; i < inputstr.length; i++)
{
var Stemmed = (natural.PorterStemmer.stem(inputstr[i]));
for(var key in cont.contractions)
{
    if (key == Stemmed)
    {
        Stemmed = cont.contractions[key];
    }
        
}
stemmed_search_terms[i] = Stemmed;
}

var stemmed_search_terms = {};
for(const term of inputstr){
  var stemmed = (natural.PorterStemmer.stem(term));
  stemmed_search_terms[stemmed]=term;//add stemming function here
}

var search_score_per_doc = {};
let res = {};
let multiplier = 0;
for(const [stemmed, term] of Object.entries(stemmed_search_terms)){
  res = mdb.findOne({"S_Word":term});//declare mdb
  for(const word of res){
    if(stemmed_search_terms[term]==word['Root']){
      multiplier = 2;
    }
    else{
      multiplier = 1;
    }
    if(word['Doc_name'] in search_score_per_doc){
      search_score_per_doc[word['Doc_name']]+=word['BM25_score']*multiplier
    }
    else{
      search_score_per_doc[word['Doc_name']]=word['BM25_score']*multiplier
    }
  }
}
search_score_per_doc = sorted_obj(search_score_per_doc);
return search_score_per_doc;