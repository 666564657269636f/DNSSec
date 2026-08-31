$TTL 86400

@   IN SOA ns1.test.com. admin.test.com. (
        1          ; Serial
        86400      ; Refresh
        3600       ; Retry
        604800     ; Expire
        86400      ; Negative Cache TTL
)

; Name server della zona
@       IN NS      ns1.test.com.

; Glue interno
ns1     IN A       10.10.2.2

; Dominio principale
@       IN A       10.10.2.2

; Alcuni host
www     IN A       10.10.2.2
mail    IN A       10.10.2.20

; Alias
ftp     IN CNAME   www