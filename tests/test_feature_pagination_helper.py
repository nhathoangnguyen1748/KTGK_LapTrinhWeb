"""
Comprehensive test suite for PaginationHelper and associated data structures.
"""
import unittest
import urllib.parse
from helpers.pagination_helper import (
    PageResult,
    PaginationHelper,
    PaginationMetadata,
)


class DummyEntity:
    """Mock model class supporting to_dict serialization."""
    def __init__(self, entity_id: int, name: str):
        self.entity_id = entity_id
        self.name = name

    def to_dict(self):
        return {"id": self.entity_id, "name": self.name}


class TestPaginationHelperSanitization(unittest.TestCase):
    """Tests for page and page size sanitization."""

    def test_sanitize_page_valid_integers(self):
        self.assertEqual(PaginationHelper.sanitize_page(1), 1)
        self.assertEqual(PaginationHelper.sanitize_page(5), 5)
        self.assertEqual(PaginationHelper.sanitize_page("5"), 5)
        self.assertEqual(PaginationHelper.sanitize_page(" 12 "), 12)

    def test_sanitize_page_edge_cases(self):
        self.assertEqual(PaginationHelper.sanitize_page(0), 1)
        self.assertEqual(PaginationHelper.sanitize_page(-10), 1)
        self.assertEqual(PaginationHelper.sanitize_page(None), 1)
        self.assertEqual(PaginationHelper.sanitize_page("invalid"), 1)
        self.assertEqual(PaginationHelper.sanitize_page(""), 1)
        self.assertEqual(PaginationHelper.sanitize_page(False), 1)
        self.assertEqual(PaginationHelper.sanitize_page(True), 1)
        self.assertEqual(PaginationHelper.sanitize_page(-5, default=3), 3)

    def test_sanitize_page_float_values(self):
        self.assertEqual(PaginationHelper.sanitize_page(5.9), 5)
        self.assertEqual(PaginationHelper.sanitize_page("7.2"), 7)
        self.assertEqual(PaginationHelper.sanitize_page(-2.5), 1)
        self.assertEqual(PaginationHelper.sanitize_page(0.0), 1)

    def test_sanitize_page_size_valid(self):
        self.assertEqual(PaginationHelper.sanitize_page_size(10), 10)
        self.assertEqual(PaginationHelper.sanitize_page_size("25"), 25)
        self.assertEqual(PaginationHelper.sanitize_page_size(50), 50)

    def test_sanitize_page_size_edge_cases(self):
        self.assertEqual(PaginationHelper.sanitize_page_size(0), 1)
        self.assertEqual(PaginationHelper.sanitize_page_size(-10), 1)
        self.assertEqual(PaginationHelper.sanitize_page_size(None), 10)
        self.assertEqual(PaginationHelper.sanitize_page_size("invalid"), 10)
        self.assertEqual(PaginationHelper.sanitize_page_size(False), 10)
        self.assertEqual(PaginationHelper.sanitize_page_size(True), 10)

    def test_sanitize_page_size_upper_clamp(self):
        self.assertEqual(PaginationHelper.sanitize_page_size(150), 100)
        self.assertEqual(PaginationHelper.sanitize_page_size(200, max_size=50), 50)
        self.assertEqual(PaginationHelper.sanitize_page_size(100), 100)


