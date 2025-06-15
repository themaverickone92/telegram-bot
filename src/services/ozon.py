import aiohttp
import pandas as pd
from config import OZON_API_KEY, OZON_CLIENT_ID, OZON_API_URL, OZON_INFO_URL

class OzonService:
    def __init__(self):
        self.api_key = OZON_API_KEY
        self.client_id = OZON_CLIENT_ID
        self.api_url = OZON_API_URL
        self.info_url = OZON_INFO_URL

    async def _make_request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """Выполнение запроса к API Ozon"""
        headers = {
            'Client-Id': self.client_id,
            'Api-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=endpoint,
                headers=headers,
                json=data
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"API Error: {error_text}")

    async def set_cargo(self, supply_id: str, cargo_id: str) -> bool:
        """Установка грузоместа для поставки"""
        try:
            data = {
                'supply_id': supply_id,
                'cargo_id': cargo_id
            }
            response = await self._make_request('POST', f"{self.api_url}/cargoes/set", data)
            return response.get('success', False)
        except Exception as e:
            print(f"Error setting cargo: {str(e)}")
            return False

    async def update_fbs_stocks(self, df: pd.DataFrame) -> bool:
        """Обновление остатков FBS"""
        try:
            # Преобразуем DataFrame в формат API
            stocks = []
            for _, row in df.iterrows():
                stocks.append({
                    'product_id': str(row['product_id']),
                    'stock': int(row['stock'])
                })
            
            data = {
                'stocks': stocks
            }
            
            response = await self._make_request('POST', f"{self.api_url}/stocks/update", data)
            return response.get('success', False)
        except Exception as e:
            print(f"Error updating FBS stocks: {str(e)}")
            return False

    async def get_fbs_stocks(self) -> pd.DataFrame:
        """Получение текущих остатков FBS"""
        try:
            response = await self._make_request('GET', f"{self.api_url}/stocks")
            stocks = response.get('stocks', [])
            
            # Преобразуем в DataFrame
            df = pd.DataFrame(stocks)
            return df
        except Exception as e:
            print(f"Error getting FBS stocks: {str(e)}")
            return pd.DataFrame()

    async def delete_fbs_stocks(self, product_ids: list) -> bool:
        """Удаление остатков FBS"""
        try:
            data = {
                'product_ids': product_ids
            }
            response = await self._make_request('POST', f"{self.api_url}/stocks/delete", data)
            return response.get('success', False)
        except Exception as e:
            print(f"Error deleting FBS stocks: {str(e)}")
            return False 