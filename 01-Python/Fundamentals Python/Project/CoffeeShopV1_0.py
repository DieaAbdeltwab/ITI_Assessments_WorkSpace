"""
 ******************************************************************************
 * @file           : CoffeeShop V1_0.py
 * @author         : Diea Abdeltwab
 * @layer          : Service
 * @brief          : V.1
 * @date           : 17/4/2025
 ******************************************************************************
 * @attention
 *  
 *  Data engineering ITI Course - Python fuduminal -> Lab6 - Q2
 *  
 *  This File is Stop 2 for Python fuduminal Project (CoffeeShop_Pagination_Project.py)
 *  
 ******************************************************************************
"""
class CoffeeShop : 
    def __init__(self , name , menu , orders ) :
        self.name = name
        if isinstance (menu,list) and isinstance (orders,list)  :
            self.menu = menu
            self.orders = orders        
        else :
            print("your DataBase Menu Must be List !")
            self.menu =[]
            self.orders=[]
        self.due_amount_value = []
    
    
    def add_order(self , item_name = "" ):
        add_order_report ="This item is currently unavailable!"
        for menu_dic in self.menu :
            try : 
                if item_name == menu_dic["item"] :
                    if  isinstance( menu_dic["price"], (int, float)) :
                        add_order_report = "Order Added !"
                        self.orders.append(item_name)
                        self.due_amount_value.append( menu_dic["price"]) 
                        break
                    else :
                        add_order_report = f"We have Problen in  Our Data base check if {item_name} prise is Number !! "
            except KeyError :
                add_order_report = "Check Data keys Format !!"
            except AttributeError :
                add_order_report = "Check Data keys Format !!"

        return  add_order_report  
        
    def list_orders(self):
        return self.orders
        
    def due_amount(self) :
        try :
            sum_value =  sum(self.due_amount_value)
        except TypeError :
            sum_value = "We have Problen in  Our Data base check if all prise is Number !!"
        return sum_value
    
    def fulfill_order(self) :
        try :
            fifo_item = self.orders.pop(0)
            fifo_amount_item = self.due_amount_value.pop(0)
        except IndexError :
            fifo_item =  "All orders have been fulfilled!"  
        else :
            fifo_item = f"The {fifo_item} is ready! , Pay the money : {fifo_amount_item}"
        return  fifo_item
    
    
    def cheapest_item(self):
        value_cheapest_item = [self.menu[0]]
        value_cheapest = self.menu[0]["price"]
        for item in self.menu :
            try :
                if item["price"] <  value_cheapest :
                    value_cheapest = item["price"]
                    value_cheapest_item.clear()
                    value_cheapest_item.append(item['item'])
                elif float(item["price"]) ==  value_cheapest :
                    value_cheapest_item.append(item['item'])
            except KeyError :
                value_cheapest_item = "Check Data keys Format !!"   
        return value_cheapest_item

    def drinks_only(self):
        drinks_list =[]
        for item in self.menu :
            try :
                if item["type"] == "drink" :
                    drinks_list.append(item["item"])
            except KeyError :
                pass
            except AttributeError :
                pass
        return drinks_list        

    def food_only(self):
        foods_list =[]
        for item in self.menu :
            try :
                if item["type"] == "food" :
                    foods_list.append(item["item"])
            except KeyError :
                pass
            except AttributeError :
                pass
        return foods_list

                
coffee_products = [
    {"item": "Cheeseburger", "type": "food", "price": 5.99},
    {"item": "French Fries", "type": "food", "price": 2.99},
    {"item": "Grilled Chicken Sandwich", "type": "food", "price": 6.75},
    {"item": "Veggie Wrap", "type": "food", "price": 5.25},
    {"item": "Lemonade", "type": "drink", "price": 1.00},
    {"item": "Iced Tea", "type": "drink", "price": 1.99},
    {"item": "Caesar Salad", "type": "food", "price": 4.50},
    {"item": "Coffee", "type": "drink", "price": 1.0},
    {"item": "Smoothie", "type": "drink", "price": 3.75},
    {"item": "Water Bottle", "type": "drink", "price": 1.50}
]
orders_list = []


coffee_object = CoffeeShop( "Diea",coffee_products,orders_list  )
print("============================================================================================================")
print(f"cheapest item : {coffee_object.cheapest_item()}")
print(f"drinks only   : {coffee_object.drinks_only()}")
print(f"food only     : {coffee_object.food_only()}")
print("============================================================================================================")
print(f"{coffee_object.add_order("Cheeseburger")}")
print(f"{coffee_object.add_order("Ice")}")
print(f"{coffee_object.add_order("Iced Tea")}")
print(f"{coffee_object.add_order("Smoothie")}")
print("======================================================================")
print(f"orders        : {coffee_object.list_orders()}")
print(f"due amount    :{coffee_object.due_amount()}")
print("======================================================================")
print(f"fulfill order : {coffee_object.fulfill_order()}")
print(f"orders        : {coffee_object.list_orders()}")
print(f"due amount    : {coffee_object.due_amount()}")
print("======================================================================")
print(f"fulfill order : {coffee_object.fulfill_order()}")
print(f"orders        : {coffee_object.list_orders()}")
print(f"due amount    : {coffee_object.due_amount()}")
print("======================================================================")
print(f"fulfill order : {coffee_object.fulfill_order()}")
print(f"orders        : {coffee_object.list_orders()}")
print(f"due amount    : {coffee_object.due_amount()}")
print("======================================================================")




