# ACAS Subsystem Communication Matrix and Event Catalog

## Overview

This document provides a comprehensive view of all communication patterns between ACAS subsystems, including synchronous calls, asynchronous file transfers, shared data access, and business events that trigger cross-subsystem interactions.

## Communication Matrix

### Direct Communication (Synchronous)

| From | To | Communication Type | Method | Data | Frequency | Criticality |
|------|----|--------------------|--------|------|-----------|-------------|
| SL_MGMT | ST_CTRL | Function Call | CALL acas011 | Stock updates | Per invoice line | HIGH |
| PL_MGMT | ST_CTRL | Function Call | CALL acas011 | Stock updates | Per receipt | HIGH |
| ALL | SYS_ADMIN | Function Call | CALL acas000 | System params | Every operation | CRITICAL |
| ALL | DAL | Function Call | CALL acas0nn | Data access | Every data operation | CRITICAL |
| ALL | COMMON_UTIL | Function Call | CALL maps04/09 | Date/validation | As needed | MEDIUM |
| MENU | ALL MODULES | Program Call | CALL program | Context/params | User navigation | HIGH |
| GL_CORE | BATCH_FW | Function Call | Internal | Batch control | Posting operations | HIGH |
| IRS_CORE | BATCH_FW | Function Call | Internal | Batch control | Posting operations | HIGH |
| INTEG_SVC | DAL | Function Call | CALL *MT | Data operations | Load/Unload | HIGH |
| Admin | INTEG_SVC | Program Call | CALL *LD/*UNL | Load/Unload | Migration/Backup | MEDIUM |
| INTEG_SVC | ALL | Data Access | Direct file/DB | Full data | During migration | CRITICAL |

### File-Based Communication (Asynchronous)

| From | To | File/Table | Data Type | Frequency | Volume | Critical Path |
|------|----|------------|-----------|-----------|---------|---------------|
| SL_MGMT | GL_CORE | SLPOSTING | Revenue postings | Daily batch | 100-500 records | YES |
| SL_MGMT | IRS_CORE | SLPOSTING | Revenue postings | Daily batch | 100-500 records | YES |
| PL_MGMT | GL_CORE | PLPOSTING | Expense postings | Daily batch | 50-300 records | YES |
| PL_MGMT | IRS_CORE | PLPOSTING | Expense postings | Daily batch | 50-300 records | YES |
| ST_CTRL | GL_CORE | Via posting | Adjustments | As needed | 10-50 records | NO |
| ST_CTRL | IRS_CORE | Via posting | Adjustments | As needed | 10-50 records | NO |
| PERIOD_PROC | ALL | Various | Period updates | Monthly | All records | YES |
| INTEG_SVC | External | Data files | Import/Export | Scheduled | 1K-100K records | NO |
| ALL | INTEG_SVC | Archive files | Unload data | Backup schedule | All records | NO |

### Shared Data Access (Read-Only)

| Data Owner | Data | Accessed By | Access Pattern | Frequency |
|------------|------|-------------|----------------|-----------|
| SYS_ADMIN | SYSTEM.DAT | ALL | Direct read | Constant |
| SYS_ADMIN | ANALYSIS.DAT | SL, PL, ST | Direct read | Per transaction |
| ST_CTRL | STOCK availability | SL_MGMT | Query via DAL | Per order |
| ST_CTRL | STOCK on-order | PL_MGMT | Query via DAL | Reorder check |
| PL_MGMT | Supplier info | ST_CTRL | Query via DAL | Reorder process |
| ALL | Master data | RPT_ENGINE | Read via DAL | Report generation |

## Event Catalog

### Business Events and Triggers

#### Sales Domain Events

**Event: CUSTOMER_ORDER_RECEIVED**
- Source: External/User
- Target Subsystem: SL_MGMT
- Triggers:
  - Stock availability check (→ ST_CTRL)
  - Credit validation (internal)
  - Pricing calculation (internal)
- Data Flow: Order details → Invoice creation
- Error Scenarios: Insufficient stock, credit exceeded

**Event: INVOICE_POSTED**
- Source: SL_MGMT (sl060)
- Target Subsystems: ST_CTRL, GL_CORE/IRS_CORE
- Triggers:
  - Stock deduction (immediate)
  - GL posting record creation
  - Customer balance update
- Data Flow: Invoice → Stock update + Posting file
- Error Scenarios: Stock update failure, posting imbalance

**Event: PAYMENT_RECEIVED**
- Source: SL_MGMT (sl080)
- Target Subsystems: GL_CORE/IRS_CORE
- Triggers:
  - Payment allocation to invoices
  - Cash posting record creation
  - Customer balance update
- Data Flow: Payment → Allocation → Posting file
- Error Scenarios: Over-allocation, invalid invoice

#### Purchase Domain Events

**Event: PURCHASE_ORDER_CREATED**
- Source: PL_MGMT (pl020)
- Target Subsystems: ST_CTRL
- Triggers:
  - On-order quantity update
  - Commitment tracking
- Data Flow: PO details → Stock on-order update
- Error Scenarios: Invalid supplier, invalid item

**Event: GOODS_RECEIVED**
- Source: PL_MGMT (pl025)
- Target Subsystems: ST_CTRL
- Triggers:
  - Stock quantity increase
  - Average cost recalculation
  - Audit trail creation
- Data Flow: Receipt → Stock addition + Cost update
- Error Scenarios: PO not found, quantity mismatch

**Event: SUPPLIER_INVOICE_POSTED**
- Source: PL_MGMT (pl060)
- Target Subsystems: GL_CORE/IRS_CORE
- Triggers:
  - Expense posting creation
  - Supplier balance update
  - Accrual matching
- Data Flow: Invoice → Posting file
- Error Scenarios: No matching PO, amount variance

#### Stock Domain Events

**Event: STOCK_ADJUSTMENT**
- Source: ST_CTRL (st020)
- Target Subsystems: GL_CORE/IRS_CORE
- Triggers:
  - Inventory value change
  - GL adjustment posting
  - Audit record creation
- Data Flow: Adjustment → Audit trail + GL posting
- Error Scenarios: Would go negative, invalid reason

**Event: REORDER_POINT_REACHED**
- Source: ST_CTRL (monitoring)
- Target Subsystems: PL_MGMT (suggested)
- Triggers:
  - Reorder report generation
  - Purchase suggestion
  - Alert notification
- Data Flow: Low stock → Reorder suggestion
- Error Scenarios: No supplier defined

#### Financial Domain Events

**Event: BATCH_POSTING_INITIATED**
- Source: User via GL_CORE/IRS_CORE
- Target Subsystems: Posting sources
- Triggers:
  - Batch validation
  - Account updates
  - Balance recalculation
- Data Flow: Posting file → Validation → GL updates
- Error Scenarios: Out of balance, invalid accounts

**Event: PERIOD_CLOSE_STARTED**
- Source: PERIOD_PROC (xl150)
- Target Subsystems: ALL
- Triggers:
  - Subsystem closing sequence
  - Balance roll-forward
  - Archive creation
- Data Flow: Close command → Sequential subsystem closing
- Error Scenarios: Unposted transactions, incomplete processes

#### System Domain Events

**Event: SYSTEM_PARAMETER_CHANGED**
- Source: SYS_ADMIN (sys002)
- Target Subsystems: ALL
- Triggers:
  - Parameter reload (on next access)
  - Validation rule updates
  - Behavioral changes
- Data Flow: Parameter update → Cached value invalidation
- Error Scenarios: Invalid parameter value

**Event: NEW_PERIOD_STARTED**
- Source: PERIOD_PROC
- Target Subsystems: ALL
- Triggers:
  - Period validation updates
  - New period initialization
  - Report generation
- Data Flow: Period increment → All subsystems notified
- Error Scenarios: Prior period not closed

#### Integration Domain Events

**Event: DATA_LOAD_INITIATED**
- Source: INTEG_SVC (*LD programs)
- Target Subsystems: DAL, Target modules
- Triggers:
  - File validation
  - Target preparation
  - Load processing
  - Statistics update
- Data Flow: File data → Validation → Database tables
- Error Scenarios: Invalid format, duplicate keys, space issues

**Event: DATA_UNLOAD_REQUESTED**
- Source: INTEG_SVC (*UNL programs)
- Target Subsystems: DAL, Source modules
- Triggers:
  - Selection processing
  - Data extraction
  - File creation
  - Verification totals
- Data Flow: Database → Extract → File creation
- Error Scenarios: I/O errors, selection errors

**Event: MIGRATION_STARTED**
- Source: INTEG_SVC (migration utilities)
- Target Subsystems: ALL affected modules
- Triggers:
  - Backup creation
  - System lock
  - Sequential migration
  - Validation checks
- Data Flow: Source storage → Transform → Target storage
- Error Scenarios: Lock failures, data corruption

## Communication Patterns

### Pattern 1: Request-Response (Synchronous)
```
Requester → Service Provider → Response
Example: SL_MGMT → ST_CTRL → Stock availability
```

### Pattern 2: Fire-and-Forget (Asynchronous)
```
Producer → File/Queue → Consumer (later)
Example: SL_MGMT → SLPOSTING → GL_CORE
```

### Pattern 3: Broadcast (One-to-Many)
```
Event Source → Multiple Consumers
Example: Period Close → All Subsystems
```

### Pattern 4: Orchestration (Sequential)
```
Coordinator → Service 1 → Service 2 → ... → Complete
Example: xl150 → SL close → PL close → ST close → GL close
```

## Communication Frequencies

### Real-Time (< 1 second)
- Stock availability checks
- Customer/supplier validation
- System parameter reads
- Credit limit checks

### Near Real-Time (< 1 minute)
- Stock updates from sales/purchases
- Balance updates
- Audit trail writes

### Batch (Scheduled)
- GL/IRS postings (daily)
- Statement generation (monthly)
- Reorder analysis (daily)
- Period closing (monthly)

### On-Demand
- Report generation
- Master data maintenance
- Manual adjustments

## Error Propagation Matrix

| Error Source | Immediate Impact | Cascading Impact | Recovery Method |
|--------------|------------------|------------------|-----------------|
| Stock update failure | Invoice not posted | Revenue not recognized | Manual adjustment |
| Posting file corruption | GL not updated | Financial reports wrong | Regenerate from source |
| Parameter read failure | Operation fails | Multiple subsystems affected | Fallback values |
| Period close incomplete | Next period blocked | No new transactions | Complete or rollback |
| Credit check failure | Order rejected | Customer dissatisfaction | Manual override |

## Performance Considerations

### High-Volume Communications
| Communication | Volume/Day | Performance Requirement | Bottleneck Risk |
|---------------|------------|------------------------|-----------------|
| Stock checks | 1,000-5,000 | < 1 sec response | File locking |
| Invoice posting | 100-500 | < 5 sec per invoice | Batch window |
| GL posting | 500-2,000 lines | < 30 min batch | Sequential processing |
| Report queries | 50-200 | < 60 sec per report | Data aggregation |

### Communication Optimization
1. **Caching**: System parameters cached per session
2. **Batching**: Posting files accumulate transactions
3. **Indexing**: Key fields indexed for quick lookup
4. **Locking**: Minimal lock duration for updates

## Security and Audit

### Communication Security
| Communication Type | Security Measure | Audit Level |
|-------------------|------------------|-------------|
| File transfers | OS permissions | File access log |
| Database access | DB credentials | Query log |
| Program calls | OS security | Execution log |
| Parameter access | Read-only | Access tracking |

### Audit Trail
- All stock movements logged with source
- All postings maintain batch references
- Parameter changes logged with timestamp
- Period operations create audit entries

## Modernization Opportunities

### Event-Driven Architecture
Replace file-based integration with:
- Message queues for posting data
- Event streams for real-time updates
- Publish-subscribe for notifications
- Webhooks for external integration

### API-Based Communication
Transform direct calls to:
- REST APIs for queries
- GraphQL for complex data needs
- WebSocket for real-time updates
- gRPC for internal services

### Microservices Preparation
Current subsystems map to services:
- Stock Service (ST_CTRL)
- Customer Service (SL_MGMT)
- Supplier Service (PL_MGMT)
- Financial Service (GL/IRS)
- Configuration Service (SYS_ADMIN)

---

Document Version: 1.0
Analysis Date: December 2024