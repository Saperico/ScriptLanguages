import logging

logging.basicConfig(level=logging.DEBUG)

def read_log(log_content):
    entries = []
    file = open(log_content, "r")
    lines = file.readlines()
    file.close()
    for line in lines:
        x = line.split()
        name = x[0]
        code = int(x[1])
        size = int(x[2])
        smth = int(x[3])
        entries.append((name, code, size, smth))

    logging.debug(f"Read {len(entries)} lines from log.txt")
    logging.debug(f"Read {4* len(entries)} entries from log.txt") #assuming each line has 4 entries
    return entries


def successful_reads(log_content):
    successful = []
    for entry in log_content:
        if entry[1]>=200 and entry[1]<300:
            successful.append(entry)
    logging.info(f"Found {len(successful)} successful entries")
    return successful


def failed_reads(log_content):
    failed400 = []
    failed500 = []
    for entry in log_content:
        if entry[1]>=400:
            if entry[1] < 500:
                failed400.append(entry)
            else: 
                if entry[1]<600:
                    failed500.append(entry)
    logging.info(f"Found {len(failed400)} failed 400 entries")
    logging.info(f"Found {len(failed500)} failed 500 entries")
    return failed400 + failed500


def html_entries(log_content):
    html = []
    for entry in log_content:
        if entry[1]>=200 and entry[1]<300 and entry[0].endswith(".html"):
                html.append(entry)
    logging.info(f"Found {len(html)} successful html entries")
    return html


def print_html_entries(log_content):
    for entry in log_content:
        print(entry)


def run():
    log_content = "log.txt"

    log_entries = read_log(log_content)

    successful_reads(log_entries)

    failed_reads(log_entries)

    html = html_entries(log_entries)

    print_html_entries(html)



if __name__ == "__main__":
    run()
