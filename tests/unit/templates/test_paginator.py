import unittest
import pybald
from pybald import context
from pybald.core.django.paginator import Paginator, PageNotAnInteger, EmptyPage


class TestPaginator(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        context._reset()

    def test_page_1(self):
        query = ["item"] * 400
        p = Paginator(query, 40)
        # 10 pages
        self.assertEqual(p.num_pages, 10)
        page = p.page(1)
        self.assertEqual(page.number, 1)
        self.assertFalse(page.has_previous())
        self.assertTrue(page.has_next())
        self.assertEqual(page.next_page_number(), 2)

    def test_page_5(self):
        query = ["item"] * 400
        p = Paginator(query, 40)
        # 10 pages
        self.assertEqual(p.num_pages, 10)
        page = p.page(5)
        self.assertEqual(page.number, 5)
        self.assertTrue(page.has_previous())
        self.assertTrue(page.has_next())
        self.assertEqual(page.previous_page_number(), 4)
        self.assertEqual(page.next_page_number(), 6)

    def test_page_10(self):
        query = ["item"] * 400
        p = Paginator(query, 40)
        # 10 pages
        self.assertEqual(p.num_pages, 10)
        page = p.page(10)
        self.assertEqual(page.number, 10)
        self.assertTrue(page.has_previous())
        self.assertFalse(page.has_next())
        self.assertEqual(page.previous_page_number(), 9)

    def test_only_one_page(self):
        query = ["item"] * 30
        p = Paginator(query, 40)
        # 10 pages
        self.assertEqual(p.num_pages, 1)
        page = p.page(1)
        self.assertFalse(page.has_other_pages())
        self.assertEqual(page.number, 1)
        self.assertFalse(page.has_previous())
        self.assertFalse(page.has_next())

    def test_bad_page(self):
        query = ["item"] * 30
        p = Paginator(query, 40)
        with self.assertRaises(PageNotAnInteger) as ctxt:
            # 10 pages
            self.assertEqual(p.num_pages, 1)
            page = p.page("A")
            # self.assertFalse(page.has_other_pages())
            # self.assertEqual(page.number, 1)
            # self.assertFalse(page.has_previous())
            # self.assertFalse(page.has_next())

    def test_negative_page(self):
        query = ["item"] * 30
        p = Paginator(query, 40)
        with self.assertRaises(EmptyPage) as ctxt:
            self.assertEqual(p.num_pages, 1)
            page = p.page(-10)

    def test_non_page(self):
        query = ["item"] * 30
        p = Paginator(query, 40)
        with self.assertRaises(EmptyPage) as ctxt:
            self.assertEqual(p.num_pages, 1)
            page = p.page(3)

    def test_page_start(self):
        query = ["item"] * 400
        p = Paginator(query, 40)
        # 10 pages
        self.assertEqual(p.num_pages, 10)
        page = p.page(10)
        self.assertEqual(page.start_index(), 361)

    def test_page_end(self):
        query = ["item"] * 400
        p = Paginator(query, 40)
        # 10 pages
        self.assertEqual(p.num_pages, 10)
        page = p.page(8)
        self.assertEqual(page.end_index(), 320)

    def test_page_end_orphans(self):
        query = ["item"] * 385
        p = Paginator(query, 40)
        # 10 pages
        self.assertEqual(p.num_pages, 10)
        page = p.page(10)
        self.assertEqual(page.end_index(), 385)

    def test_page_start_no_items(self):
        query = []
        p = Paginator(query, 40)
        # 10 pages
        self.assertEqual(p.num_pages, 1)
        page = p.page(1)
        self.assertEqual(page.start_index(), 0)