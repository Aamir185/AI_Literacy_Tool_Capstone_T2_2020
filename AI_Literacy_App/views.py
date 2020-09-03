from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from .forms import ImageForm
from django.db.utils import OperationalError
import os
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Create your views here.
def index(request):
    return render(request, 'index.html')

def examples(request):
    return render(request, 'examples.html')

def age_gender(request):
    return render(request, 'age_gender_example.html')

@csrf_exempt
def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                form.save()
            except (OperationalError):
                print("There was an DB Operational Error, but the image has been saved in FS")

            return JsonResponse({"error":"false", "message":"Succesfully saved", "data": request.FILES['image'].name})

        else:
            print(request)
            return JsonResponse({'message': 'Failure at validations', 'errors': form.errors})
    else:
        form = ImageForm()
    return JsonResponse({'message': 'Failure'})
    
@csrf_exempt
def run_module(request):
    """  """
    if request.method == "POST":
        module = request.POST['module']
        image_name = request.POST['data']
        input_path = os.path.join(BASE_DIR, "media\images\\")
        scripts_path = os.path.join(BASE_DIR, "Scripts")
        if(module == "face"):
            #face_detector = scripts_path+"\\face_detector"
            #age_detector = scripts_path+"\\age_detector"
            command = 'python "'+scripts_path+'\\face.py" '+'--image "'+input_path + image_name + '"'
            print(command)
            try:
                subprocess.call(command)
                return JsonResponse({'error': 'False'})
            except:
                return JsonResponse({'error': 'True'})


        elif(module == "features"):
            command = 'python "'+scripts_path+'\\features.py" '+'--image "'+input_path + image_name + '"'
            print(command)
            try:
                subprocess.call(command)
                return JsonResponse({'error': 'False'})
            except:
                return JsonResponse({'error': 'True'})
        

        elif(module == "age"):
            command = 'python "'+scripts_path+'\\age.py" '+'--image "'+input_path + image_name + '"'
            print(command)
            try:
                subprocess.call(command)
                return JsonResponse({'error': 'False'})
            except:
                return JsonResponse({'error': 'True'})

        else:
            command = 'python "'+scripts_path+'\\gender.py" '+'--image "'+input_path + image_name + '"'
            print(command)
            try:
                subprocess.call(command)
                return JsonResponse({'error': 'False'})
            except:
                return JsonResponse({'error': 'True'})
            
            







