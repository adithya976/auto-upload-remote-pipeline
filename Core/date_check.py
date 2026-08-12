from datetime import datetime

def verify_date(date):
    today = datetime.today().date()
    
    days = (today-date).days

    if days <= 30 and days >= 0:
        return days,True
    else:
        return days,False