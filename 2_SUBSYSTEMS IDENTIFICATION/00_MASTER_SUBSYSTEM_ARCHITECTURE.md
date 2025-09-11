# ACAS Subsystem Architecture

## Executive Summary

The ACAS (Applewood Computers Accounting System) has been analyzed to identify distinct subsystems based on functional cohesion, data ownership, and business domain boundaries. This document presents a comprehensive subsystem architecture that maps the 200+ COBOL programs into 12 clearly defined subsystems, establishing boundaries that enable potential modernization while preserving critical business logic.

### Key Findings
- **12 Distinct Subsystems** identified based on functional cohesion and data ownership
- **Clear Interface Contracts** between subsystems primarily through file-based integration
- **Modular Architecture** already present, facilitating subsystem isolation
- **Data Access Layer** (DAL) provides abstraction for database/file operations
- **Minimal Coupling** between subsystems, with well-defined integration points

## Subsystem Overview

### Core Business Subsystems (5)
1. **General Ledger Core (GL_CORE)** - Full double-entry bookkeeping
2. **IRS Ledger Core (IRS_CORE)** - Simplified accounting for incomplete records
3. **Sales Ledger Management (SL_MGMT)** - Accounts receivable and customer management
4. **Purchase Ledger Management (PL_MGMT)** - Accounts payable and supplier management
5. **Stock Control System (ST_CTRL)** - Inventory management and valuation

### Supporting Subsystems (4)
6. **Batch Processing Framework (BATCH_FW)** - Transaction batching and posting
7. **Report Generation Engine (RPT_ENGINE)** - Financial and operational reporting
8. **System Administration (SYS_ADMIN)** - Parameters, security, and configuration
9. **Period Processing (PERIOD_PROC)** - Month/year-end closing procedures

### Infrastructure Subsystems (3)
10. **Data Access Layer (DAL)** - Database and file abstraction layer
11. **Common Utilities (COMMON_UTIL)** - Shared functions and validations
12. **Integration Services (INTEG_SVC)** - Cross-module data exchange

## Subsystem Identification Methodology

### Analysis Approach
1. **Code Analysis**: Examined 200+ COBOL programs and their dependencies
2. **Data Ownership**: Mapped files/tables to owning subsystems
3. **Call Graphs**: Analyzed program invocation patterns
4. **Business Functions**: Grouped by accounting domain
5. **Transaction Boundaries**: Identified natural process boundaries

### Identification Criteria Applied
- **High Cohesion**: Programs working together for single business purpose
- **Loose Coupling**: Minimal dependencies between subsystems
- **Clear Interfaces**: Well-defined data exchange contracts
- **Business Alignment**: Maps to organizational structure
- **Independent Evolution**: Can be modified without affecting others

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         ACAS SYSTEM                             │
├─────────────────────────────────────────────────────────────────┤
│                    PRESENTATION LAYER                           │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────┐ │
│  │  ACAS   │  │   IRS   │  │  SALES  │  │PURCHASE │  │STOCK│ │
│  │  Menu   │  │  Menu   │  │  Menu   │  │  Menu   │  │Menu │ │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └──┬──┘ │
├───────┴─────────────┴───────────┴───────────┴───────────┴─────┤
│                    BUSINESS LOGIC LAYER                         │
│  ┌─────────────┐ ┌──────────────┐ ┌─────────────────────────┐ │
│  │  GL_CORE    │ │  IRS_CORE    │ │     SL_MGMT            │ │
│  │ gl020-gl120 │ │ irs010-irs090│ │   sl010-sl970          │ │
│  └──────┬──────┘ └──────┬───────┘ └──────────┬──────────────┘ │
│  ┌──────┴───────────────┴────────────────────┴──────────────┐ │
│  │              BATCH_FW & PERIOD_PROC                       │ │
│  │         xl150, gl070-072, sl060, pl060, irs090          │ │
│  └───────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                    DATA ACCESS LAYER                            │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  File Handlers: acas000-acas032                         │ │
│  │  DAL Modules: *MT.cbl (salesMT, purchMT, stockMT, etc.) │ │
│  └─────────────┬───────────────────────────┬───────────────┘ │
├─────────────────┴───────────────────────────┴─────────────────┤
│         COBOL FILES              │         RDBMS               │
│    ┌─────────────────┐          │    ┌─────────────────┐     │
│    │   ISAM Files    │          │    │ MySQL/MariaDB   │     │
│    └─────────────────┘          │    └─────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

## Subsystem Boundaries

