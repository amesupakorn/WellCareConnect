from datetime import datetime, timedelta
from django.shortcuts import redirect, render
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
    
from .serializers import ReserveSerializer
from .models import *
from django.utils.dateparse import parse_date
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from twilio.rest import Client
from django.conf import settings
from twilio.base.exceptions import TwilioRestException

    
class BookingListPage(View):
    def get(self, request):
        location = Location.objects.all()
        return render(request, 'booking/book-list.html',{
            'locations': location
        })
    
class BookingFirst(View):
    def get(self, request, id):
        location = Location.objects.get(id=id)
        return render(request, 'booking/book-first.html',{
            'location' : location
        })

class CheckAvailableTimes(View):

    def post(self, request):
        # โหลดข้อมูลจาก body ของ request ในรูปแบบ JSON
        body = json.loads(request.body)
        selected_date = body.get('date')
        facility_id = body.get('facility_id')


        if selected_date and facility_id:
            # แปลงวันที่จาก string เป็น date object
            selected_date = parse_date(selected_date)
            
            # Query ข้อมูลเวลาที่ถูกจองแล้ว โดยใช้ checkin_date และ facility_id
            bookings = Booking.objects.filter(date_reserve=selected_date, location_id=facility_id).values('time_reserve')
            times = list(bookings)
            print(times)
            
            return JsonResponse(times, safe=False)
        
        return JsonResponse([], safe=False)
    
class BookingSecond(View):  
    def post(self, request, id):
        facilities = Location.objects.get(id=id)
        date = request.POST.get('start_date')
        time = request.POST.get('selected_time')

        if date and time:
            try:
                # แปลงวันที่และเวลา
                date = datetime.strptime(date, '%Y-%m-%d').date()

                # Convert to Thai Buddhist calendar by adding 543 years
                thai_year = date.year + 543
                thai_date = date.replace(year=thai_year)

                # Output the date in the desired format (e.g., 'วัน/เดือน/ปี')
                thai_date_str = thai_date.strftime('%d/%m/%Y')
                
                time = datetime.strptime(time, '%H:%M:%S')
                time_start = time.strftime('%H:%M')


                # ถ้าทำการจองสำเร็จ, แสดงผลในหน้า booking success
                return render(request, "booking/book-second.html", {
                    'location': facilities,
                    'time_start': time_start,
                    'date': thai_date_str
                })
            except ValueError:
                return redirect('book-first', id=id)
            
        messages.error(request, "กรุณากรอกข้อมูลให้ครบด้วยครับ")
        return redirect('book-first', id=id)

    
class BookingThird(View):

    def post(self, request, id):
        facilities = Location.objects.get(id=id)
        
        date = request.POST.get('date')
        time = request.POST.get('time_start')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        symptoms = request.POST.get('symptoms')
        phone = request.POST.get('phone')
        if date and time and firstname and lastname and symptoms and phone:
            try:
                    # ถ้าทำการจองสำเร็จ, แสดงผลในหน้า booking success
                    return render(request, "booking/book-third.html", {
                        'location': facilities,
                        'time_start': time,
                        'date': date,
                        'firstname' : firstname,
                        'lastname' : lastname,
                        'symptoms': symptoms,
                        'phone' : phone
                    })
                    
            except Exception as e:
                return print({"error": str(e)})
        
        else:
            messages.error(request, "กรุณากรอกข้อมูลให้ครบด้วยครับ")
            return render(request, "booking/book-second.html", {
                    'location': facilities,
                    'time_start': time,
                    'date': date
                })
def format_phone_number(phone):
    if phone.startswith('0'):
        phone = '+66' + phone[1:]  # แปลงเบอร์ 0 นำหน้าเป็น +66
    return phone

# ฟังก์ชันสำหรับส่ง SMS
def send_sms(to_number, message_body):
    # ดึงค่า Twilio credentials จาก settings
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    from_number = settings.TWILIO_PHONE_NUMBER

    # สร้าง Client object สำหรับติดต่อ API
    client = Client(account_sid, auth_token)

    try:
        # ส่งข้อความ
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )
        return message.sid
    except TwilioRestException as e:
        print(f"Twilio Error: {e}")
        
