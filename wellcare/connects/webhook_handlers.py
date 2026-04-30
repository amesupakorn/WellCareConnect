import os
import json
import requests
from googletrans import Translator
from .models import Disease

INFERMEDICA_API_KEY = os.environ.get('INFERMEDICA_API_KEY')
INFERMEDICA_APP_ID = os.environ.get('INFERMEDICA_APP_ID')

# ฟังก์ชันเพื่อโหลดข้อมูล Symptom ID จากไฟล์ JSON
def load_symptoms(file_path='symptoms.json'):
    # Find the symptoms.json relative to the project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    full_path = os.path.join(project_root, file_path)
    
    if not os.path.exists(full_path):
        # Try local path if not found
        full_path = file_path
        
    with open(full_path, 'r', encoding='utf-8') as file:
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
            try:
                translated = translator.translate(condition, src='en', dest='th').text
                translated_conditions.append(translated)
            except:
                translated_conditions.append(condition)
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

def find_disease(user_disease_list):
    if isinstance(user_disease_list, list) and len(user_disease_list) > 0:
        user_disease = user_disease_list[0]
        matching_diseases = Disease.objects.filter(disease_name__icontains=user_disease)
        if matching_diseases.exists():
            return matching_diseases.first()
    return None

def handle_check_symptoms(parameters, session_context, data):
    if 'sex' not in session_context:
        response_text_th = f"สวัสดีครับ! ผมจะช่วยเช็คอาการเบื้องต้นให้นะครับ 🤗 \n 👋 ขั้นที่ 1 ช่วยบอกเพศกับผมหน่อยครับ (ชาย หรือ หญิง)"
        session_context['sexcheck'] = "pending"

    elif 'sex' in session_context and session_context['sexcheck'] == 'pending':
        user_sex_th = parameters.get('sex', None)
        if user_sex_th:
            user_sex = map_sex_th_to_en(user_sex_th)
            if user_sex:
                session_context['sex'] = user_sex
                session_context['sexcheck'] = "ok"
                response_text_th = "✨ ขั้นที่ 2 ช่วยบอกอายุของคุณหน่อยครับ"
                session_context['agecheck'] = "pending"
            else:
                response_text_th = "ช่วยบอกเพศของคุณอีกครั้งครับ (ชาย หรือ หญิง)"
        else:
            response_text_th = "ช่วยบอกเพศของคุณอีกครั้งครับ (ชาย หรือ หญิง)"

    elif 'age' in session_context and session_context['agecheck'] == "pending":
        user_age = parameters.get('age', None)
        if user_age:
            age_value = user_age.get('amount')
            if age_value:
                session_context['age'] = age_value
                session_context['agecheck'] = "ok"
                response_text_th = "😷 ขั้นที่ 3 ช่วยบอกอาการคุณเบื้องต้นหน่อยครับ"
                session_context['symptomscheck'] = "pending"
            else:
                response_text_th = "ช่วยระบุอายุของคุณอีกครั้งครับ"
        else:
            response_text_th = "ช่วยระบุอายุของคุณอีกครั้งครับ"

    elif 'synonyms' in session_context and session_context['symptomscheck'] == "pending":
        user_symptoms_th = parameters.get('synonyms', None)
        if user_symptoms_th:
            symptoms_data = load_symptoms()
            symptom_ids = find_symptom_ids(user_symptoms_th, symptoms_data)
            if symptom_ids:
                session_context['symptoms'] = symptom_ids
                session_context['symptomscheck'] = "ok"
                session_context['confirmcheck'] = "pending"

                sex_th = "ชาย" if session_context['sex'] == 'male' else "หญิง"
                response_text_th = (
                    f"คุณระบุเพศว่า{sex_th} , อายุ {session_context['age']} ปี, "
                    f"และอาการคือ {', '.join(user_symptoms_th)}. "
                    "ช่วยยืนยันข้อมูลว่าถูกต้องให้ผมหน่อยครับ"
                )
            else:
                response_text_th = "ขอโทษนะครับผมไม่พบอาการที่คุณระบุ ช่วยระบุอาการใหม่อีกครั้งครับ"
        else:
            response_text_th = "ช่วยระบุอาการที่คุณมีอีกครั้งครับ"

    elif 'confirm' in session_context and session_context['confirmcheck'] == "pending":
        user_confirm = parameters.get('confirm', None)
        if user_confirm:                    
            infermedica_url = "https://api.infermedica.com/v3/diagnosis"
            headers = {
                "App-Id": INFERMEDICA_APP_ID,
                "App-Key": INFERMEDICA_API_KEY,
                "Model": "infermedica-en",
                "Content-Type": "application/json"
            }

            payload = {
                "sex": session_context['sex'],
                "age": {"value": session_context['age']},
                "evidence": session_context['symptoms'],
                "extras": {
                    "enable_advice": True,
                    "enable_triage": True
                }
            }

            response = requests.post(infermedica_url, headers=headers, json=payload)

            if response.status_code == 200:
                diagnosis_data = response.json()
                conditions = diagnosis_data.get('conditions', [])

                if conditions:
                    condition_names = [condition['name'] for condition in conditions if condition['name']]
                    condition_names_th = translate_condition_names(condition_names)
                    condition_names_str = ", ".join(condition_names_th)
                    response_text_th = f"\nคุณอาจจะมีปัญหาเกี่ยวกับเรื่อง {condition_names_str}. "

                    for condition in conditions:
                        triage_level = condition.get('seriousness', 'unknown')
                        advice = condition.get('extras', {}).get('advice', None)

                        if triage_level == "emergency":
                            response_text_th += "\nระดับความเร่งด่วน: ฉุกเฉิน กรุณาพบแพทย์ทันที."
                        elif triage_level == "consultation":
                            response_text_th += "\nระดับความเร่งด่วน: ควรปรึกษาแพทย์."
                        elif triage_level == "self_care":
                            response_text_th += "\nระดับความเร่งด่วน: ดูแลตัวเองได้."

                        if advice:
                            response_text_th += f"\nคำแนะนำเพิ่มเติม: {advice}"

                    response_text_th += "\nตรวจสอบอาการเสร็จสิ้นครับ😁! เพื่อความมั่นใจอย่าลืมไปตรวจสุขภาพและดูแลตัวเองเยอะๆนะครับ"
                    session_context['action'] = 'restart'
                    response_text_th += "\n\nหากต้องการให้ผมช่วยอีกโปรดพิมพ์คำว่า 'เริ่มใหม่' 😊"
                else:
                    response_text_th = "ไม่พบเงื่อนไขที่ตรงกับอาการของคุณ กรุณาลองอีกครั้ง."
            else:
                response_text_th = "เกิดข้อผิดพลาดในการเชื่อมต่อกับ Infermedica API."
        else:
            response_text_th = "ช่วยกรอกข้อมูลใหม่ให้ผมอีกครั้งนะครับ"
    else:
        response_text_th = "ช่วยกรอกข้อมูลใหม่ให้ผมอีกครั้งนะครับ"

    return response_text_th 

