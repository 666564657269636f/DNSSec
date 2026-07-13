$TTL 86400

@   IN SOA com. admin.com. (
        1
        86400
        3600
        604800
        86400
)

;
; Name Server del TLD .com
;

@       IN NS    com.

;
; Glue record
;

com.    IN A     10.10.1.2

test.com.       IN NS    ns1.test.com.
ns1.test.com.   IN A     10.10.2.2
