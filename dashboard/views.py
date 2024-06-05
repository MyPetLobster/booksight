from django.http import JsonResponse
from django.shortcuts import render

import os
import threading

from .models import Scan
from vision.vision import vision_core
import vision.utility as util
import vision.vision_config as vision_config

from dotenv import load_dotenv
load_dotenv()

def index(request):
    return render(request, 'index.html')


def vision(request):
    if request.method == 'POST':
        # Clear all temp directories
        util.empty_export_dirs()
        util.empty_directory('media/uploaded_images')
        util.empty_directory('media/detection_temp/debug_images')
        util.empty_directory('media/detection_temp/downloaded_images')
        util.empty_directory('media/detection_temp/spines')

        # Create log file for new session
        util.create_log_file()
        util.log_print('Beginning new session with Booksight Vision Web App\n')

        # Get all form data
        image = request.FILES.get('uploaded-image')
        if not image:
            return render(request, 'index.html', {
                'error': 'No image uploaded'
            })
        email = request.POST.get('user-email')
        formats = request.POST.getlist('format')
        ai_model = request.POST.get('ai-model')
        ai_temp = float(request.POST.get('ai-temp'))
        torch_confidence = float(request.POST.get('torch-confidence')) 

        # Check if .env file exists
        if not os.path.exists('.env'):
            util.log_print('Missing .env file')
            return render(request, 'index.html', {
                # TODO: Are my errors being displayed correctly?
                'error': 'Missing .env file'
            })
        else: 
            google_gemini_key = os.getenv('GOOGLE_GEMINI_KEY')
            google_books_key = os.getenv('GOOGLE_BOOKS_KEY')
            isbndb_key = os.getenv('ISBNDB_KEY')
            open_ai_key = os.getenv('OPENAI_API_KEY')
            gmail_user = os.getenv('GMAIL_USERNAME')
            gmail_pass = os.getenv('GMAIL_PASSWORD')

            # Check if any API keys are missing
            if not google_gemini_key and not open_ai_key:
                return render(request, 'index.html', {
                    'error': 'Need at least one AI API key. As of 6/03/2024 Gemini has a generous free tier.'
                })
            elif not google_books_key:
                return render(request, 'index.html', {
                    'error': 'Missing Google Books API key. You can get this key for free.'
                })
            elif not isbndb_key:
                return render(request, 'index.html', {
                    'error': 'Missing ISBNdb API key. This key is NOT free and has strict rate limits.'
                })
            elif not gmail_user or not gmail_pass:
                return render(request, 'index.html', {
                    'error': 'Missing Gmail credentials. This is required to send emails.'
                })
        
        credentials = {
            'google_gemini_key': google_gemini_key,
            'google_books_key': google_books_key,
            'isbndb_key': isbndb_key,
            'open_ai_key': open_ai_key,
        }

        # Save data/settings in VisionConfig class
        config = vision_config.VisionConfig(email, formats, ai_model, ai_temp, torch_confidence, credentials)
        
        # Create new scan and save image
        new_scan = Scan.objects.create()
        new_scan.uploaded_image = image
        new_scan.save()
        upload_path = new_scan.uploaded_image.path

        util.log_print('\nForm Submitted, new scan request details:\n')
        util.log_print(f'Email: {email},\nFormats: {formats},\nImage: {image},\nAI Model: {ai_model},\nAI Temp: {ai_temp},\nTorch Confidence: {torch_confidence}')

        # Run Vision app in a separate thread
        thread = threading.Thread(target=vision_core, args=(upload_path, new_scan, config))
        thread.setDaemon(True)
        thread.start()

        return render(request, 'vision.html', {
            'image_path': new_scan.uploaded_image.url
        })

    else: # GET request
        return render(request, 'index.html', {
            'error': 'Invalid request method'
        })


def vision_status(request):
    """Query the status of the most recent Scan object and return the status as a JSON response.
    Used to feed data to the pseudo-terminal in the frontend to display the status of the vision app."""
    last_scan = Scan.objects.first()
    vision_status = last_scan.scan_status
    
    if vision_status == 'bbox-detected':
        return JsonResponse({
            'status': 'bbox-detected',
            'bbox_image': last_scan.bbox_image
        })
    elif vision_status == 'text-detected':
        text_images = last_scan.text_images
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
    elif vision_status == 'failed': 
        return render(request, 'vision_failed.html')
    else:
        return JsonResponse({
            'status': 'error',
        })


def about(request):
    return render(request, 'about.html')


def tips(request):
    return render(request, 'tips.html')


def vision_complete(request):
    return render(request, 'vision_complete.html')


def vision_failed(request):
    return render(request, 'vision_failed.html')