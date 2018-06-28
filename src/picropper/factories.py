# coding=utf-8
import factory
import faker

from . import models
from website.misc.factories import UserFactory

fake = faker.Faker()


class SampleModelFactory(factory.DjangoModelFactory):
    name = factory.Faker('name')
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = models.SampleModel
