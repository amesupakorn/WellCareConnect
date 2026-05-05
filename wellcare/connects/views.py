from datetime import datetime
import json
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.contrib import messages
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from .models import Disease, Location, Booking
from .serializers import ReserveSerializer

# --- Public Pages ---

class HomePage(View):
    def get(self, request):
        return render(request, 'index.html')

class CheckPage(View):
    def get(self, request):
        return render(request, 'check.html')

class ShowCheckPage(View):
    def get(self, request):
        return render(request, 'showcheck.html')

class ServiceFirst(View):
    def get(self, request):
        return render(request, 'services/first.html')

class ServiceFirst1(View):
    def get(self, request):
        return render(request, 'services/first-1.html')

class ServiceFirst2(View):
    def get(self, request):
        return render(request, 'services/first-2.html')

class ServiceFirst3(View):
    def get(self, request):
        return render(request, 'services/first-3.html')

class ServiceFirst4(View):
    def get(self, request):
        return render(request, 'services/first-4.html')

class ServiceSecond(View):
    def get(self, request):
        return render(request, 'services/second.html')

class ServiceSecond1(View):
    def get(self, request):
        return render(request, 'services/second-1.html')

class ServiceSecond2(View):
    def get(self, request):
        return render(request, 'services/second-2.html')

class ServiceSecond3(View):
    def get(self, request):
        return render(request, 'services/second-3.html')

class ServiceSecond4(View):
    def get(self, request):
        return render(request, 'services/second-4.html')

class ServiceThird(View):
    def get(self, request):
        return render(request, 'services/third.html')

class ServiceThird1(View):
    def get(self, request):
        return render(request, 'services/third-1.html')

class ServiceThird2(View):
    def get(self, request):
        return render(request, 'services/third-2.html')

class ServiceThird3(View):
    def get(self, request):
        return render(request, 'services/third-3.html')

class ServiceThird4(View):
    def get(self, request):
        return render(request, 'services/third-4.html')

# --- Booking Flow ---

class BookingListPage(View):
    def get(self, request):
        location = Location.objects.all()
        return render(request, 'booking/book-list.html', {'locations': location})

class BookingFirst(View):
    def get(self, request, id):
        location = get_object_or_404(Location, id=id)
        return render(request, 'booking/book-first.html', {'location': location})

class CheckAvailableTimes(View):
    def post(self, request):
        body = json.loads(request.body)
        selected_date = body.get('date')
        facility_id = body.get('facility_id')

        if selected_date and facility_id:
            selected_date = parse_date(selected_date)
            bookings = Booking.objects.filter(date_reserve=selected_date, location_id=facility_id).values('time_reserve')
            # Format time objects to string for JSON serialization
            result = []
            for b in bookings:
                result.append({'time_reserve': b['time_reserve'].strftime('%H:%M:%S')})
            return JsonResponse(result, safe=False)
        return JsonResponse([], safe=False)

class BookingSecond(View):
    def post(self, request, id):
        location = get_object_or_404(Location, id=id)
        date_str = request.POST.get('start_date')
        time_str = request.POST.get('selected_time')

        if date_str and time_str:
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                thai_date = date_obj.replace(year=date_obj.year + 543)
                thai_date_str = thai_date.strftime('%d/%m/%Y')
                
                time_obj = datetime.strptime(time_str, '%H:%M:%S')
                time_start = time_obj.strftime('%H:%M')

                return render(request, "booking/book-second.html", {
                    'location': location,
                    'time_start': time_start,
                    'date': thai_date_str
                })
            except ValueError:
                return redirect('book-first', id=id)
        
        messages.error(request, "กรุณากรอกข้อมูลให้ครบด้วยครับ")
        return redirect('book-first', id=id)

