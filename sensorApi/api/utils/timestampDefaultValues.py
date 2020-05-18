from datetime import datetime
import time
import pytz


def generate_timestamps(request, default_time_delta=3600):
    try:
        start = float(request.GET.get("start"))
    except TypeError:
        start = None

    try:
        end = float(request.GET.get("end"))
    except TypeError:
        end = None

    # none set
    if not isinstance(start, float) and not isinstance(end, float):
        et = time.time()
        st = et - default_time_delta
    # only start set
    elif not isinstance(start, float) and isinstance(end, float):
        et = end
        st = end - default_time_delta
    # only end set
    elif isinstance(start, float) and not isinstance(end, float):
        st = start
        et = st + default_time_delta
    # all set
    else:
        st = start
        et = end

    startDate = datetime.fromtimestamp(st, tz=pytz.utc)
    endDate = datetime.fromtimestamp(et, tz=pytz.utc)

    return (startDate, endDate)
