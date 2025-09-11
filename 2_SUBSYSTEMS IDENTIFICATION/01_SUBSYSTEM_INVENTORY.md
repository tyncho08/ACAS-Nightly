# ACAS Subsystem Inventory

## Overview
This document provides a complete inventory of all identified subsystems within ACAS, mapping programs to their respective subsystems and documenting their business purpose and criticality.

## Subsystem Summary

| ID | Subsystem Code | Subsystem Name | Type | Programs | Criticality |
|----|----------------|----------------|------|----------|-------------|
| 1 | GL_CORE | General Ledger Core | Core Business | 17 | HIGH |
| 2 | IRS_CORE | IRS Ledger Core | Core Business | 15 | HIGH |
| 3 | SL_MGMT | Sales Ledger Management | Core Business | 36 | HIGH |
| 4 | PL_MGMT | Purchase Ledger Management | Core Business | 31 | HIGH |
| 5 | ST_CTRL | Stock Control System | Core Business | 10 | HIGH |
| 6 | BATCH_FW | Batch Processing Framework | Supporting | 8 | HIGH |
| 7 | RPT_ENGINE | Report Generation Engine | Supporting | 25 | MEDIUM |
| 8 | SYS_ADMIN | System Administration | Supporting | 5 | HIGH |
| 9 | PERIOD_PROC | Period Processing | Supporting | 3 | HIGH |
| 10 | DAL | Data Access Layer | Infrastructure | 50+ | CRITICAL |
| 11 | COMMON_UTIL | Common Utilities | Infrastructure | 10 | HIGH |
| 12 | INTEG_SVC | Integration Services | Infrastructure | 5 | HIGH |

---

## Detailed Subsystem Inventory

### 1. GL_CORE - General Ledger Core

**Purpose**: Full double-entry bookkeeping with multi-profit center support

**Business Functions**:
- Chart of accounts maintenance
- Journal entry processing
- Financial statement generation
- Multi-branch/profit center accounting
- Period-end closing

**Programs**:
| Program | Description | Type | Priority |
|---------|-------------|------|----------|
| general | GL main menu | Menu | HIGH |
| gl000 | Start of day initialization | Utility | HIGH |
| gl020 | Default accounts setup | Setup | HIGH |
| gl030 | Chart of Accounts maintenance | Master | HIGH |
| gl050 | Transaction entry | Transaction | HIGH |
| gl051 | Transaction proof/modify | Transaction | HIGH |
| gl060 | Batch status reports | Report | MEDIUM |
| gl070 | Transaction posting phase 1 | Posting | HIGH |
| gl071 | Batch checking | Validation | HIGH |
| gl072 | Final posting phase 2 | Posting | HIGH |
| gl080 | End of cycle processing | Period-End | HIGH |
| gl090 | Trial balance | Report | HIGH |
| gl090a | Trial balance variant A | Report | MEDIUM |
| gl090b | Trial balance variant B | Report | MEDIUM |
| gl100 | Profit & Loss statement | Report | HIGH |
| gl105 | Balance Sheet | Report | HIGH |
| gl120 | Transaction report | Report | MEDIUM |

**Missing Programs** (identified in documentation):
- gl040 - Final accounts setup
- gl130 - Print final accounts
- gl190 - File garbage collector

**Data Ownership**:
- GLLEDGER (Nominal ledger accounts)
- GLPOSTING (Transaction details)
- GLBATCH (Batch control)

---

### 2. IRS_CORE - IRS Ledger Core

**Purpose**: Simplified accounting system for businesses with incomplete records

**Business Functions**:
- Simplified chart of accounts
- Single-entry bookkeeping option
- Basic financial reporting
- VAT tracking
- Small business compliance

**Programs**:
| Program | Description | Type | Priority |
|---------|-------------|------|----------|
| irs | IRS main menu | Menu | HIGH |
| irs000 | Start of day | Utility | HIGH |
| irs010 | Chart of Accounts utilities | Master | HIGH |
| irs020 | Posting defaults maintenance | Setup | HIGH |
| irs030 | Transaction posting | Transaction | HIGH |
| irs040 | Trial balance | Report | HIGH |
| irs050 | Profit & Loss | Report | HIGH |
| irs055 | P&L by quarter (sort) | Report | MEDIUM |
| irs060 | Balance Sheet | Report | HIGH |
| irs065 | Balance Sheet by quarter | Report | MEDIUM |
| irs070 | Nominal listing | Report | MEDIUM |
| irs080 | Transaction report | Report | MEDIUM |
| irs085 | Transaction report (sorted) | Report | LOW |
| irs090 | End of period | Period-End | HIGH |
| irsubp | IRS subroutines | Utility | MEDIUM |

