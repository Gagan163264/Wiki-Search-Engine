var express= require('express')
var MongoClient= require('mongodb').MongoClient;
var router= express.Router();

router.get("/",function(req,res){ //GET/student
    MongoClient.connect("mongodb://localhost:27017",{
        useUnifiedTopology:true
    },function(err,client){
        if (err) throw err;
        const db= client.db('newdb')
        db.collection('books.collection').find(req.query).toArray(function(err,objs){
            res.send(objs)
        })
    })
})

router.get("/:id",function(req,res){ //GET/student/PES1234
    MongoClient.connect("mongodb://localhost:27017",{
        useUnifiedTopology:true
    },function(err,client){
        if (err) throw err;
        const db= client.db('newdb')
        db.collection('books.collection').findOne({book_id:parseInt(req.params.id)},function(err,objs){
            res.send(objs)
        })
    })
})

router.post("/",function(req,res){ 
    //POST/student message body{srn="PES67878", name:"abc"}
    MongoClient.connect("mongodb://localhost:27017",{
        useUnifiedTopology:true
    },function(err,client){
        if (err) throw err;
        const db= client.db('newdb')
        db.collection('books.collection').insert(req.body,function(err,objs){
            res.send("Save Succesfull!!!")
        })
    })
})

router.put("/:price",function(req,res){ 
    //PUT/student/PES1234 message body-{srn="",hostel:"yes"}
    MongoClient.connect("mongodb://localhost:27017",{
        useUnifiedTopology:true
    },function(err,client){
        if (err) throw err;
        const db= client.db('newdb')
        db.collection('books.collection').update({book_price:req.params.price}, { $set: req.body },{ new: true, upsert: true, returnOriginal: false },function(err,objs){
            res.send("Update Succesfull!!!")
        })
    })
});

module.exports=router

var fetch=require("node-fetch");
var newd={
    "book_id":3,
    "book_name":"death of the nile",
    "book_price":"1500",
    "book_author":"Agatha Christie"
}
fetch("http://localhost:3000/book",{
    method:"POST",
    body: JSON.stringify(newd),
    headers:{'content-type':'application/json'}
}).then(res=>res.json)
  .then(json=>console.log(json))
var fetch=require("node-fetch");
var newd={
    "book_id":3,
    "book_name":"death of the nile",
    "book_price":"11100",
    "book_author":"Agatha Christie"
}
fetch("http://localhost:3000/book/1500",{
    method:"PUT",
    body: JSON.stringify(newd),
    headers:{'content-type':'application/json'}
}).then(res=>res.json)
  .then(json=>console.log(json))

  var express= require('express');
  var https=require('https');
var http = require('http');
var app=express();
var MongoClient=require("mongodb").MongoClient;
var bodyParse= require("body-parser")
app.use(bodyParse.json());
var studrouter= require("./student.js")
app.use("/book",studrouter)
app.listen(3000,function(){
    console.log("Serve is up and running")
})

var express=require("express")

var app= express()
var fileupload= require("express-fileupload")
app.use(fileupload());
app.post('/upload',function(req,res){
    if(!req.files||req.files.length==0)
    return res.status(400).send("No file to upload")
    var sampleFile= req.files.sampleFile;
    sampleFile.mv("./files/"+sampleFile.name,function(err){
        if(err)
        return req.statusCode(500).send(err)
        res.send("File"+sampleFile.name+"Uploaded")
    })
})
app.get("/form",function(req,res){
    var retform="<form action='http://localhost:4000/upload' method='post' encType='multipart/form-data'><input type='file' name='sampleFile'/> <input type='submit' value='upload'/></form>";
    res.send(retform)
    })
app.listen(4000,function(){
    console.log("Server is up and running")
})


