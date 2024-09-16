import cv2
import os

# 读取图像
image_path = 'images/4.png'
image = cv2.imread(image_path)


# 获取图像的高度和宽度
height, width, _ = image.shape

image =image[8:height-5,1:width-1]

height, width, _ = image.shape
# 计算小图的大小
rows, cols = 5, 5
cell_height = height // rows
cell_width = width // cols

# 创建一个文件夹来保存小图
output_dir = 'output_images'
os.makedirs(output_dir, exist_ok=True)

# 分割并保存小图
for i in range(rows):
    for j in range(cols):
        # 计算每个小图的起始和结束坐标
        start_row = i * cell_height
        start_col = j * cell_width
        end_row = start_row + cell_height
        end_col = start_col + cell_width

        # 裁剪小图
        small_image = image[start_row:end_row, start_col:end_col]
        height, width, _ = small_image.shape
        small_image = small_image[2:height-3,8:width-10 ]
        # 保存小图
        output_path = os.path.join(output_dir, f'small_image_{i}_{j}.jpg')
        cv2.imwrite(output_path, small_image)

print("图像分割完成！所有小图已保存。")
