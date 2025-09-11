# Subsystem: GL_CORE - General Ledger Core

## Executive Summary
- **Purpose**: Provides full double-entry bookkeeping capabilities with multi-profit center support for medium to large businesses requiring comprehensive financial accounting
- **Business Value**: Ensures financial integrity, regulatory compliance, and provides complete financial reporting capabilities
- **Key Users**: Financial controllers, accountants, bookkeepers, management
- **Criticality**: HIGH - Core financial system of record

## Functional Capabilities

### Core Functions

1. **Chart of Accounts Management**
   - Description: Maintain hierarchical account structure with multiple levels
   - Business Rules: 
     - Account numbers: 6 digits + 2 digit profit center
     - Account types: Balance Sheet (1), P&L (2), Header (9)
     - Hierarchy levels: 1-9 for reporting aggregation
   - Triggers: Manual setup, account creation/modification
   - Outcomes: Structured chart ready for posting

2. **Journal Entry Processing**
   - Description: Enter and validate double-entry transactions
   - Business Rules:
     - Debits must equal credits within batch
     - Valid account numbers required
     - Period must be open
     - Date within acceptable range
   - Triggers: Manual entry, automated posting from subsystems
   - Outcomes: Validated entries ready for posting

3. **Batch Posting Control**
   - Description: Two-phase posting with validation and commit
   - Business Rules:
     - Phase 1: Validate all entries, create work file
     - Phase 2: Post to ledger, update balances
     - Batch status tracking (0=Open, 1=Proofed, 2=Posted)
   - Triggers: User-initiated posting process
   - Outcomes: Updated account balances, audit trail

4. **Financial Statement Generation**
   - Description: Produce standard financial reports
   - Business Rules:
     - Trial balance must balance
     - P&L rolls to retained earnings
     - Multi-level consolidation by hierarchy
   - Triggers: On-demand, period-end
   - Outcomes: Trial Balance, P&L, Balance Sheet

5. **Period Management**
   - Description: Control accounting periods and year-end
   - Business Rules:
     - 12 monthly periods + year-end adjustments
     - Period locking prevents back-dating
     - Automatic balance roll-forward
   - Triggers: Month-end processing
   - Outcomes: Closed period, opening balances

### Business Processes Supported
- Month-end financial closing
- Year-end statutory reporting
- Management reporting
- Audit support
- Multi-branch consolidation
- Inter-company eliminations

## Data Domain

### Owned Entities

**GLLEDGER (Nominal Ledger)**
- Business description: Chart of accounts with balances
- Key Attributes:
  - LEDGER-KEY (8 digits: 6 account + 2 PC)
  - LEDGER-TYPE (1=BS, 2=PL, 9=Header)
  - LEDGER-NAME (32 chars)
  - LEDGER-BALANCE (current balance)
  - LEDGER-LAST (prior period)
  - LEDGER-Q1-4 (quarterly movements)
- Business Identifiers: Account + Profit Center
- Lifecycle: Created at setup, permanent, balance updates monthly

**GLPOSTING (Transaction Details)**
- Business description: Individual journal entries
- Key Attributes:
  - POST-KEY (Batch + Sequence)
  - POST-CODE (Transaction type)
  - POST-DATE (Posting date)
  - POST-DR/CR (Account numbers)
  - POST-AMOUNT
  - POST-LEGEND (Description)
- Business Identifiers: Batch + Line number
- Lifecycle: Created at entry, posted to ledger, archived annually

**GLBATCH (Batch Control)**
- Business description: Controls transaction batches
- Key Attributes:
  - BATCH-KEY (6 digits sequential)
  - BATCH-STATUS (0/1/2)
  - ENTERED/POSTED dates
  - INPUT-GROSS (control total)
  - ACTUAL-GROSS (calculated total)
- Business Identifiers: Batch number
- Lifecycle: Created at entry, closed at posting

### Referenced Entities
- SYSTEM-REC: System parameters, VAT rates
- SLPOSTING: Sales ledger postings (read-only)
- PLPOSTING: Purchase ledger postings (read-only)

## Interface Contracts

### Inbound Interfaces

| Interface ID | Source | Data Type | Frequency | Business Purpose |
|-------------|--------|-----------|-----------|------------------|
| INT_SL_GL_001 | SL_MGMT | SLPOSTING file | Daily batch | Revenue/receivables posting |
| INT_PL_GL_001 | PL_MGMT | PLPOSTING file | Daily batch | Expenses/payables posting |
| INT_ST_GL_001 | ST_CTRL | Adjustment file | As needed | Inventory adjustments |
| INT_MANUAL_001 | User | Screen entry | Daily | Manual journal entries |

### Outbound Interfaces

