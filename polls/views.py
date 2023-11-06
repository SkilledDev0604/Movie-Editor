from django.shortcuts import render
from .utils import (make_video_1)

def page_view(request):
    if request.method == 'POST':
        make_video_1(request.POST)
        print(request.POST['linea1'])
    return render(request, 'polls/page.html')
