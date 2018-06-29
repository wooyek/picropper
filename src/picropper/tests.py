# # coding=utf-8
#
# import logging
#
# import faker
# from django import test
# from django.shortcuts import resolve_url
#
# from website.misc.testing import UserTestCase
# from . import factories, models
#
# log = logging.getLogger(__name__)
# fake = faker.Faker()
#
#
# class ImageDetailTests(UserTestCase):
#     def test_anonymous(self):
#         item = factories.ImageModelFactory()
#         url = resolve_url("picropper:ImageDetail", item.pk)
#         response = test.Client().get(url)
#         self.assertEqual(302, response.status_code)
#
#     def test_forbidden(self):
#         item = factories.ImageModelFactory()
#         url = resolve_url('picropper:ImageDetail', item.pk)
#         response = self.client.get(url)
#         self.assertEqual(403, response.status_code)
#
#     def test_get(self):
#         item = factories.ImageModelFactory(user=self.user)
#         url = resolve_url('picropper:ImageDetail', item.pk)
#         response = self.client.get(url)
#         self.assertEqual(200, response.status_code)
#
#
# class ImageCreateTests(UserTestCase):
#     def test_anonymous(self):
#         url = resolve_url('picropper:ImageCreate')
#         response = test.Client().get(url)
#         self.assertEqual(302, response.status_code)
#
#     def test_get(self):
#         url = resolve_url('picropper:ImageCreate')
#         response = self.client.get(url)
#         self.assertEqual(200, response.status_code)
#
#     def test_post(self):
#         url = resolve_url('picropper:ImageCreate')
#         response = self.client.post(url, data={
#             'user': self.user.pk
#         })
#         item = models.ImageModel.objects.first()
#         self.assertRedirects(response, resolve_url('picropper:ImageDetail', item.pk), fetch_redirect_response=False)
