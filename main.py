import utils
import analyze
import yaml
import re

yaml_data = analyze.load_yaml_file("files2.yaml")

'''for entry in parsed_data:
    if entry['name'] == 'SYSTEM_FILE':
        items = yaml.safe_load(entry['out'])
        for item in items:
            print(item)
            for key, value in item.items():
                print("  {}: {}".format(key, value))'''


disk = "/media/veracrypt1/forensic/ewf/ewf/disk.E01"
'''print(analyze.analyze(disk))
print(utils.dict_list_to_json(analyze.analyze(disk)))
print(analyze.get_main_partition(analyze.analyze(disk)))'''
partition = analyze.get_main_partition(analyze.list_partitions(disk))
#analyze.generate_timeline(disk, analyze.get_main_partition(analyze.list_partitions(disk)))
#fls_out = analyze.execute_fls_and_save(disk, partition)
#print(fls_out)
fls_out = analyze.generate_timeline(disk,partition)
spliied = fls_out.splitlines()
regex = ".*/Windows/System32/config.*\\b(?:SAM|SECURITY|SOFTWARE|SYSTEM)"
#analyze.extract_line_from_splitted_fls_out(spliied, regex=regex)

list_of_files, file_with_comm = analyze.get_files_to_extract_list_using_yaml_file(yaml_data, spliied)

analyze.extract_files_with_icat(disk, partition, list_of_files)


# icat 

#print(utils.dict_list_to_json(analyze.list_partitions(disk)))

#print(analyze.get_partition_additionals_info(disk, analyze.get_main_partition(analyze.list_partitions(disk))))
