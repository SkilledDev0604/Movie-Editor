from django.shortcuts import render
from .utils import (make_video_1)
from django.shortcuts import redirect
from django.http import QueryDict
from django.templatetags.static import static

def product_view(request):
    if request.method == 'POST':
        preview_url = make_video_1(request.POST)
        # Create a QueryDict object to hold the GET parameters for redirect
        query_params = QueryDict(mutable=True)

        # Add or update the desired GET parameter
        query_params['preview_url'] = preview_url

        # Create the redirect URL with the updated query parameters
        redirect_url = '/video/preview/?{}'.format(query_params.urlencode())

        return redirect(redirect_url)
    return render(request, 'polls/product.html')

def preview_view(request):
    preview_url = request.GET.get('preview_url')
    video_url = static(preview_url)
    context = {'preview_url': video_url}
    return render(request, 'polls/preview.html', context)
