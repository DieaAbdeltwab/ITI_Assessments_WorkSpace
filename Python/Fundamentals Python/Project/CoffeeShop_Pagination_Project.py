"""
? *****************************************************************************
 ? @file           : CoffeeShop_Pagination_Project.py
 ? @author         : Diea Abdeltwab
 ? @layer          : Service
 ? @brief          : V.1
 ? @date           : 20/4/2025
? *****************************************************************************
 ? @attention
 ?  Data engineering ITI Course - Python fuduminal 
 ?  This File is a Practise for all Python fuduminal course
 ?  It is In Integration for (Coffee Shop , Pagination )  
? *****************************************************************************
 ?  this File Used Two another Files :
 ?  work_with_files.py -> I created it to work with files (json , csv ,txt )
 ?  python_coffee_products.csv -> has products of coffee 
 ?                                delimitar  = ','   
 ?                                fieldnames = ["id","item","type","price"]                        
? *****************************************************************************
"""
#******************************************************************************
#************************ LIB Layer *******************************************
#******************************************************************************
import os 
#******************************************************************************
#************************ Service Layer ***************************************
#******************************************************************************
import work_with_files
#******************************************************************************
#******************************************************************************
#******************************************************************************

#********************************************************************************************************************************************
#********************************************************************************************************************************************
#********************************************************************************************************************************************
def print_gui_header():
        print("+------+--------------------------+---------+-------+")
        print("| ID   |            item          |   type  | price |")
        print("+------+--------------------------+---------+-------+")  
def print_gui_tail():
        print("+------+--------------------------+---------+-------+")
#********************************************************************************************************************************************
#**************************************************** Class *********************************************************************************
#********************************************************************************************************************************************

class Pagination :
    def __init__ (self , list_item  : list , pageSize = 10 ):
        self.list_item   = list_item
        try :
            self.num_in_page = abs(int(pageSize))
        except ValueError:
                print("Enter Number ! , in Init ")
                self.num_in_page = 10

        self.currentPage = 0 
        self.temp = [self.list_item[i:i+self.num_in_page] for i in range(0, len(self.list_item), self.num_in_page)]
    def get_visbale_items (self):
        try :
            self.currentlist = self.temp[self.currentPage] 
            print_gui_header()
            for  item in self.currentlist :
                print(f"| {item['id']:4} | {item['item']:24} | {item['type']:7} | {item['price']:5} | ")
            print_gui_tail()
        except IndexError :
            print("We have Problem in Data ! , Reset Your program by Enter 0 and check data source ")
            self.currentPage = 0 
        except KeyError :
                print("Check Data Format !!!! ")
        except TypeError :
                print("We have Problem in Data ! , Reset Your program by Enter 0 and check data source ")
            
        
    def next_page (self):
        if self.currentPage >= (len(self.temp)-1) :
            self.currentPage = 0 
        else :
            self.currentPage += 1
        return self
    def prev_page (self):
        if abs(self.currentPage) >= len(self.temp) :
            self.currentPage = -1 
        else :
            self.currentPage -= 1
        return self
        return self
    def first_page (self):
        self.currentPage = 0
        return self
    def last_page (self):
        self.currentPage = -1
        return self
    def go_to_page ( self , page_index ):
        try :
            page_index = int(page_index)
        except ValueError:
                print("Enter Number !")
        else :
            if page_index > (len(self.temp)-1) :
                self.currentPage = -1
            elif page_index <= 0 :       
                self.currentPage = 0
            else :
                self.currentPage = page_index - 1
        return self
            
    

class CoffeeShop : 
    def __init__(self , name , menu , orders ) :
        self.name = name
        if isinstance (menu,list) and isinstance (orders,list)  :
            self.menu = menu
            self.orders = orders        
        else :
            self.menu =[]
            self.orders=[]
        self.due_amount_value = []
    
 
    def print_orders(self):
        print_gui_header()   
        for item_str in self.orders :
            try :
                for item in self.menu :
                    if item['item'] == item_str :
                        print(f"| {item['id']:4} | {item['item']:24} | {item['type']:7} | {item['price']:5} | ")
            except KeyError :
                pass
            except AttributeError :
                pass
        print_gui_tail()  
        print(f"+------+--------------------------+---------+{sum(self.due_amount_value):5.2f}  +")
        print_gui_tail() 
    
    def add_order(self , name_item ):
        add_order_report = "This item is currently unavailable!" 
        srting_format = 30
        for menu_dic in self.menu :
            try : 
                if name_item == menu_dic["item"]  :
                    add_order_report = "Order Added !"
                    self.orders.append(name_item)
                    self.due_amount_value.append( float(menu_dic["price"])) 
                    break
            except KeyError :
                pass
            except AttributeError :
                pass
                
        print("+=====================================================================================+")
        print(f"+                             {add_order_report:40}                +")  
        print("+=====================================================================================+")
        
    
    def fulfill_order(self) :
        try :
            fifo_item = self.orders.pop(0)
            self.due_amount_value.pop(0)
        except IndexError :
            print("+=====================================================================================+")
            print("+                          All orders have been fulfilled!                            +")  
            print("+=====================================================================================+")


        else :
            print("+=====================================================================================+")
            print(f"+                             The {fifo_item:15}is ready!                            +")  
            print("+=====================================================================================+")
        
    
    def print_cheapest_item(self):
        value_cheapest_item = [self.menu[0]]
        value_cheapest = float(self.menu[0]["price"])
        for item in self.menu :
            try :
                if float(item["price"]) <  value_cheapest :
                    value_cheapest = float(item["price"])
                    value_cheapest_item.clear()
                    value_cheapest_item.append(item)
                elif float(item["price"]) ==  value_cheapest :
                    value_cheapest_item.append(item)

            except KeyError :
                pass
        print_gui_header()   
        for counter in range(len(value_cheapest_item)) :   
            print(f"| {value_cheapest_item[counter]['id']:4} | {value_cheapest_item[counter]['item']:24} | {value_cheapest_item[counter]['type']:7} | {value_cheapest_item[counter]['price']:5} | ")
        print_gui_tail()         

    def print_drinks_only(self):
        print_gui_header()         
        for item in self.menu :
            try :
                if item["type"] == "drink" :
                    print(f"| {item['id']:4} | {item['item']:24} | {item['type']:7} | {item['price']:5} | ")
            except KeyError :
                pass
            except AttributeError :
                pass
        print_gui_tail()         
        
    def print_food_only(self):
        print_gui_header()        
        for item in self.menu :
            try :
                if item["type"] == "food" :
                    print(f"| {item['id']:4} | {item['item']:24} | {item['type']:7} | {item['price']:5} | ")
            except KeyError :
                pass
            except AttributeError :
                pass
        print_gui_tail()         
     