def handle_ask_disease(parameters, session_context, data):
    if 'disease' not in session_context:
        response_text_th = "ช่วยระบุชื่อของโรคที่ คุณต้องการรายละเอียดได้เลยครับ😁"
        session_context['diseasecheck'] = 'pending'
    
    elif 'disease' in session_context and session_context['diseasecheck'] == 'pending':
        user_disease = parameters.get('disease', None)
        if user_disease:
            matching_diseases = find_disease(user_disease)
            if matching_diseases:
                response_text_th = f"💡โรคที่คุณค้นหาคือ: {matching_diseases.disease_name} \n"
                response_text_th += f"💫รายละเอียดของโรค: {matching_diseases.description} \n"
                response_text_th += f"🤾อาการของโรคเบื้องต้น: {matching_diseases.symptoms} \n"
                response_text_th += f"💊การรักษาเบื้องต้น: {matching_diseases.treatment}"

                session_context['action'] = 'restart'
                response_text_th += "\n\nหากต้องการให้ผมช่วยอีกโปรดพิมพ์คำว่า 'เริ่มใหม่' 😊"
            else:
                response_text_th = "ขอโทษครับ ผมไม่พบโรคที่ตรงกับที่คุณระบุ"
    else:
        response_text_th = "ช่วยระบุุโรคที่คุณอยากทราบอีกครั้งนะครับ"
        
    return response_text_th
