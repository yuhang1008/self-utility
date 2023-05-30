import numpy as np
from scipy.spatial.transform import Rotation

def format_sequence(num):
    # Convert the number to a string
    num_str = str(num)
    
    # Pad the string with leading zeros to ensure a length of 6
    formatted_str = "{:0>2}".format(num_str)
    
    return formatted_str


txt_src_path = "/home/lde/yuhang/ITSC/A_final_odometry/seg_f/" 
result_path = "/home/lde/yuhang/ITSC/odometry_in_kitti/seg_f/"

for seq_index in range(11):
    seq_str = format_sequence(seq_index)

    tum_file_path = txt_src_path + seq_str +".txt"
    with open(tum_file_path, 'r') as file:
        lines = file.readlines()

    all_kitti_strs = []
    for line in lines:
        a_tum = line.strip().split(' ')
        kitti_str = []
        quaternion = np.array([float(a_tum[4]), float(a_tum[5]), float(a_tum[6]), float(a_tum[7])])
        rotation = Rotation.from_quat(quaternion)
        rotation_matrix = rotation.as_matrix()
        
        kitti_str.append(str("{:.6e}".format(rotation_matrix[0][0])))
        kitti_str.append(str("{:.6e}".format(rotation_matrix[0][1])))
        kitti_str.append(str("{:.6e}".format(rotation_matrix[0][2])))
        kitti_str.append(str("{:.6e}".format(float(a_tum[1]))))
        
        kitti_str.append(str("{:.6e}".format(rotation_matrix[1][0])))
        kitti_str.append(str("{:.6e}".format(rotation_matrix[1][1])))
        kitti_str.append(str("{:.6e}".format(rotation_matrix[1][2])))
        kitti_str.append(str("{:.6e}".format(float(a_tum[2]))))
        
        kitti_str.append(str("{:.6e}".format(rotation_matrix[2][0])))
        kitti_str.append(str("{:.6e}".format(rotation_matrix[2][1])))
        kitti_str.append(str("{:.6e}".format(rotation_matrix[2][2])))
        kitti_str.append(str("{:.6e}".format(float(a_tum[3]))))
        all_kitti_strs.append(kitti_str)

    output_file_path = result_path + seq_str + ".txt"
    with open(output_file_path, 'w') as file:
        for line in all_kitti_strs:
            line_data = " ".join(line)
            file.write(line_data + "\n")
    
    print(seq_str + " processed")

print("program ends")
    