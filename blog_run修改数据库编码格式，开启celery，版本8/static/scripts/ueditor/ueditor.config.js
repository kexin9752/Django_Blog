(function () {
    var URL = window.UEDITOR_HOME_URL || getUEBasePath();
    window.UEDITOR_CONFIG = {
        UEDITOR_HOME_URL: URL
        , serverUrl: URL + "../../tools/upload_ajax.ashx"
		,toolbars:[['fullscreen','source','|','undo','redo','|','bold','italic','underline','strikethrough','superscript','subscript','forecolor','backcolor','|','insertorderedlist','insertunorderedlist','indent','justifyleft','justifycenter','justifyright','|','rowspacingtop', 'rowspacingbottom', 'lineheight', '|','removeformat','formatmatch','autotypeset','pasteplain','searchreplace','preview','wordimage','|','help'],['paragraph','fontfamily','fontsize','insertcode','emotion','link','inserttable','|','simpleupload', 'insertimage','imagenone','imageleft','imageright','imagecenter','|','insertvideo','music','attachment','map','|','horizontal','spechars','scrawl','snapscreen','drafts']]
        ,autoHeightEnabled:false
        ,autoFloatEnabled:false
		,zIndex : 1
    };
    function getUEBasePath(docUrl, confUrl) {
        return getBasePath(docUrl || self.document.URL || self.location.href, confUrl || getConfigFilePath());
    }
    function getConfigFilePath() {
        var configPath = document.getElementsByTagName('script');
        return configPath[ configPath.length - 1 ].src;
    }
    function getBasePath(docUrl, confUrl) {
        var basePath = confUrl;
        if (/^(\/|\\\\)/.test(confUrl)) {
            basePath = /^.+?\w(\/|\\\\)/.exec(docUrl)[0] + confUrl.replace(/^(\/|\\\\)/, '');
        } else if (!/^[a-z]+:/i.test(confUrl)) {
            docUrl = docUrl.split("#")[0].split("?")[0].replace(/[^\\\/]+$/, '');
            basePath = docUrl + "" + confUrl;
        }
        return optimizationPath(basePath);
    }
    function optimizationPath(path) {
        var protocol = /^[a-z]+:\/\//.exec(path)[ 0 ],
            tmp = null,
            res = [];
        path = path.replace(protocol, "").split("?")[0].split("#")[0];
        path = path.replace(/\\/g, '/').split(/\//);
        path[ path.length - 1 ] = "";
        while (path.length) {
            if (( tmp = path.shift() ) === "..") {
                res.pop();
            } else if (tmp !== ".") {
                res.push(tmp);
            }
        }
        return protocol + res.join("/");
    }
    window.UE = {
        getUEBasePath: getUEBasePath
    };
})();
