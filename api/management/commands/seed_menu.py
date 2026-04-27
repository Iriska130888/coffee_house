# Coffee House — Command to Seed Menu Data

from django.core.management.base import BaseCommand
from api.models import Category, MenuItem

# Initial data for seeding the menu
SEED_DATA = {
    'espresso': {
        'name': 'Еспресо', 'order': 1,
        'items': [
            dict(name='Еспресо', tag='Класика', price=65,
                 description='Інтенсивний, насичений, з шоколадними нотами. Подвійний шот.',
                 image_url='https://images.unsplash.com/photo-1610889556528-9a770e32642f?w=600&q=80&auto=format'),
            dict(name='Капучіно', tag='Популярне', price=85,
                 description='Еспресо з ніжною молочною пінкою. Ідеальний баланс кави та молока.',
                 image_url='https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=600&q=80&auto=format'),
            dict(name='Латте', tag='Хіт', price=90,
                 description="М'яка кава з великою кількістю парного молока та красивим латте-артом.",
                 image_url='https://images.unsplash.com/photo-1541167760496-1628856ab772?w=600&q=80&auto=format'),
            dict(name='Флет Уайт', tag='Авторський', price=95,
                 description='Концентрований еспресо з мікропінкою. Улюблений напій баристи.',
                 image_url='https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&q=80&auto=format'),
            dict(name='Американо', tag='Класика', price=70,
                 description="Еспресо розбавлений гарячою водою. Великий об'єм, чистий смак.",
                 image_url='https://images.unsplash.com/photo-1521302200778-33500795e128?w=600&q=80&auto=format'),
            dict(name='Кортадо', tag='Іспанський', price=80,
                 description='Еспресо з рівною кількістю теплого молока. Іспанська кавова класика.',
                 image_url='https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=600&q=80&auto=format'),
        ],
    },
    'filter': {
        'name': 'Фільтр', 'order': 2,
        'items': [
            dict(name='V60 Pourover', tag='Ручна заварка', price=110,
                 description='Повільна заварка через V60 фільтр. Чистий, яскравий, квітковий смак.',
                 image_url='https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=600&q=80&auto=format'),
            dict(name='Аеропрес', tag='Насичений', price=100,
                 description='Концентрований та гладкий. Унікальний метод заварки під тиском.',
                 image_url='https://images.unsplash.com/photo-1511537190424-bbbab87ac5eb?w=600&q=80&auto=format'),
            dict(name='Кемекс', tag='Преміум', price=120,
                 description='Заварка у скляному кемексі. Чистий, збалансований, без гіркоти.',
                 image_url='https://images.unsplash.com/photo-1442512595331-e89e73853f31?w=600&q=80&auto=format'),
        ],
    },
    'cold': {
        'name': 'Холодне', 'order': 3,
        'items': [
            dict(name='Cold Brew', tag='Холодний', price=105,
                 description="12-годинна холодна екстракція. М'який, без кислотності, освіжає.",
                 image_url='https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=600&q=80&auto=format'),
            dict(name='Айс Латте', tag='Освіжаючий', price=95,
                 description='Еспресо на льоду з холодним молоком. Ідеальний для спекотного дня.',
                 image_url='https://images.unsplash.com/photo-1559496417-e7f25cb247f3?w=600&q=80&auto=format'),
            dict(name='Нітро Кава', tag='Унікальний', price=130,
                 description='Cold Brew насичений азотом. Кремова текстура без молока.',
                 image_url='https://images.unsplash.com/photo-1509785307050-d4066910ec1e?w=600&q=80&auto=format'),
        ],
    },
    'food': {
        'name': 'Їжа', 'order': 4,
        'items': [
            dict(name='Авокадо Тост', tag='Сніданок', price=160,
                 description='Хрустке бріош, крем-авокадо, яйце пашот, мікрозелень, насіння.',
                 image_url='https://images.unsplash.com/photo-1541519227354-08fa5d50c820?w=600&q=80&auto=format'),
            dict(name='Круасан', tag='Випічка', price=75,
                 description="Свіжий масловий круасан з мигдальним кремом або jam.",
                 image_url='https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=600&q=80&auto=format'),
            dict(name='Яйця Бенедикт', tag='Сніданок', price=185,
                 description='Яйця пашот на английських маффінах з голландським соусом та лососем.',
                 image_url='https://images.unsplash.com/photo-1608039829572-78524f79c4c7?w=600&q=80&auto=format'),
            dict(name='Боул з Гранолою', tag='Здорове', price=145,
                 description='Домашня гранола, грецький йогурт, сезонні фрукти та мед.',
                 image_url='https://images.unsplash.com/photo-1511690656952-34342bb7c2f2?w=600&q=80&auto=format'),
        ],
    },
    'dessert': {
        'name': 'Десерти', 'order': 5,
        'items': [
            dict(name='Тірамісу', tag='Десерт', price=145,
                 description='Класичний тірамісу з маскарпоне та еспресо. Наш фірмовий рецепт.',
                 image_url='https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=600&q=80&auto=format'),
            dict(name='Чізкейк', tag='Десерт', price=135,
                 description='Ніжний нью-йоркський чізкейк з сезонними ягодами.',
                 image_url='https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=600&q=80&auto=format'),
            dict(name='Brownie', tag='Шоколадне', price=115,
                 description='Вологий шоколадний брауні з горіхами та карамельним соусом.',
                 image_url='https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=600&q=80&auto=format'),
            dict(name='Панакота', tag='Ніжне', price=125,
                 description='Ванільна панакота з ягідним кулі. Тане у роті.',
                 image_url='https://images.unsplash.com/photo-1488477181946-6428a0291777?w=600&q=80&auto=format'),
        ],
    },
}

class Command(BaseCommand):
    help = 'Seed the database with initial menu data'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing data before seeding')

    def handle(self, *args, **options):
        if options['clear']:
            MenuItem.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING('Existing menu data cleared.'))

        created_cats = 0
        created_items = 0

        for slug, data in SEED_DATA.items():
            category, category_created = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': data['name'], 'order': data['order']},
            )
            if category_created:
                created_cats += 1

            for item_data in data['items']:
                menu_item, item_created = MenuItem.objects.get_or_create(
                    category=category,
                    name=item_data['name'],
                    defaults=item_data,
                )
                if item_created:
                    created_items += 1

        self.stdout.write(self.style.SUCCESS(
            f'✅ Done! Categories: {created_cats}, Menu items: {created_items}'
        ))