from typing import Dict, DefaultDict, NamedTuple, List
from enum import Enum

class StrEnum(str, Enum):
    pass

class ReviewStatus(StrEnum):
  ON_TIME = 'on_time'
  LATE = 'late'
  NO_RESPONSE = 'no_response'

class Review(NamedTuple):
  reviewer: str
  status: ReviewStatus
  time_due: str

class Reviews:
  def __init__(self):
    self.on_time = 0
    self.late = 0
    self.no_response = 0

  @property
  def total(self):
    return self.on_time + self.late + self.no_response

  @property
  def on_time_ratio(self):
    if not self.on_time and not self.late:
      return 0
    return self.on_time / (self.on_time + self.late)

  @property
  def late_ratio(self):
    if not self.on_time and not self.late:
      return 0
    return self.late / (self.on_time + self.late)

  @property
  def no_response_ratio(self):
    if not self.total:
      return 0
    return self.no_response / self.total

  def __str__(self):
    return "total: {:>4} on_time: {:>4} ({:7.2%}); late: {:>4} ({:7.2%}); no_response: {:>4} ({:7.2%})".format(
      self.total, self.on_time, self.on_time_ratio, self.late, self.late_ratio, self.no_response, self.no_response_ratio,
    )
