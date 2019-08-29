import re

from django import forms

class LinkForm(forms.Form):
    txtTitle = forms.CharField(label='网站名称',max_length=24,error_messages={
        'required':'请输入网站名称'
    })
    txtUserName = forms.CharField(label='联系人姓名',max_length=6,error_messages={
        'required':'请输入联系人姓名'
    })
    txtUserTel = forms.CharField(label='联系人电话',max_length=11,required=False,error_messages={
        'max_length':'请输入11位数的手机号码'
    })
    txtEmail = forms.EmailField(label='邮箱地址',required=False,error_messages={
        'invalid':'邮箱格式不对'
    })
    txtSiteUrl = forms.URLField(label='网站网址',error_messages={
        'required':'请输入网站网址'
    })
    txaArticle = forms.CharField(label='网站描述',widget=forms.TextInput,error_messages={
        'required':'请输入网站描述'
    })

    def clean_txtUserTel(self):
        txtUserTel = self.cleaned_data.get('txtUserTel')
        pattern = r'^1[3-9][0-9]{9}$'
        if not re.search(pattern, txtUserTel):
            raise forms.ValidationError('请输入正确的手机号码')
        return txtUserTel

    def clean_txaArticle(self):
        txaArticle = self.cleaned_data.get('txaArticle')
        if len(txaArticle) > 500:
            raise forms.ValidationError('网站描述不得超过500个字')
        return txaArticle

    # 这个应该在forms.Model这个底下才有效
    # def save(self):
    #     obj = super().save()
    #     txtTitle = self.cleaned_data.get('txtTitle')
    #     txtUserName = self.cleaned_data.get('txtUserName')
    #     txtUserTel = self.cleaned_data.get('txtUserTel')
    #     txtEmail = self.cleaned_data.get('txtEmail')
    #     txtSiteUrl = self.cleaned_data.get('txtSiteUrl')
    #     txaArticle = self.cleaned_data.get('txaArticle')
    #     obj.web_name = txtTitle
    #     obj.contact_man = txtUserName
    #     obj.phone = txtUserTel
    #     obj.email = txtEmail
    #     obj.web_link = txtSiteUrl
    #     obj.web_description = txaArticle
    #     obj.save()
