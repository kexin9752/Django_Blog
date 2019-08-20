/* 
*作者：一些事情
*时间：2015-4-17
*需要结合jquery和Validform和artdialog一起使用
----------------------------------------------------------*/

/*检测浏览器方法
------------------------------------------------*/
var pageurl = window.location.search;
if(pageurl == '?m2w') {
    addCookie('m2wcookie', '1', 0);
}
/*工具类方法
------------------------------------------------*/
//检测是否移动设备来访
function browserRedirect() { 
	var sUserAgent= navigator.userAgent.toLowerCase(); 
	var bIsIpad= sUserAgent.match(/ipad/i) == "ipad"; 
	var bIsIphoneOs= sUserAgent.match(/iphone os/i) == "iphone os"; 
	var bIsMidp= sUserAgent.match(/midp/i) == "midp"; 
	var bIsUc7= sUserAgent.match(/rv:1.2.3.4/i) == "rv:1.2.3.4"; 
	var bIsUc= sUserAgent.match(/ucweb/i) == "ucweb"; 
	var bIsAndroid= sUserAgent.match(/android/i) == "android"; 
	var bIsCE= sUserAgent.match(/windows ce/i) == "windows ce"; 
	var bIsWM= sUserAgent.match(/windows mobile/i) == "windows mobile"; 
	if (bIsIpad || bIsIphoneOs || bIsMidp || bIsUc7 || bIsUc || bIsAndroid || bIsCE || bIsWM) { 
		return true;
	} else { 
		return false;
	} 
}
//写Cookie
function addCookie(objName, objValue, objHours) {
    var str = objName + "=" + escape(objValue);
    if (objHours > 0) {//为0时不设定过期时间，浏览器关闭时cookie自动消失
        var date = new Date();
        var ms = objHours * 3600 * 1000;
        date.setTime(date.getTime() + ms);
        str += "; expires=" + date.toGMTString();
    }
    document.cookie = str;
}

//读Cookie
function getCookie(objName) {//获取指定名称的cookie的值
    var arrStr = document.cookie.split("; ");
    for (var i = 0; i < arrStr.length; i++) {
        var temp = arrStr[i].split("=");
        if (temp[0] == objName) return unescape(temp[1]);
    }
    return "";
}
//四舍五入函数
function ForDight(Dight, How) {
    Dight = Math.round(Dight * Math.pow(10, How)) / Math.pow(10, How);
    return Dight;
}
//只允许输入数字
function checkNumber(e) {
    var keynum = window.event ? e.keyCode : e.which;
    if ((48 <= keynum && keynum <= 57) || (96 <= keynum && keynum <= 105) || keynum == 8) {
        return true;
    } else {
        return false;
    }
}
//只允许输入小数
function checkForFloat(obj, e) {
    var isOK = false;
    var key = window.event ? e.keyCode : e.which;
    if ((key > 95 && key < 106) || //小键盘上的0到9  
        (key > 47 && key < 60) ||  //大键盘上的0到9  
        (key == 110 && obj.value.indexOf(".") < 0) || //小键盘上的.而且以前没有输入.  
        (key == 190 && obj.value.indexOf(".") < 0) || //大键盘上的.而且以前没有输入.  
         key == 8 || key == 9 || key == 46 || key == 37 || key == 39) {
        isOK = true;
    } else {
        if (window.event) { //IE
            e.returnValue = false;   //event.returnValue=false 效果相同.    
        } else { //Firefox 
            e.preventDefault();
        }
    }  
    return isOK;  
}
//复制文本
function copyText(txt){
	window.clipboardData.setData("Text",txt); 
	var d = dialog({content:'复制成功，可以通过粘贴来发送！'}).show();
	setTimeout(function () {
		d.close().remove();
	}, 2000);
}
//切换验证码
// function ToggleCode(obj, codeurl) {
//     $(obj).children("img").eq(0).attr("src", codeurl + "?time=" + Math.random());
// 	return false;
// }
//全选取消按钮函数，调用样式如：
function checkAll(chkobj){
	if($(chkobj).text()=="全选"){
	    $(chkobj).text("取消");
		$(".checkall").prop("checked", true);
	}else{
    	$(chkobj).text("全选");
		$(".checkall").prop("checked", false);
	}
}
//Tab控制选项卡
function tabs(tabObj, event) {
    //绑定事件
	var tabItem = $(tabObj).find(".tab-head ul li a");
	tabItem.bind(event,  function(){
		//设置点击后的切换样式
		tabItem.removeClass("selected");
		$(this).addClass("selected");
		//设置点击后的切换内容
		var tabNum = tabItem.parent().index($(this).parent());
		$(tabObj).find(".tab-content").hide();
        $(tabObj).find(".tab-content").eq(tabNum).show();
	});
}

