import string as STR
from colorama import Fore, Style, init as coloramaInit

import os
import shutil

coloramaInit()




class Colors:
    """
    A utility class for styling text with color using the colorama library.

    Provides static methods to return text wrapped in ANSI escape codes for specific colors.
    """
    GREEN_STYLE = Fore.LIGHTGREEN_EX + "{}" + Style.RESET_ALL
    RED_STYLE = Fore.LIGHTRED_EX + "{}" + Style.RESET_ALL
    YELLOW_STYLE = Fore.LIGHTYELLOW_EX + "{}" + Style.RESET_ALL

    @staticmethod
    def green_text(text):
        if not isinstance(text, str):
            raise TypeError("The 'text' parameter must be a string.")
        return Colors.GREEN_STYLE.format(text)

    @staticmethod
    def red_text(text):
        if not isinstance(text, str):
            raise TypeError("The 'text' parameter must be a string.")
        return Colors.RED_STYLE.format(text)

    @staticmethod
    def yellow_bright(text):
        if not isinstance(text, str):
            raise TypeError("The 'text' parameter must be a string.")
        return Colors.YELLOW_STYLE.format(text)

# def main():
#     """Main function for demonstrating the Color class."""
#     print(Color.green_text("This is green text"))
#     print(Color.red_text("This is red text"))
#     print(Color.yellow_bright("This is bright yellow text"))




def create_directory(path):
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        print(f"Failed to create directory '{path}': {e}")


def readFile(input_css_file_path):
    try:
        with open(input_css_file_path, mode='r') as data:
            return data.read()
        
    except Exception as e:
        if type(e).__name__ == "FileNotFoundError":
            print(f"<Error - {Colors.red_text(input_css_file_path)} Doesn't Exist>")
        else:
            print(f"Failed to Read File '{Colors.red_text(input_css_file_path)}': {e}")
        return None

def writeFile(content,file_path,good_msg=f"<Dev> - Default Success Msg ",error_msg="<Dev> - Default Error Msg"):
    try:
        folder_path=os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        # Handle existing files by adding a counter
        counter = 1
        while os.path.exists(file_path):
            # Split the filename and extension
            extension_and_filename=os.path.splitext(file_name)
            extname = extension_and_filename[1]
            basename = extension_and_filename[0]
            
            # Create a new filename with a counter
            new_file_name = f"{basename} ({counter}){extname}"
            file_path = os.path.join(folder_path, new_file_name)
            counter += 1
        good_msg=f"Successfully Created a File without WhiteSpace in {Colors.green_text(file_path)}"
        if folder_path:
            create_directory(folder_path)
        with open(file_path,'w')as file:
            file.write(content)
        print(good_msg)
    except Exception as e:
        print(error_msg)

def failSafeRootPath(inputted_path):
    """Returns right format for root path or inputted path

    Args:
        inputted_path (string): Unformatted path from user

    Returns:
        string: Right Format of Root path or inputted path
    """
    new_path = inputted_path
    if inputted_path in [" ", "", '/']:
        print(Colors.yellow_bright(f"Waring use './' as Based Directory, not '{inputted_path}'"))
        new_path = "."

    return new_path


def canReadandWritePermission(absolute_path):
    """Checks read and write permission for File/Folder

    Args:
        absolute_path (path): Location of File/Folder

    Returns:
        boolean: Either true or false
    """
    return os.access(absolute_path,os.R_OK) and os.access(absolute_path,os.W_OK)

def isFolderEmpty(folder_path):
    try:
        return next(os.scandir(folder_path), None) is None
    except:     #Incase Folder is Moved
        return False
    
    
import os
import shutil
from typing import Union

def moveFileToDirectory(
    src: Union[str, os.PathLike], 
    dest_dir: Union[str, os.PathLike]
) -> str:
    """
    Move a file to a destination directory, handling name conflicts.
    
    Args:
        src: Source file path
        dest_dir: Destination directory path
    
    Returns:
        The final path of the moved file
    
    Raises:
        FileNotFoundError: If source file does not exist
        PermissionError: If there are permission issues
    """
    # Validate inputs
    if not os.path.exists(src):
        return
        # raise FileNotFoundError(f"Source file not found: {src}")
    
    if not os.path.isdir(dest_dir):
        return
        # raise NotADirectoryError(f"Destination is not a directory: {dest_dir}")
    
    # Get the original file name
    file_name = os.path.basename(src)
    dest = os.path.join(dest_dir, file_name)
    
    # Handle existing files by adding a counter
    counter = 1
    while os.path.exists(dest):
        # Split the filename and extension
        filename_and_extension=os.path.splitext(file_name)
        extname = filename_and_extension[1]
        basename = filename_and_extension[0]
        
        # Create a new filename with a counter
        new_file_name = f"{basename} ({counter}){extname}"
        dest = os.path.join(dest_dir, new_file_name)
        counter += 1
    
    # Move the file
    try:
        shutil.move(src, dest)
        return dest
    except PermissionError:
        return
        # raise PermissionError(f"Permission denied when moving {src} to {dest}")
    

def delEmptyAll(path):
    for folder,sub,files in os.walk(path):
        if len(folder) > 2 and len(files) < 1 and folder != os.path.join(path,'System Volume Information'): # if path not '.'
            try:
                os.rmdir(folder)
            except Exception as e:
                # print('del error')
                pass    