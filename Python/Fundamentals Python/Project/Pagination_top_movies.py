import os
import work_with_files

def clear_terminal():
    # Check the OS name
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Linux and macOS
        os.system('clear')

top_movies = work_with_files.openfunc_json_file_reader("top_movies.json")

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
            print("+--------+------------+---------------------------+----------------+")
            print("|   ID   |    Genre   |         Movie Name        |   IMDB Rating  |")
            print("+--------+------------+---------------------------+----------------+")
            for  entry in self.currentlist :
                print(f"| {entry['ID']:5}  | {entry['Genre']:10} | {entry['Movie Name']:25} | {entry['IMDB Rating']:14} |")
        except IndexError :
            print("We have Problem in Data ! , Reset Your program by Enter 0 and check data source ")
            self.currentPage = 0 
        except KeyError :
                print("Check Data Format !!!! ")
        except TypeError :
                print("We have Problem in Data ! , Reset Your program by Enter 0 and check data source ")
        else :
            print("+--------+------------+---------------------------+----------------+")
            print("====================================================================")
            print("+--------+------------+------------------+--------+----------------+")
            print("+  Next  +  previous  +  Specific Page   +  First +  Last  +  exit +")
            print("+--------+------------+------------------+--------+----------------+")
            print("+    1   +      2     +         3        +    4   +    5   +    0  +")
            print("+--------+------------+------------------+--------+----------------+")
        
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
                self.currentPage = page_index -1 
        return self
            
    
    
    
    
movie_object = Pagination( top_movies ,7)
def menu_loop () :
    movie_object.get_visbale_items()
    while True :
        try :
            menu_key = int(input ("\n--> Choose : "))
            clear_terminal()
        except ValueError:
            print("Enter Valed input !")
        else :
            if 0== menu_key :
                break
            elif  1 == menu_key :
                movie_object.next_page().get_visbale_items()
            elif  2 == menu_key :
                movie_object.prev_page().get_visbale_items() 
            elif  3 == menu_key :
                try :
                    page_index=int(input("Enter Number of Page : "))
                except ValueError:
                    print("Enter Number !")
                else :
                    movie_object.go_to_page(page_index).get_visbale_items()
            elif  4 == menu_key :
                movie_object.first_page().get_visbale_items() 
            elif  5 == menu_key :
                movie_object.last_page().get_visbale_items() 
            else :
                print("Enter Valed Number !")

if __name__ == "__main__":
    menu_loop()
