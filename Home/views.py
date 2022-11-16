from django.shortcuts import render, HttpResponse, redirect

# added by me
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

import requests
import json
import os
import time

def about(request):
    return render(request,"about.html")
def blog(request):
    return render(request,"blog.html")
def contact(request):
    return render(request,"contact.html")
def details(request):
    return render(request,"details.html")
def gallery(request):
    return render(request,"gallery.html")
def index1(request):
    return render(request,"index.html")
def services(request):
    return render(request,"services.html")
def shopdet(request):
    return render(request,"shop-details.html")
def shop(request):
    return render(request,"shop.html")



def myhome(request):
    if request.method == "POST" and request.user.is_authenticated == True:
        geojson = request.POST.get("areaData")


        url1 = "https://api-connect.eos.com/field-management"
        payload1 = geojson
        headers = {
            "x-api-key" : "apk.b4298ea53d7845b1d6d00b8d989b4e62190900bfe0c35eac84bea59add85bf84"
        }
        response1 = requests.request("POST", url1, headers=headers, data=payload1)
        print(response1.text)
        dict1 = json.loads(response1.text)
        fieldId = dict1["id"]


        
        url2 = "https://api-connect.eos.com/scene-search/for-field/"+str(fieldId)
        payload2 = '''{
        "params": {
            "date_start" : "2022-11-02",
            "date_end" : "2022-11-07",
            "data_source" : [
                "sentinel2"
            ]

        }
        }'''
        response2 = requests.request("POST", url2, headers=headers, data=payload2)
        print(response2.text)
        dict2 = json.loads(response2.text)
        reqId = dict2["request_id"]
        response2.close()
        

        url3 = "https://api-connect.eos.com/scene-search/for-field/"+str(fieldId)+"/"+str(reqId)
        payload3 = ""
        time.sleep(20)
        response3 = requests.request("GET", url3, headers=headers, data=payload3)
        print(response3.text) 
        dict3 = json.loads(response3.text)
        resultListOfDict = dict3["result"]
        i = len(resultListOfDict)-1
        viewId = resultListOfDict[i]["view_id"]
        while i!=-1:
            if resultListOfDict[i]["cloud"]==0.0:
                viewId = resultListOfDict[i]["view_id"]
                break
            i = i-1

        
        url4 = "https://api-connect.eos.com/field-imagery/indicies/"+str(fieldId)
        payload4 = '''{
            "params": {
                "view_id": "S2/43/Q/HC/2022/11/4/0",
                "index": "NDVI",
                "format": "png"
            },
            "callback_url": "https://test.local"
        }'''
        p4Dict = json.loads(payload4)
        p4Dict["params"]["view_id"] = viewId
        payload4 = json.dumps(p4Dict)
        time.sleep(20)
        response4 = requests.request("POST", url4, headers=headers, data=payload4)
        print(response4.text)
        dict4 = json.loads(response4.text)
        requestId = dict4["request_id"]

        print("wait for 5th url")
        url5 = "https://api-connect.eos.com/field-imagery/"+str(fieldId)+"/"+str(requestId)
        payload5 = ""
        time.sleep(20)
        response5 = requests.request("GET", url5, headers=headers, data=payload5)

        # save image
        open(str(os.getcwd())+"\\static\\fieldimages\\image.png", 'wb').write(response5.content)

        # Load image page
        return render(request,"image.html")
    
    if request.user.is_authenticated:
        userInfo = {
            "userID": request.user.username,
            "fname": request.user.first_name
        }
        return render(request,"mapselect.html", userInfo)
    else:
        return redirect("signin")









def signin(request):
    if request.method == "POST":
        userName = request.POST.get("userName")
        password = request.POST.get("password")

        user = authenticate(request, username = userName, password = password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return redirect("signin")
    return render(request,"LoginRegister.html")

def register(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        userName = request.POST.get("userName")
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(fname,lname,userName,email,password)
        newUser = User.objects.create_user(userName, email, password)
        newUser.first_name = fname
        newUser.last_name = lname
        newUser.save()
        return redirect("signin")
    else:
        return render(request,"LoginRegister.html")

def signout(request):
    logout(request)
    return redirect("signin")
























    