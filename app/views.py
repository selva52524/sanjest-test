from django.shortcuts import render, redirect
from .models import Resume
from .gdrive_service import upload_to_gdrive
import os

def upload_resume(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['resume']
        file_name = uploaded_file.name
        
        # Ensure the 'temp' directory exists
        temp_dir = 'temp'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        file_path = os.path.join(temp_dir, file_name)

        # Save the uploaded file temporarily
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Google Drive folder ID where you want to store the files
        folder_id = ''  # Your actual folder ID

        # Upload to Google Drive
        gdrive_link = upload_to_gdrive(file_path, file_name, folder_id)

        if gdrive_link:
            # Save the link in the database
            resume = Resume.objects.create(name=file_name, gdrive_link=gdrive_link)
            resume.save()

            # Delete the temporary file
            os.remove(file_path)

            return redirect('resume_list')
        else:
            return render(request, 'app/upload_resume.html', {'error': 'Failed to upload to Google Drive. Please try again.'})

    return render(request, 'app/upload_resume.html')

def resume_list(request):
    resumes = Resume.objects.all()
    return render(request, 'app/resume_list.html', {'resumes': resumes})