**Data Ownership**:
- IRSNL (IRS nominal ledger)
- IRSPOSTING (IRS postings)
- IRSDFLT (IRS defaults)
- IRSFINAL (IRS final accounts)

---

### 3. SL_MGMT - Sales Ledger Management

**Purpose**: Complete accounts receivable and customer relationship management

**Business Functions**:
- Customer master maintenance
- Invoice generation and printing
- Payment processing and allocation
- Credit control and dunning
- Customer statements
- Sales analysis

**Programs**:
| Program | Description | Type | Priority |
|---------|-------------|------|----------|
| sales | Sales Ledger menu | Menu | HIGH |
| sl000 | Start of day | Utility | HIGH |
| sl010 | Customer maintenance | Master | HIGH |
| sl020 | Ledger enquiry | Inquiry | HIGH |
| sl050 | Unapplied items report | Report | MEDIUM |
| sl055 | Invoice proof & analysis | Validation | HIGH |
| sl060 | Invoice posting | Posting | HIGH |
| sl070 | Product analysis maintenance | Setup | MEDIUM |
| sl080 | Payment entry | Transaction | HIGH |
| sl085 | Payment proof | Validation | HIGH |
| sl090 | Remittance advice | Document | MEDIUM |
| sl095 | Payments analysis | Report | MEDIUM |
| sl100 | Cash posting | Posting | HIGH |
| sl110 | Statement production | Document | HIGH |
| sl115 | Statement sort | Utility | LOW |
| sl120 | Aged debtors | Report | HIGH |
| sl130 | Product analysis report | Report | MEDIUM |
| sl140 | Invoice day book | Report | MEDIUM |
| sl160 | Alpha customer list | Report | LOW |
| sl165 | Alpha sort | Utility | LOW |
| sl170 | Customer dump | Report | LOW |
| sl180 | Customer turnover | Report | MEDIUM |
| sl190 | Dunning letters | Document | MEDIUM |
| sl200 | Invoice deletion report | Report | LOW |
| sl800 | Standing orders setup | Setup | MEDIUM |
| sl810 | Create standing orders | Transaction | MEDIUM |
| sl900 | Invoice entry (batch) | Transaction | HIGH |
| sl910 | Invoice entry (immediate) | Transaction | HIGH |
| sl920 | Invoice amendment | Transaction | HIGH |
| sl930 | Invoice reprint | Document | MEDIUM |
| sl940 | Proforma invoice | Document | MEDIUM |
| sl950 | Invoice deletion | Transaction | MEDIUM |
| sl960 | Dispatch notes | Document | MEDIUM |
| sl970 | Manifest printing | Document | LOW |

**Data Ownership**:
- SALEDGER (Customer master)
- SAINVOICE (Invoice headers)
- SAINV-LINES (Invoice details)
- SAITM3 (Open items)
- SLPOSTING (Sales postings)
- PAYMENTS (Payment records)
- SAAUTOGEN (Standing orders)
- SADELINV (Deleted invoices)

---

### 4. PL_MGMT - Purchase Ledger Management

**Purpose**: Complete accounts payable and supplier management

**Business Functions**:
- Supplier master maintenance
- Purchase order processing
- Goods receipt processing
- Invoice matching
- Payment selection and processing
- Supplier analysis

