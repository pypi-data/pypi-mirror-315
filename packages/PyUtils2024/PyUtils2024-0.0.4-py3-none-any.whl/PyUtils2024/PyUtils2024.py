
import os
import stat
import time

import PyPDF2
import pyautogui
import requests
from PIL import Image
import cv2
import numpy as np
import sqlite3
import hashlib

from paddleocr import PaddleOCR,draw_ocr

"""获取指定目录下指定后缀文件"""

def get_files(dir_path,ext=''):
    files=os.listdir(dir_path)
    file_list=[]
    for file in files:
        if ext!='':
            if file[-len(ext):].upper()==ext.upper():
                file_list.append(os.path.join(dir_path,file))
        else:
            file_path=os.path.join(dir_path, file)
            if os.path.isfile(file_path):
                file_list.append(file_path)
    return file_list

"""获取指定目录含子目录下所有指定后缀的文件"""

def get_all_files(dir_path,ext=''):
    file_list=[]
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if ext!='':
                if file[-len(ext):].upper()==ext.upper():
                    file_path = os.path.join(root, file)
                    file_list.append(file_path)
            else:
                file_path = os.path.join(root, file)
                file_list.append(file_path)
    return file_list

"""将图片转换为PDF"""

def image_to_pdf(image_path, output_pdf_path):
    print("正在转换",image_path)
    image = Image.open(image_path)
    im_list = [image]
    im_list[0].save(output_pdf_path, "PDF", resolution=100.0, save_all=True)


def images_to_pdf(image_paths, output_pdf_path):
    if len(image_paths)==0:
        return None
    elif len(image_paths)==1:
        image_to_pdf(image_paths[0],output_pdf_path)
    else:
       images = []
       for image_path in image_paths:
           image = Image.open(image_path)
           image=image.convert('RGB')
           images.append(image)
       images[0].save(output_pdf_path, "PDF", resolution = 100.0, save_all=True, append_images=images[1:])

"""合并多个PDF,input_files:PDF文件列表"""

def merge_pdfs(input_files, output_file):
    merger = PyPDF2.PdfMerger()
    for input_file in input_files:
        with open(input_file, 'rb') as f:
            pdf = PyPDF2.PdfReader(f)
            for page in range(len(pdf.pages)):
                merger.append(pdf, pages=(page, page + 1))
    with open(output_file, 'wb') as f:
        merger.write(f)

def split_pdf_pages(pdf_file_path):
    print("正在处理PDF文件：",pdf_file_path)
    pdf=PyPDF2.PdfReader(open(pdf_file_path,'rb'))
    page_index=1
    for page in pdf.pages:
        out_pdf_path=pdf_file_path[:-4]+"_"+str(page_index)+".pdf"
        writer=PyPDF2.PdfWriter()
        writer.add_page(page)
        writer.write(out_pdf_path)
        page_index+=1


    """处理图片，使其变得可打印"""
def process_image(image_path):
    image=cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)

    # 1. 复制图层并进行高斯模糊
    blurred = cv2.GaussianBlur(image, (201, 201), 0).astype(float)
    # 2. 实现“划分”模式
    epsilon = 1e-7
    divided = image / (blurred + epsilon)
    # 将结果缩放到0-255范围并转换为8位无符号整数
    divided = np.clip(divided * 255, 0, 255).astype(np.uint8)
    merged = divided.astype(float)  # 转换为浮点数以避免操作中的整数截断
    # 3. 实现正片叠底模式
    multiply = (divided * merged) / 255
    # ret,img=cv2.threshold(multiply,180,255,cv2.THRESH_BINARY)
    cv2.imwrite(image_path[:-4]+'_print.png',multiply)

def remove_quark_watermark(dir_path,resize=False):
    file_list=get_files(dir_path)
    for pdf_file_path in file_list:
        # 处理PDF文件
        if pdf_file_path[-4:].upper()=='.PDF':
            pdf_writer = PyPDF2.PdfWriter()
            has_mark = False
            with open(pdf_file_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                for page in reader.pages:
                    resources = page['/Resources']
                    if '/QuarkX2' in resources['/XObject']:
                        del resources['/XObject']['/QuarkX2']
                        has_mark = True
                        if resize:
                            w=page.cropbox.width
                            h=page.cropbox.height
                            wc=25
                            hc=60
                            page.cropbox.lower_left=(wc,hc)
                            page.cropbox.upper_right=(w-wc,h)
                    pdf_writer.add_page(page)

            if has_mark:
                os.chmod(pdf_file_path,stat.S_IWRITE)
                with open(pdf_file_path, 'wb') as pdf_file:
                    pdf_writer.write(pdf_file)
                    print("\033[32m夸克水印已经删除：", pdf_file_path,"\033[0m")
            else:
                print("\033[31m",pdf_file_path, "该文件没有夸克水印\033[0m")

def md5_file(file_path):
    with open(file_path, 'rb') as f:
        md5_obj = hashlib.md5()
        md5_obj.update(f.read())
        return md5_obj.hexdigest()
def md5_str(input_str):
    return hashlib.md5(input_str.encode('utf-8')).hexdigest()

def sha256_file(file_path):
    with open(file_path, 'rb') as f:
        sha256_obj = hashlib.sha256()
        sha256_obj.update(f.read())
        return sha256_obj.hexdigest()

def sha256_str(input_str):
    return hashlib.sha256(input_str.encode('utf-8')).hexdigest()
def get_file_size(file_path):
    return os.path.getsize(file_path)
def get_file_md5(file_path):
    return md5_file(file_path)
def get_file_sha256(file_path):
    return sha256_file(file_path)

def screen_shot(file_path):
    pyautogui.screenshot(file_path)

def pyautogui_test():

    time.sleep(1)
    pyautogui.hotkey('win', 'r')
    time.sleep(1)
    pyautogui.typewrite('notepad')
    time.sleep(1)
    pyautogui.press('shift')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.typewrite('hello  world')
    pyautogui.press('shift')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 's')
    time.sleep(1)
    pyautogui.typewrite('test.txt')
    time.sleep(1)
    pyautogui.press('enter')

