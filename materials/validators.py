from rest_framework.validators import ValidationError


url = 'https://www.youtube.com'


def validates_url(value):
    if not value.startswith(url):
        raise ValidationError(f'URL - запрещен, допускаются только видео с {url}')
