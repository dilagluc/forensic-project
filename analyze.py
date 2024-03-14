import utils
import re
import json


###Check exist before ??????????????
# --------------------------------------------------------------------------------------------------------
def list_partitions(disk_img_path):
    if not utils.file_exists(disk_img_path):
        print(f"Cannot access {disk_img_path}: No such file or directory")
        return None
    mmls_out = utils.execute([
        "mmls",
        "-B", "-r",
        disk_img_path
    ])
    if mmls_out is not None and len(mmls_out) > 0:
        return parse_mmls_output(mmls_out)


def parse_mmls_output(mmls_output):
    partitions = []
    units = None
    units_match = re.search(r'(\d+)-byte sectors', mmls_output)
    if units_match:
        units = int(units_match.group(1))
    
    pattern = re.compile(r'(\d+):\s+(\w+|-+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(.+)')
    
    for line in mmls_output.splitlines():
        match = pattern.match(line)
        if match:
            index, slot, start, end, length, size, description = match.groups()
            partition = {
                'index': int(index),
                'start': int(start),
                'end': int(end),
                'length': int(length),
                'units': units,
                'size_in_bytes': units * int(length),
                'size': size.strip(),
                'description': description.strip(), 
            }
            #partitions[index] = partition_info
            partitions.append(partition)

    return partitions


def get_partition_additionals_info(disk_img_path, partition={}):
    fsstat_out = utils.execute([
        "fsstat",
        disk_img_path,
        "-o", 
        str(partition['start'])
    ])
    return fsstat_out

def get_main_partition(partitions):
    main_partition = max(partitions, key=lambda x:x['size_in_bytes'])
    return main_partition


'''def analyze(disk_img_path):
    partitions = list_partitions(disk_img_path=disk_img_path)
    return partitions'''


# -----------------------------------------------------Timeline---------------------------------------------------

def generate_timeline_fls(disk_img_path, partition={}, output_file="timeline.body"):
    utils.execute([
        "fls",
        "-o", 
        str(partition['start']),
        "-mc",
        "-r",
        "-p",
        disk_img_path
    ], stdout=False, outfile=output_file)

def generate_timeline_ascii_with_mactime(input_file="timeline.body", output_file="timeline.csv"): 
    if not utils.file_exists(input_file):
        print(f"Cannot access {input_file}: No such file or directory")
        return None
    utils.execute([
        "mactime",
        "-y",
        "-d",
        "-b",
        input_file
    ], stdout=False, outfile=output_file)

def generate_timeline(disk_img_path, partition={}, output_file=b"timeline.csv"):
    generate_timeline_fls(disk_img_path=disk_img_path, partition=partition)
    generate_timeline_ascii_with_mactime(output_file=output_file)