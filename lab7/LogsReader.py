import logging
import re

class LogsReader:
    class LogEntry:
        def __init__(self, ip, user, time, request_method, status_code, bytes_send, browser):
            self.ip = ip
            self.user = user
            self.time = time
            self.request_method = request_method
            self.status_code = status_code
            self.bytes_send = bytes_send
            self.browser = browser

    def __init__(self, file_path):
        file = self.__load_file(file_path)


    def __load_file(self, file_path):
        try:
            file = open(file_path, 'r')
        except FileNotFoundError:
            raise FileNotFoundError("Log file with given path does not exists")
        lines = file.readlines()
        file.close()
        return lines

    def get_ip(self, ip):
        ip = re.search('((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?){4}', ip)
        if ip is not None:
            return ip[0]
        return None
    
    def get_date(self, date):
        date = re.search("[0-9]{1,2}\/[a-zA-z]{3}\/[1-2][0-9]{3}(:[0-9]{2}){3} \+\d{4}", date)
        if date is not None:
            return date[0]
        return False

    def get_request_header(self, request):
        request = re.search("(GET|POST|PUT|DELETE|HEAD|OPTIONS) \/ HTTP\/\d.\d", request)
        if request is not None:
            return request[0]
        return None
    
    def get_return_code(self, return_code):
        return_code = re.search(" \d{3} ", return_code)
        if return_code is not None:
            return int(return_code[0][1:-1])
        return None
    
    def get_bytes_send(self, bytes_send):
        bytes_send = re.search('[0-9]{1,} "', bytes_send)
        if bytes_send is not None:
            return int(bytes_send[0][0:-2])
        return None


   
    
def run():
    log = '73.62.179.5 - - [18/Oct/2020:03:14:40 +0200] "GET / HTTP/1.1" 301 231 "-" "-"'
    reader = LogsReader("lab7\lab.config")
    print(reader.get_ip(log))
    print(reader.get_date(log))
    print(reader.get_request_header(log))
    print(reader.get_return_code(log))
    print(reader.get_bytes_send(log))

if __name__ == "__main__":
    run()