**Programs**:
| Program | Description | Type | Priority |
|---------|-------------|------|----------|
| purchase | Purchase Ledger menu | Menu | HIGH |
| pl000 | Start of day | Utility | HIGH |
| pl010 | Supplier maintenance | Master | HIGH |
| pl015 | Supplier notes | Master | LOW |
| pl020 | Purchase order entry | Transaction | HIGH |
| pl025 | Goods receipt | Transaction | HIGH |
| pl030 | Order amendment | Transaction | HIGH |
| pl040 | Invoice deletion | Transaction | MEDIUM |
| pl050 | Proof report | Validation | HIGH |
| pl055 | Order analysis | Report | MEDIUM |
| pl060 | Invoice posting | Posting | HIGH |
| pl070 | Product analysis maintenance | Setup | MEDIUM |
| pl080 | Payment selection | Transaction | HIGH |
| pl085 | Payment amendment | Transaction | HIGH |
| pl090 | Remittance advice | Document | MEDIUM |
| pl095 | Cheque printing | Document | MEDIUM |
| pl100 | Payment posting | Posting | HIGH |
| pl115 | Payments analysis | Report | MEDIUM |
| pl120 | Aged creditors | Report | HIGH |
| pl130 | Product analysis report | Report | MEDIUM |
| pl140 | Invoice day book | Report | MEDIUM |
| pl160 | Alpha supplier list | Report | LOW |
| pl165 | Ledger enquiry | Inquiry | HIGH |
| pl170 | Supplier dump | Report | LOW |
| pl180 | Supplier turnover | Report | MEDIUM |
| pl190 | Supplier labels | Document | LOW |
| pl800 | Standing orders setup | Setup | MEDIUM |
| pl900 | Purchase order (batch) | Transaction | HIGH |
| pl910 | Purchase order (immediate) | Transaction | HIGH |
| pl920 | Credit note entry | Transaction | HIGH |
| pl930 | Order confirmation | Document | MEDIUM |
| pl940 | Requisition entry | Transaction | MEDIUM |
| pl950 | Order cancellation | Transaction | MEDIUM |
| pl960 | Goods receipt notes | Document | MEDIUM |

**Data Ownership**:
- PULEDGER (Supplier master)
- PUINVOICE (Purchase orders/invoices)
- PUITM5 (Open items)
- PLPOSTING (Purchase postings)
- PUAUTOGEN (Standing orders)
- DELFOLIO (Deleted documents)

---

### 5. ST_CTRL - Stock Control System

**Purpose**: Inventory management, valuation, and control

**Business Functions**:
- Stock item maintenance
- Stock movement recording
- Valuation (average cost)
- Reorder management
- Stock take support
- Audit trail

**Programs**:
| Program | Description | Type | Priority |
|---------|-------------|------|----------|
| stock | Stock Control menu | Menu | HIGH |
| st000 | Start of day | Utility | HIGH |
| st010 | Stock item maintenance | Master | HIGH |
| st020 | Stock movements | Transaction | HIGH |
| st030 | Stock reports | Report | HIGH |
| st040 | End of cycle | Period-End | HIGH |
| st050 | Stock conversion | Utility | LOW |
| st060 | Audit trail report | Report | MEDIUM |
| stockconvert2 | Conversion utility | Utility | LOW |
| stockconvert3 | Conversion utility | Utility | LOW |

**Data Ownership**:
- STOCK (Stock master file)
- AUDIT (Movement history)

---

### 6. BATCH_FW - Batch Processing Framework

**Purpose**: Transaction batching, validation, and posting control

**Business Functions**:
- Batch creation and control
- Transaction validation
- Posting orchestration
- Error handling
- Rollback support

**Programs**:
| Program | Description | Type | Priority |
|---------|-------------|------|----------|
| gl070 | GL posting phase 1 | Framework | HIGH |
| gl071 | Batch validation | Framework | HIGH |
| gl072 | GL posting phase 2 | Framework | HIGH |
| sl060 | Sales posting | Framework | HIGH |
| pl060 | Purchase posting | Framework | HIGH |
| sl100 | Cash posting | Framework | HIGH |
| pl100 | Payment posting | Framework | HIGH |
| irs030 | IRS posting | Framework | HIGH |

**Shared Data**:
- Batch control records
- Posting files
- Validation rules

---

### 7. RPT_ENGINE - Report Generation Engine

**Purpose**: Financial and operational reporting across all modules

**Business Functions**:
- Financial statements
- Management reports
- Operational reports
- Analysis reports
- Document generation

**Report Programs** (Examples):
- Trial balances (gl090, irs040)
- P&L statements (gl100, irs050)
- Balance sheets (gl105, irs060)
- Aged debt analysis (sl120, pl120)
- Product analysis (sl130, pl130)
- Transaction listings
- Stock valuations