| Interface ID | Target | Data Type | Frequency | Business Purpose |
|-------------|--------|-----------|-----------|------------------|
| INT_GL_RPT_001 | Reports | Account data | On-demand | Financial statements |
| INT_GL_AUDIT_001 | Archive | Posted trans | Monthly | Audit trail |

### Internal APIs/Services

**Account Validation Service**
- Parameters: Account-Number, Profit-Center
- Returns: Valid/Invalid, Account-Name, Account-Type
- Purpose: Validate account exists and is active
- Validation: Check account exists, not deleted, valid PC
- Error Handling: Invalid account, deleted account, invalid PC

**Balance Inquiry Service**  
- Parameters: Account-Number, PC, Period-Range
- Returns: Opening-Balance, Movements, Closing-Balance
- Purpose: Retrieve account balances
- Validation: Valid account, authorized user
- Error Handling: Account not found, access denied

**Posting Service**
- Parameters: Batch-Number
- Returns: Success/Failure, Error-Details
- Purpose: Post validated batch to ledger
- Validation: Batch validated, period open, balanced
- Error Handling: Validation errors, period closed, system errors

## Business Rules Engine

### Validation Rules
- **VAL-GL-001**: Batch debits must equal credits
- **VAL-GL-002**: Accounts must exist and be active
- **VAL-GL-003**: Posting date within current or prior period
- **VAL-GL-004**: Profit center must be valid
- **VAL-GL-005**: No posting to header accounts (type 9)

### Calculation Rules
- **CALC-GL-001**: Update account balance = Previous + Movement
- **CALC-GL-002**: Roll P&L to retained earnings at year-end
- **CALC-GL-003**: Consolidate by hierarchy level for reports

### Workflow Rules
- **WF-GL-001**: Batch states: Open → Proofed → Posted
- **WF-GL-002**: Period close requires all batches posted
- **WF-GL-003**: Year-end requires all periods closed

## Operational Characteristics

### Processing Patterns
- **Batch Processing**: 
  - Journal posting runs: End of business day
  - Integration posting: After SL/PL daily close
  - Report generation: On-demand
- **Real-time Processing**: 
  - Balance inquiries
  - Account validation
  - Journal entry
- **Peak Periods**: 
  - Month-end (last 5 business days)
  - Year-end close

### Data Volumes
- Transaction Volume: 
  - Daily: 100-500 journal lines
  - Monthly: 3,000-15,000 lines
  - Yearly: 40,000-200,000 lines
- Data Growth Rate: 
  - Transactions: 5-10% annually
  - Accounts: 1-2% annually
- Retention Requirements:
  - Online: Current + 1 year
  - Archive: 7 years minimum

## Dependencies

### Upstream Dependencies
- SL_MGMT: Sales postings file
- PL_MGMT: Purchase postings file  
- ST_CTRL: Inventory adjustment postings
- SYS_ADMIN: System parameters, period control

### Downstream Dependencies
- RPT_ENGINE: Financial statements
- PERIOD_PROC: Period-end processing
- External auditors: Compliance reports

### External Dependencies
- None directly (all through integration layer)

## Quality Attributes

### Performance Requirements
- Response Time: 
  - Account inquiry: < 2 seconds
  - Batch validation: < 30 seconds per 100 lines
  - Report generation: < 60 seconds
- Throughput: 500 transactions per batch maximum
- Batch Windows: 2-hour posting window daily

### Reliability Requirements
- Availability: 99.5% during business hours
- Recovery Time: 4 hours RTO
- Recovery Point: End of last successful batch

### Compliance Requirements
- GAAP/IFRS: Full compliance via COA structure
- Tax regulations: VAT tracking and reporting
- Audit trail: Complete transaction history
- Data retention: 7-year legal requirement

## Evolution Potential

### Enhancement Opportunities
- Real-time posting: Replace batch with immediate posting
- Multi-currency: Add foreign currency capabilities
- Automated reconciliation: Bank/intercompany matching
- Enhanced analytics: Drill-down capabilities

### Modernization Candidates
- Web-based UI: Replace character interface
- REST APIs: For integration and reporting
- Cloud deployment: Multi-tenant architecture
- Real-time consolidation: Replace batch consolidation

### Known Limitations
- Batch-only posting model
- Limited to 2-character profit centers
- No multi-currency support
- Character-based interface only
- No workflow approvals

## Risk Assessment

### Technical Risks
- Aging codebase (COBOL)
- Limited error recovery
- No real-time integration
- File-based architecture

### Business Risks
- Manual processes prone to error
- Limited audit capabilities
- No segregation of duties
- Compliance reporting gaps

### Mitigation Strategies
- Implement automated controls
- Add approval workflows
- Enhance audit logging
- Regular compliance reviews

---

Document Version: 1.0  
Subsystem Version: GL v3.02  
Analysis Date: December 2024