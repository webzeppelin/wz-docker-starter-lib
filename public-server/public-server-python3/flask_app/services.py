"""Entry point for the server application."""

import logging
import json
from gevent.wsgi import WSGIServer
from flask import request, Response, jsonify
from datetime import datetime
import uuid
import time
from pytz import timezone, utc
from tzlocal import get_localzone
from .config import configure_app, app, HOSTNAME, PORT
from .utils import encode
from .models import HealthStatus, ServerTime, GuestbookEntry, GuestbookEntrySet
import redis

GUESTBOOK_BROWSE_PAGE_SIZE = 10

@app.before_first_request
def set_up():
    """Configure the application to be used by the application."""
    configure_app(app)


@app.route('/api/v1/health', methods=['GET'])
def get_health():
    """Return service health information."""
    ret = HealthStatus(is_up=True)
    return jsonify(**(ret.to_dict()))

@app.route('/api/v1/time', methods=['GET'])
def get_time():
    """Return the current server time in the server's timezone"""
    tz = get_localzone()
    t = datetime.now(tz)
    #t = tz.localize(t, is_dst=None)

    st = ServerTime(hour=t.hour,
                      minute=t.minute,
                      second=t.second,
                      tz_name=tz.zone,
                      tz_offset=tz.utcoffset(datetime.now()).total_seconds()/3600)
    return jsonify(st.to_dict())

@app.route('/api/v1/guestbook', methods=['POST'])
def sign_guestbook():
    """Accept a new guestbook entry posted to the API and return the new entry"""
    print('Signing the guestbook')
    payload = request.get_json(force=True)
    if payload is None:
        return error_response(400, 'Missing guestbook entry in POST payload')

    name = payload.get('name')
    message = payload.get('message')

    if not name or not message:
        return error_response(400, 'Missing required parameters')

    entry = GuestbookEntry(
        id=new_guid(),
        name=name,
        message=message,
        timestamp=current_datetime()
    )

    # this is where it will get stored in redis
    redis_key = get_redis_key(entry.id)
    json_str = json.dumps(entry.to_dict(), cls=encode.MyJSONEncoder)
    r = get_redis()
    r.set(redis_key, json_str)
    r.lpush('guestbook_list', redis_key)

    return success_response(entry.to_dict())

@app.route('/api/v1/guestbook', methods=['GET'])
def browse_guestbook():
    """Return the most recent guestbook entries"""
    print('Browsing the guestbook')
    last_id = request.args.get("last_id")
    if last_id is None:
        last_id = 0
    else:
        last_id = int(last_id)

    r = get_redis()
    keys = r.lrange('guestbook_list', last_id, (last_id+GUESTBOOK_BROWSE_PAGE_SIZE-1))
    # map(lambda x:x.decode('utf-8'), keys)

    entries = []
    for key in keys:
        json_str = r.get(key).decode('utf-8')
        json_dic = json.loads(json_str)
        entry = GuestbookEntry.from_dict(json_dic)
        entries.append(entry)

    entry_set = GuestbookEntrySet(
        entries=entries,
        count=len(entries),
        last_id=str(last_id+len(entries)),
        has_more=len(entries)==GUESTBOOK_BROWSE_PAGE_SIZE
    )

    return success_response(entry_set.to_dict())


def current_datetime():
    return datetime.now(utc)


def error_response(status_code=400, message="Bad request"):
    print('Sending error response')
    ret = jsonify(message=message)
    ret.status_code = status_code
    ret.mimetype = 'application/json'
    return ret


def success_response(response_dict={}):
    print('Sending success response')
    ret = jsonify(response_dict)
    ret.status_code = 200
    ret.mimetype='application/json'
    return ret

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error))
    return error_response(500, error.message)

@app.errorhandler(404)
def internal_server_error(error):
    return error_response(404, "Not found")

@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error('Unhandled Exception: %s', (e))
    print('Unhandled Exception: %s', (e))
    return error_response(500, str(e))

def new_guid():
    return str(uuid.uuid4())

def get_redis():
    cfg = app.redis_config
    return redis.StrictRedis(host=cfg.hostname, port=cfg.port)

def get_redis_key(id):
    return 'guestbook:'+id

def parse_redis_key(key):
    return key.split(':')[1]

def main():
    """Main entry point of the app."""
    try:
        http_server = WSGIServer((HOSTNAME, PORT),
                                 app,
                                 log=logging,
                                 error_log=logging)

        http_server.serve_forever()
    except Exception as exc:
        logging.error(exc.message)
    finally:
        # get last entry and insert build appended if not completed
        # Do something here
        pass
