from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse


def homepage(request):
    return render(request, 'homepage.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'user_list.html', {'users': users})


@login_required
def chat_with(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        recipient__in=[request.user, other_user]
    ).order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content')
        uploaded_file = request.FILES.get('file')
        if content or uploaded_file:
            Message.objects.create(
                sender=request.user,
                recipient=other_user,
                content=content,
                file=uploaded_file
            )
        return redirect('chat_with', user_id=other_user.id)

    return render(request, 'chat.html', {
        'other_user': other_user,
        'messages': messages
    })


@login_required
def get_messages(request, user_id):
    other_user = User.objects.get(id=user_id)
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        recipient__in=[request.user, other_user]
    ).order_by('timestamp')

    Message.objects.filter(
        sender=other_user,
        recipient=request.user,
        is_read=False
    ).update(is_read=True)

    messages_data = [
        {
            'sender': msg.sender.username,
            'content': msg.content,
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'is_read': msg.is_read,
            'file': msg.file.url if msg.file else None

        }
        for msg in messages
    ]
    return JsonResponse({'messages': messages_data})
