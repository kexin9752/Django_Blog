

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import F

import constants
from article.models import Article
from mall.models import Goods


class User(AbstractUser):
    nickname = models.CharField('昵称',max_length=64,null=True,blank=True)
    sign = models.CharField('个性签名',max_length=32,default='困而知之,学而知之,生而知之')
    balance = models.DecimalField('余额',max_digits=7, decimal_places=2,default=0)
    integral = models.IntegerField("用户的积分", default=0)
    is_fresh = models.BooleanField('是否刷新', default=1)
    level = models.IntegerField('用户等级', default=0)
    growth_value = models.IntegerField('成长值',default=0)
    ip = models.CharField('用户本次IP',max_length=64,default='暂无记录')
    before_ip = models.CharField('用户上次IP',max_length=64,default='暂无记录')

    class Meta:
        db_table = "accounts_user"
        verbose_name_plural = '用户列表'

    def sum_balance(self,num,status=1):
        if status == 1:
            self.balance = F('balance') + abs(num)
        else:
            self.balance = F('balance') - abs(num)
        self.save()
        self.refresh_from_db()

    def sum_integral(self,num,status=1):
        if status == 1:
            self.integral = F('integral') + int(num)
            # self.user_integral.get(user=self).detail = '+'+str(num)
        else:
            self.integral = F('integral') - int(num)
        self.save()
        self.refresh_from_db()

    def integral_save(self,num,source,status=1):
        if status == 1:
            detail = '+'+str(num)
        else:
            detail = '-'+str(num)
        UserIntegral.objects.create(user=self, detail=detail, source=source)

    @property
    def default_addr(self):
        addr = None
        user_list = self.user_addr.filter(is_valid=True)
        try:
            addr = user_list.filter(is_default=True)[0]
        except IndexError:
            try:
                addr = user_list[0]
            except IndexError:
                pass
        return addr

    def ip_save(self,ip):
        self.before_ip = self.ip
        self.ip = ip
        self.save()

    def __str__(self):
        return self.username


class UserProfile(models.Model):

    user = models.OneToOneField(User)
    avatar = models.ImageField('图片', upload_to='avatar', null=True, blank=True)
    real_name = models.CharField("真实姓名",max_length=32,null=True,blank=True)
    is_email_valid = models.BooleanField("邮箱是否验证",default=False)
    phone_no = models.CharField("手机电话",max_length=20,null=True,blank=True)
    is_phone_valid = models.BooleanField("手机电话是否已经验证",default=False)
    gender = models.SmallIntegerField("性别",choices=constants.USER_GENDER_CHOICES,default=constants.USER_GENDER_SHADOW)
    age = models.DateField("年龄",null=True,blank=True)
    qq = models.IntegerField('QQ账号',null=True,blank=True)
    province = models.CharField("省份", max_length=32,null=True,blank=True)
    city = models.CharField("城市", max_length=32,null=True,blank=True)
    area = models.CharField("区域", max_length=32,null=True,blank=True)
    address = models.CharField("详细地址", max_length=64,null=True,blank=True)

    created_at = models.DateTimeField("创建时间",auto_now_add=True)
    updated_at = models.DateTimeField("更新时间",auto_now=True)

    class Meta:
        db_table = "accounts_user_profile"
        verbose_name_plural = '用户详情'

    def __str__(self):
        return self.user.username


class Collect(models.Model):
    article = models.ForeignKey(Article,related_name='collect')
    user = models.ForeignKey(User,related_name='user_collect')
    classify = models.CharField('文章类别',max_length=32)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name_plural = '用户收藏'


class LoginRecord(models.Model):
    user = models.ForeignKey(User,related_name='user_record')
    username = models.CharField("登录的用户名",max_length=64)
    ip = models.CharField("ip地址",max_length=32)
    address = models.CharField("登录地址",max_length=32,null=True,blank=True)
    source = models.CharField("登录的来源",max_length=32,null=True,blank=True)
    integral = models.IntegerField('用户积分', default=0)
    created_at = models.DateTimeField("登录的时间",auto_now_add=True)

    class Meta:
        db_table = "accounts_login_record"
        verbose_name_plural = '登录历史'

    def __str__(self):
        return self.username


