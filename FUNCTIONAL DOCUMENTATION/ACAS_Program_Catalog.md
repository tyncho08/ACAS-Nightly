# ACAS Program Catalog

## Overview
This catalog provides an alphabetical listing of all programs in the ACAS system, their business function mapping, dependencies, and maintenance priority.

## Program Naming Conventions
- **ACAS**: Main system menu
- **xx000**: Start of day programs (xx = module prefix)
- **xx0nn**: Module-specific programs
- **xxnnn**: Module transaction and reporting programs
- **acas0nn**: System-wide file handlers
- **maps0n**: Utility programs
- **sys002**: System parameter handler
- **xl150**: End of cycle program
- **\*MT**: Data Access Layer modules (MySQL/Table handlers)
- **\*LD**: Load modules (file to database)
- **\*UNL**: Unload modules (database to file)
- **\*RES**: Restore modules

## Module Prefixes
- **IR/irs**: Incomplete Records System
- **SL/sl**: Sales Ledger
- **PL/pl**: Purchase Ledger
- **ST/st**: Stock Control
- **GL/gl**: General Ledger

---

## System-Wide Programs

| Program | Description | Business Function | Dependencies | Priority |
|---------|-------------|-------------------|--------------|----------|
| ACAS | Main system menu | System navigation and control | All modules | HIGH |
| sys002 | System parameter maintenance | Configuration management | systemMT | HIGH |
| xl150 | End of cycle processing | Period/year end for all modules | All ledgers | HIGH |
| maps01 | Encryption/decryption (removed) | Security (obsolete) | None | LOW |
| maps04 | Date conversion utilities | Date validation and formatting | None | HIGH |
| maps09 | Check digit verification | Data validation | None | MEDIUM |

## File Handlers (acas0nn series)

| Program | Description | File/Table | Business Function | Priority |
|---------|-------------|------------|-------------------|----------|
| acas000 | System/defaults/finals handler | system.dat | System configuration | HIGH |
| acas004 | Nominal ledger handler | Nominal/GLLEDGER | GL accounts | HIGH |
| acas005 | Sales ledger handler | Sales/SALEDGER | Customer accounts | HIGH |
| acas006 | Purchase ledger handler | Purchase/PULEDGER | Supplier accounts | HIGH |
| acas007 | Stock file handler | Stock/STOCK | Inventory | HIGH |
| acas008 | SL posting handler | SLPosting/SLPOSTING | AR postings | HIGH |
| acas010 | PL posting handler | PLPosting/PLPOSTING | AP postings | HIGH |
| acas011 | GL posting handler | GLPosting/GLPOSTING | GL entries | HIGH |
| acas012 | Analysis file handler | Analysis/ANALYSIS | Analysis codes | MEDIUM |
| acas013 | Audit file handler | Audit/AUDIT | Stock movements | MEDIUM |
| acas014 | Invoice handler | Invoice/SAINVOICE | Sales invoices | HIGH |
| acas015 | OTM3 handler | OTM3/SAITM3 | Sales open items | HIGH |
| acas016 | OTM5 handler | OTM5/PUITM5 | Purchase open items | HIGH |
| acas017 | Payments handler | Payments/PAYMENTS | Payment records | HIGH |
| acas019 | SL invoice lines handler | InvLines/SAINV-LINES | Invoice details | HIGH |
| acas022 | Delivery handler | Delivery/DELIVERY | Delivery addresses | MEDIUM |
| acas023 | Value file handler | Value/VALUE | Period values | MEDIUM |
| acas026 | GL batch handler | GLBatch/GLBATCH | Batch control | HIGH |
| acas029 | Deleted invoice handler | DelInvNos/SADELINV | Deleted numbers | LOW |
| acas030 | SL autogen handler | SLAutogen/SAAUTOGEN | Recurring invoices | MEDIUM |
| acas032 | PL autogen handler | PLAutogen/PUAUTOGEN | Recurring orders | MEDIUM |

## IRS (Incomplete Records System)

| Program | Description | Business Function | Dependencies | Priority |
|---------|-------------|-------------------|--------------|----------|
| irs | IRS main menu | Module navigation | irs000-090 | HIGH |
| irs000 | Start of day | Date initialization | maps04 | HIGH |
| irs010 | Chart of Accounts utilities | Account setup/maintenance | irsnominalMT | HIGH |
| irs020 | Posting defaults maintenance | Default accounts, VAT setup | irsdfltMT, irsfinalMT | HIGH |
| irs030 | Transaction posting | Journal entries | irspostingMT | HIGH |
| irs040 | Trial balance | Financial reporting | irsnominalMT | HIGH |
| irs050 | Profit & Loss | P&L statement | irsnominalMT | HIGH |
| irs055 | P&L by quarter (sort) | Quarterly P&L | irs050 | MEDIUM |
| irs060 | Balance Sheet | Financial position | irsnominalMT | HIGH |
| irs065 | Balance Sheet by quarter | Quarterly BS | irs060 | MEDIUM |
| irs070 | Nominal listing | Account reports | irsnominalMT | MEDIUM |
| irs080 | Transaction report | Posting details | irspostingMT | MEDIUM |
| irs085 | Transaction report (sort) | Sorted postings | irs080 | LOW |
| irs090 | End of period | Period closing | All IRS files | HIGH |
| irsubp | IRS subroutines | Common functions | None | MEDIUM |

