$(function () {
    var oExports = {
        initialize: fInitialize,
        // 渲染更多数据
        renderMore: fRenderMore,
        // 请求数据
        requestData: fRequestData,
        // 简单的模板替换
        tpl: fTpl
    };
    // 初始化页面脚本
    oExports.initialize();

    function fInitialize() {
        var that = this;
        // 常用元素
        that.listEl = $('div.js-image-list');
        // 初始化数据
        that.uid = window.uid;
        that.page = 1;
        that.pageSize = 10;
        that.listHasNext = true;
        // 绑定事件
        $('.js-load-more').on('click', function (oEvent) {
            var oEl = $(oEvent.currentTarget);
            var sAttName = 'data-load';
            // 正在请求数据中，忽略点击事件
            if (oEl.attr(sAttName) === '1') {
                return;
            }
            // 增加标记，避免请求过程中的频繁点击
            oEl.attr(sAttName, '1');
            that.renderMore(function () {
                // 取消点击标记位，可以进行下一次加载
                oEl.removeAttr(sAttName);
                // 没有数据隐藏加载更多按钮
                !that.listHasNext && oEl.hide();
            });
        });
    }

    function fRenderMore(fCb) {
        var that = this;
        // 没有更多数据，不处理
        if (!that.listHasNext) {
            return;
        }
        that.requestData({
            uid: that.uid,
            page: that.page + 1,
            pageSize: that.pageSize,
            call: function (oResult) {
                // 是否有更多数据
                that.listHasNext = !!oResult.has_next && (oResult.images || []).length > 0;
                // 更新当前页面
                that.page++;
                // 渲染数据
                var sHtml = '';
                $.each(oResult.images, function (nIndex, oImage) {
                    var sHtml1='';
                    var sHtml2='';
                    var sHtml3='';
                    sHtml1 = that.tpl([
                        '<article class="mod">',
                        '<header class="mod-hd">',
                            '<time class="time">#{create_time}</time>',
                            '<a href="/profile/#{user_id}/" class="avatar">',
                                '<img src="#{head_url}">',
                            '</a>',
                            '<div class="profile-info">',
                               '<a title="{{i.user.username}}" href="/profile/#{user_id}/">#{username}</a>',
                            '</div>',
                        '</header>',
                        '<div class="mod-bd">',
                            '<div class="img-box">',
                                '<a href="/image/#{image_id}">',
                                    '<img src="#{url}">',
                                '</a>',
                            '</div>',
                        '</div>',
                        '<div class="mod-ft">',
                            '<section class="times">',
                                '<span></span>',
                                '<span>6.2百万</span>',
                                '<span> 次播放</span>',
                            '</section>',
                            '<ul class="discuss-list">',
                                '<li class="more-discuss">',
                                    '<a>',
                                        '<span>全部 </span><span class="">#{comment_length}</span>',
                                        '<span> 条评论</span></a>',
                                '</li>'].join(''), oImage);
                    for (var ni = 0; ni < oImage.comment_length; ni++){
                        dict={'comment_username':oImage.comments_user[ni],'comment_content':oImage.comments[ni],
                                'comment_userid':oImage.comments_userid[ni]};
                        sHtml2 += that.tpl([
                                '<li>',
                                    '<a class=" icon-remove" title="删除评论"></a>',
                                    '<a class="_4zhc5 _iqaka" title="#{comment_username}" href="/profile/#{comment_userid}/" data-reactid=".0.1.0.0.0.2.1.2:$comment-17856951190001917.1">#{comment_username}</a>',
                                    '<span>',
                                        '<span>#{comment_content}</span>',
                                    '</span>',
                                '</li>'].join(''), dict);}
                    var str ="form = document.getElementById('form-"+ oImage.image_id + "'); form.action='/addindexcomment/';window.imageId="+oImage.image_id + ";";
                    var aa=oImage.image_id;
                    //console.log(str);
                    //console.log(aa);
                    sHtml3=that.tpl([
                            '</ul>',
                            '<section class="discuss-edit">',
                                '<a class="icon-heart"></a>',
                                '<form id="form-#{image_id}" method="post">',
                                    '<input placeholder="添加评论..." type="text" id="jsCmt" name="content">',
                                    '<input type="hidden" name="image_id" value="{{i.id}}">',
                                '</form>',
                                '<button class="more-info" onclick='+ str +' >更多选项</button>',
                            '</section>',
                        '</div>',
                    '</article>'].join(''), oImage);
                    sHtml+=sHtml1+sHtml2+sHtml3
                });
                sHtml && that.listEl.append(sHtml);
            },
            error: function () {
                alert('出现错误，请稍后重试');
            },
            always: fCb
        });
    }

    function fRequestData(oConf) {
        var that = this;
        var sUrl = '/index/' + oConf.page + '/' + oConf.pageSize + '/';
        $.ajax({url: sUrl, dataType: 'json'}).done(oConf.call).fail(oConf.error).always(oConf.always);
    }

    function fTpl(sTpl, oData) {
        var that = this;
        sTpl = $.trim(sTpl);
        return sTpl.replace(/#{(.*?)}/g, function (sStr, sName) {
            return oData[sName] === undefined || oData[sName] === null ? '' : oData[sName];
        });
    }
});