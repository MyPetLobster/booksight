from django.shortcuts import render

import shutil
import threading

from .models import Scan
from vision.vision import vision as vision_app


def index(request):
    return render(request, 'index.html', {
        'scans': [scan.serialize() for scan in Scan.objects.all()]
    })


def vision(request):
    if request.method == 'POST':
        image = request.FILES.get('uploaded-image')
        email = request.POST.get('user-email')
        formats = request.POST.getlist('format')

        print(f'Email: {email}')
        print(f'Formats: {formats}')
        print(f'Image: {image}')

        if not image:
            return render(request, 'index.html', {
                'error': 'No image uploaded'
            })
        
        new_scan = Scan.objects.create()
        new_scan.uploaded_image = image
        new_scan.save()

        # Copy user uploaded image to scan_images directory
        shutil.copy(new_scan.uploaded_image.path, f'vision/images/scan_images/{new_scan.id}.jpg')
        new_path = f'vision/images/scan_images/{new_scan.id}.jpg'

        # Run vision function
        # vision_app(new_path)

        # Create separate thread to run vision function
        thread = threading.Thread(target=vision_app, args=(new_path, email, formats))
        thread.setDaemon(True)
        thread.start()

        return render(request, 'vision.html', {
            'scan': new_scan.serialize()
        })

    else: # GET request
        return render(request, 'index.html', {
            'error': 'Invalid request method'
        })


def about(request):
    return render(request, 'about.html')