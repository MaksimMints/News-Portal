from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Подсказка вашей команды'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no ')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
            return
        try:
            postCategory = Category.objects.get(name=options['category'])
            Post.objects.filter(postCategory=postCategory).delete()
            self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all news from category {postCategory.name}')) # в случае неправильного подтверждения говорим, что в доступе отказано
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category '))