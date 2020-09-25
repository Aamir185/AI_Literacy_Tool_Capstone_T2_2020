from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from .forms import ImageForm
from django.db.utils import OperationalError
import os, sys
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, os.path.join(BASE_DIR, "Scripts\\Example_2"))

import sentiment_analysis as sent


# Create your views here.
def index(request):
    return render(request, 'index.html')

def examples(request):
    return render(request, 'examples.html')

def age_gender(request):
    return render(request, 'age_gender_example.html')

def sentiment_analysis(request):
    return render(request, 'sentiment_analysis_example.html')

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
            command = 'python "'+scripts_path+'\\Example_1\\face.py" '+'--image "'+input_path + image_name + '"'
            print(command)
            try:
                subprocess.call(command)
                return JsonResponse({'error': 'False'})
            except:
                return JsonResponse({'error': 'True'})


        elif(module == "features"):
            command = 'python "'+scripts_path+'\\Example_1\\features.py" '+'--image "'+input_path + image_name + '"'
            print(command)
            try:
                subprocess.call(command)
                return JsonResponse({'error': 'False'})
            except:
                return JsonResponse({'error': 'True'})
        

        elif(module == "age"):
            command = 'python "'+scripts_path+'\\Example_1\\age.py" '+'--image "'+input_path + image_name + '"'
            print(command)
            try:
                subprocess.call(command)
                return JsonResponse({'error': 'False'})
            except:
                return JsonResponse({'error': 'True'})

        else:
            command = 'python "'+scripts_path+'\\Example_1\\gender.py" '+'--image "'+input_path + image_name + '"'
            print(command)
            try:
                subprocess.call(command)
                return JsonResponse({'error': 'False'})
            except:
                return JsonResponse({'error': 'True'})
@csrf_exempt           
def run_sentiment(request):
    if request.method == "GET":
        # Get a random tweet from data and send to server
        tweet = sent.getRandomTweet()
        return(HttpResponse(tweet))
    
    if request.method == "POST":
        tweet = request.POST['tweet']
        # Tokenize
        tokenized_words = sent.word_tokenize(tweet)
        # Lemmatize and remove stop words
        custom_tokens, lemmatized_tokens = sent.remove_noise(tokenized_words)
        # Detect sentiment
        sentiment = sent.getSentiment(custom_tokens)
        response = {
            'tweet': tweet,
            'tokenized': tokenized_words,
            'lemmatized': lemmatized_tokens,
            'cleaned': custom_tokens,
            'sentiment': sentiment
        }
        return(JsonResponse(response))





