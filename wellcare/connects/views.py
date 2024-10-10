from django.shortcuts import render
from django.views import View

# Create your views here.
class HomePage(View):
    def get(self, request):
        return render(request, 'index.html',{
            
        })

class CheckPage(View):
    def get(self, request):
        return render(request, 'check.html',{
            
        })

class ShowCheckPage(View):
    def get(self, request):
        return render(request, 'showcheck.html',{
            
        })