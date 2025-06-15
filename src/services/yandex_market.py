import aiohttp
from config import YANDEX_MARKET_TOKEN, YANDEX_MARKET_CAMPAIGN_ID, YANDEX_MARKET_API_URL

class YandexMarketService:
    def __init__(self):
        self.token = YANDEX_MARKET_TOKEN
        self.campaign_id = YANDEX_MARKET_CAMPAIGN_ID
        self.api_url = YANDEX_MARKET_API_URL

    async def _make_request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """Выполнение запроса к API Яндекс.Маркет"""
        headers = {
            'Authorization': f'OAuth {self.token}',
            'Content-Type': 'application/json'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=f"{self.api_url}{endpoint}",
                headers=headers,
                json=data
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"API Error: {error_text}")

    async def get_hidden_offers_with_stocks(self) -> list:
        """Получение скрытых товаров с остатками"""
        try:
            # Получаем все товары
            offers = await self._make_request(
                'GET',
                f'/campaigns/{self.campaign_id}/offers'
            )
            
            # Фильтруем скрытые товары с остатками
            hidden_offers = []
            for offer in offers.get('offers', []):
                if offer.get('status') == 'HIDDEN' and offer.get('stock', 0) > 0:
                    hidden_offers.append({
                        'id': offer.get('id'),
                        'name': offer.get('name'),
                        'stock': offer.get('stock')
                    })
            
            return hidden_offers
        except Exception as e:
            print(f"Error getting hidden offers: {str(e)}")
            return []

    async def update_offer_stock(self, offer_id: str, stock: int) -> bool:
        """Обновление остатков товара"""
        try:
            data = {
                'offers': [{
                    'id': offer_id,
                    'stock': stock
                }]
            }
            
            response = await self._make_request(
                'PUT',
                f'/campaigns/{self.campaign_id}/offers/stocks',
                data
            )
            
            return response.get('success', False)
        except Exception as e:
            print(f"Error updating offer stock: {str(e)}")
            return False

    async def get_offer_info(self, offer_id: str) -> dict:
        """Получение информации о товаре"""
        try:
            response = await self._make_request(
                'GET',
                f'/campaigns/{self.campaign_id}/offers/{offer_id}'
            )
            
            return response.get('offer', {})
        except Exception as e:
            print(f"Error getting offer info: {str(e)}")
            return {} 