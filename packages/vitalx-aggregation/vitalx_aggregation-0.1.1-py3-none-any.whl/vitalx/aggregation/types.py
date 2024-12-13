from datetime import date
from typing import Annotated, Any, Literal, Self, Sequence

from pydantic import BaseModel, Field, field_validator, model_validator

from vitalx.types.providers import Labs, Providers

DateTimeUnit = Literal["minute", "hour", "day", "week", "month", "year"]


class Placeholder(BaseModel):
    placeholder: Literal[True]


class Period(BaseModel):
    value: Annotated[int, Field(ge=1)] = 1
    unit: DateTimeUnit


class RelativeTimeframe(BaseModel):
    type: Literal["relative"]
    anchor: date
    past: Period


Timeframe = RelativeTimeframe | Placeholder


# Select Expressions

TableT = Literal["sleep", "activity", "workout", "body", "meal"]

SleepColumnT = Literal[
    "session_start",
    "session_end",
    "state",
    "type",
    "duration_second",
    "stage_asleep_second",
    "stage_awake_second",
    "stage_light_second",
    "stage_rem_second",
    "stage_deep_second",
    "stage_unknown_second",
    "latency_second",
    "heart_rate_minimum",
    "heart_rate_mean",
    "heart_rate_maximum",
    "heart_rate_dip",
    "efficiency",
    "hrv_mean_rmssd",
    "hrv_mean_sdnn",
    "skin_temperature_delta",
    "respiratory_rate",
    "score",
    "source_type",
    "source_provider",
    "source_app_id",
]


ActivityColumnT = Literal[
    "date",
    "calories_total",
    "calories_active",
    "steps",
    "distance_meter",
    "floors_climbed",
    "duration_active_second",
    "intensity_sedentary_second",
    "intensity_low_second",
    "intensity_medium_second",
    "intensity_high_second",
    "heart_rate_mean",
    "heart_rate_minimum",
    "heart_rate_maximum",
    "heart_rate_resting",
    "source_type",
    "source_provider",
    "source_app_id",
]

WorkoutColumnT = Literal[
    "session_start",
    "session_end",
    "title",
    "sport_name",
    "sport_slug",
    "duration_active_second",
    "heart_rate_mean",
    "heart_rate_minimum",
    "heart_rate_maximum",
    "heart_rate_zone_1",
    "heart_rate_zone_2",
    "heart_rate_zone_3",
    "heart_rate_zone_4",
    "heart_rate_zone_5",
    "heart_rate_zone_6",
    "distance_meter",
    "calories",
    "elevation_gain_meter",
    "elevation_maximum_meter",
    "elevation_minimum_meter",
    "speed_mean",
    "speed_maximum",
    "power_source",
    "power_mean",
    "power_maximum",
    "power_weighted_mean",
    "steps",
    "map",
    "source_type",
    "source_provider",
    "source_app_id",
]

BodyColumnT = Literal[
    "measured_at",
    "weight_kilogram",
    "fat_mass_percentage",
    "water_percentage",
    "muscle_mass_percentage",
    "visceral_fat_index",
    "bone_mass_percentage",
    "source_type",
    "source_provider",
    "source_app_id",
]

MealColumnT = Literal[
    "calories",
    # Macros
    "carbohydrate_gram",
    "protein_gram",
    "alcohol_gram",
    "water_gram",
    "fibre_gram",
    "sugar_gram",
    "cholesterol_gram",
    # Fats
    "saturated_fat_gram",
    "monounsaturated_fat_gram",
    "polyunsaturated_fat_gram",
    "omega3_fat_gram",
    "omega6_fat_gram",
    "total_fat_gram",
    # Minerals
    "sodium_milligram",
    "potassium_milligram",
    "calcium_milligram",
    "phosphorus_milligram",
    "magnesium_milligram",
    "iron_milligram",
    "zinc_milligram",
    "fluoride_milligram",
    "chloride_milligram",
    # Vitamins
    "vitamin_a_milligram",
    "vitamin_b1_milligram",
    "riboflavin_milligram",
    "niacin_milligram",
    "pantothenic_acid_milligram",
    "vitamin_b6_milligram",
    "biotin_microgram",
    "vitamin_b12_microgram",
    "vitamin_c_milligram",
    "vitamin_d_microgram",
    "vitamin_e_milligram",
    "vitamin_k_microgram",
    "folic_acid_microgram",
    # Trace Elements
    "chromium_microgram",
    "copper_milligram",
    "iodine_microgram",
    "manganese_milligram",
    "molybdenum_microgram",
    "selenium_microgram",
    "date",
    "name",
    "source_type",
    "source_provider",
    "source_app_id",
]

