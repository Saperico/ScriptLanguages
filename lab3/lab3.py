import logging
import sys


def read_log(file):
    lines = file.readlines()
    file.close()
    entries = []
    for line in lines:
        line_arr = line.split()
        path = line_arr[0]
        code = int(line_arr[1])
        byte_size = int(line_arr[2])
        proccessing_time = int(line_arr[3])
        entries.append((path, code, byte_size, proccessing_time))

    logging.debug(f"Read {len(entries)} lines from log.txt")
    logging.debug(f"Read {4* len(entries)} entries from log.txt") #assuming each line has 4 entries
    return entries


def succesful_reads(log_content):
    succesful = [entry for entry in log_content if entry[1]>=200 and entry[1]<300]
    logging.info(f"Found {len(succesful)} successful entries")
    return succesful


def failed_reads(log_content):
    failed400 = []
    failed500 = []
    for entry in log_content:
        if entry[1]>=400:
            if entry[1] < 500:
                failed400.append(entry)
            elif entry[1] < 600:
                    failed500.append(entry)
    logging.info(f"Found {len(failed400)} entries with code 400")
    logging.info(f"Found {len(failed500)} entries with code 500")
    return failed400 + failed500


def html_entries(succesful_entries):
    html = [entry for entry in succesful_entries if entry[0].endswith(".html")]
    logging.info(f"Found {len(html)} successful html entries")
    return html


def print_html_entries(log_content):
    for entry in log_content:
        print(entry)


def run():
    logging.basicConfig(level=logging.DEBUG)
    file = sys.stdin

    log_entries = read_log(file)

    succesfuls = succesful_reads(log_entries)

    failed_reads(log_entries)

    html = html_entries(succesfuls)
    
    print_html_entries(html)

if __name__ == "__main__":
    run()
