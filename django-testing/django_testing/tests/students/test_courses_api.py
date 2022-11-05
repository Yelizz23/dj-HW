import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


# проверка получения 1-го курса (retrieve-логика)
@pytest.mark.django_db
def test_get_course(client, course_factory):
    courses = course_factory(_quantity=1)
    response = client.get(f'/api/v1/courses/{courses[0].id}/')
    data = response.json()
    assert response.status_code == 200
    assert data['name'] == courses[0].name


# проверка получения списка курсов (list-логика)
@pytest.mark.django_db
def test_get_courses_list(client, course_factory):
    courses = course_factory(_quantity=13)
    response = client.get(f'/api/v1/courses/')
    data = response.json()
    assert response.status_code == 200
    assert len(data) == len(courses)


# проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_filter_by_id(client, course_factory):
    courses = course_factory(_quantity=13)
    response = client.get(f'/api/v1/courses/?id={courses[0].id}')
    data = response.json()
    assert response.status_code == 200
    assert data[0]['id'] == courses[0].id


# проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_filter_by_name(client, course_factory):
    courses = course_factory(_quantity=13)
    response = client.get(f'/api/v1/courses/?name={courses[0].name}')
    data = response.json()
    assert response.status_code == 200
    assert data[0]['name'] == courses[0].name


# тест успешного создания курса
@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    response = client.post('/api/v1/courses/', data={'name': 'Python'})
    data = response.json()
    assert response.status_code == 201
    assert data['name'] == 'Python'
    assert Course.objects.count() == count + 1


# тест успешного обновления курса
@pytest.mark.django_db
def test_update_course(client, course_factory):
    courses = course_factory(_quantity=13)
    count = Course.objects.count()
    response = client.patch(f'/api/v1/courses/{courses[0].id}/', data={'name': 'Python-2'})
    data = response.json()
    assert response.status_code == 200
    assert data['name'] == 'Python-2'
    assert Course.objects.count() == count


# тест успешного удаления курса
@pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=13)
    count = Course.objects.count()
    response = client.delete(f'/api/v1/courses/{courses[0].id}/')
    assert response.status_code == 204
    assert Course.objects.count() == count - 1
