//1.Try Export any Collection and import it into new Collection using Mongo Robo 3T
use ITI_Mongo

use import_test
db.employee.find({})
db.employee.countDocuments()
db.sales.find({})
db.employees.find({})



//=================================================================================================================================================================================
use ITI_Mongo
db.employee.find({})

//=================================================================================================================================================================================
//2.Calculate the total revenue for product from sales collection documents within the date range '01-01-2020' to '01-01-2023' and then sort them in descending order by total revenue.
//a.Total Revenue=  Sum (Quantity * Price)
db.sales.find({})
db.sales.aggregate([
  {
    $match: { 
      date: { 
        $gte: ISODate('2020-01-01'), 
        $lte: ISODate('2023-01-01') 
      } 
    }
  },
  {
    $group: { 
      _id: "$product", 
      Total_Revenue: { 
        $sum: { 
          $multiply: ["$quantity", "$price"] 
        } 
      }
    }
  },
  {
    $sort: { Total_Revenue: -1 }
  }
])

//=================================================================================================================================================================================

//3.Try Query 2 using Robo 3T using aggregate wizard and insert result into new collection named “newColl”

const result = db.sales.aggregate([
  {
    $match: {
      date: {
        $gte: ISODate("2020-01-01T00:00:00Z"),
        $lte: ISODate("2023-01-01T00:00:00Z")
      }
    }
  },
  {
    $group: {
      _id: "$product",
      totalRevenue: {
        $sum: { $multiply: ["$quantity", "$price"] }
      }
    }
  },
  {
    $sort: { totalRevenue: -1 }
  }
]).toArray();

db.newColl.insertMany(result);
// out <<===
//=================================================================================================================================================================================

//4.Calculate the average salary for employees for each department from the employee’s collection.
db.employees.find({})
db.employees.aggregate([
  {
    $group: { 
      _id: "$department", 
      average_salary: { 
        $avg: "$salary"
      }
    }
  }
  
])
//=================================================================================================================================================================================

//5.Use likes Collection to calculate max and min likes per title
db.likes.find({})
db.likes.aggregate([
  {
    $group: { 
      _id: "$title", 
      max_likes : { 
        $max: "$likes"
      },
      min_likes : { 
        $min: "$likes"
      }
    }
  }
  
])
//=================================================================================================================================================================================

//6.Get inventory collection Count , countDocuments
db.inventory.find({})

db.inventory.count()

db.inventory.countDocuments()
//=================================================================================================================================================================================

//7.Display 5 documents only from inventory collection

db.inventory.find({})

db.inventory.find().limit(5)
//=================================================================================================================================================================================

//8.Count numbers of large Pizza size from orders collection  [using $count inside aggregate function]
db.orders.find({})

db.orders.aggregate([
        {
            $match :{ size : "large"}
        },
        {
            $count : 'largePizzaCount'
        }

])
//=================================================================================================================================================================================

//9.Create two collections in MongoDB that represent a manual relationship between students and their projects. Then retrieve related data using aggregation.
//Insert into students collection
db.students.insertMany([
  { _id: 1, name: "Ali", email: "ali@mail.com" },
  { _id: 2, name: "Sara", email: "sara@mail.com" }
])

//Insert into projects collection
db.projects.insertMany([
  { _id: 101, title: "AI Project", studentId: 1 },
  { _id: 102, title: "Web App", studentId: 2 }
])

//============================================================================================

db.projects.aggregate([
  {
    $lookup: {
      from: "students",
      localField: "studentId",
      foreignField: "_id",
      as: "studentInfo"
    }
  },
  {
    $unwind: "$studentInfo" 
  },
  {
    $project: {
      _id: 1,
      title: 1,
      studentName: "$studentInfo.name",
      studentEmail: "$studentInfo.email"
    }
  }
])




