/*================================
=====2016-7-16 power by zzc=========
================================*/
//function fuckyou() {
//    window.close(); //关闭当前窗口(防抽)
//    window.location = "about:blank"; //将当前窗口跳转置空白页
//}
//function ck() {
//    console.profile();
//    console.profileEnd();
//    //我们判断一下profiles里面有没有东西，如果有，肯定有人按F12了，没错！！
//    if (console.clear) { console.clear() };
//    if (typeof console.profiles == "object") {
//        return console.profiles.length > 0;
//    }
//}
//function hehe() {
//    if ((window.console && (console.firebug || console.table && /firebug/i.test(console.table()))) || (typeof opera == 'object' && typeof opera.postError == 'function' && console.profile.length > 0)) {
//        fuckyou();
//    }
//    if (typeof console.profiles == "object" && console.profiles.length > 0) {
//        fuckyou();
//    }
//}
//hehe();
//window.onresize = function () {
//    if ((window.outerHeight - window.innerHeight) > 200)
//    //判断当前窗口内页高度和窗口高度，如果差值大于200，那么呵呵
//    fuckyou();
//}


$(document).ready(function () {
    $("section").addClass("mysection")
    //动画加载
    $("body").show();

    $(".jiazai").remove();
    $(".top-left").css({ "animation": "fuzuo 1s", "-webkit-animation": "fuzuo 1s" });
    $(".swiper-container,.myaside ,.homeh4,.mysection").css({ "-webkit-animation": "fuxiasuo 0.8s", "animation": "fuxiasuo 0.8s" })
    $(".myheader").css({ "-webkit-animation": "fushang 0.5s", "animation": "fushang 0.5s" })
    //$(".skin-btn").css({"-webkit-animation": "zuo2 0.5s","-webkit-animation":"zuo2 0.5s"})

    var sidelen = $(".animation-div").length
    var arclen = $(".arclist> ul>li").length
    for (var s = 0; s <= sidelen; s++) {

        $(".animation-div").eq(s).css({
            "-webkit-animation-name": "fuxiasuo",
            "-webkit-animation-duration": s / 7 + 1 + "s",
            "animation-name": "fuxiasuo",
            "animation-duration": s / 7 + 1 + "s"
        });
    }
    for (var a = 0; a <= arclen; a++) {

        $(".arclist >ul>li").eq(a).css({
            "-webkit-animation-name": "fuxiasuo",
            "-webkit-animation-duration": a / 8 + 1 + "s",
            "animation-name": "fuxiasuo",
            "animation-duration": a / 8 + 1 + "s"
        });
    }
    //通过调用新浪IP地址库接口查询用户当前所在国家、省份、城市、运营商信息
    //$.getScript('http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=js', function () {
    //    var citys = remote_ip_info.province + "省" + remote_ip_info.city + "市";
    //    $("#mycity").val(citys);
    //});
    //$.getScript('http://pv.sohu.com/cityjson', function () {
    //    $("#myip").html(returnCitySN.cip);
    //});
    showsectime();
    footrcount();
    var pcli = $(".mynav >ul >li")
    var pclien = pcli.length
    var pcliinde = pcli.index()
    var ulwidth = $(".mynav >ul").width();
    $(".mynav >ul >li").css("width", ulwidth / pclien)
    for (var j = 0; j <= pclien; j++) {

        pcli.eq(j).css({
            "-webkit-animation-name": "fushang",
            "-webkit-animation-duration": j / 6 + 0.5 + "s",
            "animation-name": "fushang",
            "animation-duration": j / 6 + 0.5 + "s"
        });
    }

    //当前连接高亮

    $('nav li a').each(function () {
        if ($($(this))[0].href == String(window.location))
            $(this).parent("li").addClass('nav-active');
    });

    //菜单下拉


    $(".mob-drop").click(function () {
        $(".mob-dropmenu").slideToggle();

    });

    //手机菜单下拉


    var mb = $(".mobile-nav")
    var mli = $(".mob-ulnav>li")
    var mlen = mli.length;
    var mindex = mli.index();




    mb.find(".el-lines").click(function () {
        $(this).hide();
        $(this).next("i").show()
        for (var m = 0; m <= mlen; m++) {

            mli.eq(m).css({
                "-webkit-animation-name": "zuo",
                "-webkit-animation-duration": m / 10 + 0.5 + "s",
                "animation-name": "zuo",
                "animation-duration": m / 10 + 0.5 + "s"
            });
        }
        $(".mob-menu").show().css({ "-webkit-animation": "zuo 0.8s", "animation": "zuo 0.8s" })
    });


    mb.find(".el-remove").click(function () {
        $(this).hide();
        $(this).prev("i").show();
        for (var m = 0; m <= mlen; m++) {

            mli.eq(m).css({
                "-webkit-animation-name": "fuzuo",
                "-webkit-animation-duration": m / 10 + 0.5 + "s",
                "animation-name": "fuzuo",
                "animation-duration": m / 10 + 0.5 + "s"
            });
        }
        $(".mob-menu").css({ "-webkit-animation": "zuo3 0.8s", "animation": "zuo3 0.8s" });
        setTimeout(function () {
            $(".mob-menu").hide();
        }, 500);
    });


    //相册动画

    //滑动效果	
    $(".drop").mouseenter(function () {

        $(this).find(".drop-nav").css({ "-webkit-animation": "zuo1 0.8s", "animation": "zuo1 0.8s" }).show();

    });


    $(".drop").mouseleave(function () {

        $(".drop-nav").hide();


    });

    //TAB切换
    $(".mytab a").click(function () {
        var index = $(this).index();
        $(this).addClass("tab-active").siblings().removeClass("tab-active");
        $(this).parents(".mytab").find("ul").eq(index).show().siblings('ul').hide();

    });
    //滚动
    //文字滚动
    $(function () {

        var _wrap = $('.mulitline'); //定义滚动区域
        var _interval = 3000; //定义滚动间隙时间
        var _moving; //需要清除的动画
        _wrap.hover(function () {
            clearInterval(_moving); //当鼠标在滚动区域中时,停止滚动
        }, function () {
            _moving = setInterval(function () {
                var _field = _wrap.find('li:first'); //此变量不可放置于函数起始处，li:first取值是变化的
                var _h = _field.height(); //取得每次滚动高度
                _field.animate({ marginTop: -_h + 'px' }, 500, function () {//通过取负margin值，隐藏第一行
                    _field.css('marginTop', 0).appendTo(_wrap); //隐藏后，将该行的margin值置零，并插入到最后，实现无缝滚动
                })
            }, _interval)//滚动间隔时间取决于_interval
        }).trigger('mouseleave'); //函数载入时，模拟执行mouseleave，即自动滚动
        if ($(".mulitline li").length <= 1)//小于等于1条时，不滚动
        {
            clearInterval(_moving);

        }

    });


    //邮箱弹窗
    $(".mail-btn").click(function (e) {

        $(".mail-dy").show();
        $(".side-bdfx").hide();
        $(document).one("click", function () {

            $(".side-bdfx").hide();
            $(".mail-dy").hide();

        });
        e.stopPropagation();
    });
    //返回顶部
    $(function () {
        $(window).scroll(function () {
            if ($(this).scrollTop() >= 500) {
                $('#toTop').fadeIn();
            }
            else {
                $('#toTop').fadeOut();
            }
        });

        $('#toTop').click(function () {
            $('body,html').animate({ scrollTop: 0 }, 800);
        });
    });
    //表单下拉
    $(".form-btn a").click(function () {
        $(".form-zd").slideToggle();
    });

    //弹出分享层
    $(".fx-btn").click(function (e) {
        $(".arc-bdfx").show();
        $(document).one("click", function () {

            $(".arc-bdfx").hide();

        });
        e.stopPropagation();
    });
    $(".side-fx").click(function (e) {
        $(".side-bdfx").show();
        $(".mail-dy").hide();
        $(document).one("click", function () {

            $(".side-bdfx").hide();
            $(".mail-dy").hide();

        });
        e.stopPropagation();

    });
    $(".el-remove").click(function () {
        $(".arc-bdfx").hide();
        $(".mail-dy").hide();
        $(".side-bdfx").hide();
    });

    //图片查看器
    $(".mail-dy").click(function (e) {
        e.stopPropagation();
    });

    //2016-7-7-30修改
    var dragging = false;
    var iX, iY;
    $(document).on("mouseenter", ".face-main", function (e) {
        $(".face-tab").on("mousedown", function (e) {
            dragging = true;

            iX = e.clientX - $(this).parents(".face-main").get(0).offsetLeft;
            iY = e.clientY - $(this).parents(".face-main").get(0).offsetTop;
            $(this).parents(".face-main").get(0).setCapture && $(this).parents(".face-main").get(0).setCapture();
            return false;
            e.stopPropagation();

        })
        $(document).mouseup(function (e) {
            dragging = false;
            //$(".face-main")[0].releaseCapture(); 
            e.cancelBubble = true;
        });
    });
    document.onmousemove = function (e) {
        if (dragging) {
            var e = e || window.event;
            var oX = e.clientX - iX;
            var oY = e.clientY - iY;
            $(".face-main").css({ "left": oX + "px", "top": oY + "px" });
            return false;
        }
    };
});         //END Document ready
function NewDate(str) {
    str = str.split('-');
    var date = new Date();
    date.setUTCFullYear(str[0], str[1] - 1, str[2]);
    date.setUTCHours(0, 0, 0, 0);
    return date;
}
function showsectime() {
    var birthDay = NewDate("2016-09-02");
    var today = new Date();
    var timeold = today.getTime() - birthDay.getTime();

    var sectimeold = timeold / 1000
    var secondsold = Math.floor(sectimeold);
    var msPerDay = 24 * 60 * 60 * 1000;

    var e_daysold = timeold / msPerDay;
    var daysold = Math.floor(e_daysold);
    var e_hrsold = (daysold - e_daysold) * -24;
    var hrsold = Math.floor(e_hrsold);
    var e_minsold = (hrsold - e_hrsold) * -60;
    var minsold = Math.floor((hrsold - e_hrsold) * -60);

    var seconds = Math.floor((minsold - e_minsold) * -60).toString();
    $("#myday").text(daysold);
}

function footrcount() {
    $.ajax({
        type: "POST",
        url: "/tools/submit_ajax.ashx?action=view_count",
        dataType: "json",
        timeout: 20000,
        success: function (data) {
            $(".footer_picture").text(data.photo);
            $(".footer_headphones").text(data.shuo);
            $(".footer_pencil").text(data.news);
            $(".footer_comment").text("0");
            $("#newcount").text(data.news);
            $(".footer_comment_alt").text(data.comment);
            $(".footer_paper_clip").text(data.down);
        }
    });
}