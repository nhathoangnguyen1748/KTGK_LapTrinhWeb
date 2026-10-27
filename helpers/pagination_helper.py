"""
Pagination helper utility for managing collection slicing,
navigation ranges, sanitizing query parameters, and metadata calculation.
"""
import math
import urllib.parse
from dataclasses import dataclass
from typing import Any, Dict, Generic, List, Optional, Sequence, TypeVar, Union

T = TypeVar("T")


@dataclass
class PaginationMetadata:
    """
    Data model encapsulating pagination state and navigation information.
    """
    current_page: int
    page_size: int
    total_items: int
    total_pages: int
    offset: int
    limit: int
    has_previous: bool
    has_next: bool
    previous_page: Optional[int] = None
    next_page: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes all metadata attributes to a standard dictionary.
        """
        return {
            "current_page": self.current_page,
            "page_size": self.page_size,
            "total_items": self.total_items,
            "total_pages": self.total_pages,
            "offset": self.offset,
            "limit": self.limit,
            "has_previous": self.has_previous,
            "has_next": self.has_next,
            "previous_page": self.previous_page,
            "next_page": self.next_page,
        }


@dataclass
class PageResult(Generic[T]):
    """
    Generic result model containing paginated items and associated metadata.
    """
    items: List[T]
    metadata: PaginationMetadata

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes items and nested metadata dictionary.
        """
        serialized_items = []
        for item in self.items:
            if hasattr(item, "to_dict") and callable(getattr(item, "to_dict")):
                serialized_items.append(item.to_dict())
            else:
                serialized_items.append(item)
        return {
            "items": serialized_items,
            "metadata": self.metadata.to_dict() if hasattr(self.metadata, "to_dict") else self.metadata,
        }


class PaginationHelper:
    """
    Utility engine providing pagination calculation, sanitization,
    page range generation, and query string construction.
    """
    DEFAULT_PAGE: int = 1
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100

    @classmethod
    def sanitize_page(cls, page: Any, default: int = DEFAULT_PAGE) -> int:
        """
        Converts input to integer; if invalid, negative, or zero, returns default.
        """
        if isinstance(page, bool):
            return default
        try:
            val = int(float(page))
            return val if val > 0 else default
        except (ValueError, TypeError, OverflowError):
            return default

    @classmethod
    def sanitize_page_size(
        cls,
        page_size: Any,
        default: int = DEFAULT_PAGE_SIZE,
        max_size: int = MAX_PAGE_SIZE,
    ) -> int:
        """
        Converts input to integer; clamps values within range [1, max_size];
        returns default on error.
        """
        if isinstance(page_size, bool):
            return default
        try:
            val = int(float(page_size))
            if val < 1:
                return 1
            return min(val, max_size)
        except (ValueError, TypeError, OverflowError):
            return default

    @classmethod
    def calculate_total_pages(cls, total_items: int, page_size: int) -> int:
        """
        Computes math.ceil(total_items / page_size) if total_items > 0 else 1.
        """
        try:
            items_count = int(total_items)
            size = max(1, int(page_size))
        except (ValueError, TypeError):
            return 1

        if items_count > 0:
            return math.ceil(items_count / size)
        return 1

    @classmethod
    def calculate_offset(cls, page: int, page_size: int) -> int:
        """
        Computes (max(1, page) - 1) * page_size.
        """
        try:
            p = max(1, int(page))
            size = max(0, int(page_size))
            return (p - 1) * size
        except (ValueError, TypeError):
            return 0

    @classmethod
    def get_metadata(
        cls,
        total_items: int,
        page: Any = DEFAULT_PAGE,
        page_size: Any = DEFAULT_PAGE_SIZE,
        max_page_size: int = MAX_PAGE_SIZE,
    ) -> PaginationMetadata:
        """
        Validates boundaries, calculates total pages, and instantiates PaginationMetadata.
        """
        safe_page = cls.sanitize_page(page)
        safe_page_size = cls.sanitize_page_size(page_size, max_size=max_page_size)
        try:
            safe_total_items = max(0, int(total_items))
        except (ValueError, TypeError):
            safe_total_items = 0

        total_pages = cls.calculate_total_pages(safe_total_items, safe_page_size)
        offset = cls.calculate_offset(safe_page, safe_page_size)
        limit = safe_page_size
        has_previous = safe_page > 1
        has_next = safe_page < total_pages
        previous_page = (safe_page - 1) if has_previous else None
        next_page = (safe_page + 1) if has_next else None

        return PaginationMetadata(
            current_page=safe_page,
            page_size=safe_page_size,
            total_items=safe_total_items,
            total_pages=total_pages,
            offset=offset,
            limit=limit,
            has_previous=has_previous,
            has_next=has_next,
            previous_page=previous_page,
            next_page=next_page,
        )

    @classmethod
    def paginate(
        cls,
        items: Sequence[T],
        page: Any = DEFAULT_PAGE,
        page_size: Any = DEFAULT_PAGE_SIZE,
        max_page_size: int = MAX_PAGE_SIZE,
    ) -> PageResult[T]:
        """
        Computes metadata, slices items[offset : offset + limit], and returns PageResult.
        """
        if items is None:
            sequence_items: Sequence[T] = []
        else:
            sequence_items = items

        total_items = len(sequence_items)
        metadata = cls.get_metadata(total_items, page, page_size, max_page_size)
        sliced_items = list(sequence_items[metadata.offset : metadata.offset + metadata.limit])

        return PageResult(items=sliced_items, metadata=metadata)

    @classmethod
    def generate_page_range(
        cls,
        current_page: int,
        total_pages: int,
        window: int = 2,
        ellipsis: str = "...",
    ) -> List[Union[int, str]]:
        """
        Generates a sliding page number list with ellipses for UI rendering
        (e.g., [1, '...', 4, 5, 6, '...', 10]).
        """
        safe_total = max(1, int(total_pages))
        safe_current = max(1, min(int(current_page), safe_total))
        safe_window = max(1, int(window))

        threshold = 2 * safe_window + 3
        if safe_total <= threshold:
            return list(range(1, safe_total + 1))

        near_start = safe_current <= safe_window + 2
        near_end = safe_current >= safe_total - (safe_window + 1)

        if near_start and not near_end:
            end_idx = max(2 * safe_window + 1, safe_current + safe_window)
            if end_idx >= safe_total - 1:
                return list(range(1, safe_total + 1))
            return list(range(1, end_idx + 1)) + [ellipsis, safe_total]

        if near_end and not near_start:
            start_idx = min(safe_total - 2 * safe_window, safe_current - safe_window)
            if start_idx <= 2:
                return list(range(1, safe_total + 1))
            return [1, ellipsis] + list(range(start_idx, safe_total + 1))

        if near_start and near_end:
            return list(range(1, safe_total + 1))

        # Middle sliding window
        left = safe_current - safe_window
        right = safe_current + safe_window
        return [1, ellipsis] + list(range(left, right + 1)) + [ellipsis, safe_total]

    @classmethod
    def build_query_string(
        cls,
        params: Optional[Dict[str, Any]],
        page: int,
        page_param: str = "page",
    ) -> str:
        """
        Takes existing dictionary query params, updates page_param,
        and returns a safe query string (e.g., ?keyword=it&page=2).
        """
        safe_page = cls.sanitize_page(page)
        cleaned_params: Dict[str, Any] = {}
        if params:
            for k, v in params.items():
                if v is not None:
                    cleaned_params[str(k)] = v
        cleaned_params[page_param] = safe_page
        query = urllib.parse.urlencode(cleaned_params, doseq=True)
        return f"?{query}" if query else ""