AggregateFunctionT = Literal[
    "mean", "min", "max", "sum", "count", "median", "stddev", "oldest", "newest"
]


class SleepColumnExpr(BaseModel):
    sleep: SleepColumnT


class ActivityColumnExpr(BaseModel):
    activity: ActivityColumnT


class WorkoutColumnExpr(BaseModel):
    workout: WorkoutColumnT


class BodyColumnExpr(BaseModel):
    body: BodyColumnT


class MealColumnExpr(BaseModel):
    meal: MealColumnT


class IndexColumnExpr(BaseModel):
    index: TableT


class GroupKeyColumnExpr(BaseModel):
    group_key: int | Literal["*"] = Field(default="*")


class SleepScoreValueMacroExpr(BaseModel):
    value_macro: Literal["sleep_score"]
    version: Literal["automatic"] = "automatic"


class ChronotypeValueMacroExpr(BaseModel):
    value_macro: Literal["chronotype"]
    version: Literal["automatic"] = "automatic"


class UnrecognizedValueMacroExpr(BaseModel):
    value_macro: str


ValueMacroExpr = (
    SleepScoreValueMacroExpr | ChronotypeValueMacroExpr | UnrecognizedValueMacroExpr
)


ColumnExpr = (
    SleepColumnExpr
    | ActivityColumnExpr
    | WorkoutColumnExpr
    | BodyColumnExpr
    | IndexColumnExpr
    | GroupKeyColumnExpr
    | ValueMacroExpr
)


class AggregateExpr(BaseModel):
    arg: ColumnExpr
    func: AggregateFunctionT


SelectExpr = AggregateExpr | ColumnExpr

# Partitioning and Swizzling

DatePartT = DateTimeUnit | Literal["weekday", "week_of_year", "day_of_year"]


class DateTruncExpr(BaseModel):
    date_trunc: Period
    arg: IndexColumnExpr | Placeholder


class DatePartExpr(BaseModel):
    arg: IndexColumnExpr | Placeholder
    date_part: DatePartT


GroupByExpr = DateTruncExpr | DatePartExpr

# Query


class Query(BaseModel):
    select: Sequence[SelectExpr]
    group_by: list[GroupByExpr] = Field(default_factory=list)
    split_by_source: bool = Field(default=False)

    @field_validator("group_by", mode="after")
    @classmethod
    def validate_group_by(cls, v: list[GroupByExpr]) -> list[GroupByExpr]:
        date_trunc_count = sum(isinstance(expr, DateTruncExpr) for expr in v)
        if date_trunc_count >= 2:
            raise ValueError(
                f"group_by supports at most 1 DateTruncExpr. found {date_trunc_count}."
            )
        return v

    @model_validator(mode="after")
    def validate_aggregate_expr_present(self, v) -> Self:

        if self.group_by:
            # All select expressions must be AggregateExpr or GroupKeyColumnExpr
            # in a GroupBy context.
            if any(
                not isinstance(expr, (AggregateExpr, GroupKeyColumnExpr))
                for expr in self.select
            ):
                raise ValueError(
                    "Select expressions must either be AggregateExpr or GroupKeyColumnExpr in a GroupBy context."
                )

        return self


class QueryConfig(BaseModel):
    week_starts_on: Literal["sunday", "monday"] = "monday"
    provider_priority_overrides: list[Providers | Labs] | None = None


class QueryBatch(BaseModel):
    timeframe: Timeframe
    queries: list[Query]
    config: QueryConfig = Field(default_factory=lambda: QueryConfig())

    @model_validator(mode="before")
    @classmethod
    def validate_queries(cls, values: Any) -> Any:
        if not isinstance(values, dict):
            return values

        # compatibility with SDK 0.1.x or earlier
        if "queries" not in values and (queries := values.pop("instructions", None)):
            values["queries"] = queries

        return values
