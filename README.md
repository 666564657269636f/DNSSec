# *DNS*sec

## *DNS* Network

```sh
cd dns-network
```

This section provides a static *DNS* network used to test and verify basic *DNS* configurations in an isolated environment.

```sh
docker compose down -v && docker compose up --build -d
```

## *DNS*sec Network

```sh
cd dnssec-network
```

This section provides a static *DNS*sec network used to test and verify *DNS*sec configurations, including zone signing, key management, and validation.

```sh
docker compose down -v && docker compose up --build -d
```

## *DNS*sec Lab Generator

```sh
cd dnssec-lab
```

This component automatically generates a complete *DNS*sec lab environment, including the required zones, keys, signatures, and Docker Compose configuration.

### Configuration

Before generating the lab, update `lab.yml` configuration file describing the *DNS* hierarchy and the servers to be generated.

```yml
servers: 
  - name: root 
    zone_name: . 
    container_name: root 
    hostname: root 
    ip: <ip> 
    
    children: 
      - name: <name> 
      zone_name: <zone_name> 
      container_name: <container_name> 
      hostname: <hostname> 
      ip: <ip> 
      
      children: 
      - name: <name> 
      zone_name: <zone_name> 
      container_name: <container_name> 
      hostname: <hostname> 
      ip: <ip> 
    
    children: 
      ...
```

### Execution

Generate the environment with:

```sh
uv venv
source .venv/bin/activate
docker compose -f output/docker-compose.yml down -v
rm -rf output/dns docker-compose.yml
uv run main.py
docker compose -f output/docker-compose.yml up --build -d
```

Verify **Data Integrity and Authentication**:

```sh
docker exec -it client dig @10.10.3.1 A example.com +dnssec

; <<>> DiG 9.20.26-1~deb13u1-Debian <<>> @10.10.3.1 A test.com +dnssec
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 8456
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags: do; udp: 1232
;; QUESTION SECTION:
;test.com.                      IN      A

;; ANSWER SECTION:
test.com.               86368   IN      A       10.10.2.2
test.com.               86368   IN      RRSIG   A 13 2 86400 20260929142629 20260830142629 30805 test.com. Y4GIOr0WC1pG18ATCkbQbvtV3a06/0R3iQgqN+fCPmLLwExP+wVJoVsM +yd/VC4B7uO6wQASQqy2zgLJAmPfiw==

;; Query time: 0 msec
;; SERVER: 10.10.3.1#53(10.10.3.1) (UDP)
;; WHEN: Wed Sep 02 16:00:39 UTC 2026
;; MSG SIZE  rcvd: 157
```

Verify **Authenticated Denial of Existence**:

```sh
docker exec -it client dig @10.10.3.1 A nope.test.com +dnssec

; <<>> DiG 9.20.26-1~deb13u1-Debian <<>> @10.10.3.1 A nope.test.com +dnssec
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 55718
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 0, AUTHORITY: 6, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags: do; udp: 1232
;; QUESTION SECTION:
;nope.test.com.                 IN      A

;; AUTHORITY SECTION:
test.com.               3457    IN      SOA     ns1.test.com. admin.test.com. 2 86400 3600 604800 86400
test.com.               86257   IN      RRSIG   SOA 13 2 86400 20260929142629 20260830142629 30805 test.com. ILMv+3bvrApDUzWgtYmTeZuLBVNDdL5g5G9+WeH4h3/X3Y2wiGPwOIWr 3WT7OM2/fjAy4EdzAeWNE/OWOR2djw==
test.com.               86400   IN      NSEC    ftp.test.com. A NS SOA RRSIG NSEC DNSKEY
test.com.               86400   IN      RRSIG   NSEC 13 2 86400 20260929142629 20260830142629 30805 test.com. oyOsPQPS3/hTqRUAtOdqmBc/m/7IpdtwZusisdpujrJdTeg8eby0HwQY zshRd6zz2zXBEyiNgy5DRl2y1Yft4g==
mail.test.com.          86400   IN      NSEC    ns1.test.com. A RRSIG NSEC
mail.test.com.          86400   IN      RRSIG   NSEC 13 3 86400 20260929142629 20260830142629 30805 test.com. LpK0lljJOo0RwjO+EGxiF/Jx+zMIFSfKntSJGp6sVDueyPlbu7l2+fWc /hIYmV+dRQ8SQglKFfhci/JwdGoFdg==

;; Query time: 8 msec
;; SERVER: 10.10.3.1#53(10.10.3.1) (UDP)
;; WHEN: Wed Sep 02 16:02:30 UTC 2026
;; MSG SIZE  rcvd: 474
```


