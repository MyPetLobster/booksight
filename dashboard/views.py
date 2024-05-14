from django.shortcuts import render

from .models import Scan


def index(request):
    return render(request, 'index.html', {
        'scans': [scan.serialize() for scan in Scan.objects.all()]
    })


def vision(request):
    if request.method == 'POST':
        image = request.FILES.get('uploaded-image')

        if not image:
            return render(request, 'index.html', {
                'error': 'No image uploaded'
            })
        
        new_scan = Scan.objects.create()
        new_scan.uploaded_image = image
        new_scan.save()

        return render(request, 'vision.html', {
            'scan': new_scan.serialize()
        })

    else: # GET request
        return render(request, 'index.html', {
            'error': 'Invalid request method'
        })


def about(request):
    return render(request, 'about.html')