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





# {% for order in object_list %}
# {#                      {% with a=c.article %}#}
#                       <tr>
#                         <td width="20" align="center">
#                           <input name="checkId" class="checkall" type="checkbox" value="{{ order.id }}" >
#                         </td>
#                         <td><a target="_blank" href="javascript:;">{{ order.order_sn }}</a></td>
#                         <td>{{ order.order_address.address }}</td>
#                         <td>{{ order.goods_count }}</td>
#                         <td>{{ order.order_price }}</td>
#                         <td>{{ order.order_status }}</td>
#                         <td>{{ order.created_at }}</td>
#                         <td align="center">
#                             <select onchange="ChooseExec(this.value)">
#                                 <option class="first_opt" value="3">请选择</option>
#                                 <option value="1">去支付</option>
#                                 <option value="2">删除</option>
#                             </select>
#
# {#                            <select name="" id="">#}
# {#                                <option onclick="OrderPostBack({{ c.id }});" value="" style="">去支付</option>#}
# {#                                <option onclick="ExecPostBack({{ c.id }});"  value="">删除</option>#}
# {#                            </select>#}
#                         </td>
#                       </tr>
# {#                      {% endwith %}#}
#                     {% endfor %}