## *DNS*sec KeyTrap Vulnerability (*CVE-2023-50387*)

This repository provides a minimal lab environment to replicate and analyze the *DNS*sec KeyTrap vulnerability (*CPU* exhaustion *DoS*) by generating a *DNS* zone containing multiple malformed *RRSIG* records.

### Prerequisites

Ensure Docker, Docker Compose, and the necessary BIND utilities are installed on your host system:

```sh
sudo apt update
sudo apt install bind9utils tmux
```

```sh
cd CVE-2023-50387
```

### Execution Step

1. **Generate Keys and Sign the Zone**    
Run the script to generate the *KSK/ZSK* keys, sign the target zone, and inject the payload *RRSIG* records:

```sh
python3 script.py
```

2. **Launch the Lab Environment**    
Rebuild and start the Docker containers with fresh volumes to load the updated zone files:

```sh
docker compose down -v && docker compose up --build -d
```

3. **Verify Baseline *DNS*sec Functionality**    
Query a benign record (a.a.test) to confirm that the resolver (10.10.0.3) is validating *DNS*sec correctly. Look for the ad (Authenticated Data) flag in the header:

```sh
$ docker compose exec -it attacker dig @10.10.0.3 a.a.test

; <<>> DiG 9.18.44 <<>> @10.10.0.3 a.a.test
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 9705
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;a.a.test.                      IN      A

;; ANSWER SECTION:
a.a.test.               86400   IN      A       10.10.0.4

;; Query time: 7 msec
;; SERVER: 10.10.0.3#53(10.10.0.3) (UDP)
;; WHEN: Mon Aug 17 19:56:19 UTC 2026
;; MSG SIZE  rcvd: 53
```

4. **Trigger the KeyTrap Vulnerability**    
Monitor CPU utilization in real time using tmux while sending the malicious query:

    - Open tmux and split the terminal:

    ```sh
    tmux
    ```

    Press `CTRL + B`, then `%` to split the window vertically.

    - In the right pane, monitor resource consumption:

    ```sh
    docker stats kt_resolver
    ```

    - In the left pane `CTRL + B` then `←`, send the exploit query:

    ```sh
    $ docker compose exec -it attacker dig @10.10.0.3 www.a.test

    ;; communications error to 10.10.0.3#53: timed out
    ;; communications error to 10.10.0.3#53: timed out
    ;; communications error to 10.10.0.3#53: timed out

    ; <<>> DiG 9.18.44 <<>> @10.10.0.3 www.a.test
    ; (1 server found)
    ;; global options: +cmd
    ;; no servers could be reached
    ```

## License

This project is licensed under the MIT License. See the `LICENSE` file for
the full license text.

### Third-Party Code

The `CVE-2023-50387/` component contains a portion of code derived from
[CVE-2023-50387](https://github.com/knqyf263/CVE-2023-50387) by Teppei Fukuda.

The derived code is distributed under the MIT License. The original copyright
and license notices are preserved in `THIRD-PARTY-NOTICES`.

### References

* Fukuda, T. — [CVE-2023-50387 / KeyTrap](https://github.com/knqyf263/CVE-2023-50387)
* [CVE-2023-50387](https://nvd.nist.gov/vuln/detail/CVE-2023-50387)
