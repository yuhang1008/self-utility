import numpy as np
from scipy.spatial.transform import Rotation

def format_sequence(num):
    # Convert the number to a string
    num_str = str(num)
    
    # Pad the string with leading zeros to ensure a length of 6
    formatted_str = "{:0>2}".format(num_str)
    
    return formatted_str


# ---------------------------------------------------------------
kitti_gt_path = "/home/lde/KITTI_ODOMETRY/data_odometry_poses/dataset/poses/"
kitti_time_path = "/home/lde/KITTI_ODOMETRY/data_odometry_calib/dataset/sequences/"
output_path =  "/media/lde/SSD_2T/Akitti_to_tum/"

for sequence_index in range (11):

    sequence_str = format_sequence(sequence_index)

    gt_file = kitti_gt_path + sequence_str + ".txt"
    time_file = kitti_time_path + sequence_str + "/times.txt"

    # read time stamp
    with open(time_file, 'r') as file:
        lines = file.readlines()
        # Convert lines to floats
        float_times = [float(line.strip()) for line in lines]

    # read gt
    with open(gt_file, 'r') as file:
        lines = file.readlines()

    all_tum_strings = []
    frame_index = 0
    for line in lines:
        # Remove leading/trailing whitespace and split attributes by space
        raw_transformation = line.strip().split(' ')
        
        tum_string = []
        Tcw = np.array([[float(raw_transformation[0]), float(raw_transformation[1]), float(raw_transformation[2]), float(raw_transformation[3])],
                        [float(raw_transformation[4]), float(raw_transformation[5]), float(raw_transformation[6]), float(raw_transformation[7])],
                        [float(raw_transformation[8]), float(raw_transformation[9]), float(raw_transformation[10]), float(raw_transformation[11])],
                        [0,                            0,                            0,                             1      ]])

        Rcw = Tcw[:3, :3]
        rotation = Rotation.from_matrix(Rcw)
        quat_cw = rotation.as_quat()
        
        tum_string.append(str("{:.4f}".format(float_times[frame_index])))
        tum_string.append(str("{:.4f}".format(Tcw[0][3])))
        tum_string.append(str("{:.4f}".format(Tcw[1][3])))
        tum_string.append(str("{:.4f}".format(Tcw[2][3])))
        tum_string.append(str("{:.4f}".format(quat_cw[0])))
        tum_string.append(str("{:.4f}".format(quat_cw[1])))
        tum_string.append(str("{:.4f}".format(quat_cw[2])))
        tum_string.append(str("{:.4f}".format(quat_cw[3])))
        
        all_tum_strings.append(tum_string)
        frame_index += 1
        
    output_file_path = output_path + sequence_str + ".txt"
    with open(output_file_path, "w") as file:
        # Write data line by line with attributes separated by spaces
        for line in all_tum_strings:
            line_data = " ".join(line)
            file.write(line_data + "\n")

print("program ends")
        