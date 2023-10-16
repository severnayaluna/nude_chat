import redis


r = redis.Redis(
    host="my-redis.cloud.redislabs.com", port=6379,
    username="redis_98",
    password="wesrdftygh@#$R56y7uhjbbvrtfyguih,j,ukbyjterfthcgmhrtdcymgubilhnjbjvhzWRJETZT<xygztua,RYMZKxtcyudrkfghnjkm,225996259821"
)
r.set('foo', 'bar')
# True

r.get('foo')
# b'bar'

m = r.get('foo')

print( m )

m = r.get('foo')

print( m )