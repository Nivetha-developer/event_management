from apps.models import *
from apps.serializer import *
from rest_framework.views import APIView
from apps.permission import *
from rest_framework.response import Response
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from apps.json import *
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
from apps.forms import *
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import jwt
from configurations.settings import *
from django.utils.decorators import method_decorator
import json as j
from django.contrib.auth.hashers import make_password



class Register(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self,request,  *args, **kwargs):
        return super(Register, self).dispatch(request, *args, **kwargs)

    def post(self,request,*args, **kwargs):
        datas = j.loads(request.body.decode('utf-8'))

        if 'email' not in datas:
            return APIResponse('Email Address is missing', 400, False)
        else:
            email = datas['email']
        if 'password' not in datas:
            return APIResponse('password is missing', 400, False)
        else:
            password = datas['password']
        username = datas['username']
        phone_number = datas['phone_number']

        User_Profile.objects.create(email=email,password=make_password(password),phone_number=phone_number,username=username,role="Customer")
        return APIResponse("Registration successful, We have sent an otp to your Email address",200, True)


class Login(APIView):
    def post(self,request,**kwargs):
        email = request.data['email']
        password = request.data['password']
        role = request.data['role']
        # login(email,password)
        user = User_Profile.objects.filter(email=email,role=role)
        if not user:
            if role == "Admin":
                return APIResponse("please provide registerd admin email",400,False)
            else:
               return APIResponse("please provide registerd user email",400,False)

        if not user:
            return APIResponse("Please enter correct email",400,False)
        if not user.latest().check_password(password):
            return APIResponse("Please enter correct password",400,False)

        access = AccessToken.for_user(user.latest())
        refresh=RefreshToken.for_user(user.latest())
        result = {
                'access': str(access),
                'refresh': str(refresh),
                'message' : "Logged in successfully"
            }
        return APIResponse(result,200,True)

class EventManagementAPI(APIView):
    permission_classes=[IsOwner]
    serializer_class = EventSerializer 
    
    def post(self, request, *args, **kwargs):
        name = request.data['name']
        total_tickets = request.data['total_tickets']
        description = request.data['description']
        start_date = request.data['start_date']
        end_date = request.data['end_date']
        query_set = Event.objects.filter(name=name,is_active=True)
        if query_set.count()!=0:
            return APIResponse("Event with same name exists", 400, False)
        data = Event.objects.create(name=name,total_tickets=total_tickets,description=description,available_tickets=total_tickets,start_date=start_date,end_date=end_date)
        print(data.id)
        return APIResponse("Event created successfully", 200, True)

    def put(self, request, *args, **kwargs):
        if "id" in request.query_params:
            id=request.query_params.get('id')
        name = request.data['name']
        description = request.data['description']
        total_tickets = request.data['total_tickets']  
        start_date = request.data['start_date']
        end_date = request.data['end_date']
        query_set = Event.objects.filter(name=name,is_active=True).exclude(id=id)
        if query_set.count()!=0:
            return APIResponse("Event with same exists", 400, False)
        query = Event.objects.filter(id=id).update(name=name,description=description,total_tickets=total_tickets,start_date=start_date,end_date=end_date)
        return APIResponse("Event updated successfully", 200, True)

class EventFetch(APIView):
    permission_classes=[IsAppuser]
    serializer_class = EventSerializer 

    def get(self,request):
        query_set = Event.objects.filter(is_active=True)
        if "id" in request.query_params:
            id=request.query_params.get('id')
            query_set = query_set.filter(id=id)
        if "search" in request.query_params:
            search=request.query_params.get('search')
            query_set = query_set.filter(Q(name__icontains=search)|Q(available_tickets__icontains=search)|Q(description__icontains=search))
        if "sort" in request.query_params:
            sort=request.query_params.get('sort')
            if sort == 'ascending':
                query_set = query_set.order_by('created_on')
            if sort == 'decending':
                query_set = query_set.order_by('-created_on')
        result = EventSerializer(query_set,many=True).data
        return APIResponse(result, 200, True)
    
class BookingAPI(APIView):
    permission_classes=[IsAppuser]
    serializer_class = BookingSerializer 

    def get(self,request):
        query_set = BookingMaster.objects.filter(is_deleted=False)
        if request.user.role !="Admin":
            query_set = query_set.filter(user_id=request.user.id)
        if "id" in request.query_params:
            id=request.query_params.get('id')
            query_set = query_set.filter(id=id)
        if "search" in request.query_params:
            search=request.query_params.get('search')
            query_set = query_set.filter(Q(user__email__icontains=search)|Q(event__name__icontains=search))
        if "sort" in request.query_params:
            sort=request.query_params.get('sort')
            if sort == 'ascending':
                query_set = query_set.order_by('created_on')
            if sort == 'decending':
                query_set = query_set.order_by('-created_on')
        
        result = BookingSerializer(query_set,many=True).data
        return APIResponse(result, 200, True)
    
    def post(self, request, *args, **kwargs):
        event = request.data['event']
        tickets = request.data['tickets']
        available_tickets = Event.objects.get(id=event).available_tickets
        if int(available_tickets) < int(tickets):
            return APIResponse(f"{available_tickets} only available",400,False)
        BookingMaster.objects.create(event_id=event,tickets=tickets,user_id=request.user.id)
        Event.objects.filter(id=event).update(available_tickets=int(available_tickets)-int(tickets))
        return APIResponse("Booking successfully", 200, True)
    
    def post(self,request):
        if request.method == 'POST':
            form = TicketBookingForm(request.POST)
            if form.is_valid():
                ticket = form.save(commit=False)
                print(form.data)
                # current_date = date.today()
                # if ticket.booking_start_date <= current_date <= ticket.booking_end_date:
                if form.error:
                    print(form.error)
                else:
                    ticket.save()
                return render(request,'success.html')  # Redirect to a success page
                # else:
                #     return render(request, 'booking_closed.html')
        else:
            form = TicketBookingForm()
        return render(request, 'book_ticket.html', {'form': form})
@csrf_exempt
def ticket_booking(request):  
    import json as j
    if request.method == 'POST':
        token = request.POST.get('token')
        ticket = request.POST.get('ticket')
        event = request.POST.get('event')
        date = request.POST.get('date')
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        total_ticket = Event.objects.get(id=event)
        booked_tickets =  BookingMaster.objects.filter(booking_date=date,event_id=event).aggregate(total_tickets=Sum('tickets'))
        if booked_tickets['total_tickets'] == None:
            booked_tickets['total_tickets'] = 0
        if (int(total_ticket.total_tickets) - int(booked_tickets['total_tickets'])) == 0:
            return APIResponse("No tickets availabel",400,False)
        if (int(total_ticket.total_tickets) - int(booked_tickets['total_tickets'])) < int(ticket):
            return APIResponse(f"{(total_ticket.total_tickets) - booked_tickets['total_tickets']} tickets only available",400,False)
        
        ticket = BookingMaster(event_id=event,tickets=ticket,user_id=decoded_token['user_id'],booking_date=date)
        ticket.save()
        return APIResponse("booked successfully",200,True)  
    else:
        return render(request, 'book_ticket.html')

def success(request):
    return render(request, 'success.html')