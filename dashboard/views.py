from django.shortcuts import render

from .models import Scan


def index(request):
    if request.method == 'POST':
        image = request.FILES.get('uploaded-image')
        print(f"image: {image}")

        new_scan = Scan.objects.create()
        new_scan.uploaded_image = image
        new_scan.save()

        print(new_scan.uploaded_image.url)

    return render(request, 'index.html', {
        'scans': [scan.serialize() for scan in Scan.objects.all()]
    })
