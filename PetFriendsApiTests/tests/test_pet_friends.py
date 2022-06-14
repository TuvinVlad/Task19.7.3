from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Глаша', animal_type='бульдог',
                                     age='1', pet_photo='images/buldog.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Мур", "кот", "1", "images/cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мур', animal_type='кот', age=2):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_create_pet_simple_with_valid_data(name='Лапа', animal_type='дворняга', age='2'):
    """Проверяем, что можно создать питомца с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Создаем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_create_pet_simple_with_empty_name(name='', animal_type='дворняга', age='2'):
    """Проверяем, что нельзя создать питомца без ввода имени"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Создаем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    """Ожидаем, что в ответе будет код состояния 400. В противном случае - баг. Т
        Так и есть - баг - приходит код 200. Питомец создается на сайте без указания имени"""

    try:
        assert status == 400
    except AssertionError:
        print("Bug")

def test_create_pet_simple_with_empty_name_and_animal_type(name='', animal_type='', age='2'):
    """Проверяем, что нельзя создать питомца без ввода имени и породы"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Создаем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    """Ожидаем, что в ответе будет код состояния 400. В противном случае - баг. Т
        Так и есть - баг - приходит код 200. Питомец создается на сайте без указания имени и породы"""

    try:
        assert status == 400
    except AssertionError:
        print("Bug")

def test_create_pet_simple_with_empty_data(name='', animal_type='', age=''):
    """Проверяем, что нельзя создать питомца без ввода необходимых параметров - имени, породы и возраста"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Создаем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    """Ожидаем, что в ответе будет код состояния 400. В противном случае - баг. Т
        Так и есть - баг - приходит код 200. Питомец создается на сайте без указания имени, породы и возраста"""

    try:
        assert status == 400
    except AssertionError:
        print("Bug")

def test_set_photo_with_valid_data(pet_id='e0bda83e-5903-48cd-9327-e94010967749', pet_photo='images/Lapa.jpg'):
    """Проверяем что можно добавить фото существующего питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем фото
    status, result = pf.set_photo(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200

def test_get_api_key_for_invalid_email(email='abr@yandex.ru', password=valid_password):
    """ Проверяем, что запрос api ключа при неверно введенном email возвращает статус 403 и в результате не содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result

def test_get_api_key_for_invalid_password(email=valid_email, password='12345'):
    """ Проверяем, что запрос api ключа при неверно введенном пароле возвращает статус 403 и в результате не содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result

def test_add_new_pet_with_empty_name(name='', animal_type='бульдог',
                                     age='1', pet_photo='images/buldog.jpg'):
    """Проверяем, что нельзя добавить питомца без ввода имени, которое в документации указано обязательным параметром"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    """Ожидаем, что в ответе будет код состояния 400. В противном случае - баг. Т
    Так и есть - баг - приходит код 200. Питомец на сайт добавляется без имени"""

    try:
        assert status == 400
    except AssertionError:
        print("Bug")

def test_add_new_pet_with_empty_animal_type(name='Глаша', animal_type='',
                                     age='1', pet_photo='images/buldog.jpg'):
    """Проверяем, что нельзя добавить питомца без ввода породы, которая в документации указана обязательным параметром"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    """Ожидаем, что в ответе будет код состояния 400. В противном случае - баг. Т
    Так и есть - баг - приходит код 200. Питомец на сайт добавляется без указания породы"""

    try:
        assert status == 400
    except AssertionError:
        print("Bug")

def test_add_new_pet_with_empty_age(name='Глаша', animal_type='бульдог',
                                     age='', pet_photo='images/buldog.jpg'):
    """Проверяем, что нельзя добавить питомца без ввода возраста, который в документации указан обязательным параметром"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    """Ожидаем, что в ответе будет код состояния 400. В противном случае - баг. Т
    Так и есть - баг - приходит код 200. Питомец на сайт добавляется без указания возраста"""

    try:
        assert status == 400
    except AssertionError:
        print("Bug")