#********************************************************************************************************************************************
#**************************************************** Variables *****************************************************************************
#********************************************************************************************************************************************               
python_coffee_products = work_with_files.openfunc_csv_file_reader("python_coffee_products.csv")
coffee_object = Pagination( python_coffee_products )
orders_list = []
python_coffee = CoffeeShop( "Python Coffee Shop", python_coffee_products ,orders_list  )

#********************************************************************************************************************************************
#**************************************************** Functions *****************************************************************************
#********************************************************************************************************************************************
def clear_screen():
    if os.name == 'posix':  # For Linux and macOS
        os.system('clear')
    elif os.name == 'nt':  # For Windows
        os.system('cls')
def menu_loop () :
    coffee_object.get_visbale_items()
    while True :
        print("======================================================================")
        print("+--------+------------+------------------+--------+--------+---------+")
        print("+  Next  +  previous  +  Specific Page   +  First +  Last  +   Back  +")
        print("+--------+------------+------------------+--------+--------+---------+")
        print("+    1   +      2     +         3        +    4   +    5   +     0   +")
        print("+--------+------------+------------------+--------+--------+---------+")
        try :
            menu_key = int(input ("\n--> Choose : "))
        except ValueError:
            print("Enter Valed input !")
        else :
            if 0== menu_key :
                break
            elif  1 == menu_key :
                clear_screen()
                coffee_object.next_page().get_visbale_items()
            elif  2 == menu_key :
                clear_screen()
                coffee_object.prev_page().get_visbale_items() 
            elif  3 == menu_key :
                try :
                    page_index=int(input("Enter Number of Page : "))
                except ValueError:
                    print("Enter Number !")
                else :
                    clear_screen()
                    coffee_object.go_to_page(page_index).get_visbale_items()
            elif  4 == menu_key :
                clear_screen()
                coffee_object.first_page().get_visbale_items() 
            elif  5 == menu_key :
                clear_screen()
                coffee_object.last_page().get_visbale_items() 
            else :
                print("Enter Valed Number !")


def main_loop () :
    while True :
        print("+==============================================================================================+")
        print("+------+--------+-----------+---------------+---------------+-------------+-----------+--------+")
        print("+ Menu + Orders + Add order + Fulfill order + Cheapest item + Drinks only + Food only +  exit  +")
        print("+------+--------+-----------+---------------+---------------+-------------+-----------+--------+")
        print("+   1  +   2    +      3    +       4       +       5       +      6      +     7     +    0   +")
        print("+------+--------+-----------+---------------+---------------+-------------+-----------+--------+")
        try :
            menu_key = int(input ("\n--> Choose : "))
        except ValueError:
            print("Enter Valed input !")
        else :
            if 0 == menu_key :
                print("+=====================================================================================+")
                print("+                          GoodBye....                                                +")  
                print("+=====================================================================================+")
                break
            elif 1 == menu_key :
                clear_screen()
                menu_loop()
            elif 2 == menu_key :
                clear_screen()
                python_coffee.print_orders()
            elif 3 == menu_key :
                order_name = input("-->Enter Order Name : ")
                clear_screen()
                python_coffee.add_order(order_name)
            elif 4 == menu_key :
                clear_screen()
                python_coffee.fulfill_order()
            elif 5 == menu_key :
                clear_screen()
                python_coffee.print_cheapest_item()
            elif 6 == menu_key :
                clear_screen()
                python_coffee.print_drinks_only()
            elif 7 == menu_key :
                clear_screen()
                python_coffee.print_food_only()
            else :
                print("Enter Valed Number !")

#********************************************************************************************************************************************
#**************************************************** Start Point ***************************************************************************
#********************************************************************************************************************************************
main_loop()
#********************************************************************************************************************************************
#********************************************************************************************************************************************
#********************************************************************************************************************************************

