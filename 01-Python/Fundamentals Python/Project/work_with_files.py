"""
? *****************************************************************************
 ? @file           : work_with_files.py
 ? @author         : Diea Abdeltwab
 ? @layer          : Service
 ? @brief          : V.1
 ? @date           : 19/4/2025
? *****************************************************************************
 ? @attention
 ?  I Created this file to make working with file easy and in one place
 ?  Data engineering ITI Course - Python fuduminal 
 ?  this file has a Functions Only 
? *****************************************************************************
"""
#******************************************************************************
#************************ LIB Layer *******************************************
#******************************************************************************
from   pathlib import Path
import json
from   json import JSONDecodeError
import csv
#******************************************************************************
#******************************************************************************
#******************************************************************************

#********************************************************************************************************************************************
#**************************************************** Functions *****************************************************************************
#********************************************************************************************************************************************

# ==================================================================================================================================
#============================================== Path library ======================================================================
#==================================================================================================================================
def pathlib_file_reader(file_path_name  ):
    path = Path(file_path_name) 
    file_content_report = ""
    try :
        file_content_report = path.read_text()
    except FileNotFoundError : # if file not found  
        print(f"Error: File '{file_path_name}' not found.")
        yes_no = input("Would you like to try again? (yes/no)")
        if yes_no == "yes" :
            file_path = input("Enter file name: ")
            file_content_report = file_reader(file_path)
        elif yes_no == "no"  :
            file_content_report =  f"Error: File '{file_path_name}' not found and you not like to try again"
        else :
            file_content_report  = f"Non Validation input , you should enter (yes/no) ,Stop playing !!"
    except IsADirectoryError : # if you try to read directory
        file_content_report = f"except : This Is a directory : {file_path_name} !! , i raed files "
    return file_content_report

def pathlib_file_writer(file_path_name , text_file ):
    path = Path(file_path_name) 
    report_action = ""
    try :
        path.write_text(text_file)
    except PermissionError : # if you dont have Permission to write in this file 
        report_action  = f"except : Error: Permission denied to write to {file_path_name}"
    except FileNotFoundError :  # if file not found  
        report_action  = f"\nexcept : No such directory by this name : {file_path_name}\n"
        report_action += f"except :  .write_text() method can creat file but can't creat directory "
    except IsADirectoryError : # if you try to write directory
        report_action = f"\nexcept : This Is a directory : {file_path_name} !! , i write in files"

    else :
        report_action  = f"\nData saved successfully to {file_path_name}\n"
        report_action += f"Contents of {file_path_name}\n"
        report_action += path.read_text()
        #report_action += file_reader(file_path_name))
    return report_action

def pathlib_file_json_writer(file_path_name , data_json ):
    try :
        data_json_temp = json.dumps(data_json)
        report_action  = file_write(file_path_name ,data_json_temp )
    except IOError : #genaral for Input/Output Error , Python 3: merge OSError
        report_action = "except : Input/Output Error !!" 
    return report_action
        
def pathlib_file_json_reader (file_path_name ):
    try :
        file_content_report = json.loads(file_reader(file_path_name))
    except IOError : #genaral for Input/Output Error , Python 3: merge OSError
        file_content_report = "except : Input/Output Error !!" 
    except JSONDecodeError : # Error in decode , any file should i write in it as Json file befor i read it as a Json
        file_content_report = "except : Sorry !! , i have problem in decode !" 
    return file_content_report
#==================================================================================================================================
#============================================== Open built-in function ============================================================
#==================================================================================================================================
def openfunc_file_writer( file_path_name , data):
    report_action = ""
    try :
        with open( file_path_name , "w") as file :
            file.write(data)
    except PermissionError : # if you dont have Permission to write in this file 
        report_action  = f"except : Error: Permission denied to write to {file_path_name}"
    except FileNotFoundError :  # if file not found  
        report_action  = f"\nexcept : No such directory by this name : {file_path_name}\n"
        report_action += f"except :  .write_text() method can creat file but can't creat directory "
    except IsADirectoryError : # if you try to write directory
        report_action = f"\nexcept : This Is a directory : {file_path_name} !! , i write in files"

    else :
        report_action  = f"\nData saved successfully to {file_path_name}\n"
        report_action += f"Contents of {file_path_name}\n"
    return report_action

def openfunc_file_appender ( file_path_name , data):
    report_action = ""
    try :
        with open( file_path_name , "a") as file :
            file.write(data)
    except PermissionError : # if you dont have Permission to write in this file 
        report_action  = f"except : Error: Permission denied to write to {file_path_name}"
    except FileNotFoundError :  # if file not found  
        report_action  = f"\nexcept : No such directory by this name : {file_path_name}\n"
        report_action += f"except :  .write_text() method can creat file but can't creat directory "
    except IsADirectoryError : # if you try to write directory
        report_action = f"\nexcept : This Is a directory : {file_path_name} !! , i write in files"

    else :
        report_action  = f"\nData saved successfully to {file_path_name}\n"
        report_action += f"Contents of {file_path_name}\n"
    return report_action

