import random
import string
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import *





# otp sender function

def send_otp(request, to_email, length=6):
    """Generate an OTP and send it via email."""
    characters = string.digits
    otp = ''.join(random.choice(characters) for i in range(length))
    save_otp = OtpCode(otpcode = otp, email = to_email )
    save_otp.save()
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp}'
    from_email = settings.EMAIL_HOST_USER

    send_mail(subject, message, from_email, [to_email])

    return otp




@csrf_exempt
@api_view(['POST'])
def send_otp_view(request):
    if request.method == 'POST':
        data = request.data
        email = data.get('email')
        to_email = email
        # to_email = "mohammadosama2021@gmail.com"
        
        if to_email:
            otp = send_otp(to_email)
            return JsonResponse({'status': 'success', 'otp': otp})
        else:
            return JsonResponse({'status': 'fail', 'message': 'Email is required.'})
    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid request method.'})