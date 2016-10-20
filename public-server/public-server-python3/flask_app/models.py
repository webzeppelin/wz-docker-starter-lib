import iso8601

class HealthStatus(object):
    def __init__(self, is_up = False):
        self.is_up = is_up

    def to_dict(self):
        return self.__dict__


class ServerTime(object):
    def __init__(self, hour = 0, minute = 0, second = 0, tz_name = 'Default', tz_offset = 0):
        self.hour = hour
        self.minute = minute
        self.second = second
        self.tz_name = tz_name
        self.tz_offset = tz_offset

    def to_dict(self):
        return self.__dict__


class GuestbookEntry(object):
    def __init__(self, id = None, name = None, message = None, timestamp = None):
        self.id = id
        self.name = name
        self.message = message
        self.timestamp = timestamp

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(dic):
        ret = GuestbookEntry(
            id = dic.get('id'),
            name = dic.get('name'),
            message = dic.get('message'),
            timestamp=dic.get('timestamp')
        )
        if isinstance(ret.timestamp, str):
            ret.timestamp = iso8601.parse_date(ret.timestamp)
        return ret

class GuestbookEntrySet(object):
    def __init__(self, entries=[], count=0, last_id=None, has_more=False):
        self.entries = entries
        self.count = count
        self.last_id = last_id
        self.has_more = has_more

    def to_dict(self):
        ret = dict(
            count=self.count,
            last_id=self.last_id,
            has_more=self.has_more
        )
        entries = []
        for x in self.entries:
            entries.append(x.to_dict())
        ret['entries'] = entries
        return ret
