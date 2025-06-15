import pandas as pd
from io import BytesIO
import aiohttp
from config import WAREHOUSES

class ThreePLService:
    def __init__(self):
        self.warehouses = WAREHOUSES

    async def fetch_warehouse_stock(self, warehouse: str) -> list:
        """Получение остатков со склада"""
        try:
            # Здесь должна быть реальная логика получения данных со склада
            # Для примера возвращаем тестовые данные
            return [
                {
                    'Склад': warehouse,
                    'Код товара': f'PROD_{i}',
                    'Количество': i * 10
                }
                for i in range(1, 6)
            ]
        except Exception as e:
            print(f"Error fetching warehouse stock: {str(e)}")
            return []

    async def export_stocks(self) -> BytesIO:
        """Экспорт остатков со всех складов"""
        try:
            all_rows = []
            
            # Получаем данные со всех складов
            for warehouse in self.warehouses:
                rows = await self.fetch_warehouse_stock(warehouse)
                all_rows.extend(rows)
            
            if not all_rows:
                return None
            
            # Создаем DataFrame и группируем данные
            df = pd.DataFrame(all_rows)
            grouped = df.groupby(['Склад', 'Код товара'], as_index=False).agg({'Количество': 'sum'})
            
            # Создаем Excel файл
            output = BytesIO()
            grouped.to_excel(output, index=False)
            output.seek(0)
            
            return output
        except Exception as e:
            print(f"Error exporting stocks: {str(e)}")
            return None

    async def get_warehouse_info(self, warehouse: str) -> dict:
        """Получение информации о складе"""
        try:
            # Здесь должна быть реальная логика получения информации о складе
            return {
                'name': warehouse,
                'address': f'Address for {warehouse}',
                'capacity': 1000,
                'current_load': 500
            }
        except Exception as e:
            print(f"Error getting warehouse info: {str(e)}")
            return {} 