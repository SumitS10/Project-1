import os
from django.conf import settings
from django.http import FileResponse, Http404
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView

from .utils import import_fidelity, import_tradier, import_webull
from .models import FidelityTrade, TradierTrade, WebullTrade, TradeLog
from .serializers import (
    FidelityTradeSerializer, 
    TradierTradeSerializer, 
    WebullTradeSerializer,
    TradeLogSerializer
)


class UploadFidelityView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        path = os.path.join(settings.MEDIA_ROOT, file.name)

        with open(path, 'wb+') as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        try:
            import_fidelity(path)
            return Response({'status': 'Fidelity imported successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UploadTradierView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        path = os.path.join(settings.MEDIA_ROOT, file.name)

        with open(path, 'wb+') as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        try:
            import_tradier(path)
            return Response({'status': 'Tradier imported successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FidelityTradeListView(ListAPIView):
    queryset = FidelityTrade.objects.all()
    serializer_class = FidelityTradeSerializer


class UploadWebullView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        path = os.path.join(settings.MEDIA_ROOT, file.name)

        with open(path, 'wb+') as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        try:
            import_webull(path)
            return Response({'status': 'Webull imported successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TradierTradeListView(ListAPIView):
    queryset = TradierTrade.objects.all()
    serializer_class = TradierTradeSerializer


class WebullTradeListView(ListAPIView):
    queryset = WebullTrade.objects.all()
    serializer_class = WebullTradeSerializer


class TradeLogListView(ListAPIView):
    queryset = TradeLog.objects.all()
    serializer_class = TradeLogSerializer


# Serve React app - catch-all for client-side routing
class ReactAppView(View):
    def get(self, request):
        index_path = settings.FRONTEND_BUILD_DIR / 'index.html'
        if index_path.exists():
            return FileResponse(open(index_path, 'rb'), content_type='text/html')
        raise Http404('React build not found. Run: npm run build')
