$TTL 86400

@   IN SOA ns1.test.com. admin.test.com. (
        1          ; Serial
        86400      ; Refresh
        3600       ; Retry
        604800     ; Expire
        86400      ; Negative Cache TTL
)

@       IN NS      ns1.test.com.

ns1     IN A       10.10.2.2

@       IN A       10.10.2.2

www     IN A       10.10.2.2
mail    IN A       10.10.2.20

ftp     IN CNAME   www
