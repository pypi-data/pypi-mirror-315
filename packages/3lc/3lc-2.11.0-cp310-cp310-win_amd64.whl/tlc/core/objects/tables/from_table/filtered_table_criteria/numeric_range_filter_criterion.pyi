from _typeshed import Incomplete
from tlc.core.objects.tables.from_table.filtered_table_criteria.filter_criterion import ColumnFilterCriterion as ColumnFilterCriterion, FilterCriterion as FilterCriterion
from tlc.core.schema import Float32Value as Float32Value, Schema as Schema
from typing import Any, Mapping

Numeric = int | float

class NumericRangeFilterCriterion(ColumnFilterCriterion):
    value_range_min: Incomplete
    value_range_max: Incomplete
    def __init__(self, attribute: str | None = None, min_value: Numeric | None = None, max_value: Numeric | None = None, init_parameters: Any = None) -> None: ...
    @staticmethod
    def from_any(any_filter_criterion: FilterCriterion | Mapping) -> NumericRangeFilterCriterion: ...
