import typing
import datetime

from pydantic import BaseModel, Field


class Teacher(BaseModel):
	first_name: str
	last_name: str
	middle_name: str
	sex: typing.Optional[str] = None
	user_id: typing.Optional[int] = None
	birth_date: typing.Optional[str] = None


class HouseworkType(BaseModel):
	id: int
	schedule_item_id: int
	name: str
	is_done: typing.Optional[bool] = None


class InfoHouseworkType(HouseworkType):
	homework: str
	room_number: str
	teacher: Teacher
	date: str


class Marks(BaseModel):
	comment: str
	comment_exists: bool
	control_form_name: str
	created_at: typing.Optional[str] = None
	criteria: typing.Optional[str] = None
	date: str
	id: int
	is_exam: bool
	is_point: bool
	original_grade_system_type: str
	point_date: typing.Optional[str] = None
	update_at: typing.Optional[str] = None
	value: str
	values: typing.Optional[list] = None
	weight: int


class MarkPeriodType(BaseModel):
	count: int
	dynamic: str
	end: str
	end_iso: str
	fixed_value: typing.Optional[str] = None
	marks: typing.List[Marks]
	start: str
	start_iso: str
	title: str
	value: str


class SubjectMarksType(BaseModel):
	id: int = Field(alias="subject_id")
	name: str = Field(alias="subject_name")
	average: float
	average_by_all: float
	dynamic: str
	periods: typing.List[MarkPeriodType]
	year_mark: typing.Optional[str] = None


class Rank(BaseModel):
	averageMarkFive: float
	rankPlace: int
	rankStatus: str
	trend: str


class RankShortType(BaseModel):
	date: str
	rankPlace: int


class SubjectRankType(BaseModel):
	rank: Rank
	id: int = Field(alias='subjectId')
	name: str = Field(alias='subjectName')
