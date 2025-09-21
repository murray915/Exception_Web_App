from xml.dom import minidom
import os, shutil, pathlib, fnmatch
from icecream import ic

def create_xmls(despath: str, no_files: int, start_name_no: int, filepattern:str) -> bool:
    """ 
    create xmls into despath
    inputs: despath for files
    No. of files: int value for numbers of files
    start_name_no: int value for starting name (int) for files
    filepattern: pattern in the filename to searchfor

    return True/False on success
    """

    try:
        if no_files == 0:
            return False

        root = minidom.Document()

        xml = root.createElement('root') 
        root.appendChild(xml)

        productChild = root.createElement('product')
        productChild.setAttribute('name', 'Geeks for Geeks')
        xml.appendChild(productChild)

        xml_str = root.toprettyxml(indent ="\t") 

        ic("Files generated: ",despath)
        ic(     "No of files: ",no_files)

        for i in range(start_name_no, (start_name_no+no_files)):
            save_path_file = despath+"/SOP-"+filepattern+"-"+str(i)+".xml"

            with open(save_path_file, "w") as f:
                f.write(xml_str) 

        return True

    except Exception as err: # Exception Block. Return data to user & False
        ic(f"\n\n** Unexpected {err=}, {type(err)=} ** \n\n")
        return False


def move_dir(src: str, dst: str, move_target_no: int, pattern: str = '*'):
    """ 
    src: source folder path (if not exist, create)
    dst: destination folder path (if not exist, create)
    pattern: filetype input, move only these ("*.xml")
    move_target_no: break loop after x number of files
    """

    # check dest path/create
    if not os.path.isdir(dst):
        pathlib.Path(dst).mkdir(parents=True, exist_ok=True)
    
    # get files from path & move
    for i,f in enumerate(fnmatch.filter(os.listdir(src), pattern)):

        # break for x number files
        if move_target_no > 0 and i == move_target_no:
            return
        else:
            shutil.move(os.path.join(src, f), os.path.join(dst, f))


def create_magma_folder(rootfolder: str):
    """ 
    create folders for magma simulation in root location    
    rootfolder: where magma folders to be created
    """
    ic("/magma paths creating ... ")    
    paths = [
        rootfolder+'/magma/magma_in/Sales_Orders',
        rootfolder+'/magma/magma_in/Priority_Sales_Orders',
        rootfolder+'/magma/magma_in/Suppliers',
        rootfolder+'/magma/magma_in/Customers',
        rootfolder+'/magma/magma_in/Vendor_Items',
        rootfolder+'/magma/magma_in/Products',
        rootfolder+'/magma/magma_in/BIN',
        rootfolder+'/magma/magma_recv/HTTP-IN',
        rootfolder+'/magma/magma_recv/HTTP-MASTER-IN'
    ]        

    for path in paths:
        if not os.path.exists(path):            
            ic(path)
            os.makedirs(path)


def delete_magma_folder(rootpath: str):
    """ 
    Delete folder used for magma simulation in root location  
    """
    
    ic("Deleted /magma dir folder(s)")
    path = os.path.join(rootpath, "magma")
    shutil.rmtree(path, ignore_errors=False)


def list_files(dir_path):
    # list to store files
    res = []
    try:
        for file_path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, file_path)):
                res.append(file_path)
    except FileNotFoundError:
        print(f"The directory {dir_path} does not exist")
    except PermissionError:
        print(f"Permission denied to access the directory {dir_path}")
    except OSError as e:
        print(f"An OS error occurred: {e}")
    return res