class BookingThird(View):
    def post(self, request, id):
        location = get_object_or_404(Location, id=id)
        date = request.POST.get('date')
        time = request.POST.get('time_start')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        symptoms = request.POST.get('symptoms')
        phone = request.POST.get('phone')

        if all([date, time, firstname, lastname, phone]):
            return render(request, "booking/book-third.html", {
                'location': location,
                'time_start': time,
                'date': date,
                'firstname': firstname,
                'lastname': lastname,
                'symptoms': symptoms,
                'phone': phone
            })
        
        messages.error(request, "กรุณากรอกข้อมูลให้ครบด้วยครับ")
        return render(request, "booking/book-second.html", {
            'location': location,
            'time_start': time,
            'date': date
        })

# --- API & Utils ---

def format_phone_number(phone):
    if phone.startswith('0'):
        return '+66' + phone[1:]
    return phone

def send_sms(to_number, message_body):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        message = client.messages.create(
            body=message_body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_number
        )
        return message.sid
    except TwilioRestException as e:
        print(f"Twilio Error: {e}")
        return None

class ConfirmBooking(APIView):
    permission_classes = [AllowAny]
    def post(self, request, id):
        data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
        data['location'] = id
        serializer = ReserveSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # phone = format_phone_number(request.data.get('phone'))
            # send_sms(phone, "Reservation created...")
            return Response({"success": True}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class MyTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"

class ViewBooking(APIView):
    authentication_classes = [MyTokenAuthentication] 
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        bookings = Booking.objects.filter(location_id__staff_id=request.user)
        if bookings.exists():
            serializer = ReserveSerializer(bookings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'No bookings found.'}, status=status.HTTP_404_NOT_FOUND)

# --- ERP Pages (Staff Only) ---

class ERPPage(LoginRequiredMixin, View):
    login_url = '/admin/login/'
    
    def get(self, request):
        if request.user.is_superuser:
            bookings = Booking.objects.all().order_by('-date_reserve', '-time_reserve')
        else:
            bookings = Booking.objects.filter(location__staff=request.user).order_by('-date_reserve', '-time_reserve')
            
        total_bookings = bookings.count()
        today = datetime.now().date()
        today_bookings = bookings.filter(date_reserve=today).count()
        
        return render(request, 'erp/dashboard.html', {
            'bookings': bookings,
            'total_bookings': total_bookings,
            'today_bookings': today_bookings,
        })

class AddLocationPage(LoginRequiredMixin, View):
    login_url = '/admin/login/'
    
    def get(self, request):
        users = User.objects.all()
        return render(request, 'erp/add_location.html', {'users': users})
        
    def post(self, request):
        try:
            Location.objects.create(
                name=request.POST.get('name'),
                opening=request.POST.get('opening'),
                closing=request.POST.get('closing'),
                status=request.POST.get('status'),
                booking_status=request.POST.get('booking_status', 'available'),
                staff=User.objects.get(id=request.POST.get('staff'))
            )
            return redirect('erp')
        except Exception as e:
            return render(request, 'erp/add_location.html', {'users': User.objects.all(), 'error': str(e)})

class ManageLocationPage(LoginRequiredMixin, View):
    login_url = '/admin/login/'
    def get(self, request):
        locations = Location.objects.all().order_by('name')
        return render(request, 'erp/manage_location.html', {'locations': locations})

class EditLocationPage(LoginRequiredMixin, View):
    login_url = '/admin/login/'
    def get(self, request, id):
        location = get_object_or_404(Location, id=id)
        return render(request, 'erp/edit_location.html', {'location': location, 'users': User.objects.all()})
        
    def post(self, request, id):
        location = get_object_or_404(Location, id=id)
        try:
            location.name = request.POST.get('name')
            location.opening = request.POST.get('opening')
            location.closing = request.POST.get('closing')
            location.status = request.POST.get('status')
            location.booking_status = request.POST.get('booking_status')
            location.staff = User.objects.get(id=request.POST.get('staff'))
            location.save()
            return redirect('manage-location')
        except Exception as e:
            return render(request, 'erp/edit_location.html', {'location': location, 'users': User.objects.all(), 'error': str(e)})

@login_required(login_url='/admin/login/')
def delete_location(request, id):
    location = get_object_or_404(Location, id=id)
    location.delete()
    return redirect('manage-location')
