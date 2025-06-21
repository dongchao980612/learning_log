from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from django.contrib.auth.models import User
# Create your views here.
from django.urls import reverse

from learning_log_app.forms import TopicForm, EntryForm, UserEditForm
from learning_log_app.models import Topic, Entry


def base(request):
    return render(request, "learning_log_app/base.html")


def index(request):
    return render(request, "learning_log_app/index.html")

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# 注销视图
def logout_view(request):
    """注销当前用户"""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('/log/index')

# 登录视图
def login_view(request):
    """用户登录"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are now logged in as "+username+".")
                return redirect('/log/index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'learning_log_app/login.html', {'form': form})

# 注册视图
def register_view(request):
    """注册新用户"""
    if request.method != 'POST':
        # 显示空的注册表单
        form = UserCreationForm()
    else:
        # 处理填写好的表单
        form = UserCreationForm(data=request.POST)
        # print("form.is_valid() = ",form.is_valid())
        if form.is_valid():
            new_user = form.save()
            # 让用户自动登录，再重定向到主页
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
            messages.success(request, "注册成功！")
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('learning_log_app:index'))
        else:
            # messages.error(request, "注册失败！")
            print(form.errors)
    context = {'form': form}
    return render(request, 'learning_log_app/register.html', context)


def topics(request):
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_log_app/topics.html', context)


def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_log_app/topic.html', context)

def dashboard(request):
    return render(request, 'learning_log_app/profile.html')


def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = TopicForm()
    else:
        # POST提交的数据,对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('learning_log_app:topics'))
    context = {'form': form}
    return render(request, 'learning_log_app/new_topic.html', context)


def manage_topics(request):
    """主题管理页面"""
    topics = Topic.objects.all()
    context = {'topics': topics}
    return render(request, 'learning_log_app/manage_topics.html', context)

def manage_user(request):
    """用户管理页面"""
    users = User.objects.all().order_by('username')
    context = {'users': users}
    return render(request, 'learning_log_app/manage_users.html', context)


def new_user(request):
    """添加新用户"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return redirect('learning_log_app:manage_users')
    else:
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'learning_log_app/new_user.html', context)





def edit_user(request, user_id):
    """编辑用户"""
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('learning_log_app:manage_users')
    else:
        form = UserEditForm(instance=user)
    context = {'user': user, 'form': form}
    return render(request, 'learning_log_app/edit_user.html', context)


def delete_user(request, user_id):
    """删除用户"""
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('learning_log_app:manage_users')
    context = {'user': user}
    return render(request, 'learning_log_app/delete_user.html', context)




def new_entry(request,topic_id):
    """在特定的主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # 未提交数据,创建一个空表单
        form = EntryForm()
    else:
        # POST提交的数据,对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.title = new_entry.title or ''  # 提供默认值
            new_entry.save()
        return HttpResponseRedirect(reverse('learning_log_app:topic',
                                            args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_log_app/new_entry.html', context)


def edit_entry(request, entry_id):
    """编辑既有条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic


    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_log_app:topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_log_app/edit_entry.html', context)



def manage_notes(request):
    """笔记管理页面"""
    entrys = Entry.objects.all().order_by('date_added')
    context = {'entrys': entrys}
    return render(request, 'learning_log_app/manage_entrys.html', context)


def edit_topic(request,topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('learning_log_app:manage_topics')
    else:
        form = TopicForm(instance=topic)
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_log_app/edit_topic.html', context)