# VANETLAB - Backend

## Ako toto spustit ?

Nainstalujeme si python < 3.9, lebo ns3 je neschopne byt aktualne

My pouzivame toto na vyvoj: `python3.6 python3.6-dev python3.6-venv`.

Nainstalujeme flask.

Pre spustenie treba zadat tieto ENV variables:

```bash
export NS3_WAF_PATH=/path/na/priecinok/v/ktorom/je/waf
```

potom uz staci len `python main.py`

## Ako to funguje

Ideme na `localhost:9000`, kde cez `Choose file` tlacitko nacitame `.py` ns3 simulacny scenar.

![](./media/images/1.png)

Stlacime tlacitko `Submit`, cim sa odosle na BE, ale este sa nevykona.
Nasledne stlacime tlacitko `Run`, po ktorom sa vykona scenar a dostaneme output.

![](./media/images/2.png)

Ked klikneme na jeden z `*.pcap` odkazov tak si vieme stiahnut trace file vygenerovany simulaciou.

tada
