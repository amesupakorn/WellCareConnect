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
    
class ServiceFirst(View):
    def get(self, request):
        return render(request, 'services/first.html',{
            
        })
    
class ServiceFirst1(View):
    def get(self, request):
        return render(request, 'services/first-1.html',{
            
        })
    
class ServiceFirst2(View):
    def get(self, request):
        return render(request, 'services/first-2.html',{
            
        })
    
class ServiceFirst3(View):
    def get(self, request):
        return render(request, 'services/first-3.html',{
            
        })
    
class ServiceFirst4(View):
    def get(self, request):
        return render(request, 'services/first-4.html',{
            
        })
    
class ServiceSecond(View):
    def get(self, request):
        return render(request, 'services/second.html',{
            
        })

class ServiceSecond1(View):
    def get(self, request):
        return render(request, 'services/second-1.html',{
            
        })

class ServiceSecond2(View):
    def get(self, request):
        return render(request, 'services/second-2.html',{
            
        })
    
class ServiceSecond3(View):
    def get(self, request):
        return render(request, 'services/second-3.html',{
            
        })
    
class ServiceSecond4(View):
    def get(self, request):
        return render(request, 'services/second-4.html',{
            
        })
    
class ServiceThird(View):
    def get(self, request):
        return render(request, 'services/third.html',{
            
        })

class ServiceThird1(View):
    def get(self, request):
        return render(request, 'services/third-1.html',{
            
        })

class ServiceThird2(View):
    def get(self, request):
        return render(request, 'services/third-2.html',{
            
        })
    
class ServiceThird3(View):
    def get(self, request):
        return render(request, 'services/third-3.html',{
            
        })
    
class ServiceThird4(View):
    def get(self, request):
        return render(request, 'services/third-4.html',{
            
        })