class TestPaginationHelperMetadata(unittest.TestCase):
    """Tests for metadata calculations."""

    def test_metadata_empty_dataset(self):
        meta = PaginationHelper.get_metadata(total_items=0, page=1, page_size=10)
        self.assertEqual(meta.total_items, 0)
        self.assertEqual(meta.total_pages, 1)
        self.assertEqual(meta.current_page, 1)
        self.assertEqual(meta.page_size, 10)
        self.assertEqual(meta.offset, 0)
        self.assertEqual(meta.limit, 10)
        self.assertFalse(meta.has_previous)
        self.assertFalse(meta.has_next)
        self.assertIsNone(meta.previous_page)
        self.assertIsNone(meta.next_page)

    def test_metadata_exact_multiple(self):
        meta = PaginationHelper.get_metadata(total_items=30, page=2, page_size=10)
        self.assertEqual(meta.total_pages, 3)
        self.assertEqual(meta.current_page, 2)
        self.assertEqual(meta.offset, 10)
        self.assertTrue(meta.has_previous)
        self.assertTrue(meta.has_next)
        self.assertEqual(meta.previous_page, 1)
        self.assertEqual(meta.next_page, 3)

    def test_metadata_partial_multiple(self):
        meta = PaginationHelper.get_metadata(total_items=35, page=1, page_size=10)
        self.assertEqual(meta.total_pages, 4)
        self.assertEqual(meta.total_items, 35)

    def test_metadata_boundary_flags(self):
        # First page
        meta_first = PaginationHelper.get_metadata(total_items=40, page=1, page_size=10)
        self.assertFalse(meta_first.has_previous)
        self.assertIsNone(meta_first.previous_page)
        self.assertTrue(meta_first.has_next)
        self.assertEqual(meta_first.next_page, 2)

        # Last page
        meta_last = PaginationHelper.get_metadata(total_items=40, page=4, page_size=10)
        self.assertTrue(meta_last.has_previous)
        self.assertEqual(meta_last.previous_page, 3)
        self.assertFalse(meta_last.has_next)
        self.assertIsNone(meta_last.next_page)

        # Beyond last page
        meta_beyond = PaginationHelper.get_metadata(total_items=40, page=8, page_size=10)
        self.assertTrue(meta_beyond.has_previous)
        self.assertEqual(meta_beyond.previous_page, 7)
        self.assertFalse(meta_beyond.has_next)
        self.assertIsNone(meta_beyond.next_page)


