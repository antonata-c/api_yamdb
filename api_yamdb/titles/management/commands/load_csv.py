import csv
import os

from django.core.management import BaseCommand
from django.conf import settings

from reviews.models import Review, Comment
from titles.models import Genre, Category, GenreTitle, Title
from users.models import User

FILENAMES_TO_MODELS = {
    'category': Category,
    'genre': Genre,
    'titles': Title,
    'genre_title': GenreTitle,
    'users': User,
    'review': Review,
    'comments': Comment,
}

FOREIGN_FIELDS = {
    'category': ('category', Category),
    'title_id': ('title', Title),
    'author': ('author', User),
    'review_id': ('review', Review),
    'genre_id': ('genre', Genre),
}


def fix_data(csv_data):
    csv_data_copy = csv_data.copy()
    for key, value in csv_data.items():
        if key in FOREIGN_FIELDS:
            csv_new_key = FOREIGN_FIELDS[key][0]
            csv_data_copy[csv_new_key] = FOREIGN_FIELDS[key][1].objects.get(
                pk=value
            )
    return csv_data_copy


class Command(BaseCommand):
    """Класс команды для загрузки в базу данных."""

    def handle(self, *args, **kwargs):
        for filename, model_name in FILENAMES_TO_MODELS.items():
            csv_path = os.path.join(settings.CSV_DIRS, filename + '.csv')
            if not os.path.exists(csv_path):
                print(f'Файл по пути {csv_path} не найден')
                return
            with open(csv_path, encoding='utf-8') as file:
                all_data = list(csv.reader(file))
            headers = all_data[0]
            data = all_data[1:]
            for row in data:
                data_to_save = dict(zip(headers, row))
                data_to_save = fix_data(data_to_save)
                try:
                    final_data = model_name(**data_to_save)
                    final_data.save()
                except ValueError as error:
                    print(f'Ошибка: {error}\nЗапись не была загружена.')
                    return
        print('Все данные были успешно загружены')
