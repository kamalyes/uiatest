# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
@File  :Verification.py
@Author:v_yanqyu
@Desc  : 验证码自动解析库
@Date  :2020/9/25-22:19
'''
import random
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

_numbers = ''.join(map(str, [i for i in range(10) if i != 4]))  # 数字
init_chars = ''.join(_numbers)


def create_validate_code(size=(75, 30),
                         chars=init_chars,
                         mode="RGB",
                         bg_color=(230, 230, 230),
                         font_size=26,
                         font_type='fonts/DejaVuSans.ttf',  # # Windows - ARIAL, Linux - DejaVuSans
                         length=4,
                         n_line=(1, 2),
                         point_chance=1):
    '''
    @todo: 生成验证码图片
    @param size: 图片的大小，格式（宽，高），默认为(120, 30)
    @param chars: 允许的字符集合，格式字符串
    @param img_type: 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
    @param mode: 图片模式，默认为RGB
    @param bg_color: 背景颜色，默认为白色
    @param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
    @param font_size: 验证码字体大小
    @param font_type: 验证码字体的详细路径，默认为 ae_AlArabiya.ttf
    @param length: 验证码字符个数
    @param draw_lines: 是否划干扰线
    @param n_lines: 干扰线的条数范围，格式元组，默认为(1, 2)，只有draw_lines为True时有效
    @param draw_points: 是否画干扰点
    @param point_chance: 干扰点出现的概率，大小范围[0, 100]
    @return: [0]: PIL Image实例
    @return: [1]: 验证码图片中的字符串
    '''
    width, height = size  # 宽， 高
    img = Image.new(mode, size, bg_color)  # 创建图形
    draw = ImageDraw.Draw(img)  # 创建画笔

    def get_chars():
        '''生成给定长度的字符串，返回列表格式'''
        return random.sample(chars, length)

    def create_lines():
        '''绘制干扰线'''
        line_num = random.randint(*n_line)  # 干扰线条数
        for i in range(line_num):
            # 起始点
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))
            # 结束点
            end = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line([begin, end], fill=(0, 0, 0))

    def create_points():
        '''绘制干扰点'''
        chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def getRandomColor():
        '''获取一个随机颜色(r,g,b)格式的'''
        c1 = random.randint(30, 225)
        c2 = random.randint(30, 200)
        c3 = random.randint(30, 205)
        return (c1, c2, c3)

    def create_strs():
        '''绘制验证码字符'''
        font_path = os.path.dirname(__file__) + "\\" + font_type
        c_chars = get_chars()
        strs = ' %s ' % ' '.join(c_chars)  # 每个字符前后以空格隔开
        font = ImageFont.truetype(font_path, font_size)
        # font = ImageFont.load_default().font
        font_width, font_height = font.getsize(strs)
        font_width += 5
        for i in range(len(c_chars)):
            draw.text((5 + i * 18, (height - font_height) / 3), c_chars[i], getRandomColor(), font=font)
        return ''.join(c_chars)
    strs = create_strs()

    buf = BytesIO()
    img.save(buf, 'png')
    bufStr = buf.getvalue()

    return bufStr, strs


if __name__ == "__main__":
    code_img, strs = create_validate_code()
    print(os.path.basename(os.getcwd()))
