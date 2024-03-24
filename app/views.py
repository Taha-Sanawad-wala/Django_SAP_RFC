from django.shortcuts import render,redirect
from pyrfc import Connection, ABAPApplicationError, ABAPRuntimeError, LogonError, CommunicationError
import pandas as pd
import ssl
import asyncio
# Create your views here.
conn=""
def index(request):
    if request.method=="POST":
        try:
            ASHOST = request.POST.get("ashost")     
            SYSNR =  request.POST.get("sysnr")      
            CLIENT = request.POST.get("client")     
            USER = request.POST.get("user")         
            PASSWD = request.POST.get("password") 
            global conn
            conn = Connection(ashost=ASHOST, sysnr=SYSNR, client=CLIENT, user=USER, passwd=PASSWD)
            print("success")
            return redirect(tables)
        except LogonError:
            errormsg={"msg":"wrong username or password"}
            return render(request,"index.html",errormsg)
        except:
            errormsg={"msg":"error"}
            return render(request,"index.html",errormsg)
    else:
        return render(request,"index.html")

def tables(request):
    if request.method=="POST":
        rfc=request.POST.get("rfc")
        table=request.POST.get("table")
        global conn
        print(table)
        result = conn.call(rfc, 
        QUERY_TABLE = table, 
        DELIMITER ="|"
        # OPTIONS = options, 
        #   ROWSKIPS = 0
        #   ROWCOUNT = 10
        )
        print(type(result["DATA"]))
        l=[]
        for i in result["DATA"]:
            l.append(i["WA"].split("|"))
        data={"result":l,"table_name":table}
        return render(request,"tables.html",data)
    elif conn=="":
        return redirect(index)
    else:
        return render(request,"tables.html")
