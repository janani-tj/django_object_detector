from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .helper.live_stream import VideoCamera
import json

from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, StreamingHttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators import gzip
import threading
from .models import Video
import datetime


# Create your views here.

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def home(request):
    return render(request, 'users/home.html')


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required()
def profile(request):
    return render(request, 'users/profile.html')

@login_required()
@csrf_exempt
def objectdetection(request):
    template = loader.get_template('users/object.html')
    with open("C:\djangoWork\logindjango\logindjango\logintest\helper\coco.names", 'r') as f:
        classes=[w.strip() for w in f.readlines()]
    print(classes)
    a=[]
    for n, cls in enumerate(classes):
        a.append(cls)
    
    context = {
        'a':a
    }
    return HttpResponse(template.render(context, request))


cam=1
@gzip.gzip_page
@login_required()
def videostream(request):
    template = loader.get_template('users/videostream.html')
    global cam
    if cam==1:
        cam = VideoCamera()
    
    context = {
        'cam':gen(cam),
    }  

    #return HttpResponse(template.render())
    return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    #return HttpResponse(template.render(context, request))


cap=0

def game(classes1):
    #print( "here")
    global cam
    global cap
    #print(cam)
    #print(cap)
    if cam==1:
        cam=VideoCamera()
    if cap==0:
        pass
        #cap=cam.video
    #print(cam)
    #print(cap)
    
    with open("C:\djangoWork\logindjango\logindjango\logintest\helper\coco.names", 'r') as f:
        classes=[w.strip() for w in f.readlines()]
    #classes1=list(json.loads(request.body)["classes"])
    classes1
    #print ("here2")
    import cv2
    import numpy as np
    import sys
    sys.path.insert(0,"C:\djangoWork\logindjango\logindjango\logintest\helper")
# import the yolo detector file
    from .helper.YoloDetector import YoloDetector
    #from yolo.request.helper.YoloDetector import YoloDetector
    selected = {"person": (0, 255, 255),
            "laptop": (0, 0, 0)}
# initialize the detector with the paths to cfg, weights, and the list of classes
    detector = YoloDetector("C:\djangoWork\logindjango\logindjango\logintest\helper\yolov3-tiny.cfg", "C:\djangoWork\logindjango\logindjango\logintest\helper\yolov3-tiny.weights", classes,classes1)
# initialize video stream
    cap = cv2.VideoCapture("C:\djangoWork\logindjango\logindjango\logintest\helper\input_video.mp4")
    #cap = cv2.VideoCapture(0)
    
# read first frame
    ret, frame = cam.grabbed,cam.frame
# loop to read frames and update window
    print(ret)
    #ret=True
    while ret:
    # this returns detections in the format {cls_1:[(top_left_x, top_left_y, top_right_x, top_right_y), ..],
    #                                        cls_4:[], ..}
    # Note: you can change the file as per your requirement if necessary
        print("here1")
        detections = detector.detect(frame)
    # loop over the selected items and check if it exists in the detected items, if it exists loop over all the items of the specific class
    # and draw rectangles and put a label in the defined color
        for cls, color in selected.items():
            print("here3")
            if cls in detections:
                for box in detections[cls]:
                    print("here4")
                    x1, y1, x2, y2 = box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness=1)
                    cv2.putText(frame, cls, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color)
    # display the detections
        cv2.imshow("detections", frame)
        #yield frameeee
        #ret, frame = cap.read()
        # yield (b'--frame\r\n'
        #        b'content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n\r\n')
        #print(frame)
        #frames.append(frame)
    # wait for key press
        key_press = cv2.waitKey(1) & 0xff
    # exit loop if q or on reaching EOF
        if key_press == ord('q'):
            break
        ret, frame = cam.grabbed,cam.frame
        
# release resources
    #cap.release()
    #cap=0
    # cam=1
# destroy window
    cv2.destroyAllWindows()
    #return frame

@csrf_exempt
@gzip.gzip_page
def run_video(request):
    classes1=json.loads(request.body)["classes"]
    game(classes1)
    #threading.Thread(target=game,args=(request)).start()
    #return StreamingHttpResponse(game(classes1),content_type="multuipart/x-mixed-replace;boundary=frame")





@csrf_exempt
def classes(request):
    with open("C:\djangoWork\logindjango\logindjango\logintest\helper\coco.names", 'r') as f:
        classes=[w.strip() for w in f.readlines()]
    print(classes)
    a=[]
    for n, cls in enumerate(classes):
        a.append(cls)
    return JsonResponse(a,safe=False)


@csrf_exempt
def add_db(request):
    x=json.loads(request.body)["name"]
    member = Video(name=x)
    member.save()
    return JsonResponse({"message":"saved"})

@csrf_exempt
def delete_db(request):
    x=json.loads(request.body)["name"]
    member = Video.objects.filter(name=x).first()
    member.delete()
    return JsonResponse({"message":"deleted"})


@csrf_exempt
@gzip.gzip_page
def objtest(request):
    classes1 = []
    classes1 = request.GET.getlist('classes')
    print(classes1)
    game(classes1)
    #return HttpResponse(classes1)
    StreamingHttpResponse(game(classes1),content_type="multuipart/x-mixed-replace;boundary=frame")






