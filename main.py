import utils
import analyze
import yaml
import re
from termcolor import colored
import sys

# Function to print in green color
def print_green(text):
    print(colored(text, 'green'))

# Function to print in blue color
def print_blue(text):
    print(colored(text, 'blue'))

def print_red(text):
    print(colored(text, 'red'))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <disk_path>")
        sys.exit(1)

    disk = sys.argv[1]
    yaml_data = analyze.load_yaml_file("files2.yaml")

    disk_fixed = utils.fixpath(disk)

    print_red("############################---------------------------------------#####################################################")
    print_blue("################   Partitions info      ###################")
    partitions = analyze.list_partitions(disk_fixed);
    print(utils.dict_list_to_json(partitions))

    print()
    print()

    print_red("############################---------------------------------------#####################################################")
    print_green("Choose partition index you want to analyze (only Windows partitions format will work: exFAT/NTFS or older): ")
    while True:
        try:
            partition_index = int(input("Enter the partition index: "))
            break
        except ValueError:
            print("Please enter a valid integer.")

    partition =  next(filter(lambda x: x['index'] == partition_index, partitions), None)

    print_red("############################---------------------------------------#####################################################")
    print_blue("################   Chosen partition info      ###################")
    print(analyze.get_partition_additionals_info(disk_fixed, analyze.get_main_partition(partitions)))
    #partition = analyze.get_main_partition(analyze.list_partitions(utils.fixpath(disk)))

    print_red("############################---------------------------------------#####################################################")
    print_blue("################   Generate timeline      ###################")
   
    fls_out = analyze.generate_timeline(utils.fixpath(disk),partition)
    spliied = fls_out.splitlines()

    print_red("############################---------------------------------------#####################################################")
    print_blue("################   Extract files to analyze      ###################")
    list_of_files, file_with_comm = analyze.get_files_to_extract_list_using_yaml_file(yaml_data, spliied)

    analyze.extract_files_with_icat(utils.fixpath(disk), partition, list_of_files)


    print_red("############################---------------------------------------#####################################################")
    print_blue("################   Analyze files     ###################")
    analyze.run_analysis_tools(file_with_comm)
