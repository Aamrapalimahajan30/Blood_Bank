import threading
import time
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings

notification_log = []
_log_lock = threading.Lock()


def _send_single_notification(donor, request_info):
    
    message = (
        f"Dear {donor.get('name')}, your blood group {donor.get('blood_group')} "
        f"is urgently needed at {request_info.get('hospital')} "
        f"({request_info.get('location')}). Please respond if available."
    )

    sent_ok = True
    error = None
    try:
        send_mail(
            subject=f"Urgent: Blood needed ({donor.get('blood_group')}) — {request_info.get('hospital')}",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[donor.get('email')],
            fail_silently=False,
        )
    except Exception as e:
        sent_ok = False
        error = str(e)

    with _log_lock:
        notification_log.append({
            'donor': donor.get('name'),
            'contact': donor.get('phone'),
            'email': donor.get('email'),
            'message': message,
            'sent_at': datetime.utcnow().isoformat(),
            'sent_ok': sent_ok,
            'error': error,
        })
    return message


def notify_matched_donors(donor_list, request_info):
    
    threads = []
    start_index = len(notification_log)

    for donor in donor_list:
        t = threading.Thread(target=_send_single_notification, args=(donor, request_info))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return notification_log[start_index:]