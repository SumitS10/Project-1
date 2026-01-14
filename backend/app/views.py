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
    def get_queryset(self):
        try:
            return FidelityTrade.objects.all()
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error fetching Fidelity trades: {str(e)}")
            return FidelityTrade.objects.none()
    
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
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error importing Webull CSV: {str(e)}", exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TradierTradeListView(ListAPIView):
    def get_queryset(self):
        try:
            return TradierTrade.objects.all()
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error fetching Tradier trades: {str(e)}")
            return TradierTrade.objects.none()
    
    serializer_class = TradierTradeSerializer


class WebullTradeListView(ListAPIView):
    def get_queryset(self):
        try:
            return WebullTrade.objects.all()
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error fetching Webull trades: {str(e)}")
            return WebullTrade.objects.none()
    
    serializer_class = WebullTradeSerializer


class TradeLogListView(ListAPIView):
    queryset = TradeLog.objects.all()
    serializer_class = TradeLogSerializer


class MarketPriceView(APIView):
    """Get current market price for a symbol using Tradier/Webull APIs."""
    def get(self, request):
        symbol = request.query_params.get('symbol', '').upper()
        source = request.query_params.get('source', 'tradier')  # 'tradier' or 'webull'
        
        if not symbol:
            return Response({'error': 'Symbol parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        from .api_clients import get_market_price_from_apis
        
        price = get_market_price_from_apis(symbol, preferred_source=source)
        
        if price:
            return Response({
                'symbol': symbol,
                'price': price,
                'source': source if price else None
            })
        else:
            return Response({
                'symbol': symbol,
                'price': None,
                'error': 'Unable to fetch price from APIs. Check API configuration.'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class CalculateRiskView(APIView):
    """Calculate risk metrics for an options strategy."""
    def post(self, request):
        try:
            strategy = request.data.get('strategy')
            symbol = request.data.get('symbol', '').upper()
            expiry = request.data.get('expiry')
            strikes = request.data.get('strikes', [])
            quantities = request.data.get('quantities', [])
            
            if not all([strategy, symbol, expiry, strikes, quantities]):
                return Response(
                    {'error': 'Missing required fields: strategy, symbol, expiry, strikes, quantities'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if len(strikes) != len(quantities):
                return Response(
                    {'error': 'Strikes and quantities arrays must have same length'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            from .options_calculator import calculate_strategy_risk
            from .api_clients import get_market_price_from_apis
            
            # Get current underlying price
            underlying_price = get_market_price_from_apis(symbol)
            
            # Calculate risk
            risk_analysis = calculate_strategy_risk(
                strategy=strategy,
                symbol=symbol,
                strikes=[float(s) for s in strikes],
                quantities=[int(q) for q in quantities],
                underlying_price=underlying_price
            )
            
            return Response(risk_analysis, status=status.HTTP_200_OK)
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error calculating risk: {str(e)}", exc_info=True)
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PlaceTradeView(APIView):
    """Place an options trade via Webull API."""
    def post(self, request):
        try:
            strategy = request.data.get('strategy')
            symbol = request.data.get('symbol', '').upper()
            expiry = request.data.get('expiry')
            strikes = request.data.get('strikes', [])
            quantities = request.data.get('quantities', [])
            action = request.data.get('action', 'open')
            
            if not all([strategy, symbol, expiry, strikes, quantities]):
                return Response(
                    {'error': 'Missing required fields'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            from .api_clients import (
                get_webull_option_chain,
                place_webull_trade,
                get_market_price_from_apis
            )
            
            # Get options chain to find option IDs
            option_chain = get_webull_option_chain(symbol, expiry)
            
            if not option_chain:
                return Response(
                    {'error': 'Unable to fetch options chain. Check Webull API configuration.'},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            
            # Place trades for each leg
            order_results = []
            for i, (strike, quantity) in enumerate(zip(strikes, quantities)):
                # Find option ID from chain (simplified - adjust based on actual API response)
                # This is a placeholder - actual implementation depends on Webull API structure
                option_id = f"{symbol}_{expiry}_{strike}"  # Placeholder
                
                trade_action = 'BUY' if action == 'open' else 'SELL'
                result = place_webull_trade(
                    symbol=symbol,
                    option_id=option_id,
                    quantity=int(quantity),
                    action=trade_action
                )
                
                if result:
                    order_results.append(result)
                else:
                    return Response(
                        {'error': f'Failed to place trade for leg {i+1}'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            
            return Response({
                'order_id': order_results[0].get('order_id', 'pending'),
                'status': 'submitted',
                'message': f'Successfully placed {len(order_results)} leg(s)',
                'legs': order_results
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error placing trade: {str(e)}", exc_info=True)
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# Serve React app - catch-all for client-side routing
class ReactAppView(View):
    def get(self, request):
        index_path = settings.FRONTEND_BUILD_DIR / 'index.html'
        if index_path.exists():
            return FileResponse(open(index_path, 'rb'), content_type='text/html')
        raise Http404('React build not found. Run: npm run build')
