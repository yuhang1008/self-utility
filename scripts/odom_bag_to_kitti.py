import numpy as np
from numpy.linalg import inv
from bagpy import bagreader
import pandas as pd
from scipy.spatial.transform import Rotation as R

# ALOAM /laser_odom_to_init

def format_sequence(num):
    # Convert the number to a string
    num_str = str(num)
    
    # Pad the string with leading zeros to ensure a length of 6
    formatted_str = "{:0>2}".format(num_str)
    
    return formatted_str


def load_calib(calib_file_path):
    """Load and compute intrinsic and extrinsic calibration parameters."""

    raw_cali_data = []
    with open(calib_file_path, 'r') as f:
        for line in f.readlines():
            attributes = line.strip().split(' ')
            raw_cali_data.append(attributes)
            
    # left projection matrix
    P2 = np.array([[float(raw_cali_data[2][1]), float(raw_cali_data[2][2]), float(raw_cali_data[2][3]), float(raw_cali_data[2][4])],
                  [float(raw_cali_data[2][5]), float(raw_cali_data[2][6]), float(raw_cali_data[2][7]), float(raw_cali_data[2][8])],
                  [float(raw_cali_data[2][9]), float(raw_cali_data[2][10]), float(raw_cali_data[2][11]), float(raw_cali_data[2][12])]])
    
    
    # dont know why the lable in data is inverse
    Tcl = np.array([[float(raw_cali_data[4][1]), float(raw_cali_data[4][2]), float(raw_cali_data[4][3]), float(raw_cali_data[4][4])],
                   [float(raw_cali_data[4][5]), float(raw_cali_data[4][6]), float(raw_cali_data[4][7]), float(raw_cali_data[4][8])],
                   [float(raw_cali_data[4][9]), float(raw_cali_data[4][10]), float(raw_cali_data[4][11]), float(raw_cali_data[4][12])],
                   [0,                          0,                           0,                           1                          ]])
    
    data = {"P2":P2, "Tcl":Tcl}
    
    return data

#-------------------------------------------------------------------------------------------------------



output_folder = "/media/lde/SSD_2T/Aodometry_converted/aloam/"
calib_folder = "/home/lde/KITTI_ODOMETRY/data_odometry_calib/dataset/sequences/"
odom_bag_folder = "/media/lde/SSD_2T/A_pure_odom_bag/aloam/"
odometry_topic_name = '/aft_mapped_to_init_high_frec'



sequence_num = 0
sequence_str = format_sequence(sequence_num)

calib_path = calib_folder + sequence_str + "/calib.txt"
calib_data = load_calib(calib_path)

# bag_path = "/media/lde/SSD_2T/kitti_rosbag/recorded_for_evo/aloam/" + sequence_str + ".bag"
bag_path = odom_bag_folder + sequence_str + ".bag"
bag = bagreader(bag_path)
odometry = bag.message_by_topic(odometry_topic_name)

df_odometry = pd.read_csv(odometry)
Tcl = calib_data['Tcl']

full_odom_data = []
initialze = False
for a_odometry in df_odometry.values:
    a_odom_data = []
    rotation_lw = R.from_quat([a_odometry[9], a_odometry[10], a_odometry[11], a_odometry[12]])
    Rlw = rotation_lw.as_matrix()
    Tlw =  np.array([[float(Rlw[0][0]), float(Rlw[0][1]), float(Rlw[0][2]), float(a_odometry[6])],
                     [float(Rlw[1][0]), float(Rlw[1][1]), float(Rlw[1][2]), float(a_odometry[7])],
                     [float(Rlw[2][0]), float(Rlw[2][1]), float(Rlw[2][2]), float(a_odometry[8])],
                     [0,                0,                0,                1                   ]])
    
    Tcw = np.dot(Tcl, Tlw)
    if initialze == False:
        Tw0_w = Tcw
        Tw_w0 = np.linalg.inv(Tw0_w)
        initialze = True
    
    Tcw0 = np.dot(Tcw, Tw_w0)
        
    a_odom_data.append(str("{:.6e}".format(Tcw0[0][0])))
    a_odom_data.append(str("{:.6e}".format(Tcw0[0][1])))
    a_odom_data.append(str("{:.6e}".format(Tcw0[0][2])))
    a_odom_data.append(str("{:.6e}".format(Tcw0[0][3])))
    a_odom_data.append(str("{:.6e}".format(Tcw0[1][0])))
    a_odom_data.append(str("{:.6e}".format(Tcw0[1][1])))
    a_odom_data.append(str("{:.6e}".format(Tcw0[1][2])))
    a_odom_data.append(str("{:.6e}".format(Tcw0[1][3])))
    a_odom_data.append(str("{:.6e}".format(Tcw0[2][0])))
    a_odom_data.append(str("{:.6e}".format(Tcw0[2][1])))
    a_odom_data.append(str("{:.6e}".format(Tcw0[2][2])))
    a_odom_data.append(str("{:.6e}".format(Tcw0[2][3])))
    
    full_odom_data.append(a_odom_data)

output_file_path = output_folder + sequence_str + ".txt"
with open(output_file_path, "w") as file:
    # Write data line by line with attributes separated by spaces
    for line in full_odom_data:
        line_data = " ".join(line)
        file.write(line_data + "\n")


print("program ends")