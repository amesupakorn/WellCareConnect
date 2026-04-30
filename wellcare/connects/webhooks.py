import json
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .webhook_handlers import handle_check_symptoms, handle_ask_disease

@method_decorator(csrf_exempt, name='dispatch')
class HealthWebhookView(View):
    def post(self, request, *args, **kwargs):
        try:
            response_text_th = "ขอโทษครับ ผมไม่เข้าใจคำขอของคุณ กรุณาลองใหม่อีกครั้งครับ😊"

            data = json.loads(request.body)
            action = data['queryResult']['parameters'].get('action') 
            restart = data['queryResult']['parameters'].get('restart') 
            parameters = data['queryResult']['parameters']
            
            # เก็บสถานะการสนทนา (session)
            output_contexts = data['queryResult'].get('outputContexts', [])
            session_context = {}

            for context in output_contexts:
                if context['name'].endswith('/contexts/session'):
                    session_context = context.get('parameters', {})
                    break

            if isinstance(action, list):
                action = action[0]  
            else:
                action = None  
                
            if restart:
                session_context.clear()
                response_text_th = (
                    "ให้ผมช่วยคุณเรื่องไหนได้บ้างครับ😊\n"
                    "1. เช็คอาการเบื้องต้นครับ\n"
                    "2. สอบถามเบื้องต้นเกี่ยวกับโรคครับ"
                )
                session_context['action'] = 'prompt'
            else:
                if 'action' not in session_context:
                    response_text_th = (
                        "สวัสดีครับ! ยินดีต้อนรับสู่ WellCareChat ผู้ช่วยด้านสุขภาพของคุณ 🤗\n"
                        "ผมสามารถช่วยคุณเรื่องไหนได้บ้างครับ\n"
                        "1. เช็คอาการเบื้องต้นครับ\n"
                        "2. สอบถามเบื้องต้นเกี่ยวกับโรคครับ"
                    )
                    session_context['action'] = 'prompt'
                else:
                    if action in ['เช็คอาการเบื้องต้น', '1', 'อาการเบื้องต้น', 'หนึ่ง', 'อาการ', '1.เช็คอาการเบื้องต้น'] or session_context['action'] == 'check_symptoms':
                        response_text_th = handle_check_symptoms(parameters, session_context, data)
                        session_context['action'] = 'check_symptoms'  
                    elif action in ['สอบถามเบื้องต้นเกี่ยวกับโรค', '2.เช็คอาการโรคเบื้องต้น', 'สอง', '2', 'โรค'] or session_context['action'] == 'ask_disease':
                        response_text_th = handle_ask_disease(parameters, session_context, data)
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

    def get(self, request, *args, **kwargs):
        return JsonResponse({"status": "POST requests only allowed"}, status=405)
