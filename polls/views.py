from django.shortcuts import render
from .utils import (make_video, inputs, titles, samples)
from django.shortcuts import redirect
from django.http import QueryDict
from django.templatetags.static import static
from django.conf import settings
import datetime
import os

video_count = 2

def for_redirect(request):
    return redirect('/video/product/0')

def product_view(request, index):
    if not 0 <= index < video_count:
        return redirect('/video/product/0')
    print(f'request{index}')
    if request.method == 'POST':
        uploaded_image_dir = f"{settings.BASE_DIR}/static/images/uploaded/"
        image_file = request.FILES.get('image')
        image = None
        if image_file:
            now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
            image = f'{uploaded_image_dir}image_{now}.jpg'
            with open(image, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
        print('start makeing video')
        preview_url = make_video(index, request.POST, image)
        if image and os.path.exists(image):
            os.remove(image)
        query_params = QueryDict(mutable=True)
        query_params['preview_url'] = preview_url
        redirect_url = '/video/preview/?{}'.format(query_params.urlencode())
        return redirect(redirect_url)
    
    return render(request, f'polls/product.html', {"inputs": inputs[index], "title": titles[index], "sample_video": samples[index]})

def preview_view(request):
    preview_url = request.GET.get('preview_url')
    video_url = static(preview_url)
    context = {'preview_url': video_url}
    return render(request, 'polls/preview.html', context)
