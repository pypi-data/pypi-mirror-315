from typing import Collection


def indices_around_index(index: int, collection: Collection) -> list[int]:
    """Indices from first after index to last of collection, and from head of collection to last before index."""
    range_from_after_index_to_last: range = range(index + 1, len(collection))
    range_from_head_to_before_index: range = range(0, index)
    indices: list[int] = list(range_from_after_index_to_last) + list(range_from_head_to_before_index)
    return indices
