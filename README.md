# DNSSec

```

```

L'idea del progetto consiste nel creare una rete DNSSec che sia autoconfigurabile, ovvero creare un file yaml che permette di aggiungere host, client ecc in modo tale che, all'avvio del docker compose o alla creazione in questo caso, permetta di avviare tutti gli host presenti all'interno. Devo fare in modo di configurare anche tutti i client, firmare ecc e, alla fine, fare anche la aprte di gestione se riesco, quindi rollare le chiavi ecc. 
Passi da seguire: 
- Creare prima una rete funzionante di test facendo il dockercompose e i dockerfile a mano, che faccia tutto! Ovvero tutte le operazioni e che resetti e ricrei tutto all'avvio, non devo lasciare cose pendenti che se faccio docker compose down -v perdo tutto e deve essere un fastidio. Salvare il tutto in un branch tipo test locale o cose cosi.
- Automatizzare il tutto creando prima di tutto il dockercompose che avvii impostando solo gli host e poi in modo incrementale. Poi valutare come fare questa cosa nel modo piu carino usando python.
- Aggiungere anche un branch per DNS Keytrap, modificare il tutto poi che sia gestibile nel main branch


Chat consiglia:
- Installare Bind9
- Far funzionare il DNS classico
- Aggiungere una zona autorevole
- Resolver 
- DNSSec
- Automazione




feat(network): create initial Docker network topology
Scrivere bene cosa è un revolver



```
.
│
└── com
      │
      └── amogus.com
             │
             ├── www
             ├── api
             └── mail
```


```
BIND9 -> server autoreboli
Unbound -> resolver, per keytrap sostituire solo unbound con qualcosa di vulnerabile e configurare swolo lui
```

db.* sarebbe db.com, db.it??


## root configuration

### named.conf

Punto di ingresso di Bind contiene gli include dei file: 

### named.conf.options

Su quali IP ascoltare, se fare recursion, directory di lavoro e logging

### named.conf.local

Carica le configurazioni della zona


***Fare in modo di impostare il client che faccia richiesta direttamente al resolver senza fare a mano gli IP ogni volta***: 
```bash
echo "nameserver 10.10.3.1" > /etc/resolv.conf
```

***Vedere se fare una commit prima e Sistemare il resolver e testarlo, capire anche tutti i file necessari che non hai visto per niente***