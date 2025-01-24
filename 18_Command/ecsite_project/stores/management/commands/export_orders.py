from django.core.management import BaseCommand
from stores.models import Order
from django.conf import settings
from datetime import datetime
import os
import csv


class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('--user_id', default='all')
    
    def handle(self, *args, **options):
        query = Order.objects
        user_id = options['user_id']
        if user_id == 'all':
            query = query.all()
        else:
            query = query.filter(user_id=user_id)
        file_path = os.path.join(
            settings.BASE_DIR, 'output', 'orders',
            f'order_{datetime.now().strftime('%Y%m%d%H%M%S')}_{user_id}'
        )
        with open(file_path, mode='w', newline='\n', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'user', 'address', 'total_price']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for order in query:
                writer.writerow({
                    'id': order.pk,
                    'user': order.user,
                    'address': order.address,
                    'total_price': order.total_price,
                })