from datetime import datetime, timedelta, timezone


def now_hours() -> datetime:
  return (datetime.now(timezone.utc).replace(microsecond=0, second=0, minute=0) + timedelta(hours=5)).replace(tzinfo=None)