class TestPaginationHelperSlicing(unittest.TestCase):
    """Tests for dataset slicing and paginate method."""

    def test_paginate_standard_list(self):
        dataset = list(range(25))
        result = PaginationHelper.paginate(dataset, page=2, page_size=10)
        self.assertIsInstance(result, PageResult)
        self.assertEqual(result.items, [10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
        self.assertEqual(result.metadata.current_page, 2)
        self.assertEqual(result.metadata.total_items, 25)
        self.assertEqual(result.metadata.total_pages, 3)

    def test_paginate_page_exceeding_total_pages(self):
        dataset = ["a", "b", "c"]
        result = PaginationHelper.paginate(dataset, page=5, page_size=10)
        self.assertEqual(result.items, [])
        self.assertEqual(result.metadata.current_page, 5)
        self.assertEqual(result.metadata.total_pages, 1)
        self.assertFalse(result.metadata.has_next)

    def test_paginate_tuple_and_objects(self):
        dataset = (
            DummyEntity(1, "Alice"),
            DummyEntity(2, "Bob"),
            DummyEntity(3, "Charlie"),
        )
        result = PaginationHelper.paginate(dataset, page=1, page_size=2)
        self.assertEqual(len(result.items), 2)
        self.assertEqual(result.items[0].name, "Alice")
        self.assertEqual(result.items[1].name, "Bob")
        self.assertEqual(result.metadata.total_pages, 2)

    def test_paginate_none_dataset(self):
        result = PaginationHelper.paginate(None, page=1, page_size=10)
        self.assertEqual(result.items, [])
        self.assertEqual(result.metadata.total_items, 0)
        self.assertEqual(result.metadata.total_pages, 1)


class TestPaginationHelperPageRange(unittest.TestCase):
    """Tests for UI sliding page range generation with ellipses."""

    def test_page_range_small_total_pages(self):
        self.assertEqual(PaginationHelper.generate_page_range(1, 1), [1])
        self.assertEqual(PaginationHelper.generate_page_range(1, 5), [1, 2, 3, 4, 5])
        self.assertEqual(PaginationHelper.generate_page_range(3, 7, window=2), [1, 2, 3, 4, 5, 6, 7])

    def test_page_range_near_start(self):
        range_start = PaginationHelper.generate_page_range(current_page=1, total_pages=20, window=2)
        self.assertEqual(range_start, [1, 2, 3, 4, 5, "...", 20])

        range_p2 = PaginationHelper.generate_page_range(current_page=2, total_pages=20, window=2)
        self.assertEqual(range_p2, [1, 2, 3, 4, 5, "...", 20])

    def test_page_range_in_middle(self):
        range_w1 = PaginationHelper.generate_page_range(current_page=10, total_pages=20, window=1)
        self.assertEqual(range_w1, [1, "...", 9, 10, 11, "...", 20])

        range_w2 = PaginationHelper.generate_page_range(current_page=10, total_pages=20, window=2)
        self.assertEqual(range_w2, [1, "...", 8, 9, 10, 11, 12, "...", 20])

    def test_page_range_near_end(self):
        range_end = PaginationHelper.generate_page_range(current_page=20, total_pages=20, window=2)
        self.assertEqual(range_end, [1, "...", 16, 17, 18, 19, 20])

        range_p19 = PaginationHelper.generate_page_range(current_page=19, total_pages=20, window=2)
        self.assertEqual(range_p19, [1, "...", 16, 17, 18, 19, 20])

    def test_page_range_custom_ellipsis(self):
        range_custom = PaginationHelper.generate_page_range(
            current_page=10, total_pages=20, window=1, ellipsis="---"
        )
        self.assertEqual(range_custom, [1, "---", 9, 10, 11, "---", 20])


class TestPaginationHelperQueryString(unittest.TestCase):
    """Tests for query string generation."""

    def test_build_query_string_preserves_filters(self):
        params = {"search": "math", "sort": "asc"}
        query = PaginationHelper.build_query_string(params, page=2)
        self.assertTrue(query.startswith("?"))
        parsed = urllib.parse.parse_qs(query.lstrip("?"))
        self.assertEqual(parsed["search"], ["math"])
        self.assertEqual(parsed["sort"], ["asc"])
        self.assertEqual(parsed["page"], ["2"])

    def test_build_query_string_updates_existing_page(self):
        params = {"keyword": "it", "page": "1"}
        query = PaginationHelper.build_query_string(params, page=3)
        parsed = urllib.parse.parse_qs(query.lstrip("?"))
        self.assertEqual(parsed["keyword"], ["it"])
        self.assertEqual(parsed["page"], ["3"])

    def test_build_query_string_custom_param(self):
        query = PaginationHelper.build_query_string({}, page=4, page_param="p")
        self.assertEqual(query, "?p=4")

    def test_build_query_string_handles_none_values(self):
        params = {"valid": "ok", "empty": None}
        query = PaginationHelper.build_query_string(params, page=1)
        parsed = urllib.parse.parse_qs(query.lstrip("?"))
        self.assertIn("valid", parsed)
        self.assertNotIn("empty", parsed)
        self.assertEqual(parsed["page"], ["1"])


class TestPaginationHelperSerialization(unittest.TestCase):
    """Tests for to_dict serialization on metadata and page results."""

    def test_metadata_to_dict(self):
        meta = PaginationMetadata(
            current_page=1,
            page_size=10,
            total_items=100,
            total_pages=10,
            offset=0,
            limit=10,
            has_previous=False,
            has_next=True,
            previous_page=None,
            next_page=2,
        )
        data = meta.to_dict()
        self.assertIsInstance(data, dict)
        self.assertEqual(data["current_page"], 1)
        self.assertEqual(data["page_size"], 10)
        self.assertEqual(data["total_items"], 100)
        self.assertEqual(data["total_pages"], 10)
        self.assertEqual(data["offset"], 0)
        self.assertEqual(data["limit"], 10)
        self.assertFalse(data["has_previous"])
        self.assertTrue(data["has_next"])
        self.assertIsNone(data["previous_page"])
        self.assertEqual(data["next_page"], 2)

    def test_page_result_to_dict(self):
        entities = [DummyEntity(1, "Alice"), DummyEntity(2, "Bob")]
        result = PaginationHelper.paginate(entities, page=1, page_size=2)
        serialized = result.to_dict()
        self.assertIsInstance(serialized, dict)
        self.assertIn("items", serialized)
        self.assertIn("metadata", serialized)
        self.assertEqual(len(serialized["items"]), 2)
        self.assertEqual(serialized["items"][0], {"id": 1, "name": "Alice"})
        self.assertEqual(serialized["metadata"]["total_items"], 2)


if __name__ == "__main__":
    unittest.main()
