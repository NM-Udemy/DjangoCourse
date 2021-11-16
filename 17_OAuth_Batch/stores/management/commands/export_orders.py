from django.core.management.base import BaseCommand
from stores.models import Orders
from ecsite_project.settings import BASE_DIR
from datetime import datetime
import os
import csv

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--user_id', default='all')

    def handle(self, *args, **options):
        orders = Orders.objects
        user_id = options['user_id']
        if user_id == 'all':
            orders = orders.all()
        else:
            orders = orders.filter(user_id=user_id)
        file_path = os.path.join(BASE_DIR, 'output', 'orders', f'orders_{datetime.now().strftime("%Y%m%d%H%M%S")}_{user_id}')
        with open(file_path, mode='w', newline='\n', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'user', 'address', 'total_price']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for order in orders:
                writer.writerow({
                    'id': order.id,
                    'user': order.user,
                    'address': order.address,
                    'total_price': order.total_price,
                })