//显示浮动窗口
function showWindow(obj){
	var tit = $(obj).attr("title");
	var box = $(obj).html();
	dialog({
		width:500,
		title:tit,
		content:box,
		okValue:'确定',
		ok:function (){ }
	}).showModal();
}

/*页面级通用方法
------------------------------------------------*/
//智能浮动层函数
$.fn.smartFloat = function() {
	var position = function(element) {
		var top = element.position().top, pos = element.css("position");
		var w = element.innerWidth();
		$(window).scroll(function() {
			var scrolls = $(this).scrollTop();
			if (scrolls > top) {
				if (window.XMLHttpRequest) {
					element.css({
						width: w,
						position: "fixed",
						top: 1
					});	
				} else {
					element.css({
						top: scrolls
					});	
				}
			}else {
				element.css({
					position: pos,
					top: top
				});	
			}
		});
	};
	return $(this).each(function() {
		position($(this));						 
	}); 
};
//搜索查询
function SiteSearch(send_url, divTgs, channel_name) {
    var strwhere = "";
    if (channel_name !== undefined) {
        strwhere = "&channel_name=" + channel_name
    }
	var str = $.trim($(divTgs).val());
	if (str.length > 0 && str != "输入关健字") {
	    window.location.href = send_url + "?keyword=" + encodeURI($(divTgs).val()) + strwhere;
	}
	return false;
}
//链接下载
function downLink(point, linkurl){
	if(point > 0){
		dialog({
			title:'提示',
			content:"下载需扣除" + point + "个积分<br />重复下载不扣积分，需要继续吗？",
			okValue:'确定',
			ok:function (){
				window.location.href = linkurl;
			},
			cancelValue: '取消',
			cancel: function (){}
		}).showModal();
	}else{
		window.location.href = linkurl;
	}
	return false;
}
//计算积分兑换
function numConvert(obj){
	var maxAmount = parseFloat($("#hideAmount").val()); //总金额
	var pointCashrate = parseFloat($("#hideCashrate").val()); //兑换比例
	var currAmount = parseFloat($(obj).val()); //需要转换的金额
	if(isNaN(currAmount)){
		$("#convertPoint").text('');
	}else {
	if(currAmount > maxAmount){
		currAmount = maxAmount;
		$(obj).val(maxAmount);
	}
	var convertPoint = currAmount * pointCashrate;
	$("#convertPoint").text(convertPoint);
}}

//执行删除操作
function ExecDelete(sendUrl, checkValue, urlObj,csrf){

	let csrf_token = $(csrf).val();
	//检查传输的值
	if (!checkValue) {
		dialog({title:'提示', content:'对不起，请选中您要操作的记录！', okValue:'确定', ok:function (){}}).showModal();
        return false;
	}
	dialog({
        title: '提示',
        content: '删除记录后不可恢复，您确定吗？',
        okValue: '确定',
        ok: function () {
            $.ajax({
				type: "post",
				url: sendUrl,
				dataType: "json",
				data: {
					"checkId":checkValue,
					csrfmiddlewaretoken:csrf_token
				},
				timeout: 200,
				success: function(data, textStatus) {
					if (data.status === 1){
						var tipdialog = dialog({content:data.msg}).show();
						setTimeout(function () {
							tipdialog.close().remove();
							if($(urlObj)){
								location.href = $(urlObj).val();
								console.log($(urlObj).val())
							}else{
								location.reload();
							}
						}, 2000);
					} else {
						dialog({title:'提示', content:data.msg, okValue:'确定', ok:function (){}}).showModal();
					}
				},
				error: function (XMLHttpRequest, textStatus, errorThrown) {
					dialog({title:'提示', content:'状态：' + textStatus + '；出错提示：' + errorThrown, okValue:'确定', ok:function (){}}).showModal();
				}
			});
        },
        cancelValue: '取消',
        cancel: function () { }
    }).showModal();
}