def img_ocr(img_path):
    ocr=PaddleOCR()
    result=ocr.ocr(img_path,cls=True)[0]
    save_path=img_path[:-4]+'.txt'
    f=open(save_path,'w')
    for item in result:
        f.write(item[1][0]+'\n')


"操作sqlite3数据库"
class SqliteHelper:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    # sqlite.execute_sql("create table users(id integer,name text,sex text,weight real)")
    def execute_sql(self, sql, params=None):
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
            self.conn.commit()
    def close(self):
        self.cursor.close()
        self.conn.close()


# POST /jypx_api/vote/voteActivityByPoll.do HTTP/1.1
# Accept: application/json, text/javascript, */*; q=0.01
# Accept-Encoding: gzip, deflate, br, zstd
# Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
# Connection: keep-alive
# Content-Length: 135
# Content-Type: application/x-www-form-urlencoded; charset=UTF-8
# Cookie: JSESSIONID=224182DD2AC0C610A4B3B75E7F9DA2B5; cid=726618452279698476; Hm_lvt_b955e5560e41ea4554b7bd63a51df6d2=1732095736; %24loginInfo=%7B%22userName%22%3A%2218037612380%22%2C%22password%22%3A%22e10adc3949ba59abbe56e057f20f883e%22%2C%22companyId%22%3A%22726618452279698476%22%7D; info=%7B%22birthday%22%3A%22%22%2C%22city%22%3Anull%2C%22county%22%3Anull%2C%22promoterGrade%22%3A1%2C%22agentLevel%22%3Anull%2C%22userImage%22%3A%22http%3A%2F%2Fdawnfox.cn%2Fjypx%2Fcommon%2Fcommon_head.png%22%2C%22province%22%3Anull%2C%22viewName%22%3A%22112%22%2C%22aliPayAccountName%22%3A%22%22%2C%22nickname%22%3A%22112%22%2C%22email%22%3Anull%2C%22regeistTime%22%3A%222024-11-20%2015%3A35%3A15%22%2C%22wxNum%22%3Anull%2C%22address%22%3Anull%2C%22isPayPasswordSeted%22%3Atrue%2C%22aliPayAccount%22%3A%22%22%2C%22sex%22%3Anull%2C%22mobile%22%3A%2218037612380%22%2C%22postcode%22%3Anull%2C%22isBindBankCard%22%3Afalse%2C%22userName%22%3A%22MunfZ0T000793385%22%2C%22userId%22%3A10919484%2C%22realName%22%3Anull%2C%22companyId%22%3A%22726618452279698476%22%2C%22memberGrade%22%3A1%2C%22userRole%22%3A%22member%22%7D; state=%7B%22token%22%3A%22e29c800729124ed82eba46eae854624a_wap%22%2C%22companyId%22%3A%22726618452279698476%22%7D; Hm_lpvt_b955e5560e41ea4554b7bd63a51df6d2=1732095842; shareUrl=https%3A%2F%2Fdawnfox.cn%2Fjypx_api%2Fweixin%2Fshare%3FcompanyId%3D726618452279698476%26shareUserId%3D10919484%26url%3Dhttps%3A%2F%2Fdawnfox.cn%2Fjypx%2Fvote%2Fvotedetails.html%26param%3DactivityId%3D720%24companyId%3D726618452279698476%24cid%3D726618452279698476
# DNT: 1
# Host: dawnfox.cn
# Origin: https://dawnfox.cn
# Referer: https://dawnfox.cn/jypx/vote/votedetails.html?activityId=720&companyId=726618452279698476
# Sec-Fetch-Dest: empty
# Sec-Fetch-Mode: cors
# Sec-Fetch-Site: same-origin
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0
# X-Requested-With: XMLHttpRequest
# sec-ch-ua: "Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"
# sec-ch-ua-mobile: ?0
# sec-ch-ua-platform: "Windows"


if __name__ == '__main__':
    pass


