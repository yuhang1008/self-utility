import numpy as np
from numpy.linalg import inv
from bagpy import bagreader
import pandas as pd
from scipy.spatial.transform import Rotation as Rotation

# ALOAM /laser_odom_to_init

def format_sequence(num):
    # Convert the number to a string
    num_str = str(num)
    
    # Pad the string with leading zeros to ensure a length of 6
    formatted_str = "{:0>2}".format(num_str)
    
    return formatted_str



raw_folder = "/home/lde/yuhang/ITSC/A_final_odometry/lego/"
output_folder = "/home/lde/yuhang/ITSC/A_final_odometry/lego_trans/"

for seq_num in range(11):
    seq_str = format_sequence(seq_num)
    raw_data_path = raw_folder + seq_str + ".txt"

    all_transed_datas = []
    with open(raw_data_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            transed_data = []
            raw_data = line.strip().split(' ')
            raw_rot_matrix = np.array([[float(raw_data[0]), float(raw_data[1]), float(raw_data[2])],
                                      [float(raw_data[4]), float(raw_data[5]), float(raw_data[6])],
                                      [float(raw_data[8]), float(raw_data[9]), float(raw_data[10])]])
            # raw_rotation = Rotation.from_matrix(raw_rot_matrix)
            # raw_quat = raw_rotation.as_quat()
            # new_qx = raw_quat[2]
            # new_qy = - raw_quat[0]
            # new_qz = - raw_quat[1]
            # new_qw = raw_quat[3]
            # new_rot = Rotation.from_quat(np.array([new_qx, new_qy, new_qz, new_qw]))
            # new_rot_matrix = new_rot.as_matrix()
            # inv_rotation = raw_rotation.inv()
            # inv_rot_matrix = inv_rotation.as_matrix()
            trans_matrix = np.array([[-1,1,1], [-1,1,1], [-1,1,1]])
            new_rot_matrix = np.dot(trans_matrix, raw_rot_matrix)
            transed_data.append(str("{:.6e}".format(new_rot_matrix[0][0])))
            transed_data.append(str("{:.6e}".format(new_rot_matrix[0][1])))
            transed_data.append(str("{:.6e}".format(new_rot_matrix[0][2])))
            transed_data.append(str("{:.6e}".format(float(raw_data[3]))))
                    
            transed_data.append(str("{:.6e}".format(new_rot_matrix[1][0])))
            transed_data.append(str("{:.6e}".format(new_rot_matrix[1][1])))
            transed_data.append(str("{:.6e}".format(new_rot_matrix[1][2])))
            transed_data.append(str("{:.6e}".format(float(raw_data[7]))))
            
            transed_data.append(str("{:.6e}".format(new_rot_matrix[2][0])))
            transed_data.append(str("{:.6e}".format(new_rot_matrix[2][1])))
            transed_data.append(str("{:.6e}".format(new_rot_matrix[2][2])))
            transed_data.append(str("{:.6e}".format(float(raw_data[11]))))
            
            all_transed_datas.append(transed_data)

    out_path = output_folder + seq_str + ".txt"
    with open(out_path, 'w') as file:
        for line in all_transed_datas:
            line_data = " ".join(line)
            file.write(line_data + "\n")
            
    print(seq_str + " processed")

print('program finished')