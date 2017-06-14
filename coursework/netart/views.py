from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import *
from .models import *


def index(request):
    news = News.objects.all()
    past = timezone.now() - timezone.timedelta(days=1)
    recently_added = Picture.objects.filter(uploaded_at__range=(past.date(), timezone.now().date()))
    context = {'news': news, 'recently': recently_added, 'form': AuthenticationForm()}

    return render(request, 'netart/index.html', context)


def profile(request, user_id):
    user = User.objects.get(id=user_id)
    context = {'user': user}

    return render(request, 'netart/profile.html', context)


def profile_edit(request, user_id):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            city = form.cleaned_data['city']
            birthdate = form.cleaned_data['birthdate']
            role = form.cleaned_data['role']
            edit_profile(user_id, first_name, last_name, birthdate, city, role)
            return redirect('netart:profile', user_id=user_id)
    else:
        user = User.objects.get(id=user_id)
        form = ProfileEditForm(initial=
                               {
                                   "first_name": user.first_name,
                                   "last_name": user.last_name,
                                   "city": user.profile.city,
                                   "birthdate": user.profile.birthdate
                               })
    context = {'form': form}
    return render(request, 'netart/profile_edit.html', context)


def upload_new_avatar(request, user_id):
    if request.method == 'POST':
        form = ChangeAvatarForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            change_avatar(user_id, image)
            return redirect('netart:profile', user_id=user_id)
    else:
        form = ChangeAvatarForm()
    context = {'form': form}
    return render(request, 'netart/avatar_change.html', context)


def catalog(request):
    try:
        cat_nature = Picture.objects.filter(theme='Nature')
        cat_people = Picture.objects.filter(theme='People')
        cat_sketch = Picture.objects.filter(theme='Sketch')
        cat_animals = Picture.objects.filter(theme='Animals')
    except:
        cat_people =[]
        cat_sketch = []
        cat_animals = []
    paginator_nat = Paginator(cat_nature, 6)
    paginator_people = Paginator(cat_people, 6)
    paginator_sketch = Paginator(cat_sketch, 6)
    paginator_anim = Paginator(cat_animals, 6)
    page = request.GET.get('page', 1)
    try:
        pages_nat = paginator_nat.page(page)
        pages_people = paginator_people.page(page)
        pages_sketch = paginator_sketch.page(page)
        pages_anim = paginator_anim.page(page)
    except PageNotAnInteger:
        pages_nat = paginator_nat.page(1)
        pages_people = paginator_people.page(1)
        pages_sketch = paginator_sketch.page(1)
        pages_anim = paginator_anim.page(1)
    except EmptyPage:
        pages_nat = paginator_nat.page(paginator_nat.num_pages)
        pages_people = paginator_people.page(paginator_people.num_pages)
        pages_sketch = paginator_sketch.page(paginator_sketch.num_pages)
        pages_anim = paginator_anim.page(paginator_anim.num_pages)
    past = timezone.now() - timezone.timedelta(days=1)
    recently_added = Picture.objects.filter(uploaded_at__range=(past.date(), timezone.now().date()))
    context = {'pages_nat': pages_nat, 'pages_people': pages_people,
               'pages_sketch': pages_sketch, 'pages_anim': pages_anim, 'recently': recently_added}

    return render(request, 'netart/catalog.html', context)


def upload_picture(request):
    if request.method == 'POST':
        form = PictureUploadForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            theme = form.cleaned_data['theme']
            style = form.cleaned_data['style']
            image = form.cleaned_data['image']
            upload_image(request.user.id, title, theme, style, image)
            return redirect('netart:catalog')
    else:
        form = PictureUploadForm()
    return render(request, 'netart/upload.html', {'form': form})


def msg_box(request):
    msgs = Message.objects.filter(receiver=request.user.id)
    sents = Message.objects.filter(sender=request.user.id)
    return render(request, 'netart/msg_box.html', {'msgs': msgs, 'sents': sents})


def send_msg(request):
    if request.method == 'POST':
        form = SendMessageForm(request.POST)
        if form.is_valid():
            receiver = form.cleaned_data['receiver']
            msg_content = form.cleaned_data['msg_content']
            send_message(request.user.id, receiver, msg_content)
            return redirect('netart:msg_box')
    else:
        form = SendMessageForm()
    return render(request, 'netart/send_msg.html', {'form': form})


def add_news(request):
    if request.method == 'POST':
        form = AddNewsForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            expodate = form.cleaned_data['expodate']
            expotheme = form.cleaned_data['expotheme']
            upload_news(image, title, text, expodate, expotheme)
            return redirect('netart:index')
    else:
        form = AddNewsForm()
    return render(request, 'netart/add_news.html', {'form': form})


def new_detail(request, new_id):
    news = News.objects.get(id=new_id)

    return render(request, 'netart/new_detail.html', {'news': news})