# coding=utf-8
import factory
import faker

from website.misc.factories import UserFactory
from . import models

fake = faker.Faker()


class ImageModelFactory(factory.DjangoModelFactory):
    name = factory.Faker('name')
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = models.Image
