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
