import logging
import ipaddress
import re
from app7 import Configuration


class LogsReader:
    class LogEntry:
        def __init__(
                self,
                ip,
                user,
                time,
                request_method,
                status_code,
                bytes_send,
                browser):
            self.ip = ip
            self.user = user
            self.time = time
            self.request_method = request_method
            self.status_code = status_code
            self.bytes_send = bytes_send
            self.browser = browser

        def __str__(self):
            return f"IP: {self.ip} User: {self.user} Time: {self.time} Request: {self.request_method} Status code: {self.status_code} Bytes send: {self.bytes_send} Browser: {self.browser}"

    def __init__(self, file_path, config: Configuration):
        self.logs = []
        self.__load_file(file_path)
        self.config = config

    def __load_file(self, file_path):
        try:
            file = open(file_path, 'r')
        except FileNotFoundError:
            raise FileNotFoundError("Log file with given path does not exists")
        lines = file.readlines()
        file.close()
        self.make_log_entries(lines)

    def make_log_entries(self, lines):
        for line in lines:
            self.logs.append(self.__parse_line(line))
        return self.logs

    def __parse_line(self, line):
        ip = self.get_ip(line)
        time = self.get_date(line)
        request = self.get_request_header(line)
        return_code = self.get_return_code(line)
        bytes_send = self.get_bytes_send(line)
        browser = self.get_browser(line)
        return self.LogEntry(
            ip,
            None,
            time,
            request,
            return_code,
            bytes_send,
            browser)

    def get_ip(self, ip):
        ip = re.search('((25[0-5]|(2[0-4]|1\\d|[1-9]|)\\d)\\.?){4}', ip)
        if ip is not None:
            return ip[0]
        return None

    def get_date(self, date):
        date = re.search(
            "\\d{1,2}\\/[a-zA-Z]{3}\\/[1-2]\\d{3}(:\\d{2}){3} \\+\\d{4}", date)
        if date is not None:
            return date[0]
        return False

    def get_request_header(self, request):
        request = re.search("GET|POST|PUT|DELETE|HEAD|OPTIONS", request)
        if request is not None:
            return request[0]
        return None

    def get_return_code(self, return_code):
        return_code = re.search(" \\d{3} ", return_code)
        if return_code is not None:
            return int(return_code[0][1:-1])
        return None

    def get_bytes_send(self, bytes_send):
        bytes_send = re.search('\\d+ "', bytes_send)
        if bytes_send is not None:
            return int(bytes_send[0][0:-2])
        return None

    def get_browser(self, browser):
        browser = re.search('Chrome|Firefox|Safari', browser)
        if browser is not None:
            return browser[0]
        return None

    def print_logs(self):
        i = 0
        for log in self.logs:
            print(
                log.ip,
                log.time,
                log.request_method,
                log.status_code,
                log.bytes_send)
            if i == 100:
                break
            i += 1

    def print_requests(self, ip_subnet):
        mask = 238004 % 16 + 8
        lines = self.config.get_number_of_lines()
        counter = 0
        for log in self.logs:
            if self.belongs_to_subnet(log.ip, ip_subnet, mask):
                print(log.request)
                counter += 1
                if counter == lines:
                    input("Press any key to continue")

    def belongs_to_subnet(self, ip, ip_subnet, mask):
        return ipaddress.ip_address(ip) in ipaddress.ip_network(
            ip_subnet + "/" + str(mask), strict=False)

    def print_requests_by_browser(self, browser):
        for log in self.logs:
            if log.browser == browser:
                print(log)

    def print_requests_by_filter(self):
        request = self.config.get_filter()
        total_bytes = 0
        for log in self.logs:
            if request == log.request_method:
                total_bytes += log.bytes_send
        print(f"Total bytes send: {total_bytes}")


def run():
    config = Configuration()
    log = '152.32.65.99 - - [18/Oct/2020:00:15:28 +0200] "GET / HTTP/1.1" 301 234 "-" "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"'
    reader = LogsReader("lab7\\log.txt", config)
    print(reader.get_ip(log))
    print(reader.get_date(log))
    print(reader.get_request_header(log))
    print(reader.get_return_code(log))
    print(reader.get_bytes_send(log))
    reader.print_logs()
    reader.print_requests("152.0.0.0")
    reader.print_requests_by_browser("Chrome")
    reader.print_requests_by_filter()


if __name__ == "__main__":
    run()
