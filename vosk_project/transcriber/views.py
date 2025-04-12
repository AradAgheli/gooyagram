from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
from django.conf import settings
from .goh import transcribe_audio
import ffmpeg

def convert_to_wav(input_path, output_path):
    ffmpeg.input(input_path).output(output_path, ac=1, ar=16000).run(overwrite_output=True)

from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
@csrf_exempt


@csrf_exempt
def record_view(request):
    if request.method == 'POST' and request.FILES.get('audio_data'):
        # ✅ مرحله ۱: ساخت پوشه media اگر وجود نداشت
        media_dir = settings.MEDIA_ROOT
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)

        # ✅ مرحله ۲: ذخیره فایل raw
        raw_path = os.path.join(media_dir, 'raw.webm')
        with open(raw_path, 'wb+') as destination:
            for chunk in request.FILES['audio_data'].chunks():
                destination.write(chunk)

        # ✅ مرحله ۳: تبدیل به WAV
        wav_path = os.path.join(media_dir, 'voice.wav')
        try:
            convert_to_wav(raw_path, wav_path)
            transcript = transcribe_audio(wav_path)
        except Exception as e:
            transcript = f"خطا: {str(e)}"
        finally:
            # ✅ مرحله ۴: حذف فایل‌ها بعد از پردازش
            if os.path.exists(raw_path):
                os.remove(raw_path)
            if os.path.exists(wav_path):
                os.remove(wav_path)

        return JsonResponse({'text': transcript})

    return render(request, 'record.html')
