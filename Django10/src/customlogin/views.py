from django.shortcuts import render
from .forms import SigninForm, SignupForm
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse

#�쉶�썝媛��엯
def signup(request):
    #GET/POST 遺꾨━
    if request.method == "GET":
        #SignupForm 媛앹껜 �깮�꽦 諛� HTML 臾몄꽌 �쟾�떖
        form1 = SignupForm()
        return render(request, 'customlogin/signup.html', {'form':form1})
    elif request.method == "POST":
        #request.POST瑜� 湲곕컲�쑝濡� SignupForm 媛앹껜 �깮�꽦
        form1 = SignupForm(request.POST)
        #�쑀�슚�븳 媛믪씤吏� �솗�씤(�븘�씠�뵒 以묐났泥댄겕, �븘�씠�뵒�삎�떇 泥댄겕, 鍮꾨�踰덊샇 �삎�떇 泥댄겕)
        if form1.is_valid():
            #鍮꾨�踰덊샇�� 鍮꾨�踰덊샇 �솗�씤 媛믪씠 媛숈�吏� 泥댄겕
            if form1.cleaned_data['password'] == form1.cleaned_data['password_check']:
                
                #�깉濡쒖슫 �쉶�썝 �깮�꽦 諛� �뜲�씠�꽣踰좎씠�뒪�뿉 ���옣
                new_user = User.objects.create_user(form1.cleaned_data['username'],
                                                    form1.cleaned_data['email'],
                                                    form1.cleaned_data['password'])
                #異붽��궗�빆 �엯�젰 諛� �뜲�씠�꽣踰좎씠�뒪�뿉 ���옣
                new_user.first_name = form1.cleaned_data['first_name']
                new_user.last_name = form1.cleaned_data['last_name']
                new_user.save()
                return HttpResponseRedirect( reverse('index'))
            else:#鍮꾨�踰덊샇媛� �떎瑜멸꼍�슦�뿉 ���븳 泥섎━
                return render(request, 'customlogin/signup.html', {'form': form1})
        else:
            return render(request,'customlogin/signup.html', {'form':form1})

from django.contrib.auth import login,authenticate
#login : �빐�떦 �슂泥��쓣 �븳 �겢�씪�씠�뼵�듃�뿉 濡쒓렇�씤 泥섎━
#authenticate :  鍮꾨�踰덊샇瑜� �븫�샇�솕�븳 �뮘, �븘�씠�뵒�� �븫�샇�솕�맂 鍮꾨�踰덊샇 紐⑤몢 �씪移섑븯�뒗 User媛앹껜瑜� 異붿텧
#濡쒓렇�씤
def signin(request):
    if request.method =="GET":
        f = SigninForm()
        #login_required濡� 濡쒓렇�씤�럹�씠吏� �젒洹쇳뻽�쓣 �븣 �궗�슜�옄媛� �씠�쟾�뿉 �슂泥��뻽�뜕 URL 二쇱냼瑜� 異붿텧
        nexturl = request.GET.get('next','')
        return render(request, 'customlogin/signin.html', {'form' : f,
                                                           'nexturl':nexturl})
    elif request.method == 'POST':
        #�븘�씠�뵒�굹 鍮꾨�踰덊샇媛� �씪移섑븯吏��븡�뒗 寃쎌슦 �궗�슜�옄 �엯�젰�쓣 �꽆寃⑥쨪 紐⑤뜽�뤌媛앹껜�쓣 誘몃━ �깮�꽦
        f = SigninForm(request.POST) 
        #�궗�슜�옄 �슂泥��뿉 �룷�븿�맂 �뜲�씠�꽣 以� �븘�씠�뵒�� 鍮꾨�踰덊샇 媛� 異붿텧
        id = request.POST.get('username')
        pw = request.POST.get('password')
        #f.is_valid() �샇異� �썑 cleaned_data瑜� �궗�슜�븷 �닔 �뾾�쓬
        #-> id以묐났泥댄겕瑜� �빐踰꾨━湲� �븣臾몄뿉 濡쒓렇�씤�쓣 �닔�뻾�븷 �닔 �뾾�쓬(�빆�긽 False 諛섑솚)
        #�븘�씠�뵒�� 鍮꾨�踰덊샇媛� �씪移섑븯�뒗 �쑀��瑜� 諛섑솚�빐 u蹂��닔�뿉 ���옣
        #�씪移섑븯吏� �븡�뒗寃쎌슦 None 媛믪쓣 諛섑솚
        u = authenticate(username=id, password=pw)
        if u is not None : #u蹂��닔媛� None媛믪씠 �븘�땶寃쎌슦 (�븘�씠�뵒�� 鍮꾨�踰덊샇媛� �씪移섑븯�뒗 �쑀��媛� �엳�쓬)
            #�빐�떦 �슂泥��쓣 媛�吏� �겢�씪�씠�뼵�듃媛� u�뿉 ���옣�맂 User 媛앹껜濡� 濡쒓렇�씤�븯�뒗 �옉�뾽�쓣 �닔�뻾
            login(request, user = u)
            nexturl = request.POST.get('nexturl')
            if nexturl != '':
                return HttpResponseRedirect(nexturl)
            else:
                return HttpResponseRedirect(reverse('index'))
        else: #�븘�씠�뵒�굹 鍮꾨�踰덊샇媛� �씪移섑븯吏��븡�쓬
            return render(request, 'customlogin/signin.html',{'form':f, 
                                                              'error':"�븘�씠�뵒"
                                                               "�삉�뒗 鍮꾨�踰덊샇媛� �씪移섑븯吏� �븡�뒿�땲�떎."})
from django.contrib.auth import logout
#濡쒓렇�븘�썐
def signout(request):
    logout(request) #�빐�떦 �슂泥��쓣 �븳 �겢�씪�씠�뼵�듃�쓽 濡쒓렇�븘�썐(�빐�떦 �꽭�뀡�쓽 User �젙蹂� �궘�젣)
    return HttpResponseRedirect(reverse('index'))












