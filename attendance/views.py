import io
import base64
import qrcode
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.contrib import messages
from .models import Session, Attendance


@login_required
def home_view(request):
    if request.user.is_staff:
        return redirect('date_list')
    return render(request, 'attendance/home_student.html')


@staff_member_required(login_url='/login/')
def qr_generator_view(request):
    qr_image_b64 = None
    session = None

    if request.method == 'POST':
        today = timezone.localdate()
        session = Session.objects.create(date=today)

        attend_url = request.build_absolute_uri(f'/attend/{session.token}/')
        img = qrcode.make(attend_url)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        qr_image_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    return render(request, 'attendance/qr_generator.html', {
        'qr_image_b64': qr_image_b64,
        'session': session,
    })


@login_required
def attend_view(request, token):
    session = get_object_or_404(Session, token=token)

    if not session.is_valid():
        return render(request, 'attendance/error.html', {
            'message': 'This QR code has expired. Please ask your admin to generate a new one.',
        })

    if Attendance.objects.filter(user=request.user, session=session).exists():
        return render(request, 'attendance/error.html', {
            'message': 'You have already registered your attendance for this session.',
        })

    return redirect('confirm', token=token)


@login_required
def confirm_view(request, token):
    session = get_object_or_404(Session, token=token)

    if not session.is_valid():
        return render(request, 'attendance/error.html', {
            'message': 'This QR code has expired. Please ask your admin to generate a new one.',
        })

    if request.method == 'POST':
        _, created = Attendance.objects.get_or_create(user=request.user, session=session)
        if created:
            return redirect('thank_you')
        return render(request, 'attendance/error.html', {
            'message': 'You have already registered your attendance for this session.',
        })

    return render(request, 'attendance/confirm.html', {
        'session': session,
        'user': request.user,
    })


@login_required
def thank_you_view(request):
    return render(request, 'attendance/thank_you.html')


@staff_member_required(login_url='/login/')
def date_list_view(request):
    date_filter = request.GET.get('date')
    sessions = Session.objects.all()
    if date_filter:
        sessions = sessions.filter(date=date_filter)

    return render(request, 'attendance/date_list.html', {
        'sessions': sessions,
        'date_filter': date_filter,
    })


def student_list_view(request, external_token):
    session = get_object_or_404(Session, external_token=external_token)
    attendances = Attendance.objects.filter(session=session).select_related('user')

    return render(request, 'attendance/student_list.html', {
        'session': session,
        'attendances': attendances,
    })
