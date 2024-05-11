from django.shortcuts import render

from .models import Scan


def index(request):

    return render(request, 'index.html', {
        'scan': Scan.objects.first()
    })
