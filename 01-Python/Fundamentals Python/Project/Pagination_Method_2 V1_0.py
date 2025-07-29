"""
 ******************************************************************************
 * @file           : Pagination_Method_2 V1_0.py
 * @author         : Diea Abdeltwab
 * @layer          : Service
 * @brief          : V.1
 * @date           : 17/4/2025
 ******************************************************************************
 * @attention
 *  
 *  Data engineering ITI Course - Python fuduminal -> Lab6 - Q1
 *  
 *  This File is Stop 1 for Python fuduminal Project (CoffeeShop_Pagination_Project.py)
 *  
 ******************************************************************************
"""
class Pagination :
    def __init__ (self , list_item = [] , page_size = 10 ):
        if isinstance(list_item, list) :
            self.list_item   = list_item
        else : 
            print("Enter List !, In Init Object ")
            self.list_item = []
        try :
            self.num_in_page = abs(int(page_size))
        except ValueError:
                print("Enter Number !, In Init Object ")
                self.num_in_page = 10
                
        self.start_point = 0 
        self.end_point   = self.num_in_page 
        
    def get_visbale_items (self):
        # Key of this Method : 
        # Slicing is safe even if end_point > len(list); it stops at the last item
        # Handle start_point manually, while end_point is determined dynamically based on start_point and num_in_page.
        list_temp = self.list_item[self.start_point : self.end_point ]  
        print(list_temp)                                                
    
    def next_page (self):
        self.start_point += self.num_in_page
        if self.start_point > len(self.list_item) - 1  : 
            self.start_point = 0
        self.end_point    = self.num_in_page + self.start_point
        return self
    def prev_page (self):
        self.start_point -= self.num_in_page
        if  self.start_point < 0 : 
            if  len(self.list_item) % self.num_in_page  :
                self.start_point = len(self.list_item) - (len(self.list_item) % self.num_in_page)
            else :
                self.start_point = len(self.list_item) -  self.num_in_page
        self.end_point    = self.num_in_page + self.start_point
        return self
    

    def last_page (self):
        if  len(self.list_item) % self.num_in_page  :
            self.start_point = len(self.list_item) - (len(self.list_item) % self.num_in_page)
        else :
            self.start_point = len(self.list_item) -  self.num_in_page
        self.end_point    = self.num_in_page + self.start_point
        return self
    def first_page (self):
        self.start_point = 0 
        self.end_point   = self.num_in_page 
        return self
    def go_to_page ( self , page_index = 1 ):
        try :
            page_index = int(page_index)
        except ValueError:
                print("Enter Number !")
        else :
            if  page_index > ((len(self.list_item) // self.num_in_page) ) :
                self.last_page()
            elif  page_index <= 0 :
                self.first_page()
            else :
                self.start_point = self.num_in_page * (page_index - 1 )
                self.end_point   = self.num_in_page + self.start_point 
        return self
       

    
    
    
    
alph = list("abcdefghijklmnopqrstuvwxyz")
#alph = list("123456789")

alph_object = Pagination(alph , 4 )

print("================================================================")
alph_object.get_visbale_items()
print("=======================next_page================================")
alph_object.next_page().get_visbale_items()
alph_object.next_page().get_visbale_items()
alph_object.next_page().get_visbale_items()
alph_object.next_page().get_visbale_items()
alph_object.next_page().get_visbale_items()
alph_object.next_page().get_visbale_items()
alph_object.next_page().get_visbale_items()
alph_object.next_page().get_visbale_items()
alph_object.next_page().get_visbale_items()
alph_object.next_page().get_visbale_items()
alph_object.next_page().get_visbale_items()
alph_object.next_page().get_visbale_items()
alph_object.next_page().get_visbale_items()
print("===================prev_page====================================")
alph_object.prev_page().get_visbale_items()
alph_object.prev_page().get_visbale_items()
alph_object.prev_page().get_visbale_items()
alph_object.prev_page().get_visbale_items()
alph_object.prev_page().get_visbale_items()
alph_object.prev_page().get_visbale_items()
alph_object.prev_page().get_visbale_items()
alph_object.prev_page().get_visbale_items()
alph_object.prev_page().get_visbale_items()
alph_object.prev_page().get_visbale_items()
alph_object.prev_page().get_visbale_items()
print("===================last and First================================")
alph_object.last_page().get_visbale_items()
alph_object.first_page().get_visbale_items()
alph_object.last_page().get_visbale_items()
print("======================go to page=================================")
alph_object.go_to_page(-20).get_visbale_items()
alph_object.go_to_page(50).get_visbale_items()
alph_object.go_to_page(2).get_visbale_items()
alph_object.go_to_page(4).get_visbale_items()
print("=================================================================")
