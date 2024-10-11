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



class ChatPage(View):
    def get(self, request):
        return render(request, 'chatbot/chat.html',{
            
        })
        

import json
import requests  # สำหรับเรียก Infermedica API
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from googletrans import Translator


# ใส่ API key ของ Infermedica ที่คุณได้รับหลังการสมัคร
INFERMEDICA_API_KEY = "11c148e9564ce5e566cbf05d468b74ad"
INFERMEDICA_APP_ID = "b6b71842"

# ฟังก์ชันเพื่อโหลดข้อมูล Symptom ID จากไฟล์ JSON
def load_symptoms(file_path='symptoms.json'):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# ฟังก์ชันเพื่อค้นหา Symptom ID
def find_symptom_id(symptom_name, symptoms_data):
    symptom_name_cleaned = symptom_name.strip()
    for symptom in symptoms_data:
        if symptom['name_th'].strip() == symptom_name_cleaned:
            return symptom['id']
    return None

# ฟังก์ชันเพื่อค้นหา Symptom IDs หลายรายการ
def find_symptom_ids(symptom_names, symptoms_data):
    symptom_ids = []
    for symptom_name in symptom_names:
        symptom_id = find_symptom_id(symptom_name, symptoms_data)
        if symptom_id:
            symptom_ids.append({"id": symptom_id, "choice_id": "present"})
    return symptom_ids

# ฟังก์ชันแปลชื่อโรคเป็นภาษาไทย
def translate_condition_names(conditions):
    translator = Translator()
    translated_conditions = []
    for condition in conditions:
        if condition:
            translated = translator.translate(condition, src='en', dest='th').text
            translated_conditions.append(translated)
        else:
            translated_conditions.append("ไม่ทราบ")
    return translated_conditions

# ตัวอย่างการแมปเพศจากภาษาไทยเป็นภาษาอังกฤษ
def map_sex_th_to_en(user_input):
    if user_input == "ชาย":
        return "male"
    elif user_input == "หญิง":
        return "female"
    return None


