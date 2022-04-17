from unittest import result
from django.http import HttpResponse
from django.shortcuts import render
from calc.forms import PersonForm
from calc.machinelearning import pipeline_model
from django.conf import settings
from calc.models import Person, RegisteredChild
import cv2
import os

# Create your views here.
def home(request):
    return render(request, 'home.html' , {'name' : 'Harsh'})

def printt(request):
    form = PersonForm()
    if request.method == "POST":
        form = PersonForm(request.POST or None ,request.FILES or None)
        if form.is_valid():
            save = form.save(commit=True)
            pk = save.pk
            image_obj = Person.objects.get(pk = pk)
            fileroot = str(image_obj.image)
            filepath = os.path.join(settings.MEDIA_ROOT , fileroot)
            print(filepath)
            img , cnt = pipeline_model(filepath)
            detected_person = RegisteredChild.objects.get(pk = cnt)
            print(detected_person)
            print("YYYYYYYYYYYYYYAAAAAAAAAAAAAYYYYYYYYYYYYYYY -- " , cnt)
            cv2.imshow("detected" , img)
            cv2.waitKey(0)
            return render(request , 'home.html' , {'detected_person' : detected_person})
            
    return render(request , 'result.html' , {'form':form})