---

### 8. SYS_ADMIN - System Administration

**Purpose**: System configuration, security, and parameter management

**Business Functions**:
- System parameters
- User management (limited)
- Company details
- VAT configuration
- Period management

**Programs**:
| Program | Description | Type | Priority |
|---------|-------------|------|----------|
| ACAS | Main system menu | Menu | HIGH |
| sys002 | System parameter maintenance | Setup | HIGH |
| acas000 | System file handler | Utility | HIGH |
| systemMT | System DAL | DAL | HIGH |

**Data Ownership**:
- SYSTEM (System parameters)
- Company configuration
- VAT rates
- Period definitions

---

### 9. PERIOD_PROC - Period Processing

**Purpose**: Month-end and year-end closing procedures

**Business Functions**:
- Period closing
- Year-end processing
- Balance forward
- Archive management

**Programs**:
| Program | Description | Type | Priority |
|---------|-------------|------|----------|
| xl150 | End of cycle processing | Period-End | HIGH |
| st040 | Stock period end | Period-End | HIGH |
| gl080 | GL period end | Period-End | HIGH |

---

### 10. DAL - Data Access Layer

**Purpose**: Database and file abstraction for all data operations

**Components**:
- File Handlers (acas001-acas032)
- DAL Modules (*MT programs)
- Load/Unload utilities (*LD, *UNL programs)
- Database connectors

**Key DAL Modules**:
| Module | Table/File | Purpose |
|--------|------------|---------|
| salesMT | SALEDGER | Sales ledger access |
| purchMT | PULEDGER | Purchase ledger access |
| stockMT | STOCK | Stock file access |
| nominalMT | NOMINAL | GL accounts access |
| glpostingMT | GLPOSTING | GL postings |
| irsnominalMT | IRSNL | IRS accounts |
| systemMT | SYSTEM | System parameters |

---

### 11. COMMON_UTIL - Common Utilities

**Purpose**: Shared functions used across all subsystems

**Components**:
| Program | Description | Type |
|---------|-------------|------|
| maps04 | Date conversion utilities | Utility |
| maps09 | Check digit verification | Utility |
| fhlogger | File access logging | Utility |
| cobdump | COBOL dump utility | Debug |
| send-some-mail | Email utility | Utility |

---

### 12. INTEG_SVC - Integration Services

**Purpose**: Cross-subsystem data exchange and synchronization

**Functions**:
- Posting file generation
- Inter-module communication
- Data transformation
- Event propagation

---

## Subsystem Characteristics

### Coupling Analysis

| Subsystem | Inbound Dependencies | Outbound Dependencies | Coupling Level |
|-----------|---------------------|----------------------|----------------|
| ST_CTRL | SL_MGMT, PL_MGMT | None | Low |
| SL_MGMT | None | GL/IRS, ST_CTRL | Medium |
| PL_MGMT | None | GL/IRS, ST_CTRL | Medium |
| GL_CORE | SL, PL, ST | None | Medium |
| IRS_CORE | SL, PL, ST | None | Medium |
| DAL | All | None | High |
| SYS_ADMIN | None | None | Low |

### Data Flow Summary

```
Customer Orders → SL_MGMT → Stock Updates → ST_CTRL
                    ↓
                Postings → GL_CORE/IRS_CORE
                    
Supplier Orders → PL_MGMT → Stock Updates → ST_CTRL
                    ↓
                Postings → GL_CORE/IRS_CORE
```

---

## Modernization Readiness

### Extraction Complexity

| Subsystem | Complexity | Key Factors |
|-----------|-----------|-------------|
| ST_CTRL | Low | Clear boundaries, simple interfaces |
| RPT_ENGINE | Low | Read-only operations |
| COMMON_UTIL | Low | Stateless utilities |
| SYS_ADMIN | Medium | Central configuration |
| SL_MGMT | Medium | Stock integration complexity |
| PL_MGMT | Medium | Stock integration complexity |
| BATCH_FW | High | Cross-subsystem orchestration |
| GL_CORE | High | Financial integrity requirements |
| IRS_CORE | High | Complex business rules |
| DAL | Very High | Foundation layer |

---

Document Version: 1.0
Analysis Date: December 2024