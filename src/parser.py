from ics import Calendar, Event
from pytz import timezone
from datetime import datetime, timedelta


def parse_schedule_data(schedule_data):
    lines = schedule_data.split("\n")
    schedule = []
    current_day = None

    for line in lines:
        if line.startswith(
            (
                "SEGUNDA-FEIRA",
                "TERÇA-FEIRA",
                "QUARTA-FEIRA",
                "QUINTA-FEIRA",
                "SEXTA-FEIRA",
            )
        ):
            current_day = line.strip()
        elif line:
            schedule.append((current_day,) + tuple(line.split("\t")))

    return schedule


def generate_ics(schedule):
    calendar = Calendar()
    sao_paulo_tz = timezone("America/Sao_Paulo")
    day_mapping = {
        "SEGUNDA-FEIRA": "MO",
        "TERÇA-FEIRA": "TU",
        "QUARTA-FEIRA": "WE",
        "QUINTA-FEIRA": "TH",
        "SEXTA-FEIRA": "FR",
    }

    for day, time_range, discipline, event_location in schedule:
        start_time, end_time = time_range.split(" - ")
        start_datetime = sao_paulo_tz.localize(datetime.strptime(start_time, "%H:%M"))
        end_datetime = sao_paulo_tz.localize(datetime.strptime(end_time, "%H:%M"))

        event = Event()
        event.name = discipline
        event.begin = datetime.now().replace(hour=start_datetime.hour, minute=start_datetime.minute)
        event.end = datetime.now().replace(hour=end_datetime.hour, minute=end_datetime.minute)
        event.location = event_location
        event.rrule = f"FREQ=WEEKLY;BYDAY={day_mapping[day]}"
        calendar.events.add(event)

    return calendar.serialize()
