import utils
import analyze

disk = "/media/veracrypt1/forensic/ewf/ewf/disk.E01"
'''print(analyze.analyze(disk))
print(utils.dict_list_to_json(analyze.analyze(disk)))
print(analyze.get_main_partition(analyze.analyze(disk)))'''
analyze.generate_timeline(disk, analyze.get_main_partition(analyze.list_partitions(disk)))
