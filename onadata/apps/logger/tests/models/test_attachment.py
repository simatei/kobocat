# coding: utf-8
from __future__ import unicode_literals, print_function, division, absolute_import
import os
from datetime import datetime

from django.conf import settings
from django.core.files.base import File
from django.core.files.storage import default_storage
from django.core.management import call_command

from onadata.apps.main.tests.test_base import TestBase
from onadata.apps.logger.models import Attachment, Instance
from onadata.libs.utils.image_tools import image_url


class TestAttachment(TestBase):

    def setUp(self):
        super(self.__class__, self).setUp()
        self._publish_transportation_form_and_submit_instance()
        self.media_file = "1335783522563.jpg"
        media_file = os.path.join(
            self.this_directory, 'fixtures',
            'transportation', 'instances', self.surveys[0], self.media_file)
        self.instance = Instance.objects.all()[0]
        self.attachment = Attachment.objects.create(
            instance=self.instance,
            media_file=File(open(media_file, 'rb'), media_file))

    def test_mimetype(self):
        self.assertEqual(self.attachment.mimetype, 'image/jpeg')

    def test_thumbnails(self):
        for attachment in Attachment.objects.filter(instance=self.instance):
            url = image_url(attachment, 'small')
            filename = attachment.media_file.name.replace('.jpg', '')
            thumbnail = '%s-small.jpg' % filename
            self.assertNotEqual(
                url.find(thumbnail), -1)
            for size in ['small', 'medium', 'large']:
                thumbnail = f'{filename}-{size}.jpg'
                self.assertTrue(
                    default_storage.exists(thumbnail))
                default_storage.delete(thumbnail)

    def test_create_thumbnails_command(self):
        call_command("create_image_thumbnails")
        created_times = {}
        for attachment in Attachment.objects.filter(instance=self.instance):
            filename = attachment.media_file.name.replace('.jpg', '')
            for size in settings.THUMB_CONF.keys():
                thumbnail = '%s-%s.jpg' % (filename, size)
                self.assertTrue(
                    default_storage.exists(thumbnail))
                created_times[size] = default_storage.get_modified_time(thumbnail)
        # replace or regenerate thumbnails if they exist
        call_command("create_image_thumbnails", force=True)
        for attachment in Attachment.objects.filter(instance=self.instance):
            filename = attachment.media_file.name.replace('.jpg', '')
            for size in settings.THUMB_CONF.keys():
                thumbnail = f'{filename}-{size}.jpg'
                self.assertTrue(
                    default_storage.exists(thumbnail))
                self.assertTrue(
                    default_storage.get_modified_time(thumbnail) > created_times[size])
                default_storage.delete(thumbnail)