function CreateOrder(sendUrl, checkValue, urlObj){
	let csrf_token = $('#csrf').val();
	//检查传输的值
	if (!checkValue) {
		dialog({title:'提示', content:'对不起，请选中您要生成的订单！', okValue:'确定', ok:function (){}}).showModal();
        return false;
	}
	dialog({
        title: '提示',
        content: '注意：生成订单后需要在2小时内付款',
        okValue: '确定',
        ok: function () {
            $.ajax({
				type: "post",
				url: sendUrl,
				dataType: "json",
				data: {
					"checkId":checkValue,
					csrfmiddlewaretoken:csrf_token
				},
				timeout: 200,
				success: function(data, textStatus) {
					if (data.status === 1){
						var tipdialog = dialog({content:data.msg}).show();
						setTimeout(function () {
							tipdialog.close().remove();
							if($(urlObj)){
								location.href = $(urlObj).val();
								console.log($(urlObj).val())
							}else{
								location.reload();
							}
						}, 2000);
					} else {
						dialog({title:'提示', content:data.msg, okValue:'确定', ok:function (){}}).showModal();
					}
				},
				error: function (XMLHttpRequest, textStatus, errorThrown) {
					dialog({title:'提示', content:'状态：' + textStatus + '；出错提示：' + errorThrown, okValue:'确定', ok:function (){}}).showModal();
				}
			});
        },
        cancelValue: '取消',
        cancel: function () { }
    }).showModal();
}

function PayOrder(sendUrl, order_sn, current_integral,need_integral, urlObj){
	let csrf_token = $('#csrf').val();
	//检查传输的值
	if (Number(current_integral) < Number(need_integral)) {
		dialog({title:'提示', content:'对不起，支付失败，您的积分不足', okValue:'确定', ok:function (){}}).showModal();
        return false;
	}
	dialog({
        title: '提示',
        content: '您当前积分：'+current_integral+'，支付积分：'+need_integral+'，您确定购买该商品吗？',
        okValue: '确定',
        ok: function () {
            $.ajax({
				type: "post",
				url: sendUrl,
				dataType: "json",
				data: {
					"checkSn":order_sn,
					csrfmiddlewaretoken:csrf_token
				},
				timeout: 200,
				success: function(data, textStatus) {
					if (data.status === 1){
						var tipdialog = dialog({content:data.msg}).show();
						setTimeout(function () {
							tipdialog.close().remove();
							if($(urlObj)){
								location.href = $(urlObj).val();
								console.log($(urlObj).val())
							}else{
								location.reload();
							}
						}, 2000);
					} else {
						dialog({title:'提示', content:data.msg, okValue:'确定', ok:function (){}}).showModal();
					}
				},
				error: function (XMLHttpRequest, textStatus, errorThrown) {
					dialog({title:'提示', content:'状态：' + textStatus + '；出错提示：' + errorThrown, okValue:'确定', ok:function (){}}).showModal();
				}
			});
        },
        cancelValue: '取消',
        cancel: function () { }
    }).showModal();
}

//单击执行AJAX请求操作
function clickSubmit(sendUrl){
	$.ajax({
		type: "POST",
		url: sendUrl,
		dataType: "json",
		timeout: 20000,
		success: function(data, textStatus) {
			if (data.status == 1){
				var d = dialog({content:data.msg}).show();
				setTimeout(function () {
					d.close().remove();
					location.reload();
				}, 2000);
			} else {
				dialog({title:'提示', content:data.msg, okValue:'确定', ok:function (){}}).showModal();
			}
		},
		error: function (XMLHttpRequest, textStatus, errorThrown) {
			dialog({title:'提示', content:"状态：" + textStatus + "；出错提示：" + errorThrown, okValue:'确定', ok:function (){}}).showModal();
		}
	});
}

