from collections import Counter
import cv2
import os
import numpy as np

def calc_four(my_list):
    # 使用 Counter 统计每个元素的数量
    counter = Counter(my_list)
    flag = False
    name = "blank"
    color = "blank"
    # 输出每个元素及其数量
    for item, count in counter.items():
        # print(f'{item}: {count}')
        if count==4 and item != "blank":
            print(f'{item}: {count}')
            flag = True
            color = item
        if count == 1:
            name = item
    return name,flag,color

def find_four_in_a_row(board):
    #遍历行
    for i in range(5):
        res = calc_four(board[i])
        if res[1]:
            origin_pos = (i,board[i].index(res[0]))
            print("第{}行，数据：{},补充位置：{}，四字颜色：{}".format(i,board[i],origin_pos,res[2]))
            for index,j in enumerate(board):
                if res[2] in j and index != i:
                    color_index = j.index(res[2])
                    target_pos = (index,color_index)
                    print("其他位置的颜色坐标：{}".format(target_pos))
                    break
            return [target_pos,origin_pos]


    transposed_board = [[board[j][i] for j in range(5)] for i in range(5)]
    #遍历列
    for i in range(5):
        res = calc_four(transposed_board[i])
        if res[1]:
            origin_pos = (i, transposed_board[i].index(res[0]))
            origin_pos = (origin_pos[1],origin_pos[0])
            print("第{}列，数据：{},补充位置：{}，四字颜色：{}".format(i, transposed_board[i], origin_pos, res[2]))
            for index, j in enumerate(transposed_board):
                if res[2] in j and index != i:
                    color_index = j.index(res[2])
                    target_pos = (color_index,index)
                    print("其他位置的颜色坐标：{}".format(target_pos))
                    break
            return [target_pos,origin_pos]

    #左上右下对角线
    left_right_list = [board[i][i] for i in range(5)]
    left_right_res = calc_four(left_right_list)
    print(left_right_res)
    if left_right_res[1]:
        pos = left_right_list.index(left_right_res[0])
        origin_pos = [pos,pos]
        print("第左上右下对角线，数据：{},补充位置：{}，四字颜色：{}".format(left_right_list,origin_pos,left_right_res[2]))
        for index, j in enumerate(board):
            if left_right_res[2] in j :
            # if left_right_res[2] in j:
                color_index = j.index(left_right_res[2])
                if color_index == index and j.count(left_right_res[2])==2:
                    color_index = j.index(left_right_res[2],color_index+1)
                elif color_index == index and j.count(left_right_res[2])==1:
                    continue
                target_pos = (index, color_index)
                print("其他位置的颜色坐标：{}".format(target_pos))
                return [target_pos,origin_pos]


    #右上左下对角线
    right_left_list = [board[i][4-i] for i in range(5)]
    right_left_res = calc_four(right_left_list)
    print(right_left_res)
    if right_left_res[1]:
        pos = right_left_list.index(right_left_res[0])
        origin_pos = [pos,4-pos]
        print("第右上左下对角线，数据：{},补充位置：{}，四字颜色：{}".format(right_left_list,origin_pos,right_left_res[2]))
        for index, j in enumerate(board):
            # if right_left_res[2] in j and j.count(right_left_res[2])==2:
            if right_left_res[2] in j:
                color_index = j.index(right_left_res[2])
                if color_index == (4 - index) and j.count(right_left_res[2])==2:
                    color_index = j.index(right_left_res[2],color_index+1)
                elif color_index == (4 - index) and j.count(right_left_res[2])==1:
                    continue
                target_pos = (index, color_index)
                print("其他位置的颜色坐标：{}".format(target_pos))
                return [target_pos,origin_pos]

def get_match_images():
    files = os.listdir("./match_images")
    image_types = []
    for f in files:
        file_path = os.path.join("./match_images", f)
        type_name = os.path.splitext(f)[0]
        image_types.append((type_name,cv2.imread(file_path)))
    return image_types


def get_splited_images(image_path):
    image_types = get_match_images()
    # 读取图像
    # image_path = 'images/3.png'
    image = cv2.imread(image_path)

    # 获取图像的高度和宽度
    height, width, _ = image.shape

    image =image[8:height-5,1:width-1]

    height, width, _ = image.shape
    # 计算小图的大小
    rows, cols = 5, 5
    cell_height = height // rows
    cell_width = width // cols

    # 分割并保存小图
    for row in range(rows):
        for col in range(cols):
            # 计算每个小图的起始和结束坐标
            start_row = row * cell_height
            start_col = col * cell_width
            end_row = start_row + cell_height
            end_col = start_col + cell_width

            # 裁剪小图
            small_image = image[start_row:end_row, start_col:end_col]

            # 执行模板匹配
            for image_type in image_types:
                result = cv2.matchTemplate(image_type[1], small_image, cv2.TM_CCOEFF_NORMED)
                # 设置匹配的阈值（0到1之间）
                threshold = 0.85
                locations = np.where(result >= threshold)
                if len(locations[0]) > 0:
                    # print(image_type[0],end="\t")
                    board[row][col] = image_type[0]
                    pos[row][col] = ((start_col + end_col) // 2,(start_row + end_row) // 2)
        # print()
    res = find_four_in_a_row(board)
    # print(res)
    print((pos[res[0][0]][res[0][1]]), (pos[res[1][0]][res[1][1]]))
    for index, pos_f in enumerate(res):
        res_pos = pos[res[index][0]][res[index][1]]
        # 绘制文字
        cv2.putText(image, str(index), (res_pos[0] - 10, res_pos[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("res", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    board = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    pos = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    get_splited_images("images/1.png")
    exit()
    files = os.listdir("images")
    for file in files[2:]:
        board = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        pos = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        image_path = os.path.join("images/",file)
        print(image_path)
        get_splited_images(image_path)
