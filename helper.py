import pandas as pd
import numpy as np
import datetime


def generate_data():
    emails = ['fraudster@fraud.com', 'joe@signifyd.com', 'wonkytonky@gmail.com', 'bambam@yahoo.com', 'icet@aol.com']
    events = ['PURCHASE', 'FRAUD_REPORT']

    rand_emails = np.random.choice(emails, size=15)
    rand_events = np.random.choice(events, size=15, p=[0.9, 0.1])

    delta = pd.Timedelta(np.random.randint(0, 3650), 'days')
    date = datetime.date.today() - delta
    dates = [date]

    for _ in range(14):
        delta = pd.Timedelta(np.random.randint(0, 45) * (8.64 * (10**13)))
        date = date + delta
        dates.append(date)
    
    df = pd.DataFrame({'Date':dates, 'Email': rand_emails, 'Event':rand_events})
    df = df.astype('str')

    return df.to_dict('records')


def get_report(data):
    df = pd.DataFrame.from_records(data)
    df.loc[:, 'Date'] = pd.to_datetime(df.loc[:, 'Date'], format='%Y-%m-%d')
    purchases = df[df['Event'] == 'PURCHASE']

    report_arr = []
    for idx in purchases.index:
        purchase = purchases.loc[idx]
        
        status_and_count = get_status_and_counts(purchase, df)
        purchase_obj = purchase.transpose().to_dict()
        report_arr.append({**purchase_obj, **status_and_count})
    
    report = pd.DataFrame.from_records(report_arr)
    report = report.astype('str')

    return report.to_dict('records')


def get_status_and_counts(purchase: pd.DataFrame, df: pd.DataFrame) -> dict:
    date = purchase['Date']

    # we want to query all entries in the original df prior to the current entry's date
    query = df[(df['Date'] < date) & (df['Email'] == purchase['Email'])]

    # pd.TimeDelta Default is in Nanoseconds
    delta = pd.Timedelta(90 * (8.64 * (10**13)))

    # create windows to judge whether an account is GOOD_HISTORY or unconfirmed
    within_ninety_days = query[(query['Date'] >= date - delta) & (query['Date'] < date)]
    outside_ninety_days = query[query['Date'] < date - delta]

    # now, depending on the event types that occured within this window, 
    # we either return NO_HISTORY, FRAUD_HISTORY, GOOD_HISTORY, or UNCONFIRMED HISTORY
    if query.empty: 
        return {'Status':'NO_HISTORY'}
    if 'FRAUD_REPORT' in query['Event'].values: 
        count = query['Event'].value_counts()['FRAUD_REPORT']
        return {'Status': f'FRAUD_HISTORY: {count}'}
    if outside_ninety_days.empty:
        count = within_ninety_days['Event'].value_counts()['PURCHASE']
        return {'Status': f'UNCONFIRMED_HISTORY: {count}'}

    count = outside_ninety_days['Event'].value_counts()['PURCHASE']
    return {'Status': f'GOOD HISTORY: {count}'}


