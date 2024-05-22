from django.http import JsonResponse
from django.shortcuts import render

import shutil
import threading

from .models import Scan
from vision.vision import vision as vision_app
import vision.utility as util
from vision.utility import log_print


def index(request):
    return render(request, 'index.html')


def vision(request):
    if request.method == 'POST':
        # Empty temp dirs
        util.empty_directory('media/uploaded_images')
        util.empty_directory('media/detection_temp/debug_images')
        util.empty_directory('media/detection_temp/spines')

        # Create log file for new session
        util.create_log_file()
        
        image = request.FILES.get('uploaded-image')
        email = request.POST.get('user-email')
        formats = request.POST.getlist('format')

        log_print('\nForm Submitted, new scan request details:\n')
        log_print(f'Email: {email}')
        log_print(f'Formats: {formats}')
        log_print(f'Image: {image}')

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

        # Create separate thread to run Vision app
        thread = threading.Thread(target=vision_app, args=(new_path, email, formats, new_scan))
        thread.setDaemon(True)
        thread.start()

        new_scan_uploaded_image = new_scan.uploaded_image.url

        return render(request, 'vision.html', {
            'image_path': new_scan_uploaded_image
        })

    else: # GET request
        return render(request, 'index.html', {
            'error': 'Invalid request method'
        })


def about(request):
    return render(request, 'about.html')


def tips(request):
    return render(request, 'tips.html')


def vision_status(request):
    # Get most recent scan
    most_recent_scan = Scan.objects.first()
    vision_status = most_recent_scan.scan_status
    
    if vision_status == 'bbox-detected':
        return JsonResponse({
            'status': 'bbox-detected',
            'bbox_image': most_recent_scan.bbox_image
        })
    elif vision_status == 'text-detected':
        text_images = most_recent_scan.text_images
        return JsonResponse({
            'status': 'text-detected',
            'text_images': text_images,
        })
    elif vision_status == 'ai-complete':
        return JsonResponse({
            'status': 'ai-complete',
        })
    elif vision_status == 'completed':
        return JsonResponse({
            'status': 'completed',
        })
    elif vision_status == 'running':
        return JsonResponse({
            'status': 'running',
        })
    else:
        return JsonResponse({
            'status': 'error',
        })


def vision_complete(request):
    return render(request, 'vision_complete.html')