from rest_framework.permissions import AllowAny

class ConfirmBooking(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        
        serializer = ReserveSerializer(data=request.data)
        phone = request.data.get('phone')
        phone = format_phone_number(phone)
        print(phone)
        
        location = request.data.get('location')
        booker = request.data.get('booker')
        date = request.data.get('date_reserve')
        time = request.data.get('time_reserve')
        message = f"Wellcare สวัสดีครับขอบคุณที่ทำการจองกับเราเข้ามา \n นี่คือข้อมูลการจองของคุณครับ : \n สถานที่จอง: {location} \n ชื่อที่จอง: {booker} \n วันที่จอง: {date} \n เวลาที่จอง: {time}"
           
        if serializer.is_valid():
            serializer.save()

            # sms_sid = send_sms(phone, message)
            return Response({"success": True, "message": "Reservation created but SMS failed to send"}, status=status.HTTP_201_CREATED)
        
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class MyTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"
class ViewBooking(APIView):
    authentication_classes = [MyTokenAuthentication] 
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            
            bookings = Booking.objects.filter(location_id__staff_id = request.user)
            
            if bookings.exists():
                serializer = ReserveSerializer(bookings, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'No bookings found for this user.'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'detail': 'An error occurred: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
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
            response_text_th = "ขอโทษครับ ผมไม่เข้าใจคำขอของคุณ กรุณาลองใหม่อีกครั้งครับ😊"

            data = json.loads(request.body)
            action = data['queryResult']['parameters'].get('action') 
            restart = data['queryResult']['parameters'].get('restart') 
            parameters = data['queryResult']['parameters']
            print(data)

            # เก็บสถานะการสนทนา (session)
            
            output_contexts = data['queryResult'].get('outputContexts', [])
            session_context = {}

            # ตรวจสอบและเก็บ context จาก outputContexts (เพื่อหลีกเลี่ยงการทับค่า)
            for context in output_contexts:
                if context['name'].endswith('/contexts/session'):
                    session_context = context.get('parameters', {})
                    break

            if isinstance(action, list):
                action = action[0]  
            else:
                action = None  
                

            if  restart:
                session_context.clear()
                response_text_th = (
                    
                    "ให้ผมช่วยคุณเรื่องไหนได้บ้างครับ😊\n"
                    "1. เช็คอาการเบื้องต้นครับ\n"
                    "2. สอบถามเบื้องต้นเกี่ยวกับโรคครับ"
                )
                session_context['action'] = 'prompt'

            else:
                # Continue with normal conversation flow
                if 'action' not in session_context:
                    response_text_th = (
                        "สวัสดีครับ! ยินดีต้อนรับสู่ WellCareChat ผู้ช่วยด้านสุขภาพของคุณ 🤗\n"
                        "ผมสามารถช่วยคุณเรื่องไหนได้บ้างครับ\n"
                        "1. เช็คอาการเบื้องต้นครับ\n"
                        "2. สอบถามเบื้องต้นเกี่ยวกับโรคครับ"
                    )
                    session_context['action'] = 'prompt'

                else:
                    # Handle other conversation actions based on current session state
                    if action in ['เช็คอาการเบื้องต้น', '1', 'อาการเบื้องต้น', 'หนึ่ง', 'อาการ', '1.เช็คอาการเบื้องต้น'] or session_context['action'] == 'check_symptoms':
                        response_text_th = self.handle_check_symptoms(parameters, session_context, data)
                        session_context['action'] = 'check_symptoms'  

                    elif action in ['สอบถามเบื้องต้นเกี่ยวกับโรค', '2.เช็คอาการโรคเบื้องต้น', 'สอง', '2', 'โรค'] or session_context['action'] == 'ask_disease':
                        response_text_th = self.handle_ask_disease(parameters, session_context, data)
                        session_context['action'] = 'ask_disease'  

                    else:
                        response_text_th = "ขอโทษครับ ช่วยบอกสิ่งที่คุณต้องการให้ผมช่วยอีกรอบครับ😀"
                
            return JsonResponse({
                
                "fulfillmentText": response_text_th,
                "outputContexts": [{
                        "name": f"{data['session']}/contexts/session",
                        "lifespanCount": 1,
                        "parameters": session_context
                    }]
                })

        except Exception as e:
            return JsonResponse({"fulfillmentText": f"เกิดข้อผิดพลาด: {str(e)}"})
        
    def handle_check_symptoms(self, parameters, session_context, data):
            # ตรวจสอบสถานะของการสนทนา
            
            if 'sex' not in session_context:
                
                response_text_th = f"สวัสดีครับ! ผมจะช่วยเช็คอาการเบื้องต้นให้นะครับ 🤗 \n 👋 ขั้นที่ 1 ช่วยบอกเพศกับผมหน่อยครับ (ชาย หรือ หญิง)"

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
                        response_text_th = "ขอโทษนะครับผมไม่พบอาการที่คุณระบุ ช่วยระบุอาการใหม่อีกครั้งครับ"
                else:
                    response_text_th = "ช่วยระบุอาการที่คุณมีอีกครั้งครับ"

            elif 'confirm' in session_context and session_context['confirmcheck'] == "pending":
                # ตรวจสอบการยืนยันข้อมูล
                user_confirm = parameters.get('confirm', None)
                if user_confirm:                    
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
                            response_text_th = f"\nคุณอาจจะมีปัญหาเกี่ยวกับเรื่อง {condition_names_str}. "

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
                            response_text_th += "\nตรวจสอบอาการเสร็จสิ้นครับ😁! เพื่อความมั่นใจอย่าลืมไปตรวจสุขภาพและดูแลตัวเองเยอะๆนะครับ"
                            session_context['action'] = 'restart'
                            response_text_th += "\n\nหากต้องการให้ผมช่วยอีกโปรดพิมพ์คำว่า 'เริ่มใหม่' 😊"

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

            return response_text_th 


    def handle_ask_disease(self, parameters, session_context, data):
        # Logic สำหรับการสอบถามเกี่ยวกับโรคจากฐานข้อมูล SQL
        if 'disease' not in session_context:
            response_text_th = "ช่วยระบุชื่อของโรคที่ คุณต้องการรายละเอียดได้เลยครับ😁"
            session_context['diseasecheck'] = 'pending'
        
        elif 'disease' in session_context and session_context['diseasecheck'] == 'pending':
            user_disease = parameters.get('disease', None)
            if user_disease:
                # ค้นหาโรคที่เกี่ยวข้องในฐานข้อมูล SQL
                matching_diseases = self.find_disease(user_disease)
                
                if matching_diseases:
                    response_text_th = f"📌โรคที่คุณค้นหาคือ: {matching_diseases.disease_name} \n"
                    response_text_th += f"📝รายละเอียดของโรค: {matching_diseases.description} \n"
                    response_text_th += f"😷อาการของโรคเบื้องต้น: {matching_diseases.symptoms} \n"
                    response_text_th += f"💊การรักษาเบื้องต้น: {matching_diseases.treatment}"

                    session_context['action'] = 'restart'
                    response_text_th += "\n\nหากต้องการให้ผมช่วยอีกโปรดพิมพ์คำว่า 'เริ่มใหม่' 😊"
                else:
                    response_text_th = "ขอโทษครับ ผมไม่พบโรคที่ตรงกับที่คุณระบุ"
        else:
            response_text_th = "ช่วยระบุุโรคที่คุณอยากทราบอีกครั้งนะครับ"
            
        return response_text_th
    
    
    def find_disease(self, user_disease_list):
        from .models import Disease

        # แทนที่จะใช้ get() ให้ใช้ filter() เพื่อค้นหา
        if isinstance(user_disease_list, list) and len(user_disease_list) > 0:
            user_disease = user_disease_list[0]
            matching_diseases = Disease.objects.filter(disease_name__icontains=user_disease)

        # ตรวจสอบว่ามีโรคที่ค้นพบหรือไม่
            if matching_diseases.exists():
                # ถ้าพบโรคที่ตรงกัน ให้ใช้ค่าจากโรคแรกที่เจอ
                matching_disease = matching_diseases.first()
            else:
                matching_disease = None
        else:
            matching_disease = None
        
        return matching_disease

    def get(self, request, *args, **kwargs):
        return JsonResponse({"status": "POST requests only allowed"}, status=405)
    