@method_decorator(csrf_exempt, name='dispatch')
class HealthWebhookView(View):

    def post(self, request, *args, **kwargs):
        try:
            # แปลงข้อมูลจาก request body เป็น JSON
            data = json.loads(request.body)
            parameters = data['queryResult']['parameters']
            print(parameters)
            # เก็บสถานะการสนทนา (session)
            
            output_contexts = data['queryResult'].get('outputContexts', [])
            session_context = {}

            # ตรวจสอบและเก็บ context จาก outputContexts (เพื่อหลีกเลี่ยงการทับค่า)
            for context in output_contexts:
                if context['name'].endswith('/contexts/session'):
                    session_context = context.get('parameters', {})
                    break

            print(session_context)
            # ตรวจสอบสถานะของการสนทนา
            if 'sex' not in session_context:
                response_text_th = f"สวัสดีครับ! ยินดีต้อนรับสู่ WellCareChat ผู้ช่วยด้านสุขภาพของคุณ 🤗 \n 👋 ขั้นที่ 1 ช่วยบอกเพศกับผมหน่อยครับ (ชาย หรือ หญิง)"

                session_context['sexcheck'] = "pending"  # ตั้งค่าว่ากำลังถามเพศ
       
            elif 'sex' in session_context and session_context['sexcheck'] == 'pending':
                user_sex_th = parameters.get('sex', None)
                if user_sex_th:
                    user_sex = map_sex_th_to_en(user_sex_th)  # แปลงเพศเป็นภาษาอังกฤษ
                    if user_sex:
                        session_context['sex'] = user_sex  # เก็บค่าของเพศ
                        session_context['sexcheck'] = "ok"
                        response_text_th = "✨ ขั้นที่ 2 ช่วยบอกอายุของคุณหน่อยครับ"
                        session_context['agecheck'] = "pending"
                        print(session_context)
                    else:
                        response_text_th = "ช่วยบอกเพศของคุณอีกครั้งครับ (ชาย หรือ หญิง)"
                        print(session_context)
                else:
                    response_text_th = "ช่วยบอกเพศของคุณอีกครั้งครับ (ชาย หรือ หญิง)"
                    print(session_context)


            elif 'age' in session_context and session_context['agecheck'] == "pending":
                user_age = parameters.get('age', None)
                
                if user_age:
                    age_value = user_age.get('amount')  # ดึงค่าอายุออกมา
                    age_unit = user_age.get('unit', 'year')  # ตรวจสอบหน่วย ถ้าไม่มีให้เป็นปี
                    
                    if age_value:  # ตรวจสอบว่ามีค่าของอายุจริง ๆ
                        session_context['age'] = age_value  # เก็บค่าอายุ
                        session_context['agecheck'] = "ok"
                        response_text_th = "😷 ขั้นที่ 3 ช่วยบอกอาการคุณเบื้องต้นหน่อยครับ"
                        session_context['symptomscheck'] = "pending"
                    else:
                        response_text_th = "ช่วยระบุอายุของคุณอีกครั้งครับ"
                else:
                    response_text_th = "ช่วยระบุอายุของคุณอีกครั้งครับ"

            elif 'synonyms' in session_context and session_context['symptomscheck'] == "pending":
                # ตรวจสอบคำตอบเกี่ยวกับอาการ
                user_symptoms_th = parameters.get('synonyms', None)  # อาการที่รับเข้ามาเป็นภาษาไทย
                
                if user_symptoms_th:
                    symptoms_data = load_symptoms()  # โหลดข้อมูล Symptom ID
                    symptom_ids = find_symptom_ids(user_symptoms_th, symptoms_data)  # แปลงอาการเป็น Symptom ID
                    if symptom_ids:
                        session_context['symptoms'] = symptom_ids  # เก็บ Symptom ID
                        session_context['symptomscheck'] = "ok"
                        session_context['confirmcheck'] = "pending"

                        if session_context['sex'] == 'male':    
                            response_text_th = (
                                f"คุณระบุเพศว่าชาย , อายุ {session_context['age']} ปี, "
                                f"และอาการคือ {', '.join(user_symptoms_th)}. "
                                "ช่วยยืนยันข้อมูลว่าถูกต้องให้ผมหน่อยครับ"
                            )
                            print(session_context)

                        else:
                            
                            response_text_th = (
                                f"คุณระบุเพศว่าหญิง , อายุ {session_context['age']} ปี, "
                                f"และอาการคือ {', '.join(user_symptoms_th)}. "
                                "ช่วยยืนยันข้อมูลว่าถูกต้องให้ผมหน่อยครับ"
                            )
                    else:
                        response_text_th = "ขอโืทษนะครับผมไม่พบอาการที่คุณระบุ ช่วยระบุอาการใหม่อีกครั้งครับ"
                else:
                    response_text_th = "ช่วยระบุอาการที่คุณมีอีกครั้งครับ"

            elif 'confirm' in session_context and session_context['confirmcheck'] == "pending":
                # ตรวจสอบการยืนยันข้อมูล
                user_confirm = parameters.get('confirm', None)
                if user_confirm:
                    response_text_th = "ขอบคุณสำหรับข้อมูลของคุณครับ ผมกำลังทำการวินิจฉัย กรุณารอสักครู่...😃"
                    
                    # เรียกฟังก์ชันวินิจฉัย API
                    infermedica_url = "https://api.infermedica.com/v3/diagnosis"
                    headers = {
                        "App-Id": INFERMEDICA_APP_ID,
                        "App-Key": INFERMEDICA_API_KEY,
                        "Model": "infermedica-en",
                        "Content-Type": "application/json"
                    }

                    # สร้าง payload
                    payload = {
                        "sex": session_context['sex'],
                        "age": {"value": session_context['age']},
                        "evidence": session_context['symptoms'],
                        "extras": {
                            "enable_advice": True,  # เปิดใช้งานการรับคำแนะนำ
                            "enable_triage": True  # เปิดใช้งานการวิเคราะห์ระดับความเร่งด่วน
                        }
                    }

                    # ส่งข้อมูลไปยัง Infermedica API
                    response = requests.post(infermedica_url, headers=headers, json=payload)

                    if response.status_code == 200:
                        diagnosis_data = response.json()
                        conditions = diagnosis_data.get('conditions', [])

                        if conditions:
                            # ดึงชื่อโรคที่ได้รับจาก API และแปลเป็นภาษาไทย
                            condition_names = [condition['name'] for condition in conditions if condition['name']]
                            condition_names_th = translate_condition_names(condition_names)
                            condition_names_str = ", ".join(condition_names_th)

                            # สร้างข้อความเริ่มต้น
                            response_text_th += f"\nคุณอาจจะมีปัญหาเกี่ยวกับเรื่อง {condition_names_str}. "

                            # ดึงระดับ triage level และคำแนะนำเพิ่มเติมหากมีข้อมูล
                            for condition in conditions:
                                triage_level = condition.get('seriousness', 'unknown')  # ดึงระดับความเร่งด่วน
                                advice = condition.get('extras', {}).get('advice', None)  # ดึงคำแนะนำจาก extras.advice

                                # แสดงระดับความเร่งด่วน
                                if triage_level == "emergency":
                                    response_text_th += "\nระดับความเร่งด่วน: ฉุกเฉิน กรุณาพบแพทย์ทันที."
                                elif triage_level == "consultation":
                                    response_text_th += "\nระดับความเร่งด่วน: ควรปรึกษาแพทย์."
                                elif triage_level == "self_care":
                                    response_text_th += "\nระดับความเร่งด่วน: ดูแลตัวเองได้."

                                # เพิ่มคำแนะนำเพิ่มเติม
                                if advice:
                                    response_text_th += f"\nคำแนะนำเพิ่มเติม: {advice}"

                            # ต่อท้ายข้อความคำแนะนำทั่วไป
                            response_text_th += "\nเพื่อความมั่นใจอย่าลืมไปตรวจสุขภาพและดูแลตัวเองเยอะๆนะครับ"
                        else:
                            response_text_th = "ไม่พบเงื่อนไขที่ตรงกับอาการของคุณ กรุณาลองอีกครั้ง."
                    else:
                        error_message = response.text
                        print(f"Error: {response.status_code} - {error_message}")
                        response_text_th = "เกิดข้อผิดพลาดในการเชื่อมต่อกับ Infermedica API."

                else:
                    response_text_th = "ช่วยกรอกข้อมูลใหม่ให้ผมอีกครั้งนะครับ"

            else:
                response_text_th = "ช่วยกรอกข้อมูลใหม่ให้ผมอีกครั้งนะครับ"
            return JsonResponse({
                "fulfillmentText": response_text_th,
                "outputContexts": [{
                    "name": f"{data['session']}/contexts/session",
                    "lifespanCount": 10,
                    "parameters": session_context
                }]
            })

        except Exception as e:
            return JsonResponse({"fulfillmentText": f"เกิดข้อผิดพลาด: {str(e)}"})

    def get(self, request, *args, **kwargs):
        return JsonResponse({"status": "POST requests only allowed"}, status=405)
    

