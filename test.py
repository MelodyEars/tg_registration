
from faker import Faker

fake = Faker('uk_UA')  # Вказуємо локаль 'uk_UA' для українських імен та прізвищ

for _ in range(10):  # Генеруємо 10 імен та прізвищ
    print(f"{last_name} {first_name}")
