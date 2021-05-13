from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user = authenticate(request,username=username, password=password)

            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.info(request,'UserName or Password is Incorrect!')
        context={}
        return render(request,'payapp/login.html',context)

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form=UserCreationForm()
        if request.method == 'POST':
            form=UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                usrnme = form.cleaned_data.get('username')
                phone=request.POST.get('Phno')
                money=request.POST.get('Mny')
                customer = Customer(name=usrnme,phone=phone,money=money)
                customer.save()
                messages.success(request,'Account Created for '+ usrnme)

                return redirect('login')
        context={'form':form}
        return render(request,'payapp/register.html',context)


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    current_user = request.user
    ans = Customer.objects.all().filter(name=current_user)
    
    # print(a.phone)
    # a.phone = "00110011"
    # a.save()
    checkPhone = ans[0].phone
    checkMoney = ans[0].money
    print(current_user , ans[0].phone, type(checkMoney))
    if request.method == 'POST':
        
        Sender=request.POST.get('senderNumber')
        Receiver=request.POST.get('receiverNumber')
        amt=request.POST.get('transferAmount')
        Amt = float(amt)
        print(amt,Amt,checkMoney)
        remainingBalance = checkMoney-Amt
        

        

        if Sender != checkPhone:
            print("NO transaction, phone number not matching")
            messages.warning(request, 'Phone Number not matching, Transaction Failed')
            return render(request,'payapp/dashboard.html')
        #else if :
        try:
            b = Customer.objects.get(phone=Receiver)
        except:
            print("NO transaction, Receiver does not exist")
            messages.warning(request, 'Receiver does not exist, Transaction Failed')
            return render(request,'payapp/dashboard.html')
            
        if remainingBalance < 1000 :
            print("Insufficient Balance: ")
            if remainingBalance <= 0:
                messages.warning(request, 'Insufficient Balance, Transaction Failed')
            else:
                messages.warning(request, 'Transaction Failed, Minimum $1000 balance needed')
            return render(request,'payapp/dashboard.html')
        

        print("Sufficient Balance")
        print(remainingBalance)
        print("Transaction in Progress")
        transaction=Transaction(fromPhone=Sender,toPhone=Receiver,amt=amt)
        transaction.save()
        
        a = Customer.objects.get(name=current_user)
        a.money=remainingBalance
        a.save()
        b.money+=Amt
        b.save()
        messages.success(request,'Money Transferred!')
        
    
    return render(request,'payapp/dashboard.html')


from django.db.models import Q

@login_required(login_url='login')
def userTrans(request):
    current_user = request.user
    ans = Customer.objects.all().filter(name=current_user)
    checkName  = ans[0].name
    checkPhone = ans[0].phone
    checkMoney = ans[0].money
    if request.method == 'POST':
        UserName=request.POST.get('Uname')
        Phone=request.POST.get('Phno')
        if checkName == UserName and checkPhone==Phone:
            print(checkMoney)
            a=Transaction.objects.all().filter(fromPhone=Phone)
            b=Transaction.objects.all().filter(toPhone=Phone)
            c=Transaction.objects.all().filter(Q(toPhone=Phone) | Q(fromPhone=Phone))
            try:
                for x in a:
                    print('A')
                    print(x.amt)
                for y in b:
                    print('B')
                    print(y.amt)
                for z in c:
                    print('C')
                    print(z.amt)
            except:
                print("over")
            return render(request,'payapp/t_list.html',{'c': c,
                                                        'checkMoney':checkMoney})
        else:
            print("error")
    # c=Transaction.objects.all().filter(Q(toPhone=Phone) | Q(fromPhone=Phone))
    return render(request,'payapp/transaction.html')

@login_required(login_url='login')
def userTransList(request):
    return render(request,'payapp/t_list.html')