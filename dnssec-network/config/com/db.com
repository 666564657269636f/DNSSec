$TTL 86400

@   IN SOA com. admin.com. (
        1
        86400
        3600
        604800
        86400
)

@       IN NS    com.

com.    IN A     10.10.2.1

test.com.       IN NS    ns1.test.com.
ns1.test.com.   IN A     10.10.2.2
test.com. IN DS 15984 13 2 821F3CEC5115F05FCCB9A77F481800B1B42EBFDBBACD4E3B005C03F802B669C1