## Sales Ledger (Accounts Receivable)

| Program | Description | Business Function | Dependencies | Priority |
|---------|-------------|-------------------|--------------|----------|
| sales | Sales Ledger menu | Module navigation | sl000-970 | HIGH |
| sl000 | Start of day | Date initialization | maps04 | HIGH |
| sl010 | Customer maintenance | Customer setup | salesMT | HIGH |
| sl020 | Ledger enquiry | Account inquiry | salesMT, slinvoiceMT | HIGH |
| sl050 | Unapplied items report | Unposted transactions | slinvoiceMT | MEDIUM |
| sl055 | Invoice proof & analysis | Pre-posting validation | slinvoiceMT | HIGH |
| sl060 | Invoice posting | Post to ledger | slpostingMT | HIGH |
| sl070 | Product analysis maintenance | Analysis codes | analMT | MEDIUM |
| sl080 | Payment entry | Customer payments | paymentsMT | HIGH |
| sl085 | Payment proof | Payment validation | paymentsMT | HIGH |
| sl090 | Remittance advice | Payment notices | paymentsMT | MEDIUM |
| sl095 | Payments analysis | Payment breakdown | paymentsMT | MEDIUM |
| sl100 | Cash posting | Post payments | slpostingMT | HIGH |
| sl110 | Statement production | Customer statements | salesMT | HIGH |
| sl115 | Statement sort | Sort for printing | sl110 | LOW |
| sl120 | Aged debtors | Aging analysis | salesMT | HIGH |
| sl130 | Product analysis report | Sales analysis | analMT | MEDIUM |
| sl140 | Invoice day book | Invoice register | slinvoiceMT | MEDIUM |
| sl160 | Alpha customer list | Customer directory | salesMT | LOW |
| sl165 | Alpha sort | Sorting routine | sl160 | LOW |
| sl170 | Customer dump | Detailed listing | salesMT | LOW |
| sl180 | Customer turnover | Revenue analysis | salesMT | MEDIUM |
| sl190 | Dunning letters | Collection letters | salesMT | MEDIUM |
| sl200 | Invoice deletion report | Deleted invoices | sldelinvnosMT | LOW |
| sl800 | Standing orders setup | Recurring setup | slautogenMT | MEDIUM |
| sl810 | Create standing orders | Generate recurring | slautogenMT | MEDIUM |
| sl900 | Invoice entry (batch) | Batch invoicing | slinvoiceMT | HIGH |
| sl910 | Invoice entry (immediate) | Direct invoicing | slinvoiceMT | HIGH |
| sl920 | Invoice amendment | Modify invoices | slinvoiceMT | HIGH |
| sl930 | Invoice reprint | Reprint invoices | slinvoiceMT | MEDIUM |
| sl940 | Proforma invoice | Quote generation | slinvoiceMT | MEDIUM |
| sl950 | Invoice deletion | Remove invoices | sldelinvnosMT | MEDIUM |
| sl960 | Dispatch notes | Shipping documents | slinvoiceMT | MEDIUM |
| sl970 | Manifest printing | Delivery lists | deliveryMT | LOW |

## Purchase Ledger (Accounts Payable)

