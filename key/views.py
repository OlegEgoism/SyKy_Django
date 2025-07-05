from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import CodeGenerator

code_gen = CodeGenerator()


def index(request):
    if request.method == 'POST':
        secret = request.POST.get('secret', '').strip()
        if secret:
            current_code = code_gen.update_code(secret)
            return render(request, 'index.html', {
                'current_code': current_code,
                'time_left': code_gen.time_left,
                'secret': secret,
            })

    current_code = code_gen.update_code()
    return render(request, 'index.html', {
        'current_code': current_code,
        'time_left': code_gen.time_left,
        'secret': code_gen.last_secret,
    })


def verify_code(request):
    if request.method == 'POST':
        code_to_verify = request.POST.get('code', '').strip()
        is_valid = code_gen.verify_code(code_to_verify)
        return render(request, 'verify.html', {
            'is_valid': is_valid,
            'code_entered': code_to_verify,
            'current_code': code_gen.last_code,
        })
    return redirect('index')


def get_current_code(request):
    current_code = code_gen.update_code()
    return JsonResponse({
        'code': current_code,
        'time_left': code_gen.time_left,
    })