"""
 ******************************************************************************
 * @file           : Pagination_Method_1 V1_0.py
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
            print("Enter List ! , In Init Object ")
            self.list_item = []
        try :
            self.num_in_page = abs(int(page_size))
        except ValueError:
                print("Enter Number ! , In Init Object ")
                self.num_in_page = 10
        self.currentPage = 0 

        # Key of this Method : 
        # Split self.list_item into Lists of size self.num_in_page
        self.temp = [self.list_item[i:i+self.num_in_page] for i in range(0, len(self.list_item), self.num_in_page)] 
    def get_visbale_items (self):
        try :
            self.currentlist = self.temp[self.currentPage] 
        except IndexError :
            print("We have Problem in Data ! , Reset Your program by Enter 0 and check data source ")
            self.currentPage = 0 
        else:
            print(self.currentlist)
    
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
    def first_page (self):
        self.currentPage = 0
        return self
    def last_page (self):
        self.currentPage = -1
        return self
    def go_to_page ( self , page_index = 1 ):
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
print("===================last and First=============================================")
alph_object.last_page().get_visbale_items()
alph_object.first_page().get_visbale_items()
alph_object.last_page().get_visbale_items()
print("======================go to page==========================================")
alph_object.go_to_page(-20).get_visbale_items()
alph_object.go_to_page(50).get_visbale_items()
alph_object.go_to_page(2).get_visbale_items()
alph_object.go_to_page(4).get_visbale_items()
print("================================================================")