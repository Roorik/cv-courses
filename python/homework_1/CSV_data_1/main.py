"""У вас есть CSV-файл `data.csv`, содержащий информацию о продажах товаров."""
import csv
import logging

from pathlib import Path
from tabulate import tabulate
from pydantic import BaseModel, Field, PositiveInt

BASE_DIR = Path(__file__).parent
input_dir = BASE_DIR / 'data.csv'
log_dir = BASE_DIR / 'sales_log.txt'
    
logging.basicConfig(filename=log_dir, level=logging.INFO, filemode='w')
log = logging.getLogger(__name__)

class ProductSale(BaseModel):
    product_name: str = Field(..., alias='Product Name')
    units_sold: PositiveInt = Field(..., alias='Units Sold')
    unit_price: float = Field(..., alias='Unit Price')

def open_file(file: str) -> list:
    """ Чтение файла по заданной директории """
    try:
        with open(input_dir, 'r') as input_file:
            reader = csv.DictReader(input_file)
            sales_data = [ProductSale.model_validate(row) for row in reader]
            log.info(f'Файл успешно прочитан')
            return sales_data
    except Exception as e:
        log.error(f'При чтении файла возникла ошибка: {e}')
        raise e
    
def calculate_profit(data: list) -> int:
    """ Калькуляция общей суммы выручки """
    total_sum = 0
    try:
        for item in data:
            total_sum += item.unit_price
        log.info(f'Итоговая сумма продаж составила: {total_sum}')
        return total_sum
    except Exception as e:
        log.error(f'При калькуляции возникла ошибка: {e}')
        raise e
    

if __name__ == '__main__':
    product_sales = open_file(input_dir)
    sales_sum = calculate_profit(product_sales)
    table_data = [sale.dict() for sale in product_sales]
    print(tabulate(table_data, headers='keys', tablefmt='grid'))
    print(f'Общий доход составил {sales_sum}р.')