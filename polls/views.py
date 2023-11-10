from django.shortcuts import render
from .utils import (make_video_1)
from django.shortcuts import redirect
from django.http import QueryDict
from django.templatetags.static import static
from .forms import ImageForm
from django.conf import settings
import datetime
import os

def product_view(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        uploaded_image_dir = f"{settings.BASE_DIR}/static/images/uploaded/"
        image_file = request.FILES.get('image')
        image = None
        if image_file:
            now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
            image = f'{uploaded_image_dir}image_{now}.jpg'
            with open(image, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
        preview_url = make_video_1(request.POST, image)
        if image and os.path.exists(image):
            os.remove(image)
        query_params = QueryDict(mutable=True)
        query_params['preview_url'] = preview_url
        redirect_url = '/video/preview/?{}'.format(query_params.urlencode())
        return redirect(redirect_url)
    return render(request, 'polls/product.html', {"form": ImageForm})

def preview_view(request):
    preview_url = request.GET.get('preview_url')
    video_url = static(preview_url)
    context = {'preview_url': video_url}
    return render(request, 'polls/preview.html', context)
