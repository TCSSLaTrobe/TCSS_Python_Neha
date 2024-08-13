from flask import redirect,request,render_template,url_for

def login_check():
    u_name=request.form["username"]
    pass1=request.form["password"]
    if(u_name='Neha@1' and pass1=='password@123'):
        return redirect("Welcome.html")
    elif(u_name==pass1):
        return redirect('login.html')
    else:
        return redirect('login.html')