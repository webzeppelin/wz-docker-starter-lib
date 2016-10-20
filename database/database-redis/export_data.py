from optparse import OptionParser
import sys
import redis

__author__ = 'Jimmy John'
__doc__ = '''
    This is a script to make a copy of a redis db. Mainly to be used for cloning AWS Elasticache
    instancces. Elasticache seems to disable the SAVE/BGSAVE commands and you do not have access to
    the physical redis instances. The UI allows you to create 'Snapshots', but no way to download
    them !.

    NOTE: I don't handle sortedsets in this script as I did not need it. But it's a trivial
    enhancement to this script if you need it.

    Usage:
        python clone_redis.py --redis-source-url awd.prod.foobar > ~/my_redis.data
'''


def gen_redis_proto(*args):
    '''Write out the string in redis protocol so it can be replayed back later'''
    proto = '*{0}\\r\\n'.format(len(args))
    for arg in args:
        proto += '${0}\\r\\n'.format(len(arg))
        proto += '{0}\\r\\n'.format(arg)
    return proto


def extract(options):
    src_r = redis.StrictRedis(host=options.redis_source_url, port=options.redis_source_port)
    all_keys = src_r.keys('*')
    for key in all_keys:
        arr = []
        key_type = src_r.type(key)
        if key_type == 'hash':
            arr.append('HMSET')
            arr.append(key)
            for k, v in src_r.hgetall(key).items():
                arr.append(k)
                arr.append(v)
        elif key_type == 'string':
            arr.append('SET')
            arr.append(key)
            arr.append(src_r.get(key))
        elif key_type == 'set':
            arr.append('SADD')
            arr.append(key)
            arr.extend(list(src_r.smembers(key)))
        elif key_type == 'list':
            arr.append('LPUSH')
            arr.append(key)
            arr.extend(src_r.lrange(key, 0, -1))
        else:
            # TODO
            # we probably need to add support for SortedSets here at some point...
            print('Unsupported key type detected: {0}'.format(key_type))
            sys.exit(1)

        print(gen_redis_proto(*arr))


if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option('-s', '--redis-source-url',
                      action='store',
                      dest='redis_source_url',
                      help='The url of the source redis which is to be cloned [required]')
    parser.add_option('-p', '--redis-source-port',
                      action='store',
                      dest='redis_source_port',
                      default=6379,
                      type=int,
                      help='The port of the source redis which is to be cloned [required, \
                            default: 6379]')
    (options, args) = parser.parse_args()

    if not (options.redis_source_url and options.redis_source_port):
        parser.error('redis-source-url, redis-source-port are required arguments. Please see help')

    extract(options)