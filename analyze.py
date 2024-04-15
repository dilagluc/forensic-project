import utils
import re
import json
import yaml
from tqdm import tqdm


###Check exist before ??????????????
### get partitio au lieu de get_main_partition
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

def get_partition_from_index(partitions):
    main_partition = map(partitions, key=lambda x:x['size_in_bytes'])
    return main_partition

'''def analyze(disk_img_path):
    partitions = list_partitions(disk_img_path=disk_img_path)
    return partitions'''


# -----------------------------------------------------Timeline---------------------------------------------------


def execute_fls_and_save(disk_img_path, partition={}, output_file="timeline.body"):
    return utils.execute([
        "fls",
        "-o", 
        str(partition['start']),
        "-mc",
        "-r",
        "-p",
        disk_img_path
    ], stdout=True, outfile=output_file)

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
    fls_out = execute_fls_and_save(disk_img_path=disk_img_path, partition=partition)
    #generate_timeline_ascii_with_mactime(output_file=output_file)
    return fls_out


# -----------------------------------------------------icat---------------------------------------------------

def execute_icat_and_save(disk_img_path, partition={}, inode="", output_file=""):
    return utils.execute([
        "icat",
        "-o", 
        str(partition['start']),
        disk_img_path,
        inode
    ], stdout=False, outfile=output_file)


def find_inode(fls_out, to_match):
    print("Hi")

def extract_line_from_splitted_fls_out(fls_spllitted=[], regex=""):
    if not fls_spllitted or not regex:
        return []
    matched_lines = list(filter(lambda line: re.match(regex, line, re.IGNORECASE), fls_spllitted))
    processed_1 = list(filter(lambda line: "$FILE_NAME" not in line, matched_lines))
    processed_output = list(map(lambda line: (
    line.split("|")[2].split("-")[0],  # Récupérer la première partie de l'inode avant le tiret
    line.split("|")[1].replace("/", "_")  # Remplacer les '/' par des '_' dans le nom de fichier
    if len(line.split("|")) >= 3 else None),  processed_1))

    out = list(map(lambda x: (x[0], f"{x[0]}_{x[1]}"), processed_output))
    return out

# -----------------------------------------------------Yaml---------------------------------------------------
def load_yaml_file(filename):
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)
    return data


def get_files_to_extract_list_using_yaml_file(yaml_data, fls_spllitted=[]):
    out1 = []
    out2 = []
    #for member in tqdm(members):
    for entry in tqdm(yaml_data):
        items = yaml.safe_load(entry['out'])
        for item in items:
            if "dest_dir" in item and "ToMatch" in item:
                output_dir = "." + item['dest_dir']
                stdout = item['stdout']
                to_add = (output_dir, stdout)
                extract = extract_line_from_splitted_fls_out(fls_spllitted, regex=item['ToMatch'])
                #print(extract)
                new_extract = []
                for i in extract:
                    new_extract.append(tuple(i + to_add))
                    #print(new_extract)
                out1 = out1 + new_extract

                new_extract = []
                commands = yaml.safe_load(item['commands'])   
                already_in = 0                  
                for i in out1:
                    if commands is not None:
                        for command in commands:
                            for key, value in command.items():
                                if "ANY" in key:
                                    if  item['dir'] == False:
                                        dest = i[2]  + "/Analysis/" +i[1]
                                        src = i[2]  + "/" +i[1]
                                        to_add = (command['ANY'].format(input=utils.fixpath(src), output=utils.fixpath(dest)),)
                                        new_extract.append(tuple(i + to_add))
                                    elif item['dir'] == True:
                                        to_add = (command['ANY'].format(input=utils.fixpath(item['dest_dir']), output=utils.fixpath(item['dest_dir'] + "/Analysis/analysis")),)
                                        new_extract.append(tuple(i + to_add))
                                else:
                                    if i[1].endswith(key) and  item['dir'] == False:
                                        dest = i[2]  + "/" +i[1]
                                        to_add = (command[key].format(input=utils.fixpath(src), output=utils.fixpath(dest)),)
                                        new_extract.append(tuple(i + to_add))
                                    elif i[1].endswith(key) and  item['dir'] == True:
                                        to_add = (command[key].format(input=utils.fixpath(item['dest_dir']), output=utils.fixpath(item['dest_dir']+ "/Analysis/analysis")),)
                                        new_extract.append(tuple(i + to_add))
                out2 = out2 + new_extract
                #print(out2)
    return out1, out2


def extract_files_with_icat(disk_img_path, partition, list_of_files=[]):
    utils.create_dir("./extracted")
    with open("./extracted/extracted.txt", 'w') as file:
        for entry in list_of_files:
            inode = entry[0]
            dest = entry[2]  + "/" +entry[1]
            utils.create_dir(entry[2])
            execute_icat_and_save(disk_img_path, partition, inode, output_file=utils.fixpath(dest))
            file.write(str(entry) + '\n')

def run_analysis_tools(list_with_cmd=[]):
    utils.create_dir("./extracted")
    with open("./extracted/extracted_with_tools_commands.txt", 'w') as file:
        prev_command = ""
        for entry in tqdm(list_with_cmd):
            #for entry in list_with_cmd:
            command = entry[4]
            stdout = entry[3]
            argv = command.split(' ')
            argv[0] = utils.fixpath(argv[0])
            print(command)
            if(prev_command != command):
                utils.execute(argv, stdout=stdout)
            prev_command = command
            file.write(str(entry) + '\n')