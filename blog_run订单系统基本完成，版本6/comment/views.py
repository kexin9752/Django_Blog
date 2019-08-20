from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import View

from comment.models import CommentModel, ReCommentModel
from utils.verify import VerifyCode


class CommentView(View):

    #存评论数据的视图
    def post(self,request):
        # 默认提交失败
        data = {
            'msg': '评论提交失败,请重试',
            'status': 0,
        }
        print(request.POST)  #打印看一下post提交过来的内容
        txtCode = request.POST.get('txtCode') #提取出验证码
        v_code = VerifyCode(request)  #验证验证码
        if not v_code.validate_code(txtCode):  #如果验证码验证不通过，则报错返回前端
            data = {
                'msg': '验证码错啦',
                'status': 0,
            }
            return JsonResponse(data)



        # if art_uid:  #如果uid对应的文章存在
        u_name = request.POST.get('u_name')  #获取评论用户的名称
        txtContent = request.POST.get('txtContent')  #获取评论内容
        u_code = request.POST.get('u_code')  #获取一级评论的uid
        u_recode = request.POST.get('u_recode')  #获取子评论的uid
        if u_recode:  #判断此提交的评论是否为二级评论，如果是则存进数据表
            cmt = get_object_or_404(ReCommentModel, u_code=u_recode) #获取子评论的回复对象
            re_cmt = ReCommentModel() #获取子评论表的对象
            re_cmt.self_reply = cmt #外键关联要回复的子评论对象
            re_cmt.to_code = u_code #保存回复的一级评论的uid，定位自己在哪一个一级评论下
            re_cmt.to_recode = u_recode #保存回复的二级评论的uid，这里的uid存的是子评论表中的评论的uid
            re_cmt.txtContent = txtContent #保存回复内容
            re_cmt.u_name = u_name #保存回复者的名称
            re_cmt.save()  #这里保存的是回复子评论的内容
            data = {
                'msg': '评论提交成功',
                'status': 1,
            }
            return JsonResponse(data)

        if u_code:
            cmt = get_object_or_404(CommentModel,u_code=u_code)  #外键关联一级评论对象
            re_cmt = ReCommentModel()
            re_cmt.comment = cmt  #保存一级评论对象
            re_cmt.to_code = u_code  #保存一级评论的uid
            re_cmt.txtContent = txtContent  #保存回复内容
            re_cmt.u_name = u_name  #保存回复者名字
            re_cmt.save()  #这里保存的是回复一级评论的内容
            data = {
                'msg': '评论提交成功',
                'status': 1,
            }
            return JsonResponse(data)


        art_uid = request.POST.get('art_uid')  # 取评论所在文章的uid，保证评论与文章相关联
        note_id = request.POST.get('note_id')
        photo_id = request.POST.get('photo_id')
        mall_uid = request.POST.get('mall_uid')
        comment = CommentModel()
        if art_uid:
            self.help_save(request,comment,u_name,txtContent)
            comment.art_uid = art_uid  #保存文章uid
            comment.save()   #这里保存的是一级评论的内容
        elif note_id:
            self.help_save(request,comment,u_name,txtContent)
            comment.note_id = note_id
            comment.save()
        elif photo_id:
            self.help_save(request,comment,u_name,txtContent)
            comment.photo_id = photo_id
            comment.save()
        elif mall_uid:
            self.help_save(request,comment,u_name,txtContent)
            comment.mall_uid = mall_uid
            comment.save()
        data = {
            'msg': '评论提交成功',
            'status': 1,
        }
        return JsonResponse(data)

    def help_save(self,request,comment,u_name,txtContent):
        u_mail = request.POST.get('u_mail')
        mycity = request.POST.get('mycity')
        u_url = request.POST.get('u_url')
        user = request.user
        if user.id:
            comment.user_id = user.id
            comment.u_name = user.username
        else:
            comment.u_name = u_name
        if u_mail:  # 保存一级评论的email
            try:
                comment.u_mail = u_mail
            except Exception as e:
                data = {
                    'msg': '邮箱格式不对',
                    'status': 0,
                }
                return JsonResponse(data)
        if mycity:  # 保存一级评论的地址
            comment.mycity = mycity
        if u_url:  # 保存一级评论的网站关联
            comment.u_url = u_url

        comment.txtContent = txtContent  # 保存一级评论的内容

    # def help_save(self,request,art_uid):
    #     u_name = request.POST.get('u_name')  # 获取评论用户的名称
    #     txtContent = request.POST.get('txtContent')  # 获取评论内容
    #     u_code = request.POST.get('u_code')  # 获取一级评论的uid
    #     u_recode = request.POST.get('u_recode')  # 获取子评论的uid
    #     if u_recode:  # 判断此提交的评论是否为二级评论，如果是则存进数据表
    #         cmt = get_object_or_404(ReCommentModel, u_code=u_recode)  # 获取子评论的回复对象
    #         re_cmt = ReCommentModel()  # 获取子评论表的对象
    #         re_cmt.self_reply = cmt  # 外键关联要回复的子评论对象
    #         re_cmt.to_code = u_code  # 保存回复的一级评论的uid，定位自己在哪一个一级评论下
    #         re_cmt.to_recode = u_recode  # 保存回复的二级评论的uid，这里的uid存的是子评论表中的评论的uid
    #         re_cmt.txtContent = txtContent  # 保存回复内容
    #         re_cmt.u_name = u_name  # 保存回复者的名称
    #         re_cmt.save()  # 这里保存的是回复子评论的内容
    #         data = {
    #             'msg': '评论提交成功',
    #             'status': 1,
    #         }
    #         return JsonResponse(data)
    #
    #     if u_code:
    #         cmt = get_object_or_404(CommentModel, u_code=u_code)  # 外键关联一级评论对象
    #         re_cmt = ReCommentModel()
    #         re_cmt.comment = cmt  # 保存一级评论对象
    #         re_cmt.to_code = u_code  # 保存一级评论的uid
    #         re_cmt.txtContent = txtContent  # 保存回复内容
    #         re_cmt.u_name = u_name  # 保存回复者名字
    #         re_cmt.save()  # 这里保存的是回复一级评论的内容
    #         data = {
    #             'msg': '评论提交成功',
    #             'status': 1,
    #         }
    #         return JsonResponse(data)
    #
    #     comment = CommentModel()
    #     u_mail = request.POST.get('u_mail')
    #     mycity = request.POST.get('mycity')
    #     u_url = request.POST.get('u_url')
    #     user = request.user
    #     if user.id:
    #         comment.user_id = user.id
    #         comment.u_name = user.username
    #     else:
    #         comment.u_name = u_name
    #     if u_mail:  # 保存一级评论的email
    #         try:
    #             comment.u_mail = u_mail
    #         except Exception as e:
    #             data = {
    #                 'msg': '邮箱格式不对',
    #                 'status': 0,
    #             }
    #             return JsonResponse(data)
    #     if mycity:  # 保存一级评论的地址
    #         comment.mycity = mycity
    #     if u_url:  # 保存一级评论的网站关联
    #         comment.u_url = u_url
    #
    #     comment.txtContent = txtContent  # 保存一级评论的内容
    #     comment.art_uid = art_uid  # 保存文章uid
    #     comment.save()  # 这里保存的是一级评论的内容
    #     data = {
    #         'msg': '评论提交成功',
    #         'status': 1,
    #     }