//=====================发送验证邮件=====================
function sendEmail(username, sendurl) {
	if(username == ""){
		dialog({title:'提示', content:'对不起，用户名不允许为空！', okValue:'确定', ok:function (){}}).showModal();
		return false;
	}
	//提交
	$.ajax({
		url: sendurl,
		type: "POST",
		timeout: 60000,
		data: { "username": username },
		dataType: "json",
		success: function (data, type) {
			if (data.status == 1) {
				var d = dialog({content:data.msg}).show();
				setTimeout(function () {
					d.close().remove();
				}, 2000);
			} else {
				dialog({title:'提示', content:data.msg, okValue:'确定', ok:function (){}}).showModal();
			}
		},
		error: function(XMLHttpRequest, textStatus, errorThrown){
			 dialog({title:'提示', content:"状态：" + textStatus + "；出错提示：" + errorThrown, okValue:'确定', ok:function (){}}).showModal();
		}
	});
}
//=====================发送手机短信验证码=====================
var wait = 0; //计算变量
function sendSMS(btnObj, valObj, sendUrl) {
	if($(valObj).val() == ""){
		dialog({title:'提示', content:'对不起，请填写手机号码后再获取！', okValue:'确定', ok:function (){}}).showModal();
		return false;
	}
	//发送AJAX请求
	$.ajax({
		url: sendUrl,
		type: "POST",
		timeout: 60000,
		data: { "mobile": $(valObj).val() },
		dataType: "json",
		beforeSend: function(XMLHttpRequest) {
			$(btnObj).unbind("click").removeAttr("onclick"); //移除按钮事件
		},
		success: function (data, type) {
			if (data.status == 1) {
				wait = data.time * 60; //赋值时间
				time(); //调用计算器
				var d = dialog({content:data.msg}).show();
				setTimeout(function () {
					d.close().remove();
				}, 2000);
			} else {
				$(btnObj).removeClass("gray").text("发送确认码");
				$(btnObj).bind("click", function(){
					sendSMS(btnObj, valObj, sendUrl); //重新绑定事件
				});
				dialog({title:'提示', content:data.msg, okValue:'确定', ok:function (){}}).showModal();
			}
		},
		error: function(XMLHttpRequest, textStatus, errorThrown){
			$(btnObj).removeClass("gray").text("发送确认码");
			$(btnObj).bind("click", function(){
				sendSMS(btnObj, valObj, sendurl); //重新绑定事件
			});
			dialog({title:'提示', content:"状态：" + textStatus + "；出错提示：" + errorThrown, okValue:'确定', ok:function (){}}).showModal();
		}
	});
	//倒计时计算器
	function time(){
		if (wait == 0) {
			$(btnObj).removeClass("gray").text("发送确认码");
			$(btnObj).bind("click", function(){
				sendSMS(btnObj, valObj, sendurl); //重新绑定事件
			});
		}else{
			$(btnObj).addClass("gray").text("重新发送(" + wait + ")");
			wait--;
			setTimeout(function() {
				time(btnObj);
			},1000)
		}
	}
}

