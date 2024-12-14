from datetime import timedelta, datetime, timezone
import re


def display(d: timedelta, use_double_digits: bool = False) -> str:
    years = int(d.days / 365)
    remaining = d.days % 365
    weeks = int(remaining / 7)
    days = remaining % 7

    hours = int(d.seconds / 3600)
    remaining = d.seconds % 3600
    minutes = int(remaining / 60)
    seconds = remaining % 60

    if use_double_digits:
        if years:
            return f"{years:02}y{weeks:02}w"
        if weeks:
            return f"{weeks:02}w{days:02}d"
        if days:
            return f"{days:02}d{hours:02}h"
        if hours:
            return f"{hours:02}h{minutes:02}m"
        if minutes:
            return f"{minutes:02}m{seconds:02}s"
        return f"{seconds}s"
    else:
        if years:
            return f"{years}y{weeks}w"
        if weeks:
            return f"{weeks}w{days}d"
        if days:
            return f"{days}d{hours}h"
        if hours:
            return f"{hours}h{minutes}m"
        if minutes:
            return f"{minutes}m{seconds}s"
        return f"{seconds}s"


def human_time_to_iso(human_time: str) -> str:
    if human_time == "now":
        now = datetime.now(timezone.utc)
        return now.isoformat(timespec="milliseconds").replace("+00:00", "Z")

    if isinstance(human_time, int):
        result_time = datetime.fromtimestamp(human_time / 1000, tz=timezone.utc)
    elif human_time.startswith("-") or human_time.startswith("+"):
        # Initialize a timedelta object
        time_delta = timedelta()

        patterns = {
            "w": r"([+-]\d+)w",  # Weeks
            "d": r"([+-]\d+)d",  # Days
            "h": r"([+-]\d+)h",  # Hours
            "m": r"([+-]\d+)m",  # Minutes
            "s": r"([+-]\d+)s",  # Seconds
        }

        for unit, pattern in patterns.items():
            match = re.search(pattern, human_time)
            if match:
                value = int(match.group(1))
                if unit == "w":
                    time_delta += timedelta(weeks=value)
                elif unit == "d":
                    time_delta += timedelta(days=value)
                elif unit == "h":
                    time_delta += timedelta(hours=value)
                elif unit == "m":
                    time_delta += timedelta(minutes=value)
                elif unit == "s":
                    time_delta += timedelta(seconds=value)

        now = datetime.now(timezone.utc)
        result_time = now + time_delta
    else:
        length = len(human_time)
        # '1734010792148'
        if length == 13:
            result_time = datetime.fromtimestamp(int(human_time) / 1000, tz=timezone.utc)

        # '2023-12-04T00:19:22.854Z'
        elif length == 24:
            # Try parsing
            result_time = datetime.strptime(human_time, "%Y-%m-%dT%H:%M:%S.%fZ")

        # '2023-12-04T00:19:22'
        elif length == 19:
            # Try parsing
            try:
                result_time = datetime.strptime(human_time, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                result_time = datetime.strptime(human_time, "%Y-%m-%d %H:%M:%S")
        else:
            raise Exception("Unsupported time format: " + human_time)

    return result_time.strftime("%Y-%m-%dT%H:%M:%S.") + f"{result_time.microsecond // 1000:03d}Z"


def _test():
    # Example usage
    print(human_time_to_iso("-1w"))  # One week ago
    print(human_time_to_iso("-1h35m"))  # 1 hour and 35 minutes ago
    print(human_time_to_iso("+2h10m5s"))  # 2 hours, 10 minutes, and 5 seconds from now
    print(human_time_to_iso("+3d1w"))
    print(human_time_to_iso(1734010792148))
    print(human_time_to_iso("1734010792148"))
    print(human_time_to_iso("2024-12-10T17:37:53.323Z"))
    print(human_time_to_iso("2024-12-10T17:37:53"))
    print(human_time_to_iso("2024-12-10 17:37:53"))


# _test()


def iso_date_to_timestamp(datetime_string: str) -> int:
    dt_object = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    return int(dt_object.replace(tzinfo=timezone.utc).timestamp() * 1000)


def timestamp_to_iso_date(timestamp_ms: int) -> str:
    dt = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
    return dt.isoformat(timespec="milliseconds").replace("+00:00", "Z")
