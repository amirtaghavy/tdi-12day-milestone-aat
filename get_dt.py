from datetime import datetime, timedelta, timezone
import dateutil.parser


def get_dt(tweet, source):
    if source == 'twitter':
        dt = datetime.now()-tweet.created_at
    elif source == 'stocktwits':
        dt = datetime.now(timezone.utc) - \
            dateutil.parser.parse(tweet['created_at'])
    else:
        return None
    if dt.days == 1:
        o_dt = '`yesterday`'
    elif dt.days > 1:
        o_dt = '`'+str(dt.days)+' days ago`'
    else:
        if dt.seconds // 3600 > 0:
            o_dt = '`-'+str(dt.seconds//3600)+'hr`'
        else:
            o_dt = '`-'+str(dt.seconds//60)+'min`'
    return o_dt