class CommentLoad(View):
    """
    关键：因为ajax是将一级与其二级评论放在同一个json数据（也就相当于一个一层完整的评论数据放在
    一个字典中（而且是没有内嵌的字典中），然后再将每一层数据嵌套在一个字典内，以json格式返
    回，所以在实现多级评论的时候，需要对字典的子评论数量进行统计，然后用循环更改键值，放置
    冲突）
    """
    def get(self,request):
        art_uid = request.GET.get('art')
        comment_count = CommentModel.objects.filter(art_uid=art_uid).count()
        if not art_uid:
            photo_id = request.GET.get('photo_id')
            mall_uid = request.GET.get('mall')
            if photo_id:
                comment_count = CommentModel.objects.filter(photo_id=photo_id).count()
            elif mall_uid:
                comment_count = CommentModel.objects.filter(mall_uid=mall_uid).count()
        return HttpResponse(comment_count)

    def post(self,request):
        page_size = int(request.GET.get('page_size'))
        page_id = request.GET.get('page_index')
        art_uid = request.GET.get('art')  #在url中放入文章的uid，让评论加载的视图明白这是为哪一篇文章加载评论数据
        comment_list = CommentModel.objects.filter(art_uid=art_uid)  # 获取所有本文章的评论
        if not art_uid:
            photo_id = request.GET.get('photo_id')
            mall_uid = request.GET.get('mall')
            if photo_id:
                comment_list = CommentModel.objects.filter(photo_id=photo_id)
            elif mall_uid:
                comment_list = CommentModel.objects.filter(mall_uid=mall_uid)
        print(comment_list)
        data = {} #提前声明一个即将返回的字典数据容器data
        if comment_list.count() > 0:
            p = Paginator(comment_list,page_size)
            page = p.page(page_id)
            comment_list = page.object_list
            for i in range(comment_list.count()):  #循环评论数据
                dict1 = {}  #申明一个用来装每一层评论数据的字典容器
                dict1['content'] = comment_list[i].txtContent  #加入评论内容
                dict1['img_url'] = comment_list[i].img  #加入评论者头像
                dict1['user_name'] = comment_list[i].u_name  #加入评论者名字
                dict1['add_time'] = comment_list[i].created_at  #加入评论时间
                dict1['city'] = comment_list[i].mycity  #加入所在城市，默认未知
                u_code = comment_list[i].u_code #取出该评论的uid
                dict1['u_code'] = u_code  #加入文章uid
                #取出这篇文章所有与该一级评论有关的子评论
                re_comment_list = ReCommentModel.objects.filter(to_code=u_code)
                if re_comment_list:
                    for j in range(re_comment_list.count()):  #循环取出
                        dict1['is_reply_count'] = j+1  #为子评论的数量计数
                        dict1['reply_time'+str(j+1)] = re_comment_list[j].created_at #加入回复时间
                        dict1['reply_content' + str(j + 1)] = re_comment_list[j].txtContent #加入回复内容
                        dict1['reply_name' + str(j + 1)] = re_comment_list[j].u_name #加入回复者名称
                        u_recode = re_comment_list[j].u_code #取出该子评论的uid
                        dict1['u_recode'+str(j+1)] = u_recode #加入该子评论的uid
                        if re_comment_list[j].self_reply:  #判断这个子评论的回复对象是否为子评论
                            #如果是，则调用子评论表中的to_recode字段，这个字段中存的全是回复的子评论uid，
                            # 然后在子评论表中检索对应子评论
                            to_reply = ReCommentModel.objects.filter(u_code=re_comment_list[j].to_recode).first()
                            dict1['to_reply_name'+str(j+1)] = to_reply.u_name  #加入被评论的子评论的发表人的名称
                        else:
                            #如果是回复一级评论的子评论，则被回复的对象名称为一级评论的发表人的名称
                            dict1['to_reply_name' + str(j + 1)] = comment_list[i].u_name
                #将该层评论的所有数据存入data中
                data['a'+str(i)] = dict1
        return JsonResponse(data)

        # data = {'a':{
        #     'content': '注意，这是一条测试的评论',
        #     'img_url': '6',
        #     'user_name': '我是匿名',
        #     'add_time': '2019年某月某日某时',
        #     'city': '北京市朝阳区',
        # },
        #     'b': {
        #         'content': '注意，这是一条测试的评论',
        #         'img_url': '6',
        #         'user_name': '我是匿名',
        #         'add_time': '2019年某月某日某时',
        #         'city': '北京市朝阳区',
        #         'is_reply_count':2,
        #         'reply_time1': '二级回复的时间',
        #         'reply_content1': '二级回复的内容',
        #         'reply_time2': '二级回复的时间',
        #         'reply_content2': '二级回复的内容',
        #     }
        # }
