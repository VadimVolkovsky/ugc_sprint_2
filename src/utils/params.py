import enum
from dataclasses import dataclass, field
from typing import Annotated
from fastapi import Query


class Sort(enum.StrEnum):
    popular = "POPULAR"
    desc = "DESC"
    asc = "ASC"


@dataclass
class CommonQueryParams:
    page_number: Annotated[int, Query(gt=0)] = 1
    page_size: Annotated[int, Query(gt=0)] = 10
    sort: Annotated[Sort, Query(default_factory=list)] = field(default_factory=list)


def sort_by_count(k):
    return len(k['likes'])
