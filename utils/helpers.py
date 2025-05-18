from datetime import datetime, timedelta

def get_period_dates(period):
    now = datetime.now()
    if period == 'день':
        return now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == 'неделя':
        return now - timedelta(days=now.weekday())
    elif period == 'месяц':
        return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif period == 'год':
        return now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    return None

def get_progress_bar(progress):
    filled = '█' * int(progress / 10)
    empty = '░' * (10 - len(filled))
    return f"[{filled}{empty}]"