from django.shortcuts import render
from django.views import View
from .models import Disease
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
        
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import Disease
import json
import base64


@method_decorator(csrf_exempt, name='dispatch')
class DiseaseWebhookView(View):

    def post(self, request, *args, **kwargs):
        # เรียกใช้ฟังก์ชันตรวจสอบ Basic Auth

        
        try:
            data = json.loads(request.body)
            disease_name = data['queryResult']['queryText']
            # ค้นหาข้อมูลโรคจากฐานข้อมูล
            try:
                disease = Disease.objects.filter(disease_name__icontains=disease_name).first()  # ใช้ icontains เพื่อค้นหาคำบางส่วน
                if disease:
                    response_text = (
                        f"ชื่อโรค: {disease.disease_name}\n"
                        f"คำอธิบายโรค: {disease.description}\n"
                        f"อาการของโรค: {disease.symptoms}\n"
                        f"วิธีการรักษาเบื้องต้น: {disease.treatment}\n"
                        f"ยารักษาโรค: {disease.medication}"
                    )
                else:
                    response_text = "ไม่พบข้อมูลโรคนี้ กรุณาลองใหม่"
            except Disease.DoesNotExist:
                response_text = "ไม่พบข้อมูลโรคนี้ กรุณาลองใหม่"

            return JsonResponse({"fulfillmentText": response_text})

        except Exception as e:
            return JsonResponse({"fulfillmentText": f"เกิดข้อผิดพลาด: {str(e)}"})

    def get(self, request, *args, **kwargs):
        return JsonResponse({"status": "POST requests only allowed"}, status=405)