### Data Ownership Matrix

| Subsystem | Owned Files/Tables | Access Mode |
|-----------|-------------------|-------------|
| GL_CORE | GLLEDGER, GLPOSTING, GLBATCH | Read/Write |
| IRS_CORE | IRSNL, IRSPOSTING, IRSDFLT, IRSFINAL | Read/Write |
| SL_MGMT | SALEDGER, SAINVOICE, SAITM3, SAAUTOGEN | Read/Write |
| PL_MGMT | PULEDGER, PUINVOICE, PUITM5, PUAUTOGEN | Read/Write |
| ST_CTRL | STOCK, AUDIT | Read/Write |
| SYS_ADMIN | SYSTEM, ANALYSIS, DELIVERY | Read/Write |

### Integration Points

| From | To | Integration Type | Data | Frequency |
|------|-----|-----------------|------|-----------|
| SL_MGMT | GL_CORE/IRS_CORE | File Transfer | Revenue postings | Daily batch |
| PL_MGMT | GL_CORE/IRS_CORE | File Transfer | Expense postings | Daily batch |
| SL_MGMT | ST_CTRL | Direct Update | Stock deductions | Real-time |
| PL_MGMT | ST_CTRL | Direct Update | Stock additions | Real-time |
| ALL | SYS_ADMIN | Direct Read | System parameters | Every operation |

## Critical Dependencies

### Subsystem Dependency Graph
```
         SYS_ADMIN
              │
    ┌─────────┼─────────┬─────────┬─────────┐
    │         │         │         │         │
  GL_CORE  IRS_CORE  SL_MGMT  PL_MGMT  ST_CTRL
    ^         ^         │         │         ^
    │         │         └─────┬───┘         │
    └─────────┴───────────────┴─────────────┘
              via BATCH_FW & posting files
```

### Key Integration Patterns
1. **Parameter Dependency**: All subsystems read system.dat via SYS_ADMIN
2. **Posting Pattern**: SL/PL create posting files consumed by GL/IRS
3. **Stock Updates**: Sales decrements, purchases increment inventory
4. **Period Closing**: xl150 orchestrates end-of-period across all modules

## Modernization Implications

### Subsystem Extraction Difficulty

| Subsystem | Difficulty | Key Challenges |
|-----------|-----------|----------------|
| ST_CTRL | Low | Few dependencies, clear boundaries |
| RPT_ENGINE | Low | Read-only operations |
| SL_MGMT | Medium | Stock integration, posting generation |
| PL_MGMT | Medium | Stock integration, posting generation |
| GL_CORE | High | Central to financial reporting |
| IRS_CORE | High | Alternative to GL, complex rules |
| DAL | Critical | Foundation for all data access |

### Recommended Modernization Sequence
1. **Phase 1**: Extract COMMON_UTIL as shared libraries
2. **Phase 2**: Modernize DAL for cloud-native data access
3. **Phase 3**: Extract ST_CTRL as microservice
4. **Phase 4**: Modernize RPT_ENGINE with modern BI tools
5. **Phase 5**: Transform SL_MGMT and PL_MGMT
6. **Phase 6**: Core ledger modernization (GL/IRS)

## Risk Assessment

### High-Risk Areas
- **Data Consistency**: Batch posting between subsystems
- **Transaction Integrity**: No distributed transaction support
- **Error Recovery**: Limited rollback capabilities
- **Audit Trail**: Fragmented across subsystems

### Mitigation Strategies
- Implement event-driven architecture for real-time integration
- Add transaction coordinator for distributed operations
- Centralize audit logging
- Implement saga pattern for long-running transactions

## Next Steps

1. **Detailed Subsystem Specifications**: Create comprehensive documentation for each subsystem
2. **Interface Definitions**: Formalize all integration contracts
3. **Data Flow Mapping**: Document end-to-end business processes
4. **Proof of Concept**: Extract one subsystem (recommend ST_CTRL)
5. **Governance Model**: Establish ownership and change management

## Appendices

### A. Program to Subsystem Mapping
[See 01_SUBSYSTEM_INVENTORY.md for complete listing]

### B. File/Table Ownership Details
[See 03_DATA_OWNERSHIP_MAP.md for complete mapping]

### C. Integration Specifications
[See 02_INTEGRATION_ARCHITECTURE.md for detailed contracts]

### D. Business Process Allocation
[See 04_PROCESS_ALLOCATION.md for process mapping]

---

Document Version: 1.0
Analysis Date: December 2024
Based on: ACAS Version 3.02+