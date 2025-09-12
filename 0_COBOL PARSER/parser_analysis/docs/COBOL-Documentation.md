# ACAS COBOL System Documentation

Generated on: 2025-09-12T14:16:06.746Z

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Subsystems](#subsystems)
4. [Data Access Layer](#data-access-layer)
5. [Programs Index](#programs-index)
6. [Copybooks Index](#copybooks-index)
7. [Dependencies](#dependencies)
8. [Visualizations](#visualizations)

## System Overview

ACAS (Applewood Computers Accounting System) is a comprehensive accounting and business management system written in COBOL.

### Statistics

- **Total Programs:** 279
- **Total Copybooks:** 9
- **Total Files:** 288

## Architecture

### Subsystem Distribution

| Subsystem | Programs | Copybooks | Description |
|-----------|----------|-----------|-------------|
| IRS | 16 | 0 | Internal Revenue System |
| SALES | 37 | 0 | Sales Ledger |
| PURCHASE | 38 | 0 | Purchase Ledger |
| STOCK | 12 | 0 | Stock Control |
| GENERAL | 18 | 0 | General Ledger |
| COMMON | 158 | 9 | Common/Shared Modules |

## Subsystems

### IRS - Internal Revenue System

#### Programs

| Program | Divisions | Sections | Paragraphs | CALLs | COPYs |
|---------|-----------|----------|------------|-------|-------|
| dummy-rdbmsMT.cbl | 4 | 4 | 2 | 0 | 0 |
| irs.cbl | 4 | 11 | 33 | 0 | 0 |
| irs000.cbl | 4 | 4 | 7 | 0 | 0 |
| irs010.cbl | 4 | 39 | 60 | 0 | 1 |
| irs020.cbl | 4 | 14 | 40 | 0 | 0 |
| irs030.cbl | 4 | 14 | 57 | 0 | 0 |
| irs040.cbl | 4 | 7 | 26 | 0 | 0 |
| irs050.cbl | 4 | 15 | 55 | 0 | 0 |
| irs055.cbl | 4 | 7 | 6 | 0 | 0 |
| irs060.cbl | 4 | 15 | 79 | 0 | 0 |
| irs065.cbl | 4 | 7 | 6 | 0 | 0 |
| irs070.cbl | 4 | 5 | 24 | 0 | 0 |
| irs080.cbl | 4 | 5 | 8 | 0 | 0 |
| irs085.cbl | 4 | 6 | 4 | 0 | 0 |
| irs090.cbl | 4 | 11 | 17 | 0 | 0 |
| irsubp.cbl | 4 | 4 | 5 | 0 | 0 |

### SALES - Sales Ledger

#### Programs

| Program | Divisions | Sections | Paragraphs | CALLs | COPYs |
|---------|-----------|----------|------------|-------|-------|
| dummy-rdbmsMT.cbl | 4 | 4 | 2 | 0 | 0 |
| sales.cbl | 4 | 7 | 57 | 0 | 0 |
| sl000.cbl | 4 | 4 | 6 | 0 | 0 |
| sl010.cbl | 4 | 34 | 66 | 0 | 0 |
| sl020.cbl | 4 | 19 | 38 | 0 | 0 |
| sl050.cbl | 4 | 11 | 7 | 0 | 0 |
| sl055.cbl | 4 | 14 | 15 | 0 | 0 |
| sl060.cbl | 4 | 40 | 33 | 0 | 0 |
| sl070.cbl | 4 | 15 | 32 | 0 | 0 |
| sl080.cbl | 4 | 16 | 32 | 0 | 0 |
| sl085.cbl | 4 | 16 | 29 | 0 | 0 |
| sl090.cbl | 4 | 7 | 6 | 0 | 0 |
| sl095.cbl | 4 | 14 | 13 | 0 | 0 |
| sl100.cbl | 4 | 18 | 20 | 0 | 0 |
| sl110.cbl | 4 | 16 | 28 | 0 | 1 |
| sl115.cbl | 4 | 7 | 6 | 0 | 0 |
| sl120.cbl | 4 | 19 | 30 | 0 | 0 |
| sl130.cbl | 4 | 14 | 17 | 0 | 0 |
| sl140.cbl | 4 | 14 | 12 | 0 | 0 |
| sl160.cbl | 4 | 16 | 22 | 0 | 0 |
| sl165.cbl | 4 | 9 | 8 | 0 | 0 |
| sl170.cbl | 4 | 18 | 18 | 0 | 0 |
| sl180.cbl | 4 | 20 | 17 | 0 | 0 |
| sl190.cbl | 4 | 22 | 31 | 0 | 0 |
| sl200.cbl | 4 | 10 | 10 | 0 | 0 |
| sl800.cbl | 4 | 5 | 8 | 0 | 0 |
| sl810.cbl | 4 | 22 | 67 | 0 | 0 |
| sl820.cbl | 4 | 11 | 7 | 0 | 0 |
| sl830.cbl | 3 | 18 | 20 | 0 | 0 |
| sl900.cbl | 4 | 6 | 17 | 0 | 0 |
| sl910.cbl | 4 | 57 | 118 | 0 | 0 |
| sl920.cbl | 4 | 30 | 74 | 0 | 0 |
| sl930.cbl | 4 | 16 | 25 | 0 | 0 |
| sl940.cbl | 4 | 18 | 17 | 0 | 0 |
| sl950.cbl | 4 | 15 | 19 | 0 | 0 |
| sl960.cbl | 4 | 12 | 14 | 0 | 0 |
| sl970.cbl | 4 | 21 | 39 | 0 | 0 |

### PURCHASE - Purchase Ledger

#### Programs

| Program | Divisions | Sections | Paragraphs | CALLs | COPYs |
|---------|-----------|----------|------------|-------|-------|
| dummy-rdbmsMT.cbl | 4 | 4 | 2 | 0 | 0 |
| pl000.cbl | 4 | 4 | 6 | 0 | 0 |
| pl010.cbl | 4 | 30 | 51 | 0 | 0 |
| pl015.cbl | 4 | 19 | 38 | 0 | 0 |
| pl020.cbl | 4 | 32 | 51 | 0 | 0 |
| pl025.cbl | 4 | 11 | 10 | 0 | 0 |
| pl030.cbl | 4 | 27 | 41 | 0 | 0 |
| pl040.cbl | 4 | 14 | 10 | 0 | 0 |
| pl050.cbl | 4 | 16 | 12 | 0 | 0 |
| pl055.cbl | 4 | 11 | 11 | 0 | 0 |
| pl060.cbl | 4 | 24 | 20 | 0 | 0 |
| pl070.cbl | 4 | 15 | 32 | 0 | 0 |
| pl080.cbl | 4 | 16 | 32 | 0 | 0 |
| pl085.cbl | 4 | 16 | 29 | 0 | 0 |
| pl090.cbl | 4 | 7 | 7 | 0 | 0 |
| pl095.cbl | 4 | 14 | 14 | 0 | 0 |
| pl100.cbl | 4 | 18 | 20 | 0 | 0 |
| pl115.cbl | 4 | 7 | 6 | 0 | 0 |
| pl120.cbl | 4 | 19 | 33 | 0 | 0 |
| pl130.cbl | 4 | 14 | 17 | 0 | 0 |
| pl140.cbl | 4 | 14 | 13 | 0 | 0 |
| pl160.cbl | 4 | 16 | 16 | 0 | 0 |
| pl165.cbl | 4 | 9 | 9 | 0 | 0 |
| pl170.cbl | 4 | 18 | 16 | 0 | 0 |
| pl180.cbl | 4 | 6 | 12 | 0 | 0 |
| pl190.cbl | 4 | 18 | 17 | 0 | 0 |
| pl800.cbl | 4 | 5 | 8 | 0 | 0 |
| pl900.cbl | 4 | 8 | 10 | 0 | 0 |
| pl910.cbl | 4 | 15 | 14 | 0 | 0 |
| pl920.cbl | 4 | 8 | 12 | 0 | 0 |
| pl930.cbl | 4 | 12 | 11 | 0 | 0 |
| pl940.cbl | 4 | 13 | 11 | 0 | 0 |
| pl950.cbl | 4 | 19 | 19 | 0 | 0 |
| pl960.cbl | 4 | 5 | 7 | 0 | 0 |
| purchase.cbl | 4 | 7 | 53 | 0 | 0 |
| sl810.cbl | 4 | 22 | 67 | 0 | 0 |
| sl820.cbl | 4 | 11 | 7 | 0 | 0 |
| sl830.cbl | 3 | 18 | 20 | 0 | 0 |

### STOCK - Stock Control

#### Programs

| Program | Divisions | Sections | Paragraphs | CALLs | COPYs |
|---------|-----------|----------|------------|-------|-------|
| acasconvert1.cbl | 4 | 4 | 3 | 0 | 0 |
| dummy-rdbmsMT.cbl | 4 | 4 | 2 | 0 | 0 |
| st000.cbl | 4 | 4 | 6 | 0 | 0 |
| st010.cbl | 4 | 41 | 80 | 0 | 0 |
| st020.cbl | 4 | 31 | 70 | 0 | 0 |
| st030.cbl | 4 | 44 | 64 | 0 | 0 |
| st040.cbl | 4 | 9 | 16 | 0 | 0 |
| st050.cbl | 4 | 9 | 15 | 0 | 0 |
| st060.cbl | 4 | 18 | 33 | 0 | 0 |
| stock.cbl | 4 | 8 | 34 | 0 | 0 |
| stockconvert2.cbl | 4 | 4 | 5 | 0 | 0 |
| stockconvert3.cbl | 4 | 4 | 5 | 0 | 0 |

### GENERAL - General Ledger

#### Programs

| Program | Divisions | Sections | Paragraphs | CALLs | COPYs |
|---------|-----------|----------|------------|-------|-------|
| dummy-rdbmsMT.cbl | 4 | 4 | 2 | 0 | 0 |
| general.cbl | 4 | 8 | 46 | 0 | 0 |
| gl000.cbl | 4 | 2 | 6 | 0 | 0 |
| gl020.cbl | 4 | 20 | 23 | 0 | 0 |
| gl030.cbl | 4 | 40 | 125 | 0 | 1 |
| gl050.cbl | 4 | 22 | 87 | 0 | 0 |
| gl051.cbl | 4 | 18 | 51 | 0 | 0 |
| gl060.cbl | 4 | 12 | 16 | 0 | 0 |
| gl070.cbl | 4 | 15 | 19 | 0 | 0 |
| gl071.cbl | 4 | 4 | 5 | 0 | 0 |
| gl072.cbl | 4 | 8 | 12 | 0 | 0 |
| gl080.cbl | 4 | 16 | 26 | 0 | 0 |
| gl090.cbl | 4 | 5 | 7 | 0 | 0 |
| gl090a.cbl | 4 | 7 | 14 | 0 | 0 |
| gl090b.cbl | 4 | 7 | 9 | 0 | 0 |
| gl100.cbl | 4 | 6 | 5 | 0 | 0 |
| gl105.cbl | 4 | 7 | 20 | 0 | 0 |
| gl120.cbl | 4 | 11 | 25 | 0 | 0 |

### COMMON - Common/Shared Modules

#### Programs

| Program | Divisions | Sections | Paragraphs | CALLs | COPYs |
|---------|-----------|----------|------------|-------|-------|
| acas-get-params.cbl | 4 | 4 | 8 | 0 | 0 |
| ACAS-Sysout.cbl | 4 | 4 | 5 | 0 | 0 |
| acas-test-takeon-1.cbl | 4 | 8 | 35 | 0 | 0 |
| acas-test-takeon-2.cbl | 4 | 8 | 34 | 0 | 0 |
| ACAS.cbl | 4 | 7 | 46 | 0 | 0 |
| acas000.cbl | 4 | 7 | 22 | 0 | 0 |
| acas004.cbl | 4 | 7 | 33 | 0 | 0 |
| acas005.cbl | 4 | 7 | 36 | 0 | 0 |
| acas006.cbl | 4 | 7 | 36 | 0 | 0 |
| acas007.cbl | 4 | 7 | 36 | 0 | 0 |
| acas008.cbl | 4 | 7 | 28 | 0 | 0 |
| acas010.cbl | 4 | 7 | 27 | 0 | 0 |
| acas011.cbl | 4 | 7 | 51 | 0 | 0 |
| acas012.cbl | 4 | 7 | 38 | 0 | 0 |
| acas013.cbl | 4 | 7 | 35 | 0 | 0 |
| acas014.cbl | 4 | 7 | 36 | 0 | 0 |
| acas015.cbl | 4 | 7 | 34 | 0 | 0 |
| acas016.cbl | 4 | 7 | 34 | 0 | 0 |
| acas017.cbl | 4 | 7 | 36 | 0 | 0 |
| acas019.cbl | 4 | 7 | 35 | 0 | 1 |
| acas022.cbl | 4 | 7 | 36 | 0 | 0 |
| acas023.cbl | 4 | 7 | 36 | 0 | 0 |
| acas026.cbl | 4 | 7 | 34 | 0 | 0 |
| acas029.cbl | 4 | 7 | 35 | 0 | 1 |
| acas030.cbl | 4 | 7 | 34 | 0 | 0 |
| acas032.cbl | 4 | 7 | 35 | 0 | 0 |
| acasconvert1.cbl | 4 | 4 | 5 | 0 | 0 |
| acasconvert2.cbl | 4 | 4 | 5 | 0 | 0 |
| acasconvert3.cbl | 4 | 4 | 5 | 0 | 0 |
| acasirsub1.cbl | 4 | 7 | 43 | 0 | 0 |
| acasirsub3.cbl | 4 | 7 | 25 | 0 | 0 |
| acasirsub4.cbl | 4 | 7 | 36 | 0 | 0 |
| acasirsub5.cbl | 4 | 7 | 26 | 0 | 0 |
| ACCEPTNM.CPY | 0 | 0 | 0 | 0 | 0 |
| analLD.cbl | 4 | 3 | 29 | 0 | 0 |
| analMT.cbl | 4 | 13 | 32 | 0 | 0 |
| analRES.cbl | 4 | 3 | 10 | 0 | 0 |
| analUNL.cbl | 4 | 3 | 9 | 0 | 0 |
| auditLD.cbl | 4 | 3 | 29 | 0 | 0 |
| auditLD2.cbl | 4 | 7 | 26 | 0 | 0 |
| auditMT.cbl | 4 | 13 | 33 | 0 | 0 |
| auditRES.cbl | 4 | 3 | 10 | 0 | 0 |
| auditUNL.cbl | 4 | 3 | 9 | 0 | 0 |
| cbl_oc_dump.cbl | 4 | 13 | 0 | 0 | 0 |
| cobdump.cbl | 4 | 3 | 3 | 0 | 0 |
| delfolioLD.cbl | 4 | 3 | 30 | 0 | 0 |
| delfolioMT.cbl | 4 | 13 | 36 | 0 | 0 |
| delfolioRES.cbl | 4 | 3 | 10 | 0 | 0 |
| delfolioUNL.cbl | 4 | 3 | 9 | 0 | 0 |
| deliveryLD.cbl | 4 | 3 | 30 | 0 | 0 |
| deliveryMT.cbl | 4 | 13 | 36 | 0 | 0 |
| deliveryRES.cbl | 4 | 3 | 10 | 0 | 0 |
| deliveryUNL.cbl | 4 | 3 | 9 | 0 | 0 |
| dfltLD.cbl | 4 | 3 | 22 | 0 | 0 |
| dfltMT.cbl | 4 | 9 | 25 | 0 | 0 |
| dummy-rdbmsMT.cbl | 4 | 4 | 2 | 0 | 0 |
| fhlogger.cbl | 4 | 5 | 5 | 0 | 0 |
| finalLD.cbl | 4 | 3 | 23 | 0 | 0 |
| finalMT.cbl | 4 | 9 | 25 | 0 | 0 |
| glbatchLD.cbl | 4 | 3 | 30 | 0 | 0 |
| glbatchMT.cbl | 4 | 13 | 36 | 0 | 0 |
| glbatchRES.cbl | 4 | 3 | 10 | 0 | 0 |
| glbatchUNL.cbl | 4 | 3 | 9 | 0 | 0 |
| glpostingLD.cbl | 4 | 3 | 30 | 0 | 0 |
| glpostingMT.cbl | 4 | 13 | 36 | 0 | 0 |
| glpostingRES.cbl | 4 | 3 | 10 | 0 | 0 |
| glpostingUNL.cbl | 4 | 3 | 9 | 0 | 0 |
| irsdfltLD.cbl | 4 | 3 | 26 | 0 | 0 |
| irsdfltMT.cbl | 4 | 9 | 25 | 0 | 0 |
| irsdfltRES.cbl | 4 | 3 | 10 | 0 | 0 |
| irsdfltUNL.cbl | 4 | 3 | 9 | 0 | 0 |
| irsfinalLD.cbl | 4 | 3 | 25 | 0 | 0 |
| irsfinalMT.cbl | 4 | 9 | 26 | 0 | 0 |
| irsfinalRES.cbl | 4 | 3 | 10 | 0 | 0 |
| irsfinalUNL.cbl | 4 | 3 | 9 | 0 | 0 |
| irsnominalLD.cbl | 4 | 3 | 31 | 0 | 0 |
| irsnominalMT.cbl | 4 | 13 | 45 | 0 | 0 |
| irsnominalRES.cbl | 4 | 3 | 10 | 0 | 0 |
| irsnominalUNL.cbl | 4 | 3 | 9 | 0 | 0 |
| irsnominalUNL2.cbl | 4 | 3 | 9 | 0 | 0 |
| irspostingLD.cbl | 4 | 3 | 31 | 0 | 0 |
| irspostingMT.cbl | 4 | 13 | 38 | 0 | 0 |
| irspostingRES.cbl | 4 | 3 | 10 | 0 | 0 |
| irspostingUNL.cbl | 4 | 3 | 9 | 0 | 0 |
| makesqltable-free.cbl | 4 | 4 | 26 | 0 | 0 |
| makesqltable-original.cbl | 4 | 4 | 20 | 0 | 0 |
| maps01.cbl | 4 | 3 | 10 | 0 | 0 |
| maps04.cbl | 4 | 3 | 3 | 0 | 0 |
| maps09.cbl | 4 | 3 | 6 | 0 | 0 |
| nominalLD.cbl | 4 | 3 | 29 | 0 | 0 |
| nominalMT.cbl | 4 | 13 | 33 | 0 | 0 |
| nominalRES.cbl | 4 | 3 | 10 | 0 | 0 |
| nominalUNL.cbl | 4 | 3 | 9 | 0 | 0 |
| otm3LD.cbl | 4 | 3 | 29 | 0 | 0 |
| otm3MT.cbl | 4 | 13 | 42 | 0 | 0 |
| otm3RES.cbl | 4 | 3 | 10 | 0 | 0 |
| otm3UNL.cbl | 4 | 3 | 9 | 0 | 0 |
| otm5LD.cbl | 4 | 3 | 29 | 0 | 0 |
| otm5MT.cbl | 4 | 13 | 42 | 0 | 0 |
| otm5RES.cbl | 4 | 3 | 10 | 0 | 0 |
| otm5UNL.cbl | 4 | 3 | 9 | 0 | 0 |
| paymentsLD.cbl | 4 | 3 | 30 | 0 | 0 |
| paymentsMT.cbl | 4 | 21 | 40 | 0 | 0 |
| paymentsRES.cbl | 4 | 3 | 10 | 0 | 0 |
| paymentsUNL.cbl | 4 | 3 | 9 | 0 | 0 |
| plautogenLD.cbl | 4 | 3 | 29 | 0 | 0 |
| plautogenMT.cbl | 4 | 21 | 44 | 0 | 0 |
| plautogenRES.cbl | 4 | 3 | 10 | 0 | 0 |
| plautogenUNL.cbl | 4 | 3 | 9 | 0 | 0 |
| plinvoiceLD.cbl | 4 | 3 | 29 | 0 | 0 |
| plinvoiceMT.cbl | 4 | 21 | 44 | 0 | 0 |
| plinvoiceRES.cbl | 4 | 3 | 10 | 0 | 0 |
| plinvoiceUNL.cbl | 4 | 3 | 9 | 0 | 0 |
| purchLD.cbl | 4 | 3 | 28 | 0 | 0 |
| purchMT.cbl | 4 | 13 | 38 | 0 | 0 |
| purchRES.cbl | 4 | 3 | 10 | 0 | 0 |
| purchUNL.cbl | 4 | 3 | 9 | 0 | 0 |
| salesLD.cbl | 4 | 3 | 28 | 0 | 0 |
| salesMT.cbl | 4 | 13 | 38 | 0 | 0 |
| salesRES.cbl | 4 | 3 | 10 | 0 | 0 |
| salesUNL.cbl | 4 | 3 | 9 | 0 | 0 |
| send-mail-test-example.cbl | 0 | 0 | 28 | 0 | 0 |
| send-some-mail.cbl | 4 | 2 | 2 | 0 | 0 |
| send-some-mail2.cbl | 4 | 2 | 2 | 0 | 0 |
| slautogenLD.cbl | 4 | 3 | 29 | 0 | 0 |
| slautogenMT.cbl | 4 | 21 | 44 | 0 | 0 |
| slautogenRES.cbl | 4 | 3 | 10 | 0 | 0 |
| slautogenUNL.cbl | 4 | 3 | 9 | 0 | 0 |
| sldelinvnosLD.cbl | 4 | 3 | 29 | 0 | 0 |
| sldelinvnosMT.cbl | 4 | 13 | 36 | 0 | 0 |
| sldelinvnosRES.cbl | 4 | 3 | 10 | 0 | 0 |
| sldelinvnosUNL.cbl | 4 | 3 | 9 | 0 | 0 |
| slinvoiceLD.cbl | 4 | 3 | 29 | 0 | 0 |
| slinvoiceMT.cbl | 4 | 21 | 44 | 0 | 0 |
| slinvoiceRES.cbl | 4 | 3 | 10 | 0 | 0 |
| slinvoiceUNL.cbl | 4 | 3 | 9 | 0 | 0 |
| slpostingLD.cbl | 4 | 3 | 29 | 0 | 0 |
| slpostingMT.cbl | 4 | 13 | 37 | 0 | 0 |
| slpostingRES.cbl | 4 | 3 | 10 | 0 | 0 |
| slpostingUNL.cbl | 4 | 3 | 9 | 0 | 0 |
| stockLD.cbl | 4 | 3 | 28 | 0 | 0 |
| stockMT.cbl | 4 | 13 | 33 | 0 | 0 |
| stockRES.cbl | 4 | 3 | 10 | 0 | 0 |
| stockUNL.cbl | 4 | 3 | 9 | 0 | 0 |
| sys002.cbl | 4 | 31 | 68 | 0 | 0 |
| sys4LD.cbl | 4 | 3 | 22 | 0 | 0 |
| sys4MT.cbl | 4 | 13 | 30 | 0 | 0 |
| systemLD.cbl | 4 | 3 | 21 | 0 | 0 |
| systemMT.cbl | 4 | 13 | 30 | 0 | 0 |
| systemRES.cbl | 4 | 3 | 6 | 0 | 0 |
| systemUNL.cbl | 4 | 3 | 6 | 0 | 0 |
| valueLD.cbl | 4 | 3 | 30 | 0 | 0 |
| valueMT.cbl | 4 | 13 | 34 | 0 | 0 |
| valueRES.cbl | 4 | 3 | 10 | 0 | 0 |
| valueUNL.cbl | 4 | 3 | 9 | 0 | 0 |
| xl150.cbl | 4 | 18 | 102 | 0 | 1 |
| xl160.cbl | 4 | 3 | 1 | 0 | 0 |
| create-system-dat.cbl | 4 | 3 | 2 | 0 | 0 |

#### Copybooks

- **statcodes2.cpy**
- **statcodes.cpy**
- **selprint-2.cpy**
- **screenio.cpy**
- **mysql-variables.cpy**
- **mysql-procedures.cpy**
- **mysql-procedures-2.cpy**
- **MySQL-SQLCA.cpy**
- **FileStat-Msgs.cpy**

## Data Access Layer

The system uses a consistent DAL pattern with specialized modules:

### Main Table Modules (MT)

Total: 34 modules

```
analMT.cbl
auditMT.cbl
delfolioMT.cbl
deliveryMT.cbl
dfltMT.cbl
dummy-rdbmsMT.cbl
dummy-rdbmsMT.cbl
dummy-rdbmsMT.cbl
dummy-rdbmsMT.cbl
dummy-rdbmsMT.cbl
dummy-rdbmsMT.cbl
finalMT.cbl
glbatchMT.cbl
glpostingMT.cbl
irsdfltMT.cbl
irsfinalMT.cbl
irsnominalMT.cbl
irspostingMT.cbl
nominalMT.cbl
otm3MT.cbl
otm5MT.cbl
paymentsMT.cbl
plautogenMT.cbl
plinvoiceMT.cbl
purchMT.cbl
salesMT.cbl
slautogenMT.cbl
sldelinvnosMT.cbl
slinvoiceMT.cbl
slpostingMT.cbl
stockMT.cbl
sys4MT.cbl
systemMT.cbl
valueMT.cbl
```

### Load Modules (LD)

Total: 28 modules

```
analLD.cbl
auditLD.cbl
delfolioLD.cbl
deliveryLD.cbl
dfltLD.cbl
finalLD.cbl
glbatchLD.cbl
glpostingLD.cbl
irsdfltLD.cbl
irsfinalLD.cbl
irsnominalLD.cbl
irspostingLD.cbl
nominalLD.cbl
otm3LD.cbl
otm5LD.cbl
paymentsLD.cbl
plautogenLD.cbl
plinvoiceLD.cbl
purchLD.cbl
salesLD.cbl
slautogenLD.cbl
sldelinvnosLD.cbl
slinvoiceLD.cbl
slpostingLD.cbl
stockLD.cbl
sys4LD.cbl
systemLD.cbl
valueLD.cbl
```

### Unload Modules (UNL)

Total: 25 modules

```
analUNL.cbl
auditUNL.cbl
delfolioUNL.cbl
deliveryUNL.cbl
glbatchUNL.cbl
glpostingUNL.cbl
irsdfltUNL.cbl
irsfinalUNL.cbl
irsnominalUNL.cbl
irspostingUNL.cbl
nominalUNL.cbl
otm3UNL.cbl
otm5UNL.cbl
paymentsUNL.cbl
plautogenUNL.cbl
plinvoiceUNL.cbl
purchUNL.cbl
salesUNL.cbl
slautogenUNL.cbl
sldelinvnosUNL.cbl
slinvoiceUNL.cbl
slpostingUNL.cbl
stockUNL.cbl
systemUNL.cbl
valueUNL.cbl
```

### Reserve Modules (RES)

Total: 25 modules

```
analRES.cbl
auditRES.cbl
delfolioRES.cbl
deliveryRES.cbl
glbatchRES.cbl
glpostingRES.cbl
irsdfltRES.cbl
irsfinalRES.cbl
irsnominalRES.cbl
irspostingRES.cbl
nominalRES.cbl
otm3RES.cbl
otm5RES.cbl
paymentsRES.cbl
plautogenRES.cbl
plinvoiceRES.cbl
purchRES.cbl
salesRES.cbl
slautogenRES.cbl
sldelinvnosRES.cbl
slinvoiceRES.cbl
slpostingRES.cbl
stockRES.cbl
systemRES.cbl
valueRES.cbl
```

## Programs Index

Complete alphabetical listing of all programs:

| Program | Path | Program ID | Size (lines) |
|---------|------|------------|-------------|
| acas-get-params.cbl | common/acas-get-params.cbl | - | 226 |
| ACAS-Sysout.cbl | common/ACAS-Sysout.cbl | - | 146 |
| acas-test-takeon-1.cbl | common/acas-test-takeon-1.cbl | - | 698 |
| acas-test-takeon-2.cbl | common/acas-test-takeon-2.cbl | - | 702 |
| ACAS.cbl | common/ACAS.cbl | - | 774 |
| acas000.cbl | common/acas000.cbl | - | 611 |
| acas004.cbl | common/acas004.cbl | - | 595 |
| acas005.cbl | common/acas005.cbl | - | 686 |
| acas006.cbl | common/acas006.cbl | - | 676 |
| acas007.cbl | common/acas007.cbl | - | 664 |
| acas008.cbl | common/acas008.cbl | - | 603 |
| acas010.cbl | common/acas010.cbl | - | 571 |
| acas011.cbl | common/acas011.cbl | - | 848 |
| acas012.cbl | common/acas012.cbl | - | 681 |
| acas013.cbl | common/acas013.cbl | - | 687 |
| acas014.cbl | common/acas014.cbl | - | 662 |
| acas015.cbl | common/acas015.cbl | - | 677 |
| acas016.cbl | common/acas016.cbl | - | 643 |
| acas017.cbl | common/acas017.cbl | - | 661 |
| acas019.cbl | common/acas019.cbl | - | 633 |
| acas022.cbl | common/acas022.cbl | - | 682 |
| acas023.cbl | common/acas023.cbl | - | 662 |
| acas026.cbl | common/acas026.cbl | - | 633 |
| acas029.cbl | common/acas029.cbl | - | 627 |
| acas030.cbl | common/acas030.cbl | - | 600 |
| acas032.cbl | common/acas032.cbl | - | 651 |
| acasconvert1.cbl | stock/acasconvert1.cbl | - | 306 |
| acasconvert1.cbl | common/acasconvert1.cbl | - | 173 |
| acasconvert2.cbl | common/acasconvert2.cbl | - | 462 |
| acasconvert3.cbl | common/acasconvert3.cbl | - | 275 |
| acasirsub1.cbl | common/acasirsub1.cbl | - | 775 |
| acasirsub3.cbl | common/acasirsub3.cbl | - | 545 |
| acasirsub4.cbl | common/acasirsub4.cbl | - | 555 |
| acasirsub5.cbl | common/acasirsub5.cbl | - | 536 |
| ACCEPTNM.CPY | common/ACCEPTNM.CPY | - | 35 |
| analLD.cbl | common/analLD.cbl | - | 513 |
| analMT.cbl | common/analMT.cbl | - | 1110 |
| analRES.cbl | common/analRES.cbl | - | 228 |
| analUNL.cbl | common/analUNL.cbl | - | 220 |
| auditLD.cbl | common/auditLD.cbl | - | 525 |
| auditLD2.cbl | common/auditLD2.cbl | - | 455 |
| auditMT.cbl | common/auditMT.cbl | - | 1409 |
| auditRES.cbl | common/auditRES.cbl | - | 229 |
| auditUNL.cbl | common/auditUNL.cbl | - | 220 |
| cbl_oc_dump.cbl | common/cbl_oc_dump.cbl | - | 250 |
| cobdump.cbl | common/cobdump.cbl | - | 135 |
| create-system-dat.cbl | create-system-dat.cbl | - | 50 |
| delfolioLD.cbl | common/delfolioLD.cbl | - | 532 |
| delfolioMT.cbl | common/delfolioMT.cbl | - | 1168 |
| delfolioRES.cbl | common/delfolioRES.cbl | - | 229 |
| delfolioUNL.cbl | common/delfolioUNL.cbl | - | 220 |
| deliveryLD.cbl | common/deliveryLD.cbl | - | 526 |
| deliveryMT.cbl | common/deliveryMT.cbl | - | 1157 |
| deliveryRES.cbl | common/deliveryRES.cbl | - | 229 |
| deliveryUNL.cbl | common/deliveryUNL.cbl | - | 220 |
| dfltLD.cbl | common/dfltLD.cbl | - | 473 |
| dfltMT.cbl | common/dfltMT.cbl | - | 896 |
| dummy-rdbmsMT.cbl | stock/dummy-rdbmsMT.cbl | - | 174 |
| dummy-rdbmsMT.cbl | sales/dummy-rdbmsMT.cbl | - | 174 |
| dummy-rdbmsMT.cbl | purchase/dummy-rdbmsMT.cbl | - | 174 |
| dummy-rdbmsMT.cbl | irs/dummy-rdbmsMT.cbl | - | 174 |
| dummy-rdbmsMT.cbl | general/dummy-rdbmsMT.cbl | - | 174 |
| dummy-rdbmsMT.cbl | common/dummy-rdbmsMT.cbl | - | 174 |
| fhlogger.cbl | common/fhlogger.cbl | - | 258 |
| finalLD.cbl | common/finalLD.cbl | - | 483 |
| finalMT.cbl | common/finalMT.cbl | - | 830 |
| general.cbl | general/general.cbl | - | 909 |
| gl000.cbl | general/gl000.cbl | - | 296 |
| gl020.cbl | general/gl020.cbl | - | 790 |
| gl030.cbl | general/gl030.cbl | - | 2582 |
| gl050.cbl | general/gl050.cbl | - | 1728 |
| gl051.cbl | general/gl051.cbl | - | 1284 |
| gl060.cbl | general/gl060.cbl | - | 532 |
| gl070.cbl | general/gl070.cbl | - | 614 |
| gl071.cbl | general/gl071.cbl | - | 184 |
| gl072.cbl | general/gl072.cbl | - | 500 |
| gl080.cbl | general/gl080.cbl | - | 752 |
| gl090.cbl | general/gl090.cbl | - | 216 |
| gl090a.cbl | general/gl090a.cbl | - | 657 |
| gl090b.cbl | general/gl090b.cbl | - | 436 |
| gl100.cbl | general/gl100.cbl | - | 272 |
| gl105.cbl | general/gl105.cbl | - | 585 |
| gl120.cbl | general/gl120.cbl | - | 813 |
| glbatchLD.cbl | common/glbatchLD.cbl | - | 524 |
| glbatchMT.cbl | common/glbatchMT.cbl | - | 1713 |
| glbatchRES.cbl | common/glbatchRES.cbl | - | 229 |
| glbatchUNL.cbl | common/glbatchUNL.cbl | - | 220 |
| glpostingLD.cbl | common/glpostingLD.cbl | - | 526 |
| glpostingMT.cbl | common/glpostingMT.cbl | - | 1495 |
| glpostingRES.cbl | common/glpostingRES.cbl | - | 229 |
| glpostingUNL.cbl | common/glpostingUNL.cbl | - | 220 |
| irs.cbl | irs/irs.cbl | - | 1040 |
| irs000.cbl | irs/irs000.cbl | - | 273 |
| irs010.cbl | irs/irs010.cbl | - | 1366 |
| irs020.cbl | irs/irs020.cbl | - | 1142 |
| irs030.cbl | irs/irs030.cbl | - | 1728 |
| irs040.cbl | irs/irs040.cbl | - | 680 |
| irs050.cbl | irs/irs050.cbl | - | 1410 |
| irs055.cbl | irs/irs055.cbl | - | 270 |
| irs060.cbl | irs/irs060.cbl | - | 1806 |
| irs065.cbl | irs/irs065.cbl | - | 257 |
| irs070.cbl | irs/irs070.cbl | - | 829 |
| irs080.cbl | irs/irs080.cbl | - | 457 |
| irs085.cbl | irs/irs085.cbl | - | 263 |
| irs090.cbl | irs/irs090.cbl | - | 541 |
| irsdfltLD.cbl | common/irsdfltLD.cbl | - | 460 |
| irsdfltMT.cbl | common/irsdfltMT.cbl | - | 916 |
| irsdfltRES.cbl | common/irsdfltRES.cbl | - | 235 |
| irsdfltUNL.cbl | common/irsdfltUNL.cbl | - | 226 |
| irsfinalLD.cbl | common/irsfinalLD.cbl | - | 451 |
| irsfinalMT.cbl | common/irsfinalMT.cbl | - | 727 |
| irsfinalRES.cbl | common/irsfinalRES.cbl | - | 235 |
| irsfinalUNL.cbl | common/irsfinalUNL.cbl | - | 226 |
| irsnominalLD.cbl | common/irsnominalLD.cbl | - | 547 |
| irsnominalMT.cbl | common/irsnominalMT.cbl | - | 1757 |
| irsnominalRES.cbl | common/irsnominalRES.cbl | - | 235 |
| irsnominalUNL.cbl | common/irsnominalUNL.cbl | - | 226 |
| irsnominalUNL2.cbl | common/irsnominalUNL2.cbl | - | 279 |
| irspostingLD.cbl | common/irspostingLD.cbl | - | 589 |
| irspostingMT.cbl | common/irspostingMT.cbl | - | 1389 |
| irspostingRES.cbl | common/irspostingRES.cbl | - | 248 |
| irspostingUNL.cbl | common/irspostingUNL.cbl | - | 239 |
| irsubp.cbl | irs/irsubp.cbl | - | 167 |
| makesqltable-free.cbl | common/makesqltable-free.cbl | - | 324 |
| makesqltable-original.cbl | common/makesqltable-original.cbl | - | 307 |
| maps01.cbl | common/maps01.cbl | - | 212 |
| maps04.cbl | common/maps04.cbl | - | 195 |
| maps09.cbl | common/maps09.cbl | - | 146 |
| nominalLD.cbl | common/nominalLD.cbl | - | 508 |
| nominalMT.cbl | common/nominalMT.cbl | - | 1375 |
| nominalRES.cbl | common/nominalRES.cbl | - | 229 |
| nominalUNL.cbl | common/nominalUNL.cbl | - | 220 |
| otm3LD.cbl | common/otm3LD.cbl | - | 502 |
| otm3MT.cbl | common/otm3MT.cbl | - | 2192 |
| otm3RES.cbl | common/otm3RES.cbl | - | 232 |
| otm3UNL.cbl | common/otm3UNL.cbl | - | 222 |
| otm5LD.cbl | common/otm5LD.cbl | - | 514 |
| otm5MT.cbl | common/otm5MT.cbl | - | 2219 |
| otm5RES.cbl | common/otm5RES.cbl | - | 232 |
| otm5UNL.cbl | common/otm5UNL.cbl | - | 222 |
| paymentsLD.cbl | common/paymentsLD.cbl | - | 516 |
| paymentsMT.cbl | common/paymentsMT.cbl | - | 2022 |
| paymentsRES.cbl | common/paymentsRES.cbl | - | 229 |
| paymentsUNL.cbl | common/paymentsUNL.cbl | - | 220 |
| pl000.cbl | purchase/pl000.cbl | - | 303 |
| pl010.cbl | purchase/pl010.cbl | - | 1625 |
| pl015.cbl | purchase/pl015.cbl | - | 1036 |
| pl020.cbl | purchase/pl020.cbl | - | 1376 |
| pl025.cbl | purchase/pl025.cbl | - | 432 |
| pl030.cbl | purchase/pl030.cbl | - | 1248 |
| pl040.cbl | purchase/pl040.cbl | - | 448 |
| pl050.cbl | purchase/pl050.cbl | - | 679 |
| pl055.cbl | purchase/pl055.cbl | - | 637 |
| pl060.cbl | purchase/pl060.cbl | - | 1151 |
| pl070.cbl | purchase/pl070.cbl | - | 936 |
| pl080.cbl | purchase/pl080.cbl | - | 846 |
| pl085.cbl | purchase/pl085.cbl | - | 690 |
| pl090.cbl | purchase/pl090.cbl | - | 282 |
| pl095.cbl | purchase/pl095.cbl | - | 614 |
| pl100.cbl | purchase/pl100.cbl | - | 799 |
| pl115.cbl | purchase/pl115.cbl | - | 239 |
| pl120.cbl | purchase/pl120.cbl | - | 1192 |
| pl130.cbl | purchase/pl130.cbl | - | 494 |
| pl140.cbl | purchase/pl140.cbl | - | 518 |
| pl160.cbl | purchase/pl160.cbl | - | 791 |
| pl165.cbl | purchase/pl165.cbl | - | 221 |
| pl170.cbl | purchase/pl170.cbl | - | 669 |
| pl180.cbl | purchase/pl180.cbl | - | 232 |
| pl190.cbl | purchase/pl190.cbl | - | 786 |
| pl800.cbl | purchase/pl800.cbl | - | 251 |
| pl900.cbl | purchase/pl900.cbl | - | 244 |
| pl910.cbl | purchase/pl910.cbl | - | 666 |
| pl920.cbl | purchase/pl920.cbl | - | 355 |
| pl930.cbl | purchase/pl930.cbl | - | 495 |
| pl940.cbl | purchase/pl940.cbl | - | 654 |
| pl950.cbl | purchase/pl950.cbl | - | 834 |
| pl960.cbl | purchase/pl960.cbl | - | 303 |
| plautogenLD.cbl | common/plautogenLD.cbl | - | 507 |
| plautogenMT.cbl | common/plautogenMT.cbl | - | 3284 |
| plautogenRES.cbl | common/plautogenRES.cbl | - | 230 |
| plautogenUNL.cbl | common/plautogenUNL.cbl | - | 220 |
| plinvoiceLD.cbl | common/plinvoiceLD.cbl | - | 515 |
| plinvoiceMT.cbl | common/plinvoiceMT.cbl | - | 3226 |
| plinvoiceRES.cbl | common/plinvoiceRES.cbl | - | 230 |
| plinvoiceUNL.cbl | common/plinvoiceUNL.cbl | - | 220 |
| purchase.cbl | purchase/purchase.cbl | - | 940 |
| purchLD.cbl | common/purchLD.cbl | - | 536 |
| purchMT.cbl | common/purchMT.cbl | - | 2084 |
| purchRES.cbl | common/purchRES.cbl | - | 229 |
| purchUNL.cbl | common/purchUNL.cbl | - | 220 |
| sales.cbl | sales/sales.cbl | - | 956 |
| salesLD.cbl | common/salesLD.cbl | - | 526 |
| salesMT.cbl | common/salesMT.cbl | - | 2269 |
| salesRES.cbl | common/salesRES.cbl | - | 235 |
| salesUNL.cbl | common/salesUNL.cbl | - | 220 |
| send-mail-test-example.cbl | common/send-mail-test-example.cbl | - | 415 |
| send-some-mail.cbl | common/send-some-mail.cbl | - | 59 |
| send-some-mail2.cbl | common/send-some-mail2.cbl | - | 62 |
| sl000.cbl | sales/sl000.cbl | - | 293 |
| sl010.cbl | sales/sl010.cbl | - | 2139 |
| sl020.cbl | sales/sl020.cbl | - | 1042 |
| sl050.cbl | sales/sl050.cbl | - | 790 |
| sl055.cbl | sales/sl055.cbl | - | 734 |
| sl060.cbl | sales/sl060.cbl | - | 1296 |
| sl070.cbl | sales/sl070.cbl | - | 927 |
| sl080.cbl | sales/sl080.cbl | - | 879 |
| sl085.cbl | sales/sl085.cbl | - | 718 |
| sl090.cbl | sales/sl090.cbl | - | 279 |
| sl095.cbl | sales/sl095.cbl | - | 620 |
| sl100.cbl | sales/sl100.cbl | - | 805 |
| sl110.cbl | sales/sl110.cbl | - | 1089 |
| sl115.cbl | sales/sl115.cbl | - | 245 |
| sl120.cbl | sales/sl120.cbl | - | 1163 |
| sl130.cbl | sales/sl130.cbl | - | 495 |
| sl140.cbl | sales/sl140.cbl | - | 539 |
| sl160.cbl | sales/sl160.cbl | - | 916 |
| sl165.cbl | sales/sl165.cbl | - | 219 |
| sl170.cbl | sales/sl170.cbl | - | 863 |
| sl180.cbl | sales/sl180.cbl | - | 677 |
| sl190.cbl | sales/sl190.cbl | - | 909 |
| sl200.cbl | sales/sl200.cbl | - | 351 |
| sl800.cbl | sales/sl800.cbl | - | 232 |
| sl810.cbl | sales/sl810.cbl | - | 1974 |
| sl810.cbl | purchase/sl810.cbl | - | 1979 |
| sl820.cbl | sales/sl820.cbl | - | 734 |
| sl820.cbl | purchase/sl820.cbl | - | 740 |
| sl830.cbl | sales/sl830.cbl | - | 839 |
| sl830.cbl | purchase/sl830.cbl | - | 845 |
| sl900.cbl | sales/sl900.cbl | - | 486 |
| sl910.cbl | sales/sl910.cbl | - | 3374 |
| sl920.cbl | sales/sl920.cbl | - | 2454 |
| sl930.cbl | sales/sl930.cbl | - | 1492 |
| sl940.cbl | sales/sl940.cbl | - | 760 |
| sl950.cbl | sales/sl950.cbl | - | 1075 |
| sl960.cbl | sales/sl960.cbl | - | 560 |
| sl970.cbl | sales/sl970.cbl | - | 1105 |
| slautogenLD.cbl | common/slautogenLD.cbl | - | 507 |
| slautogenMT.cbl | common/slautogenMT.cbl | - | 3297 |
| slautogenRES.cbl | common/slautogenRES.cbl | - | 231 |
| slautogenUNL.cbl | common/slautogenUNL.cbl | - | 221 |
| sldelinvnosLD.cbl | common/sldelinvnosLD.cbl | - | 504 |
| sldelinvnosMT.cbl | common/sldelinvnosMT.cbl | - | 1173 |
| sldelinvnosRES.cbl | common/sldelinvnosRES.cbl | - | 230 |
| sldelinvnosUNL.cbl | common/sldelinvnosUNL.cbl | - | 220 |
| slinvoiceLD.cbl | common/slinvoiceLD.cbl | - | 514 |
| slinvoiceMT.cbl | common/slinvoiceMT.cbl | - | 3259 |
| slinvoiceRES.cbl | common/slinvoiceRES.cbl | - | 229 |
| slinvoiceUNL.cbl | common/slinvoiceUNL.cbl | - | 220 |
| slpostingLD.cbl | common/slpostingLD.cbl | - | 485 |
| slpostingMT.cbl | common/slpostingMT.cbl | - | 1337 |
| slpostingRES.cbl | common/slpostingRES.cbl | - | 229 |
| slpostingUNL.cbl | common/slpostingUNL.cbl | - | 220 |
| st000.cbl | stock/st000.cbl | - | 285 |
| st010.cbl | stock/st010.cbl | - | 2266 |
| st020.cbl | stock/st020.cbl | - | 2340 |
| st030.cbl | stock/st030.cbl | - | 2368 |
| st040.cbl | stock/st040.cbl | - | 484 |
| st050.cbl | stock/st050.cbl | - | 534 |
| st060.cbl | stock/st060.cbl | - | 859 |
| stock.cbl | stock/stock.cbl | - | 731 |
| stockconvert2.cbl | stock/stockconvert2.cbl | - | 252 |
| stockconvert3.cbl | stock/stockconvert3.cbl | - | 254 |
| stockLD.cbl | common/stockLD.cbl | - | 522 |
| stockMT.cbl | common/stockMT.cbl | - | 3380 |
| stockRES.cbl | common/stockRES.cbl | - | 235 |
| stockUNL.cbl | common/stockUNL.cbl | - | 220 |
| sys002.cbl | common/sys002.cbl | - | 3105 |
| sys4LD.cbl | common/sys4LD.cbl | - | 505 |
| sys4MT.cbl | common/sys4MT.cbl | - | 1589 |
| systemLD.cbl | common/systemLD.cbl | - | 480 |
| systemMT.cbl | common/systemMT.cbl | - | 5258 |
| systemRES.cbl | common/systemRES.cbl | - | 314 |
| systemUNL.cbl | common/systemUNL.cbl | - | 337 |
| valueLD.cbl | common/valueLD.cbl | - | 515 |
| valueMT.cbl | common/valueMT.cbl | - | 1412 |
| valueRES.cbl | common/valueRES.cbl | - | 230 |
| valueUNL.cbl | common/valueUNL.cbl | - | 219 |
| xl150.cbl | common/xl150.cbl | - | 2256 |
| xl160.cbl | common/xl160.cbl | - | 237 |

## Copybooks Index

Complete listing of all copybooks:

| Copybook | Path | Size (lines) |
|----------|------|-------------|
| FileStat-Msgs.cpy | copybooks/FileStat-Msgs.cpy | 60 |
| mysql-procedures-2.cpy | copybooks/mysql-procedures-2.cpy | 274 |
| mysql-procedures.cpy | copybooks/mysql-procedures.cpy | 269 |
| MySQL-SQLCA.cpy | copybooks/MySQL-SQLCA.cpy | 39 |
| mysql-variables.cpy | copybooks/mysql-variables.cpy | 110 |
| screenio.cpy | copybooks/screenio.cpy | 199 |
| selprint-2.cpy | copybooks/selprint-2.cpy | 12 |
| statcodes.cpy | copybooks/statcodes.cpy | 36 |
| statcodes2.cpy | copybooks/statcodes2.cpy | 36 |

## Dependencies

### Call Dependencies

No CALL dependencies found.

### Copy Dependencies

Found 6 programs with COPY statements:

**acas019.cbl** copies:
  - WS

**acas029.cbl** copies:
  - WS

**gl030.cbl** copies:
  - OF

**irs010.cbl** copies:
  - OF

**sl110.cbl** copies:
  - OF

**xl150.cbl** copies:
  - TO

## Visualizations

- [Call Graph](../visualizations/call-graph.html) - Interactive network graph of program dependencies
- [Flowcharts](../visualizations/flowcharts/index.html) - Procedure flow diagrams for programs
- [Dashboard](../dashboard/index.html) - Interactive metrics dashboard
