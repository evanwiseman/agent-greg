from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

# Test get_files_info
# try:
#     print(get_files_info("calculator", "."))  
# except Exception as e:
#     print(e)
# try:
#     print(get_files_info("calculator", "pkg"))
# except Exception as e:
#     print(e)
# try: 
#     print(get_files_info("calculator", "/bin"))
# except Exception as e:
#     print(e)
# try: 
#     print(get_files_info("calculator", "../"))
# except Exception as e:
#     print(e)


# Test get_file_content
# try:
#     print(get_file_content("calculator", "main.py"))
# except Exception as e:
#     print(e)
# try:
#     print(get_file_content("calculator", "pkg/calculator.py"))
# except Exception as e:
#     print(e)
# try:
#     print(get_file_content("calculator", "/bin/cat"))
# except Exception as e:
#     print(e)
# try:
#     print(get_file_content("calculator", "pkg/does_not_exist.py"))
# except Exception as e:
#     print(e)


# Test write_file
# try:
#     print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
# except Exception as e:
#     print(e)
# try:
#     print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
# except Exception as e:
#     print(e)
# try:
#     print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
# except Exception as e:
#     print(e) 

# Test run_python_file
try:
    print(run_python_file("calculator", "main.py")) # (should print the calculator's usage instructions)
except Exception as e:
    print(e) 
try:
    print(run_python_file("calculator", "main.py", ["3 + 5"])) # (should run the calculator... which gives a kinda nasty rendered result)
except Exception as e:
    print(e) 
try: 
    print(run_python_file("calculator", "tests.py"))
except Exception as e:
    print(e) 
try: 
    print(run_python_file("calculator", "../main.py")) # (this should return an error)
except Exception as e:
    print(e) 
try:
    print(run_python_file("calculator", "nonexistent.py")) # (this should return an error)
except Exception as e:
    print(e) 