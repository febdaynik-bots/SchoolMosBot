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
	id: int = Field(alias='subject_id')
	name: str = Field(alias='subject_name')
	schedule_item_id: typing.Optional[int] = None
	is_done: typing.Optional[bool] = None


class HouseworkTypeByNotify(HouseworkType):
	additional_materials: typing.Optional[typing.List[dict]] = []
	attachments: typing.Optional[typing.List[dict]] = []
	comments: typing.Optional[typing.List[dict]] = []
	date: str
	date_assigned_on: str
	description: str
	has_teacher_answer: bool
	homework_entry_student_id: int
	lesson_date_time: str
	materials: typing.Optional[typing.List[dict]] = []


class InfoHouseworkType(HouseworkType):
	homework: str
	room_number: str
	teacher: Teacher
	date: str


class Marks(BaseModel):
	id: int = Field(alias="subject_id")
	name: str = Field(alias="subject_name")
	comment: str
	comment_exists: bool
	control_form_name: str
	created_at: typing.Optional[str] = None
	criteria: typing.Optional[str] = None
	date: str
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
