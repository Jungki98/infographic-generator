from . import text as tx
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random
import io
import os
import math

def size(text) :
    length = 0
    for char in text:
        if '가' <= char <= '힣':  # 한글 범위
            length += 3
        elif 'a' <= char <= 'z' or 'A' <= char <= 'Z':  # 영어 알파벳 범위
            length += 2
        elif char == ' ':  # 스페이스바
            length += 1
        if '0' <= char <= '9':  # 숫자 범위
            length += 2
    return length

class TextOverlayImage:
    def __init__(self, image_path=None, canvas_width=2000, canvas_height=2000):
        if image_path:
            self.original_image = Image.open(image_path)
            self.image = self.original_image.resize((canvas_width, canvas_height), resample=Image.Resampling.LANCZOS)
        else:
            self.image = Image.new('RGB', (canvas_width, canvas_height), 'white')
        self.draw = ImageDraw.Draw(self.image)
        self.members = [] 

    def add_text_box(self, text, x, y, text_color, box_color, font_path="NanumGothic.ttf", font_size=20, limitsize = 40):
        
        if(size(text) > limitsize) :
            font_size = int(font_size * 0.666)
        
        font_path = os.path.join(os.path.dirname(__file__), font_path)  # 절대 경로로 폰트 파일 불러오기
        font = ImageFont.truetype(font_path, font_size)
        text_width = font.getlength(text)
        _, text_height = font.getbbox(text)[2:]
        
        x = x - text_width / 2
        
        box_left = x
        box_top = y
        box_right = x + text_width
        box_bottom = y + text_height
        # 텍스트 상자 그리기
        self.draw.rectangle([(box_left, box_top), (box_right, box_bottom)], fill=box_color)
        # 텍스트 그리기
        self.draw.text((x, y), text, font=font, fill=text_color)
        # 텍스트 상자와 텍스트를 하나의 객체로 저장
        text_box = {
            "text": text,
            "box": [(box_left, box_top), (box_right, box_bottom)],
            "text_color": text_color,
            "box_color": box_color,
            "font": font,
            "font_size": font_size
        }
        self.members.append(text_box)

    def add_box(self, x, y, x_width, y_height, box_color):
        box_left = x
        box_top = y
        box_right = x_width + x
        box_bottom = y_height + y
        # 텍스트 상자 그리기
        self.draw.rectangle([(box_left, box_top), (box_right, box_bottom)], fill=box_color)
        only_box = {
            "box": [(box_left, box_top), (box_right, box_bottom)],
            "box_color": box_color
        }
        self.members.append(only_box)
    
    def add_circle(self, x, y, radius, circle_color):
        circle_left = x - radius
        circle_top = y - radius
        circle_right = x + radius
        circle_bottom = y + radius
        # 원 그리기
        self.draw.ellipse([(circle_left, circle_top), (circle_right, circle_bottom)], fill=circle_color)
        only_circle = {
            "circle": [(circle_left, circle_top), (circle_right, circle_bottom)],
            "circle_color": circle_color,
            "radius": radius
        }
        self.members.append(only_circle)
        
    def add_regular_polygon(self, center_x, center_y, radius, num_sides, polygon_color):
        polygon_points = []
        for i in range(num_sides):
            angle = 2 * math.pi * i / num_sides
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            polygon_points.append((int(x), int(y)))
        # 정다각형 그리기
        self.draw.polygon(polygon_points, fill=polygon_color)
        only_polygon = {
            "points": polygon_points,
            "polygon_color": polygon_color,
            "radius": radius,
            "num_sides": num_sides
        }
        self.members.append(only_polygon)
        
    def add_triangle(self, x1, y1, x2, y2, x3, y3, color):
        self.draw.polygon([x1, y1, x2, y2, x3, y3], fill=color) 

    def save(self, output_path):
        byte_io = io.BytesIO()
        self.image.save(byte_io, format='JPEG')
        byte_array = byte_io.getvalue()
        return byte_array        