/*表单AJAX提交封装(包含验证)
------------------------------------------------*/
function AjaxInitForm(formObj, btnObj, isDialog, urlObj, callback,func){
	let csrf_token = $('#csrf').val();
	var argNum = arguments.length; //参数个数
	$(formObj).Validform({
		tiptype:3,
		callback:function(form){
			//AJAX提交表单
            $(form).ajaxSubmit({
                beforeSubmit: formRequest,
                success: formResponse,
                error: formError,
                url: $(formObj).attr("url"),
                type: "post",
                dataType: "json",
				data:{
					csrfmiddlewaretoken:csrf_token,
				},
                timeout: 60000
            });
            return false;
		}
	});
    
    //表单提交前
    function formRequest(formData, jqForm, options) {
        $(btnObj).prop("disabled", true);
        $(btnObj).val("提交中...");
    }

    //表单提交后
    function formResponse(data, textStatus) {
		if (data.status == 1) {
            $(btnObj).val("提交成功");
			//是否提示，默认不提示
			if(isDialog == 1){
				var d = dialog({content:data.msg}).show();
				setTimeout(function () {
					d.close().remove();
					if (argNum >= 5) {
						// alert($(urlObj).val());
						// location.href= $(urlObj).val();
                        func();
						callback();
					}else if(data.url){
						location.href = data.url;
					}else if($(urlObj).length > 0 && $(urlObj).val() != ""){
						location.href = $(urlObj).val();
					}else{
						location.reload();
					}
				}, 2000);
			}else{
				if (argNum >= 5) {
				    func();
					callback();
				}else if(data.url){
					location.href = data.url;
				}else if($(urlObj)){
					dialog({title:'提示', content:data.msg, okValue:'确定', ok:function (){location.href = $(urlObj).val();}}).showModal();
					// location.href = $(urlObj).val();
				}else{
					location.reload();
				}
			}
        } else {
			dialog({title:'提示', content:data.msg, okValue:'确定', ok:function (){}}).showModal();
            $(btnObj).prop("disabled", false);
            $(btnObj).val("再次提交");
        }
    }
    //表单提交出错
    function formError(XMLHttpRequest, textStatus, errorThrown) {
		dialog({title:'提示', content:'状态：'+textStatus+'；出错提示：'+errorThrown, okValue:'确定', ok:function (){}}).showModal();
        $(btnObj).prop("disabled", false);
        $(btnObj).val("再次提交");
    }
}
//显示评论AJAX分页列表
function AjaxPageList(listDiv, pageDiv, pageSize, pageCount, sendUrl, defaultAvatar) {
	let csrf_token = $('#csrf').val();
    //pageIndex -页面索引初始值
    //pageSize -每页显示条数初始化
    //pageCount -取得总页数
	InitComment(0,csrf_token);//初始化评论数据
	$(pageDiv).pagination(pageCount, {
		callback: pageselectCallback,
		prev_text: "« 上一页",
		next_text: "下一页 »",
		items_per_page:pageSize,
		num_display_entries:3,
		current_page:0,
		num_edge_entries:6,
		link_to:"?page_index=__id__"
	});

    //分页点击事件
    function pageselectCallback(page_id, jq) {
        InitComment(page_id);
    }
    //请求评论数据
    function InitComment(page_id,csrf_token) {
        page_id++;
        $.ajax({
            type: "POST",
            dataType: "json",
            url: sendUrl + "&page_size=" + pageSize + "&page_index=" + page_id,
			data:{
            	csrfmiddlewaretoken:csrf_token
			},
            beforeSend: function (XMLHttpRequest) {
                // $(listDiv).prepend('<p style="line-height:35px;">正在狠努力加载，请稍候...</p>');
            },

            success: function (data) {
                var strHtml = '';
                // 循环遍历传过来的data评论数据
                for (var i in data) {
                    var com_txt = unescape(data[i].content); //获取评论内容
                    //头像替换
                    com_txt = com_txt.replace(/\[Q([0-9]*)\]/g, "<img src='/static/picture/$1.gif'/>");
                    //接下来这一段就是编写拼接html的评论内容
                    strHtml += '<li class="bg-color">' +
					'<div class="comment-ava"><a href="#" id="Comment-21" target="_blank" rel="nofollow" title="去他的的网站看看?">';
                    strHtml += '<img class="img-circle" src="/static/images/Portrait/' + data[i].img_url + '.jpg"alt="他的导航" />';
                    strHtml += '</a></div><div class="comment-info ">' +
					'<div class="comment-line ">' +
                    '<ul>' +
					'<li><a title=""><i class="el-user"></i>' + data[i].user_name + '</a></li>' +
					'<li><a title="发表于' + data[i].add_time + '"><i class="el-time"></i>' + data[i].add_time + '</a></li>' +
					'<li><a title="' + data[i].user_name + ' 当前位于：' + data[i].city + '"><i class="el-map-marker"></i>' + data[i].city + '</a></li>' +
					'<li><a class="reply_comment" href="#txtContent" onclick="reply(this)" title="回复 ' + data[i].user_name + '" data-value="'+ data[i].u_code +'">' + '回复' + '</a></li>' +
                    '</ul>' +
					'</div>' +
					'<div class="comment-content comment_txt">' + com_txt + '</div>';
                    // if (data[i].is_reply == 1) {

					strHtml +='<ul class="re-comment">' + '<li style="border-left:none;">'
                    //如果存在子评论数据，则根据后台所记的数为标准循环
					for (let n= 0;n<data[i].is_reply_count;n++) {
					    //每一个子标签的回复内容键
						let reply_content = 'reply_content'+(n+1);
						//回复时间键
						let reply_time = 'reply_time' + (n+1);
						//回复名称键
						let reply_name = 'reply_name' + (n+1);
						//被回复者的名称键
						let to_reply_name = 'to_reply_name' + (n+1);
						//被回复的子评论的uid
						let u_recode = 'u_recode' + (n+1);
						//凭借子评论数据html
                        strHtml +=
						'<div>'+
						'<div class="admin-ava"><img src="/static/images/ava.gif" alt="管理员回复：" title="管理员回复：" class="img-circle"></div>' +
                        '<div class="re-info">' +
						'<span><img src="/static/images/icon/ok.png"><a href="#" target="_blank" title="">'+data[i][reply_name]+'</a>	 <time>' + data[i][reply_time] + '</time> 回复 <a href="#" title="">@' + data[i][to_reply_name] + '</a>' +
						'<a class="reply_comment" href="#txtContent" onclick="self_reply(this)" title="回复 ' + data[i][reply_name] + '" data-revalue="'+ data[i][u_recode] +'" data-value="'+data[i].u_code+'">' + '回复' + '</a></span>' +
                        '<div class=" re-content">' + unescape(data[i][reply_content]) + '</div>' +
						'</div></div>'
                    }
					strHtml +='</li>'+'</ul>';
					// strHtml += '<ul class="re-comment">' +
					// 	'<li style="border-left:none;">' +
					// 	'<div class="admin-ava"><img src="/static/images/ava.gif" alt="管理员回复：" title="管理员回复：" class="img-circle"></div>' +
                    //     '<div class="re-info">' +
					// 	'<span><img src="/static/images/icon/ok.png"><a href="#" target="_blank" title="">管理员</a>	 <time>' + data[i].reply_time + '</time> 回复 <a href="#" title="">@' + data[i].user_name + '</a></span>' +
                    //     '<div class=" re-content">' + unescape(data[i].reply_content) + '</div>' +
					// 	'</li></div>' +
					// 	'</ul>';
                    // }

                    strHtml += '</div></li>';
                }
                // $(listDiv).prepend(strHtml);
                //加入html内容
				$(listDiv).html(strHtml);
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                $(listDiv).html('<p style="line-height:35px;text-align:center;border:1px solid #0181DA;color:#0181DA">暂无评论，快来抢沙发吧！</p>');
            }
        });
    }
}
function SelfInitComment(listDiv,page_id,csrf_token,sendUrl,pageSize) {
        $.ajax({
            type: "POST",
            dataType: "json",
            url: sendUrl + "&page_size=" + pageSize + "&page_index=" + page_id,
			data:{
            	csrfmiddlewaretoken:csrf_token
			},
            beforeSend: function (XMLHttpRequest) {
                // $(listDiv).prepend('<p style="line-height:35px;">正在狠努力加载，请稍候...</p>');
            },

            success: function (data) {
                var strHtml = '';
                // 循环遍历传过来的data评论数据
                for (var i in data) {
                    var com_txt = unescape(data[i].content); //获取评论内容
                    //头像替换
                    com_txt = com_txt.replace(/\[Q([0-9]*)\]/g, "<img src='/static/picture/$1.gif'/>");
                    //接下来这一段就是编写拼接html的评论内容
                    strHtml += '<li class="bg-color">' +
					'<div class="comment-ava"><a href="#" id="Comment-21" target="_blank" rel="nofollow" title="去他的的网站看看?">';
                    strHtml += '<img class="img-circle" src="/static/images/Portrait/' + data[i].img_url + '.jpg"alt="他的导航" />';
                    strHtml += '</a></div><div class="comment-info ">' +
					'<div class="comment-line ">' +
                    '<ul>' +
					'<li><a title=""><i class="el-user"></i>' + data[i].user_name + '</a></li>' +
					'<li><a title="发表于' + data[i].add_time + '"><i class="el-time"></i>' + data[i].add_time + '</a></li>' +
					'<li><a title="' + data[i].user_name + ' 当前位于：' + data[i].city + '"><i class="el-map-marker"></i>' + data[i].city + '</a></li>' +
					'<li><a class="reply_comment" href="#txtContent" onclick="reply(this)" title="回复 ' + data[i].user_name + '" data-value="'+ data[i].u_code +'">' + '回复' + '</a></li>' +
                    '</ul>' +
					'</div>' +
					'<div class="comment-content comment_txt">' + com_txt + '</div>';
                    // if (data[i].is_reply == 1) {

					strHtml +='<ul class="re-comment">' + '<li style="border-left:none;">'
                    //如果存在子评论数据，则根据后台所记的数为标准循环
					for (let n= 0;n<data[i].is_reply_count;n++) {
					    //每一个子标签的回复内容键
						let reply_content = 'reply_content'+(n+1);
						//回复时间键
						let reply_time = 'reply_time' + (n+1);
						//回复名称键
						let reply_name = 'reply_name' + (n+1);
						//被回复者的名称键
						let to_reply_name = 'to_reply_name' + (n+1);
						//被回复的子评论的uid
						let u_recode = 'u_recode' + (n+1);
						//凭借子评论数据html
                        strHtml +=
						'<div>'+
						'<div class="admin-ava"><img src="/static/images/ava.gif" alt="管理员回复：" title="管理员回复：" class="img-circle"></div>' +
                        '<div class="re-info">' +
						'<span><img src="/static/images/icon/ok.png"><a href="#" target="_blank" title="">'+data[i][reply_name]+'</a>	 <time>' + data[i][reply_time] + '</time> 回复 <a href="#" title="">@' + data[i][to_reply_name] + '</a>' +
						'<a class="reply_comment" href="#txtContent" onclick="self_reply(this)" title="回复 ' + data[i][reply_name] + '" data-revalue="'+ data[i][u_recode] +'" data-value="'+data[i].u_code+'">' + '回复' + '</a></span>' +
                        '<div class=" re-content">' + unescape(data[i][reply_content]) + '</div>' +
						'</div></div>'
                    }
					strHtml +='</li>'+'</ul>';
					// strHtml += '<ul class="re-comment">' +
					// 	'<li style="border-left:none;">' +
					// 	'<div class="admin-ava"><img src="/static/images/ava.gif" alt="管理员回复：" title="管理员回复：" class="img-circle"></div>' +
                    //     '<div class="re-info">' +
					// 	'<span><img src="/static/images/icon/ok.png"><a href="#" target="_blank" title="">管理员</a>	 <time>' + data[i].reply_time + '</time> 回复 <a href="#" title="">@' + data[i].user_name + '</a></span>' +
                    //     '<div class=" re-content">' + unescape(data[i].reply_content) + '</div>' +
					// 	'</li></div>' +
					// 	'</ul>';
                    // }

                    strHtml += '</div></li>';
                }
                // $(listDiv).prepend(strHtml);
                //加入html内容
				$(listDiv).html(strHtml);
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                $(listDiv).html('<p style="line-height:35px;text-align:center;border:1px solid #0181DA;color:#0181DA">暂无评论，快来抢沙发吧！</p>');
            }
        });
    }
