from django.core.management import BaseCommand, CommandError
from datetime import datetime

class Command(BaseCommand):
    help = 'ユーザー情報を表示するバッチです'
    
    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='名前')
        parser.add_argument('age', type=int, help='年齢')
        parser.add_argument('--birthday', type=self.valid_date, default='2010/1/1')
        parser.add_argument('--three_words', nargs=3)
        parser.add_argument('--active', action='store_true')
        parser.add_argument('--color', choices=['Blue', 'Red', 'Yellow'])
        
    def valid_date(self, value):
        try:
            return datetime.strptime(value, '%Y/%m/%d')
        except ValueError:
            raise CommandError(f'誤ったフォーマットです。yyyy/mm/ddで入力してください')
    
    def handle(self, *args, **options):
        name = options['name']
        age = options['age']
        birthday = options['birthday']
        three_words = options['three_words']
        active = options['active']
        print(f'name = {name}, age = {age}, birthday = {birthday}, active = {active}')
        print(type(name),type(age),type(birthday),type(active))
        print(f'three_words: {three_words}')
        print(type(three_words))

        color = options['color']
        print(color, type(color))