def openfunc_file_reader ( file_path_name ):
    file_content_report = ""
    try :
        with open( file_path_name , "r" ) as file :
            file_content_report =  json.loads(file.read())
    except FileNotFoundError : # if file not found  
        print(f"Error: File '{file_path_name}' not found.")
    except IsADirectoryError : # if you try to read directory
        file_content_report = f"except : This Is a directory : {file_path_name} !! , i raed files "
    return file_content_report

def openfunc_json_file_writer( file_path_name , data,  json_indent = 2):
    report_action = ""
    try :
        with open( file_path_name , "w") as file :
            dumps_data=json.dumps(data ,indent = json_indent)
            file.write(dumps_data)
    except PermissionError : # if you dont have Permission to write in this file 
        report_action  = f"except : Error: Permission denied to write to {file_path_name}"
    except FileNotFoundError :  # if file not found  
        report_action  = f"\nexcept : No such directory by this name : {file_path_name}\n"
        report_action += f"except :  .write_text() method can creat file but can't creat directory "
    except IsADirectoryError : # if you try to write directory
        report_action = f"\nexcept : This Is a directory : {file_path_name} !! , i write in files"
    except IOError : #genaral for Input/Output Error , Python 3: merge OSError
        report_action = "except : Input/Output Error !!"
    else :
        report_action  = f"\nData saved successfully to {file_path_name}\n"
        report_action += f"Contents of {file_path_name}\n"
    return report_action


def openfunc_json_file_appender ( file_path_name , data , json_indent = 2 ):
    report_action = ""
    try :
        with open( file_path_name , "a") as file :
            dumps_data=json.dumps(data , indent = json_indent )
            file.write(dumps_data)
    except PermissionError : # if you dont have Permission to write in this file 
        report_action  = f"except : Error: Permission denied to write to {file_path_name}"
    except FileNotFoundError :  # if file not found  
        report_action  = f"\nexcept : No such directory by this name : {file_path_name}\n"
        report_action += f"except :  .write_text() method can creat file but can't creat directory "
    except IsADirectoryError : # if you try to write directory
        report_action = f"\nexcept : This Is a directory : {file_path_name} !! , i write in files"
    except IOError : #genaral for Input/Output Error , Python 3: merge OSError
        report_action = "except : Input/Output Error !!"
    else :
        report_action  = f"\nData saved successfully to {file_path_name}\n"
        report_action += f"Contents of {file_path_name}\n"
    return report_action

def openfunc_json_file_reader ( file_path_name ):
    file_content_report = ""
    try :
        with open( file_path_name , "r" ) as file :
            file_content_report =  json.loads(file.read())
    except FileNotFoundError : # if file not found  
        print(f"Error: File '{file_path_name}' not found.")
    except IsADirectoryError : # if you try to read directory
        file_content_report = f"except : This Is a directory : {file_path_name} !! , i raed files "
    except IOError : #genaral for Input/Output Error , Python 3: merge OSError
        file_content_report = "except : Input/Output Error !!" 
    except JSONDecodeError : # Error in decode , any file should i write in it as Json file befor i read it as a Json
        file_content_report = "except : Sorry !! , i have problem in decode !"
    return file_content_report
def openfunc_csv_file_writer( file_path_name , field_names , list_dict ,csv_delimiter =',' ):
    report_action = ""
    try :
        with open( file_path_name ,"w", newline='' ) as csvfile :
            csv_writer = csv.DictWriter(csvfile,fieldnames=field_names,delimiter = csv_delimiter)
            csv_writer.writeheader()
            for dict_row in list_dict :
                csv_writer.writerow(dict_row)

    except PermissionError : # if you dont have Permission to write in this file 
        report_action  = f"except : Error: Permission denied to write to {file_path_name}"
    except FileNotFoundError :  # if file not found  
        report_action  = f"\nexcept : No such directory by this name : {file_path_name}\n"
        report_action += f"except :  .write_text() method can creat file but can't creat directory "
    except IsADirectoryError : # if you try to write directory
        report_action = f"\nexcept : This Is a directory : {file_path_name} !! , i write in files"

    except TypeError :
        report_action = f"\ndelimiter must be a 1-character string"
    else :
        report_action  = f"\nData saved successfully to {file_path_name}\n"
        report_action += f"Contents of {file_path_name}\n"
    return report_action

def openfunc_csv_file_reader ( file_path_name  ,csv_delimiter =',' ):
    file_list_dict_report = []
    try :
        with open( file_path_name , newline='' ) as csvfile :
            dict_read =  csv.DictReader(csvfile ,delimiter = csv_delimiter )
            for dict_row in dict_read :
                file_list_dict_report.append(dict_row)

    except FileNotFoundError : # if file not found  
        print(f"Error: File '{file_path_name}' not found.")
    except IsADirectoryError : # if you try to read directory
        file_list_dict_report = f"except : This Is a directory : {file_path_name} !! , i raed files "
    return file_list_dict_report

def openfunc_csv_header(file_path_name):
    with open(file_path_name, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        return header
#==================================================================================================================================
#==================================================================================================================================
#==================================================================================================================================

#********************************************************************************************************************************************
#********************************************************************************************************************************************
#********************************************************************************************************************************************

