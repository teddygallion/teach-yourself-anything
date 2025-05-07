from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate

app_name = "accounts"

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('learn:dashboard')  
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            import json
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

        form = AuthenticationForm(request, data={'username': username, 'password': password})
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return JsonResponse({'message': 'Login successful', 'username': user.username})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    
    return JsonResponse({'error': 'GET not allowed'}, status=405)

    
def logout_view(request):
    logout(request)
    return redirect('accounts:login')