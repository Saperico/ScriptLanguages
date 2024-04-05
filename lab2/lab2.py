import logging
import sys

file = sys.stdin
lines = file.readlines()
file.close()
if len(lines) == 0:
    logging.error("File is empty or not found")
    sys.exit()

table = [line.split() for line in lines]
logging.basicConfig(level=logging.DEBUG)
logging.info("Start")


def display_all_paths():
    for i in range(len(table)):
        code = table[i][1]
        if(code.startswith("4") or code.startswith("5") and len(code)==3):
            print("!" + table[i][0])
        else :
            print(table[i][0])


def get_path_with_largest_response():
    largest_response = int(table[0][2])
    index_of_lr = 0
    for i in range(1,len(table)):
        response_size = int(table[i][2])
        if(response_size>largest_response):
            largest_response = response_size
            index_of_lr = i
    print(f"path with largest size : {table[index_of_lr][0]}, size {table[index_of_lr][2]}")


def get_number_of_failed_requests():
    count = 0
    for i in range(len(table)):
        code = table[i][1]
        if(code.startswith("4") or code.startswith("5") and len(code)==3):
            count+=1
            logging.warning(f"Found failed request {table[i][0]}")
    print(f"failed requests : {count}")


def get_total_number_of_bytes_transferred():
    total = 0
    for i in range(len(table)):
        total+=int(table[i][2])
    print(f"total bytes transferred : {total}")


def get_total_number_of_kb_transferred():
    total = 0
    for i in range(len(table)):
        total+=int(table[i][2])
    print(f"total kb transferred : {total/1024:.2f}KB")


def get_average_processing_time():
    total = 0
    for i in range(len(table)):
        total+=float(table[i][3])
    print(f"avg processing time {total/len(table):.2f}")


display_all_paths()
get_path_with_largest_response()
get_number_of_failed_requests()
get_total_number_of_bytes_transferred()
get_total_number_of_kb_transferred()
get_average_processing_time()

logging.info("End")
#https://docs.python.org/3/library/logging.html
#https://docs.python.org/3/howto/logging-cookbook.html
#https://docs.python.org/3/howto/logging.html
