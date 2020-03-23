import os, re, math, sys
sys.path.extend(["/Users/dqin/Documents/FAME/watson_experiment"])
from pprint import pprint
from matplotlib.patches import Ellipse, Circle, Rectangle
import matplotlib.pyplot as plt

annotation_folder = "watson_experiment/resources/FDDB-folds"

# Only need to tranform those ellipseList.txt files.
f_names = [name for name in sorted(os.listdir(os.path.join("/Users/dqin/Documents/FAME", annotation_folder))) if name.endswith("ellipseList.txt")]
all_angles, all_data = dict(), dict()

def cal_x_y_list(a, b, tan_theta, cot_theta):
    """
    :param a: semi-major axis for ellipse
    :param b: semi-minor axis for ellipse
    :param tan_theta:
    :param cot_theta:
    :return: list of 4 tagents point on the ellipse
    """
    x_list, y_list = [], []

    x = abs(a ** 2 * tan_theta) / math.sqrt(a ** 2 * tan_theta ** 2 + b ** 2)
    x_list.append(x)
    x_list.append((-1) * x)
    y_list.append(b ** 2 / (a ** 2 * tan_theta) * x_list[0] * (-1))
    y_list.append(b ** 2 / (a ** 2 * tan_theta) * x_list[1] * (-1))

    x = abs(a ** 2 * cot_theta) / math.sqrt(a ** 2 * cot_theta ** 2 + b ** 2)
    x_list.append(x)
    x_list.append((-1) * x)
    y_list.append(b ** 2 / (a ** 2 * cot_theta) * x_list[2])
    y_list.append(b ** 2 / (a ** 2 * cot_theta) * x_list[3])

    return x_list, y_list

def rotate_x_y(x_list, y_list, theta):
    if theta > 0:
        r_angle = math.pi / 2 - theta  # rotate rangle
    else:
        r_angle = (-1) * math.pi / 2 + theta  # seems wrong but work well?
    #         r_angle = (-1) * math.pi/2 - theta

    x_final, y_final = [], []
    for x, y in zip(x_list, y_list):
        x_prime = x * math.cos(r_angle) + y * math.sin(r_angle)
        y_prime = y * math.cos(r_angle) - x * math.sin(r_angle)
        x_final.append(x_prime)
        y_final.append(y_prime)
    return x_final, y_final

def convert_annotation(input_list, plot=False):
    """
        Do the math here

        Sample input list:
            ['123.583300', '85.549500', '1.265839', '269.693400', '161.781200', '1', '']

        Here, each face is denoted by:
            <major_axis_radius   minor_axis_radius   angle   center_x   center_y 1>.
    """
    inputs = [float(x) for x in input_list[:5]]
    b, a = inputs[0], inputs[1]
    theta = inputs[2]  # can be +ve/-ve, < pi/2

    if abs(theta - 0) < 0.01 or abs(theta - math.pi / 2) < 0.01:
        # x, y, short, long
        return inputs[4] - b, inputs[3] - a, a * 2, b * 2

    tan_theta = math.tan(theta) if theta < 0 else (-1) * math.tan(theta)
    cot_theta = math.tan(math.pi / 2 - theta) if theta < 0 else (-1) * math.tan(math.pi / 2 - theta)

    x_list, y_list = cal_x_y_list(a, b, tan_theta, cot_theta)
    x_final, y_final = rotate_x_y(x_list, y_list, theta)
    print(x_final)
    print(y_final)
    x_final = [x + inputs[3] for x in x_final]
    y_final = [y + inputs[4] for y in y_final]

    data = {
        "x_final": x_final,
        "y_final": y_final,
        'a': a,
        'b': b,
        'theta': theta,
        'center': (inputs[3], inputs[4])
    }
    pprint(data)
    if plot:
        visualize(data)

    (left, top), width, height = prepare_rectangle(x_final, y_final)
    return top, left, width, height


def prepare_rectangle(x_final, y_final):
    """prepare for visualziation of Rectangel"""
    x_s, x_b = min(x_final), max(x_final)
    y_s, y_b = min(y_final), max(y_final)
    width = x_b - x_s
    height = y_b - y_s

    return (x_s, y_s), width, height


def prepare_ellipse(a, b, theta, center):
    #     plot_angle = 180 / math.pi * ((-1)*theta + math.pi/2) if theta < 0 else 180 / math.pi * (theta - math.pi/2)
    plot_angle = 180 / math.pi * (theta + math.pi / 2) if theta < 0 else 180 / math.pi * (theta - math.pi / 2)
    return center, a * 2, b * 2, plot_angle


def visualize(kwarges):
    x_final = kwarges['x_final']
    y_final = kwarges['y_final']
    a, b, theta = kwarges['a'], kwarges['b'], kwarges['theta']

    ra, rb, rc = prepare_rectangle(x_final, y_final)
    d, e, f, g = prepare_ellipse(a, b, theta, kwarges['center'])

    fig = plt.figure()
    ax = fig.add_subplot(111)

    rect1 = Rectangle(ra, rb, rc, alpha=0.3)
    ell1 = Ellipse(xy=d, width=e, height=f, angle=g, facecolor='yellow', alpha=0.3)
    ax.add_patch(ell1)
    ax.add_patch(rect1)

    ax.plot(kwarges['center'][0], kwarges['center'][1], 'ro')

    #     plt.axis('scaled')
    plt.axis('equal')  # changes limits of x or y axis so that equal increments of x and y have the same length
    plt.show()


# visualize(kwarges = data)



for f_in_name in f_names:
    f_in_path = os.path.join(annotation_folder, f_in_name)
    f_out_path = os.path.join(annotation_folder, f_in_name[:-4] + "-transformed.txt")

    with open(f_in_path, "r") as f_in, open(f_out_path, "w") as f_out:
        cur_file_name = ""
        for line in f_in:
            input("Press to continue...")
            if "img_" in line:
                # image naming line, write as is to f_out
                f_out.writelines(line)
                cur_file_name = line
                all_angles[cur_file_name] = []
                all_data[cur_file_name] = []

            elif line.strip().isdigit():  # remove the ending \n
                # face count line, write as is to f_out
                f_out.writelines(line)

            else:
                # Face annotation line, do transformation.
                input_list = re.split("\s+", line)
                # Order:
                # <major_axis_radius   minor_axis_radius   angle   center_x   center_y 1>.
                all_angles[cur_file_name].append(float(input_list[2]))
                all_data[cur_file_name].append(input_list)
                # What is the desired format by IBM? Check tutorial's code and modify the return of convert_
                # accordingly...
                top, left, width, height = convert_annotation(input_list)

                f_out.writelines(', '.join(["{0:.3f}".format(x) for x in [top, left, width, height]]) + "\n")