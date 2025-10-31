from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pylogalert as log
from pylogalert.notify import Notifier
import json
import os

def fake_channel(payload):
    print('>>> ALERT', payload)

notifier = Notifier(
    channels = [fake_channel],
    rate_limit=("2/min", 5),
    dedupe_window=30,
)

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = data.get("username")
        password = data.get("password")

        log.set_context(user=user, ip=request.META.get("REMOTE_ADDR"))
        if user == "admin" and password == "123":
            log.info("login_success", status="ok")
            return JsonResponse({"message":"Login"})
        else:
            log.warning("log_failed", reason="invalid_credentials")
            return JsonResponse({"error": "Login inválido"}, status=401)

@csrf_exempt
def post_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = data.get("user")
        text = data.get("text")

        log.set_context(user=user)
        log.info("post_created", content=text)
        return JsonResponse({"message": "Post publicado"})

@csrf_exempt
def admin_view(request):
    log.set_context(ip=request.META.get("REMOTE_ADDR"))
    log.emergency("unaunthorized_admin_access", endpoint="/admin/", _notify=notifier)
    return JsonResponse({"error": "Acesso negado"}, status=403)

@csrf_exempt
def ping(request):
    log.debug("ping_received")
    return JsonResponse({"message": "pong"})

@api_view(['GET'])
def get_logs(request):
    log_file_path = os.path.join(os.path.dirname(__file__), "../logs/activity.log")
    try:
        with open(log_file_path, "r") as f:
            lines = f.readlines()

        logs = []
        last_ts = None

        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                logs.append(obj)
                if 'ts' in obj:
                    last_ts = obj['ts']
            except json.JSONDecodeError:
                continue
        return Response({
            "logs": logs,
            "last_timestamp": last_ts
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)