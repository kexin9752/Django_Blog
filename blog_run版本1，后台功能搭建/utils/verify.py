import os
import random
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from django.http import HttpResponse


class VerifyCode:
    def __init__(self,dj_request):
        self.dj_request = dj_request
        self.width = 100
        self.height = 30
        self.code_len = 4
        self.session_key = "verify_code"

    def gen_code(self):
        code = self.gen_code_num()
        self.dj_request.session[self.session_key] = code

        #指定颜色
        str1 = 'AliceBlue,AntiqueWhite,Aqua,Aquamarine,Azure,Beige,Bisque,Black,BlanchedAlmond,Blue,BlueViolet,Brown'
        color = str1.split(',')
        font_color = ['black', 'darkblue', 'darkred', 'brown', 'green', 'darkmagenta', 'cyan', 'darkcyan']
        bg_color = (random.randint(230,255),random.randint(1,25),random.randint(230,255))

        #字体路径
        font_path = os.path.join(settings.BASE_DIR,"static","fonts","timesbi.ttf")

        #创建图片
        im = Image.new('RGB',(self.width,self.height),bg_color)
        draw = ImageDraw.Draw(im)

        #画干扰线

        for i in range(random.randrange(1,int(self.code_len / 2)+1)):
            line_color = random.choice(color)
            num = random.randint(0,10)
            width_num = random.randint(1,3)
            draw.line((num,random.randint(0,self.height),self.width-num,random.randint(0,self.height)),fill=line_color,width=width_num)

        for index,char in enumerate(code):
            font_num = 1/random.randint(2,5)
            if index == 0:
                index += 1/random.randint(3,6)
            point = (index * self.width / (self.code_len-font_num),random.randrange(self.height/3))
            code_color = random.choice(font_color)
            font_size = random.randrange(15,25)
            font = ImageFont.truetype(font_path,font_size)
                    #位置    内容  字体     颜色
            draw.text(point,char,font=font,fill=code_color)


        #传入IO流
        buf = BytesIO()
        im.save(buf,'gif')
        return HttpResponse(buf.getvalue(),"image/gif")




    def gen_code_num(self):
        code_list = [chr(i) for i in list(range(65,91))+list(range(97,123))] + [str(j) for j in range(10)]
        code = ''.join(random.sample(code_list,4))
        return code



    def validate_code(self,code):
        code = str(code).lower()
        vcode = self.dj_request.session.get(self.session_key,'')
        return code == vcode.lower()


if __name__ == "__main__":
    c = VerifyCode(None)
    c.gen_code_num()