| Program | Description | Business Function | Dependencies | Priority |
|---------|-------------|-------------------|--------------|----------|
| purchase | Purchase Ledger menu | Module navigation | pl000-960 | HIGH |
| pl000 | Start of day | Date initialization | maps04 | HIGH |
| pl010 | Supplier maintenance | Supplier setup | purchMT | HIGH |
| pl015 | Supplier notes | Additional info | deliveryMT | LOW |
| pl020 | Purchase order entry | Order creation | plinvoiceMT | HIGH |
| pl025 | Goods receipt | Receive inventory | plinvoiceMT | HIGH |
| pl030 | Order amendment | Modify orders | plinvoiceMT | HIGH |
| pl040 | Invoice deletion | Remove invoices | delfolioMT | MEDIUM |
| pl050 | Proof report | Pre-posting check | plinvoiceMT | HIGH |
| pl055 | Order analysis | Purchase analysis | analMT | MEDIUM |
| pl060 | Invoice posting | Post to ledger | plpostingMT | HIGH |
| pl070 | Product analysis maintenance | Analysis codes | analMT | MEDIUM |
| pl080 | Payment selection | Choose payments | paymentsMT | HIGH |
| pl085 | Payment amendment | Modify payments | paymentsMT | HIGH |
| pl090 | Remittance advice | Payment notices | paymentsMT | MEDIUM |
| pl095 | Cheque printing | Print checks | paymentsMT | MEDIUM |
| pl100 | Payment posting | Post payments | plpostingMT | HIGH |
| pl115 | Payments analysis | Payment breakdown | paymentsMT | MEDIUM |
| pl120 | Aged creditors | Aging analysis | purchMT | HIGH |
| pl130 | Product analysis report | Purchase analysis | analMT | MEDIUM |
| pl140 | Invoice day book | Invoice register | plinvoiceMT | MEDIUM |
| pl160 | Alpha supplier list | Supplier directory | purchMT | LOW |
| pl165 | Ledger enquiry | Account inquiry | purchMT | HIGH |
| pl170 | Supplier dump | Detailed listing | purchMT | LOW |
| pl180 | Supplier turnover | Purchase analysis | purchMT | MEDIUM |
| pl190 | Supplier labels | Mailing labels | purchMT | LOW |
| pl800 | Standing orders setup | Recurring setup | plautogenMT | MEDIUM |
| pl900 | Purchase order (batch) | Batch orders | plinvoiceMT | HIGH |
| pl910 | Purchase order (immediate) | Direct orders | plinvoiceMT | HIGH |
| pl920 | Credit note entry | Returns/credits | plinvoiceMT | HIGH |
| pl930 | Order confirmation | Print orders | plinvoiceMT | MEDIUM |
| pl940 | Requisition entry | Purchase requests | plinvoiceMT | MEDIUM |
| pl950 | Order cancellation | Cancel orders | delfolioMT | MEDIUM |
| pl960 | Goods receipt notes | Receiving docs | plinvoiceMT | MEDIUM |

## Stock Control (Inventory Management)

| Program | Description | Business Function | Dependencies | Priority |
|---------|-------------|-------------------|--------------|----------|
| stock | Stock Control menu | Module navigation | st000-060 | HIGH |
| st000 | Start of day | Date initialization | maps04 | HIGH |
| st010 | Stock item maintenance | Item setup | stockMT | HIGH |
| st020 | Stock movements | Receipts/issues | stockMT, auditMT | HIGH |
| st030 | Stock reports | Various reports | stockMT | HIGH |
| st040 | End of cycle | Period closing | stockMT | HIGH |
| st050 | Stock conversion | File conversion | stockMT | LOW |
| st060 | Audit trail report | Movement history | auditMT | MEDIUM |
| stockconvert2 | Conversion utility | Data migration | stockMT | LOW |
| stockconvert3 | Conversion utility | Data migration | stockMT | LOW |

## General Ledger (Full Accounting)

| Program | Description | Business Function | Dependencies | Priority |
|---------|-------------|-------------------|--------------|----------|
| general | General Ledger menu | Module navigation | gl000-190 | HIGH |
| gl000 | Start of day | Date initialization | maps04 | HIGH |
| gl020 | Default accounts | Default setup | nominalMT | HIGH |
| gl030 | Chart of Accounts | Account setup | nominalMT | HIGH |
| gl050 | Transaction entry | Journal entries | glbatchMT, glpostingMT | HIGH |
| gl051 | Transaction proof/modify | Edit batches | glbatchMT | HIGH |
| gl060 | Batch status | Batch reports | glbatchMT | MEDIUM |
| gl070 | Transaction posting (phase 1) | Pre-posting | glpostingMT | HIGH |
| gl071 | Batch checking | Validation | glbatchMT | HIGH |
| gl072 | Final posting (phase 2) | Complete posting | glpostingMT | HIGH |
| gl080 | End of cycle | Period closing | All GL files | HIGH |
| gl090 | Trial balance | Account balances | nominalMT | HIGH |
| gl090a | Trial balance (variant) | Alt format | nominalMT | MEDIUM |
| gl090b | Trial balance (variant) | Alt format | nominalMT | MEDIUM |
| gl100 | Profit & Loss | Income statement | nominalMT | HIGH |
| gl105 | Balance Sheet | Financial position | nominalMT | HIGH |
| gl120 | Transaction report | Posting details | glpostingMT | MEDIUM |
| **gl040** | **Final accounts setup** | **MISSING** | - | **HIGH** |
| **gl130** | **Print final accounts** | **MISSING** | - | **HIGH** |
| **gl190** | **File garbage collector** | **MISSING** | - | **MEDIUM** |

