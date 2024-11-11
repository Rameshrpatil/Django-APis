from django.shortcuts import render
from django.http import HttpResponse

def check(request):
    return render(request, 'check.html')

from django.shortcuts import render, HttpResponse
from firebase_admin import storage

def upload_image(request):
    if request.method == 'POST':
        # Extract file from the request
        file = request.FILES.get('files[]')
        if not file:
            return HttpResponse("No file uploaded", status=400)

        # Firebase storage
        bucket = storage.bucket()
        blob = bucket.blob(file.name)

        # Upload the file to Firebase Storage
        blob.upload_from_file(file, content_type=file.content_type)

        # Get the file's URL after upload
        file_url = blob.public_url

        return HttpResponse(f'File uploaded successfully! URL: {file_url}')
    return HttpResponse("Invalid method", status=405)

