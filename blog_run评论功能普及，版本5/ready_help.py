# u_mail = request.POST.get('u_mail')
# mycity = request.POST.get('mycity')
# u_url = request.POST.get('u_url')
# user = request.user
# if user.id:
#     comment.user_id = user.id
#     comment.u_name = user.username
# else:
#     comment.u_name = u_name
# if u_mail:          #保存一级评论的email
#     try:
#         comment.u_mail = u_mail
#     except Exception as e:
#         data = {
#             'msg': '邮箱格式不对',
#             'status': 0,
#         }
#         return JsonResponse(data)
# if mycity:          #保存一级评论的地址
#     comment.mycity = mycity
# if u_url:           #保存一级评论的网站关联
#     comment.u_url = u_url
#
# comment.txtContent = txtContent  #保存一级评论的内容