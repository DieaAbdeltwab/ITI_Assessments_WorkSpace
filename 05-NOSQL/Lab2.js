use ITI_Mongo

//1.Find documents where the "tags" field exists.

db.inventory.find({ tags: { $exists: true } })

//2.Find documents where the "tags" field does not contain values "ssl" or "security."

db.inventory.find({ tags:  { $nin: ["ssl", "security"]} })

db.inventory.find({ tags:  { $exists: true , $nin: ["ssl", "security"]} })

//3.Find documents where the "qty" field is equal to 85.
db.inventory.find({ qty: 85  })
db.inventory.find({ qty:  {$eq: 85 } })

//4.Find documents where the "tags" array contains all of the values [ssl, security] using the `$all` operator.

db.inventory.find({ tags:  { $all: ["ssl", "security"]} })

// $all: ["ssl", "security" , + ,,,,]

//5.Find documents where the "tags" array has a size of 3.

db.inventory.find({tags : {$size : 3 } })


//=======================================================================================================================
db.inventory.find({ item: "paper" })

//6.Update the "item" field in the "paper" document, setting "size.uom" to "meter" and using the `$currentDate` operator.
    //a.Also, use the upsert option and change filter condition item:”paper”.
    db.inventory.updateOne(
      { item: "paper" },
      {
        $set: { "size.uom": "meter" },
        $currentDate: { lastModified: true },
        $setOnInsert: { note :"data comes from Upsert" }
      },
      { upsert: true }
    )
    
    //b.Use the `$setOnInsert` operator.
     db.inventory.updateMany(
      { item: "paper" },
      {
        $set: { "size.uom": "meter" },
        $currentDate: { lastModified: true },
        $setOnInsert: { note :"data comes from Upsert" }
      },
      { upsert: true }
    )
    //c.Try `updateOne`, `updateMany`, and `replaceOne`.
    db.inventory.replaceOne(
      { item: "paper" },
      {
        item: "paper",
        size: { uom: "meter" },
        lastModified: new Date(),
      },
      { upsert: true }
    )

    
    
//7.Insert a document with incorrect field names "neme" and "ege," then rename them to "name" and "age."
db.inventory.insertOne({
  neme: "Diea",
  ege: 24,
})

db.inventory.updateOne(
  { neme: "Diea" },
  {
    $rename: {
      "neme": "name",
      "ege": "age"
    }
  }
)
db.inventory.find({ name: "Diea" })

//8.Try to reset any document field using the `$unset` function.

db.inventory.updateOne(
  { item: "paper" },
  {
    $unset: {
      "qty": ""
    }
  }
)
db.inventory.find({  item: "paper" })


//9.Try update operators like `$inc`, `$min`, `$max`, and `$mul` to modify document fields.



    //Use $max on the field: salary
    db.inventory.updateOne(
      { item: "paper" },
      {
        $max: { salary: 6000 }
      }
    )
    db.inventory.find({  item: "paper" })
    
    //Use $min on the field: overtime  
    db.inventory.updateOne(
      { item: "paper" },
      {
        $min: { overtime: 5 }
      }
    )
    db.inventory.find({  item: "paper" })
    
    //Use $inc on the field: age
    db.inventory.updateOne(
      { item: "paper" },
      {
        $inc: { age: 1 }
      }
    )
    db.inventory.find({  item: "paper" })
    
    //Use $mul on the fields: quantity and price
    db.inventory.updateOne(
      { item: "paper" },
      {
        $mul: {
          quantity: 2,
          price: 1.5
        }
      }
    )
    db.inventory.find({  item: "paper" })
    
    
    
//10.Provide the MongoDB code for enforcing JSON schema validation when creating a collection named 
//"employees" with required fields "name," "age" (min. 18), and "department" (limited to ["HR," "Engineering," "Finance"]).
db.createCollection("employeees", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "age", "department"],
      properties: {
        name: {
          bsonType: "string",
          description: "must be a string and is required"
        },
        age: {
          bsonType: "int",
          minimum: 18,
          description: "must be an integer and at least 18"
        },
        department: {
          enum: ["HR", "Engineering", "Finance"],
          description: "must be one of: HR, Engineering, Finance"
        }
      }
    }
  }
})


db.employeees.insertOne({
  name: "Ali",
  age: 28,
  department: "HR"
})

db.employeees.insertOne({
  name: "Salma",
  age: 35,
  department: "Engineering"
})

//----------------------------------
db.employeees.find({ })

//---------------------
db.employeees.insertOne({
  name: "Omar",
  age: 17,
  department: "Marketing"
})