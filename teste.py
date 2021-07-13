def showdate():
    from datetime import date
    from calendar import monthrange

    year = date.today().year
    month = date.today().month
    lastDay = monthrange(year, month)[1]

    if month < 10:
        return f'010{month}{year}{lastDay}0{month}{year}'
    else:
        return f'01{month}{year}{lastDay}{month}{year}'
#ok

