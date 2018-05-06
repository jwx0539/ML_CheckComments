import os


# 结果保存路径
output_path = './output'
if not os.path.exists(output_path):
    os.makedirs(output_path)
text_type_dic = {'力荐':1,'推荐':1,'还行':1,'较差':0,'很差':0 }
