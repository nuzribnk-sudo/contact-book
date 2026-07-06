from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Contact
from .forms import ContactForm
from django.db.models import Q


# ==========================
# Signup
# ==========================
def signup_user(request):

    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors)

    return render(request, 'signup.html', {'form': form})


# ==========================
# Login
# ==========================
def login_user(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            return render(request, 'login.html', {
                'error': 'Invalid Username or Password'
            })

    return render(request, 'login.html')


# ==========================
# Logout
# ==========================
def logout_user(request):
    logout(request)
    return redirect('login')


# ==========================
# Home
# ==========================
@login_required(login_url='login')
def home(request):

    query = request.GET.get('q')

    contacts = Contact.objects.filter(user=request.user)

    if query:
        contacts = contacts.filter(
            Q(name__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query)
        )

    return render(request, 'home.html', {
        'contacts': contacts,
        'query': query
    })


# ==========================
# Add Contact
# ==========================
@login_required(login_url='login')
def add_contact(request):

    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES)

        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('home')

        else:
            print(form.errors)   

    else:
        form = ContactForm()

    return render(request, 'add_contact.html', {'form': form})
# ==========================
# View Contact
# ==========================
@login_required(login_url='login')
def view_contact(request, id):

    contact = get_object_or_404(
        Contact,
        id=id,
        user=request.user
    )

    return render(request, 'viewcontact.html', {
        'contact': contact
    })


# ==========================
# Edit Contact
# ==========================
@login_required(login_url='login')
def edit_contact(request, id):

    contact = get_object_or_404(
        Contact,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        form = ContactForm(
            request.POST,
            request.FILES,
            instance=contact
        )

        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = ContactForm(instance=contact)

    return render(request, 'editcontact.html', {
        'form': form
    })


# ==========================
# Delete Contact
# ==========================
@login_required(login_url='login')
def delete_contact(request, id):
    contact = get_object_or_404(Contact, id=id)
    contact.delete()
    return redirect('home')
