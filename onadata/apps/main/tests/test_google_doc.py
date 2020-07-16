# coding: utf-8
import os

from django.test import TestCase

from onadata.apps.main.google_doc import GoogleDoc


class TestGoogleDoc(TestCase):

    def test_view(self):
        doc = GoogleDoc()
        folder = os.path.join(
            os.path.dirname(__file__), "fixtures", "google_doc"
            )
        input_path = os.path.join(folder, "input.html")
        with open(input_path, 'rb') as f:
            input_html = f.read().decode()
        doc.set_html(input_html)
        self.assertEqual(doc._html, input_html)
        self.assertEqual(len(doc._sections), 14)
        output_path = os.path.join(folder, "navigation.html")
        with open(output_path, 'rb') as f:
            self.assertEqual(doc._navigation_html(), f.read().decode())