//初始化视频播放器需配合ckplayer.js使用
function initCKPlayer(boxId, videoSrc, playerSrc){
	var flashvars={
        f:videoSrc,
        c:0,
        loaded:'loadedHandler'
    };
    var video=[videoSrc];
    CKobject.embed(playerSrc,boxId,'video_v1','100%','100%',false,flashvars,video);
}
// 获取评论总数
function ajaxComment(obj, webpath) {
    $.get(webpath, function (data) {
    	// alert(data);
        $(obj).text(data);
    });
// function ajaxComment(obj, webpath, id) {
//     $.get(webpath + "tools/submit_ajax.ashx?action=view_comment_count&id=" + id, function (data) {
//         $(obj).text(data);
//     }, "html");
// }
//获取点击总数
function ajaxView(obj, webpath, id) {
    $.get(webpath + "tools/submit_ajax.ashx?action=view_article_click&id=" + id, function (data) {
        $(obj).text(data);
    }, "html");
}
//批量请求
function ajaxEash(obj, webpath, num) {
    var $this, url, i = 0;
    if (num == 1) {
        url = webpath + "tools/submit_ajax.ashx?action=view_article_click&id=";
    } else {
        url = webpath + "tools/submit_ajax.ashx?action=view_comment_count&id=";
    }
    $(obj).each(function (index) {
        $this = $(this);
        $.get(url + $this.attr("i"), function (data) {
            $(obj).next("em").eq(index).html(data);
        }, "html");
    });
}}