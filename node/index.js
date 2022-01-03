const { MongoClient } = require('mongodb');
var sw = require('stopword');
var natural = require('natural');


const uri = " mongodb://localhost:27017/";

const client = new MongoClient(uri);
client.connect();
const db = client.db("Wiki-SE");

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


let inputstring = "iron man is";
inputstring = inputstring.split(/[\n\s()-]/);
inputstr = sw.removeStopwords(inputstring);

var stemmed;
var stemmed_search_terms = {};
for(const term of inputstr){
  stemmed = (natural.PorterStemmer.stem(term));
  stemmed_search_terms[stemmed]=term;
}

var search_score_per_doc = {};
let res = {};
let multiplier = 0;
for(const [stemmed, term] of Object.entries(stemmed_search_terms)){
  db.collection('Content').findOne({"S_Word":term})
   .then(function(res) {
          if(res){
          for(const word of res['Tree']){
            if(stemmed_search_terms[term]==word['Root']){
              multiplier = 2;
            }
            else{
              multiplier = 1;
            }
            if(word['Doc_name'] in search_score_per_doc){
              search_score_per_doc[word['Doc_name']]+=word['BM25_score']*multiplier;
            }
            else{
              search_score_per_doc[word['Doc_name']]=word['BM25_score']*multiplier;
            }
          }
        }
        var items = Object.keys(search_score_per_doc).map(function(key) {
          return [key, search_score_per_doc[key]];
        });

        items.sort(function(first, second) {
          return second[1] - first[1];
        });
        console.log("OUTPUT:", items);
    });
}

//search_score_per_doc = sort_object(search_score_per_doc);
/*let res_dict = {}
for(const [doc, score] of Object.entries(stemmed_search_terms)){
  res_dict[doc]=mdoc.findOne({"Title":doc})['Preview']
}

console.log(res_dict)
*/
