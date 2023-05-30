import numpy as np

def format_sequence(num):
    # Convert the number to a string
    num_str = str(num)
    
    # Pad the string with leading zeros to ensure a length of 6
    formatted_str = "{:0>2}".format(num_str)
    
    return formatted_str




for index in range(11):
    index_string = format_sequence(index)
    print("evo_ape tum gt_tum/" + index_string + ".txt aloam/" + index_string + ".txt -v " + "--save_results evo_results/aloam_" + index_string +".zip")
    # print("evo_ape kitti gt/" + index_string + ".txt lego/" + index_string + ".txt -va")