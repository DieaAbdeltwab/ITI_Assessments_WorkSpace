//======================================================================================================================
db.trainningCenter2.find({ status: "active" }).forEach(function(n) {
  var fullName = n.name.firstName + " " + n.name.lastName;
  print(
    "-----------------------------------------\n" +
    "Name     : " + fullName + "\n"  +
    "Age      : " + n.age + "\n"     +
    "Address  : " + n.address + "\n" +
    "-----------------------------------------"
  )
})

//======================================================================================================================
//1.Create new Database named Demo And Collections named trainningCenter1, trainningCenter2 
use Demo
db.createCollection("trainningCenter1")
db.createCollection("trainningCenter2")


//2.Insert documents into trainningCenter1 collection contains (Use Variable named data as Array)
//_id , name as firstName lastName , age , address as array , status
//Using insert ONE from data Variable

// Step 1: Define the data array
var data = [
  {
    _id: 1,
    name: { firstName: "Ahmed", lastName: "Hassan" },
    age: 25,
    address: ["Cairo", "Nasr City", "Building 12"],
    status: "active"
  },
  {
    _id: 2,
    name: { firstName: "Sara", lastName: "Ali" },
    age: 30,
    address: ["Giza", "Dokki", "Street 10"],
    status: "inactive"
  },
  {
    _id: 5,
    name: { firstName: "Mohamed", lastName: "Ahmed" },
    age: 30,
    address: ["Giza", "Dokki", "Street 10"],
    status: "active"
  }
]

// Step 2: Insert ONE document from the array
db.trainningCenter1.insertOne(data)

db.trainningCenter1.find({})


//3.Using Same Variable (data) with same data and insert MANY into trainningCenter2 collection
db.trainningCenter2.insertMany(data);
db.trainningCenter2.find({})

//======================================================================================================================

//4.Use find. explain function (find by age field) and mention scanning type

db.trainningCenter1.find({ age: 25 }).explain()
//==>            "stage" : "COLLSCAN",


//5.Create index on created collection named it “IX_age” on age field 
db.trainningCenter1.createIndex(
  { age: 1 },                   
  { name: "IX_age" }            
)

db.trainningCenter1.getIndexes()


//6.Use find. explain view winning plan for index created (find by age field) and mention scanning type

db.trainningCenter1.find({ age: 25 }).explain()
//==>                 "stage" : "IXSCAN",

//********************************************************************
//7.Create index on created collection named it “compound” on firstNsme and lastName
//1.Try find().explain before create index and mention scanning type
db.trainningCenter1.find({
  "name.firstName": "Ahmed",
  "name.lastName": "Hassan"
}).explain()
//==>            "stage" : "COLLSCAN",
//********************************************************************
db.trainningCenter1.createIndex(
  { "name.firstName": 1, "name.lastName": 1 },
  { name: "compound" }
)
//********************************************************************
//2.Try find().explain after create index and mention scanning type

db.trainningCenter1.find({
  "name.firstName": "Ahmed",
  "name.lastName": "Hassan"
}).explain()
//==>                "stage" : "IXSCAN",
//********************************************************************
db.trainningCenter1.find({
  
  "name.lastName": "Hassan",
  "name.firstName": "Ahmed"
}).explain()
//==>                "stage" : "IXSCAN",
//********************************************************************
db.trainningCenter1.find({
  "name.firstName": "Ahmed"
}).explain()
//==>                "stage" : "IXSCAN",
//********************************************************************
db.trainningCenter1.find({
  "name.lastName": "Hassan"
}).explain()
//==>                "stage" : "COLLSCAN",
//********************************************************************

//======================================================================================================================

//8.Try to delete from your collection where _id = 5 [insert it if not exists]
db.trainningCenter1.deleteOne({ _id: 5 })
db.trainningCenter1.findOneAndDelete({ _id: 5 })

//9.Delete all documents from the trainingCenter collection.

db.trainningCenter1.deleteMany({})
db.trainningCenter2.deleteMany({})

//10.Drop the database and confirm its removal. Which command do you use to ensure the deletion?
db.dropDatabase();
show dbs
//======================================================================================================================
//11.Backup your Labs database (Mongo_ITI) 
//mongodump --db=ITI_Mongo --out=D:\Data\NOSQL\MongoDB_Day4


//12.Restore the taken back-up by new DB name Called Mongo_ITI_New

//mongorestore --db=Mongo_ITI --dir=D:\Data\NOSQL\MongoDB_Day4\ITI_Mongo



//======================================================================================================================

