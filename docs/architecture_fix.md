Jah — sul on täiesti õige tunne, et draft_architecture_design.md läks liiga “AI-generated ETL fantasy” suunas ja tegelik andmevoog muutus segaseks.

Ja kõige olulisem tähelepanek sul oli siin:

> build_observations.py on lihtsalt transformatsioon mis võtab andmed cleansed ja joinib ja viib need curated kihti

See on täiesti õige.

See EI ole analysis layer.

See on transformation layer.

---

# Tegelik probleem

Praeguses draftis segunesid ära:

* transformation;
* feature engineering;
* curated dataset creation;
* analysis/modeling;
* output generation.

Need on eri asjad.

---

# Tegelikult on sul ainult 3 päris olulist etappi

## 1. Raw

salvestad originaalandmed

## 2. Cleansed

muudad andmed tehniliselt kasutatavaks

## 3. Curated

ehitad analüüsiks vajalikud “business/statistical entities”

Ja alles siis:

## 4. Analysis

teed Monte Carlo / statistika / plotid

---

# Kuidas mõelda GPS flowst päriselt

See on kõige olulisem koht.

Sul on:

```text
gps.txt snapshot every ~30 sec
```

Üks fail sisaldab:

```text
ALL Tallinn vehicles at one moment in time
```

Näiteks:

```text
08:30:00 snapshot
    vehicle 213 at x,y
    vehicle 415 at x,y
    tram 52 at x,y
    ...
```

Järgmine fail:

```text
08:30:30 snapshot
```

jne.

---

# Mida sa päriselt tahad lõpuks teada?

Sa tahad teada:

```text
Millal konkreetne buss jõudis Zoo peatusesse?
Millal jõudis Toomparki?
Kui kaua sõit kestis?
Kui palju hilines?
```

GPS raw EI anna seda otse.

Sa pead selle INFERIMA.

---

# Seega tegelik flow on pigem selline

# RAW

Sul on lihtsalt snapshotid.

```text
gps_20260515_083000.txt
gps_20260515_083030.txt
gps_20260515_083100.txt
```

Need jäävad puutumata.

---

# CLEANSED

Siin toimub TEHNILINE puhastus.

Mitte veel “business events”.

Näiteks:

## gps_positions.parquet

See on lihtsalt kõik GPS read normaalsel kujul.

```text
snapshot_ts
vehicle_id
line_number
lon
lat
speed
heading
destination
```

See on põhimõtteliselt:

```text
raw txt
→ parsed structured table
```

AINULT.

---

# Siis järgmine cleansed dataset

## bus8_positions.parquet

Nüüd filtreerid:

```text
transport_type == bus
line_number == 8
```

See on juba kasulik intermediate dataset.

---

# Siis järgmine samm

Sa tahad teada:

```text
Kui lähedal buss oli Zoole?
```

Seega:

## bus8_stop_distances.parquet

Näiteks:

```text
snapshot_ts
vehicle_id
stop_name
distance_m
```

Näited:

```text
08:30:00 | 213 | Zoo | 18m
08:30:30 | 213 | Zoo | 4m
08:31:00 | 213 | Zoo | 42m
```

See on juba palju loogilisem kui:

> bus_8_stop_proximity.csv

---

# Siis järgmine VERY IMPORTANT STEP

Nüüd sa tahad leida EVENTI.

Näiteks:

```text
BUS ENTERED STOP RADIUS
```

See EI ole enam lihtsalt GPS punkt.

See on inferred event.

Näiteks:

## stop_events.parquet

```text
vehicle_id
stop_name
event_ts
event_type
```

Näiteks:

```text
213 | Zoo | 08:30:28 | arrived
213 | Zoo | 08:30:55 | departed
```

SEE on juba väga oluline dataset.

Ja see on minu meelest:

# CURATED

mitte cleansed.

Sest:

* see pole enam technical cleaning;
* see on inferred business entity.

---

# Siis järgmine curated dataset

## observed_trips.parquet

Nüüd sa ühendad:

```text
Zoo arrival
+
Toompark arrival
```

ja saad:

```text
vehicle_id
service_date
zoo_arrival_ts
toompark_arrival_ts
drive_duration_seconds
```

SEE on juba ideaalne curated dataset.

---

# Alles nüüd tuleb ANALYSIS

Monte Carlo.

Näiteks:

```text
if Rita leaves home at 08:37
what is probability she is late?
```

See kasutab:

```text
observed_trips.parquet
```

mitte raw GPS.

---

# Seega tegelik arhitektuur võiks olla

# RAW

immutables

```text
gps snapshots
gtfs zip
```

---

# CLEANSED

tehniliselt puhastatud/intermediate

```text
gps_positions.parquet
route8_positions.parquet

gtfs_stops.parquet
gtfs_trips.parquet
gtfs_stop_times.parquet
```

Need on:

* parsed
* normalized
* filtered

AGA mitte inferred.

---

# CURATED

business/statistical entities

```text
stop_events.parquet
observed_trips.parquet
trip_delays.parquet
```

Need on:

* derived;
* semantic;
* modelling-ready.

---

# ANALYSIS

```text
lateness_probability.csv
probability_plot.svg
simulation_results.parquet
```

---

# Sinu suur confusion tuli sellest

Draft architecture pani:

```text
bus_8_stop_events.csv
```

cleansed alla.

Aga tegelikult see on juba:

# CURATED

sest see sisaldab inferred business meaningut.

---

# build_observations.py

Sul oli täiesti õige intuition.

See peaks olema:

```text
transformation/build_observations.py
```

mitte analysis.

Sest see teeb:

```text
cleansed → curated
```

transformatsiooni.

---

# Kuidas GTFS päriselt flowb

GTFS on palju lihtsam.

GTFS raw:

```text
gtfs.zip
```

---

# Cleansed

parsed tables:

```text
stops.parquet
routes.parquet
trips.parquet
stop_times.parquet
```

---

# Curated

ainult vajalik subset:

```text
route8_stop_schedule.parquet
target_stops.parquet
```

võibolla isegi:

```text
scheduled_route8_trips.parquet
```

---

# VERY IMPORTANT INSIGHT

Curated EI tähenda:

> final reports

Curated tähendab:

```text
stable modelling-oriented entities
```

See on data warehouse thinking.

---

# Ma arvan et kõige õigem flow sulle oleks

```text
RAW
    immutable snapshots

↓ parse / normalize

CLEANSED
    technically usable datasets

↓ infer / derive / join

CURATED
    modelling-ready datasets

↓ statistical analysis

ANALYSIS

↓ plots / exports

OUTPUT
```

See on palju puhtam kui praegune AI-generated failide nimekiri.

Ja nüüd sul on loogiline vastus küsimusele:

> kuidas ühest 10 veerusega gps.txt failist saab 4 faili?

Vastus:

sest sa liigud:

```text
raw snapshots
→ parsed positions
→ filtered route positions
→ inferred stop events
→ inferred trips
→ statistical datasets
```

Need EI ole sama abstraktsioonitaseme failid.
