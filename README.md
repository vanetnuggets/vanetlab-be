# VANETLAB - Backend

## Spustenie:

 - Treba mat nainstalovany docker
 - Zbuildime docker image prikazom `docker build -t vanetlab-be . `, bude to celkom dlhu chvilu trvat
 - spustime image prikazom `docker run -itdp 80:9000 vanetlab-be:latest`
 - k api sa nasledne dostanes u seba na `127.0.0.1`, ak chces iny port zmen lavu stranu prepinacu `-p`.

## Development setup:

Nainštalujeme si Python < 3.9, kvôli kompatibilite s nástrojom ns-3.

Náš tím používa na vývoj: `python3.6 python3.6-dev python3.6-venv`

Nainštalujeme flask.

Pre spustenie treba zadat tieto ENV variables:

```bash
export NS3_WAF_PATH=/path/na/priecinok/v/ktorom/je/waf
export VANETLAB-BE-PORT=9000
export VANETLAB-BE-HOST=127.0.0.1
```

Samozrejme upravit podla potreby.

potom už stačí len `python main.py`

## Ako to funguje

Ideme na `localhost:9000`, kde cez `Choose file` tlačidlo načítame `.py` ns3 simulačný scenár.

![](./media/images/1.png)

Stlačíme tlačidlo `Submit`, čím sa odošle na BE, ale ešte sa nevykoná.
Následne stlačíme tlačidlo `Run`, po ktorom sa vykoná scenár a dostaneme output.

![](./media/images/2.png)

Kde klikneme na jeden z `*.pcap` odkazov,  tak si vieme stiahnuť trace file vygenerovaný simuláciou.
