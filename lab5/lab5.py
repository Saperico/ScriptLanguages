class LogsReader:
    def __init__(self, file_path):
        file = self.__load_file(file_path)
        lines = self.__split_lines(file)
        self.logs = self.__create_dictionary(lines)
        self.ip_count = self.__count_request_by_ip()

    def __load_file(self, file_path):
        file = open(file_path, 'r')
        lines = file.readlines()
        file.close()
        return lines

    def __split_lines(self, lines):
        lines = [line.split('"') for line in lines]
        lines = [line[0].split(" ", 2) + [line[1]] + line[2].split() + line[5:6] for line in lines]
        lines = [line[:2] + [line[2].split(" ", 1)[1][1:-2]] + line[3:] for line in lines]
        return lines

    def __create_dictionary(self, lines):
        logs = {}
        for i in range(len(lines)):
            logs[i]={
                "ip": lines[i][0],
                "user": lines[i][1],
                "time": lines[i][2],
                "request_method": lines[i][3],
                "status_code": lines[i][4],
                "bytes_send": lines[i][5],
                "browser": lines[i][6]
            }
        return logs

    def __count_request_by_ip(self):
        ip_count = {}
        for log in self.logs:
            ip = self.logs[log]["ip"]
            if ip in ip_count:
                ip_count[ip] += 1
            else:
                ip_count[ip] = 1
        return ip_count

    def ip_find(self, most_active = True):
        value = 0
        if most_active:
            value = max(self.ip_count.values())
        else:
            value = min(self.ip_count.values())
        return [ip for ip in self.ip_count if self.ip_count[ip] == value]

    def longest_request(self):
        max_bytes = 0
        for log in self.logs:
            if self.logs[log]["bytes_send"] != "-":
                if int(self.logs[log]["bytes_send"]) > max_bytes:
                    max_bytes = int(self.logs[log]["bytes_send"])
                    request = self.logs[log]["request_method"]
        return (request, max_bytes)

    def non_existent_requests(self):
        requests = set()
        for log in self.logs:
            if self.logs[log]["status_code"] == "404":
                requests.add(self.logs[log]["request_method"])
        return requests

def run():
    logs_reader = LogsReader("lab5/log.txt")
    print(logs_reader.ip_find())
    print(logs_reader.ip_find(False))
    print(logs_reader.longest_request())
    non_existent_requests = logs_reader.non_existent_requests()
    for request in non_existent_requests:
        print(request)

if __name__ == "__main__":
    run()