class UserAddress(models.Model):
    user = models.ForeignKey(User,related_name='user_addr')
    province = models.CharField("省份",max_length=32)
    city = models.CharField("城市",max_length=32)
    area = models.CharField("区域",max_length=32)
    town = models.CharField("街道",max_length=32,null=True,blank=True)
    address = models.CharField("详细地址",max_length=64)
    username = models.CharField("收件人",max_length=32)
    phone = models.CharField("收件人电话",max_length=32)
    is_default = models.BooleanField("是否为默认地址",default=False)
    is_valid = models.BooleanField("是否为有效地址",default=True)

    created_at = models.DateTimeField("创建时间",auto_now_add=True)
    updated_at = models.DateTimeField("更新时间",auto_now=True)

    class Meta:
        db_table = "accounts_user_address"
        ordering = ["-is_default","-updated_at"]
        verbose_name_plural = '用户地址'

    def get_phone_format(self):
        return self.phone[0:3]+"****"+self.phone[7:]

    def get_region_format(self):
        return '{} {} {}'.format(self.province,self.city,self.area)


class UserIntegral(models.Model):
    user = models.ForeignKey(User,related_name='user_integral')
    source = models.CharField('积分来源',max_length=200,default='每日登陆获得积分')
    detail = models.CharField('积分明细',max_length=16,default='+5')
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)



class UserBalance(models.Model):
    user = models.ForeignKey(User, related_name='user_balance')
    sn = models.CharField('充值单号',max_length=128)
    method = models.CharField('支付方式',max_length=32)
    cash = models.DecimalField('充值金额',max_digits=7, decimal_places=2,default=0)
    status = models.SmallIntegerField('支付状态',choices=constants.USER_BALANCE_STATUS,default=constants.USER_UNPAY)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)


class PasswdChangeLog(models.Model):
    user = models.ForeignKey(User,related_name='pw_change')
    old_passwd = models.CharField("未修改的密码",max_length=32)
    new_passwd = models.CharField("修改后的密码",max_length=32)
    created_at = models.DateTimeField("修改的时间",auto_now_add=True)

    class Meta:
        db_table = "accounts_passwd_change_log"
        verbose_name_plural = '密码更改历史'


class Order(models.Model):
    user = models.ForeignKey(to=User, related_name='order',on_delete=models.CASCADE, verbose_name="订单用户")
    order_address = models.ForeignKey(to=UserAddress, related_name='order',on_delete=models.CASCADE, verbose_name="订单地址", blank=True,null=True)
    order_sn=models.CharField(max_length=32,verbose_name="id订单编号")
    goods_count=models.IntegerField(verbose_name="商品数量")
    order_price=models.FloatField(verbose_name="订单总价")
    order_status=models.SmallIntegerField('订单状态',choices=constants.ORDER_STATUS_CHOICES,default=constants.ORDER_STATUS_SUBMIT)
    remark = models.CharField("备注", max_length=256, null=True, blank=True)

    express_type = models.CharField("快递信息", max_length=32, null=True, blank=True)
    express_no = models.CharField("快递单号", max_length=64, null=True, blank=True)
    status = models.SmallIntegerField("订单状态", choices=constants.ORDER_STATUS_CHOICES,
                                      default=constants.ORDER_STATUS_SUBMIT)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name_plural = '订单管理'


class OrderDetail(models.Model):
    order=models.ForeignKey(to=Order,related_name='order_detail',on_delete=models.CASCADE,verbose_name="订单编号")
    goods_id=models.IntegerField(verbose_name="商品id")
    goods_name=models.CharField(max_length=32,verbose_name="商品名称")
    goods_price=models.FloatField(verbose_name="商品价格")
    goods_number=models.IntegerField(verbose_name="商品购买数量")
    goods_total=models.FloatField(verbose_name="商品总价")
    goods_store=models.IntegerField(verbose_name="商品id")
    goods_image = models.ImageField('商品图片',upload_to='%Y%m_order')


class Cart(models.Model):
    user = models.ForeignKey(User,related_name="carts",on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE,related_name='carts')
    name = models.CharField("商品名称",max_length=128)
    img = models.ImageField("商品主图",upload_to="cart")
    price = models.IntegerField("商品单价")
    count = models.PositiveIntegerField("购买的数量")
    total_price = models.FloatField("商品总价")
    created_at = models.DateTimeField("创建时间",auto_now_add=True)
    updated_at = models.DateTimeField("更新时间",auto_now=True)




