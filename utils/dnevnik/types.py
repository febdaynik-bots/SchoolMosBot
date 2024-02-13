import typing
import datetime

from pydantic import BaseModel


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


class SubjectMarksType(BaseModel):
	id: int
	name: str
	average: float
	average_by_all: float
	dynamic: str
	periods: typing.List[str]