## Data Access Layer (DAL) Modules

| Module | Table/File | Business Function | Priority |
|--------|------------|-------------------|----------|
| analMT | ANALYSIS-REC | Product/service analysis codes | MEDIUM |
| auditMT | AUDIT-REC | Stock movement audit trail | MEDIUM |
| delfolioMT | DELFOLIO-REC | Deleted transaction tracking | LOW |
| deliveryMT | DELIVERY-REC | Delivery addresses | MEDIUM |
| dfltMT | DFLT-REC | Default accounts (IRS) | HIGH |
| finalMT | FINAL-REC | Final accounts (IRS) | HIGH |
| glbatchMT | GLBATCH-REC | GL batch control | HIGH |
| glpostingMT | GLPOSTING-REC | GL transaction postings | HIGH |
| irsdfltMT | IRSDFLT-REC | IRS default accounts | HIGH |
| irsfinalMT | IRSFINAL-REC | IRS final accounts | HIGH |
| irsnominalMT | IRSNL-REC | IRS nominal ledger | HIGH |
| irspostingMT | IRSPOSTING-REC | IRS postings | HIGH |
| nominalMT | NOMINAL-REC | GL nominal ledger | HIGH |
| otm3MT | SAITM3-REC | Sales open items | HIGH |
| otm5MT | PUITM5-REC | Purchase open items | HIGH |
| paymentsMT | PAYMENTS-REC | Payment records | HIGH |
| plautogenMT | PUAUTOGEN-REC | Purchase standing orders | MEDIUM |
| plinvoiceMT | PUINVOICE-REC | Purchase invoices | HIGH |
| purchMT | PULEDGER-REC | Purchase ledger master | HIGH |
| salesMT | SALEDGER-REC | Sales ledger master | HIGH |
| slautogenMT | SAAUTOGEN-REC | Sales standing orders | MEDIUM |
| sldelinvnosMT | SADELINV-REC | Deleted invoice numbers | LOW |
| slinvoiceMT | SAINVOICE-REC | Sales invoices | HIGH |
| slpostingMT | SLPOSTING-REC | Sales postings | HIGH |
| stockMT | STOCK-REC | Stock master file | HIGH |
| sys4MT | SYS4-REC | System file 4 | MEDIUM |
| systemMT | SYSTEM-REC | System parameters | HIGH |
| valueMT | VALUE-REC | Period values | MEDIUM |

## Load/Unload/Restore Modules

| Module | Function | Business Purpose | Priority |
|--------|----------|------------------|----------|
| *LD modules | Load COBOL file to database | Data migration | MEDIUM |
| *UNL modules | Unload database to file | Backup/migration | MEDIUM |
| *RES modules | Restore from backup | Recovery | HIGH |

## Supporting Programs

| Program | Description | Business Function | Priority |
|---------|-------------|-------------------|----------|
| fhlogger | File access logger | Debugging/audit | LOW |
| cobdump | COBOL dump utility | Error diagnostics | LOW |
| cbl_oc_dump | OpenCOBOL dump | Error diagnostics | LOW |
| send-some-mail | Email utility | Notifications | LOW |
| makesqltable-* | SQL table creation | Database setup | MEDIUM |
| acasconvert* | Data conversion | Migration tools | LOW |
| dummy-rdbmsMT | RDBMS stub | Non-DB operation | LOW |

## Maintenance Priority Guide

### HIGH Priority
- Core transaction processing programs
- Master file maintenance
- Posting and period-end programs
- Financial reporting
- System configuration
- Missing GL programs (gl040, gl130)

### MEDIUM Priority
- Analysis and reporting programs
- Standing order/recurring transactions
- Audit trails
- Data migration tools
- Supporting utilities

### LOW Priority
- Label printing
- Alphabetical listings
- Conversion utilities
- Diagnostic tools
- Obsolete programs

## Program Dependencies Matrix

### Common Dependencies
- All programs depend on: System parameters (sys002)
- All date operations use: maps04
- All file operations use: Appropriate acas0nn handler
- All database operations use: Corresponding *MT module

### Module Cross-Dependencies
- Sales → Stock (for inventory updates)
- Purchase → Stock (for receipts)
- Sales → GL/IRS (for postings)
- Purchase → GL/IRS (for postings)
- Stock → GL/IRS (for adjustments)
- All → System parameters

### Critical Path Programs
These programs must function for basic operations:
1. System initialization: ACAS, sys002, *000 programs
2. Master file setup: *010 programs
3. Transaction entry: sl910, pl020, irs030, gl050
4. Posting: sl060, pl060, gl070/072
5. Period end: xl150, *090 programs, st040, gl080