from unittest import TestCase
from utils.pagination import make_pagination_range

class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_apgination_range(self):
        # [1] 2 3 4 5 6 7 8 9 10
        # 1 [2] 3 4 5 6 7 8 9 10
        # 2 3 4 5 6 [7] 8 9 10 11
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qtd_pages=4,
            current_page=1,
        )
        self.assertEqual([1,2,3,4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):
        pass
