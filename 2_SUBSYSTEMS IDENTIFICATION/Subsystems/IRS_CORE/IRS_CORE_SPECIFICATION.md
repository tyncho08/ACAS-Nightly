# Subsystem: IRS_CORE - IRS Ledger Core

## Executive Summary
- **Purpose**: Simplified accounting system designed for small businesses with incomplete records, providing basic bookkeeping without requiring full double-entry expertise
- **Business Value**: Enables small businesses to maintain compliant financial records with minimal accounting knowledge, supports tax reporting requirements
- **Key Users**: Small business owners, bookkeepers, tax preparers, accountants handling simple accounts
- **Criticality**: HIGH - Essential for businesses not using full GL system

## Functional Capabilities

### Core Functions

1. **Simplified Chart of Accounts**
   - Description: Maintain basic nominal ledger with simplified structure
   - Business Rules:
     - Account numbers: 5 main + 5 sub (10 digits total)
     - Account types: Single letter classification
     - Pre-defined common accounts
     - No complex hierarchies
     - Built-in VAT accounts
   - Triggers: Initial setup, business changes
   - Outcomes: Ready-to-use account structure

2. **Single-Entry Posting**
   - Description: Allow single-entry bookkeeping with automatic double-entry generation
   - Business Rules:
     - 32 pre-defined posting defaults
     - Automatic VAT calculation
     - Simplified posting codes (2 chars)
     - Automatic contra entries
     - No batch balancing required
   - Triggers: Daily transactions, bank entries
   - Outcomes: Posted transactions with automatic completion

3. **VAT Management**
   - Description: Comprehensive VAT tracking for tax compliance
   - Business Rules:
     - Input/Output VAT separation
     - Multiple VAT rates supported
     - Automatic VAT account posting
     - VAT return preparation
     - EU VAT compliance
   - Triggers: Any VATable transaction
   - Outcomes: VAT records ready for returns

4. **Basic Financial Reporting**
   - Description: Essential financial statements for small business
   - Business Rules:
     - Simplified P&L format
     - Basic balance sheet
     - Cash/accrual basis option
     - Quarterly comparisons
     - Tax-ready formats
   - Triggers: Period-end, tax filing, management needs
   - Outcomes: Compliant financial statements

5. **Integration with Sales/Purchase**
   - Description: Receive postings from operational modules
   - Business Rules:
     - Accept SL/PL posting files
     - Simplified posting codes
     - Automatic account mapping
     - No complex allocations
   - Triggers: Daily posting runs
   - Outcomes: Updated financial position

### Business Processes Supported
- Daily cash book entries
- Bank reconciliation
- VAT return preparation
- Simple financial statements
- Tax filing support
- Basic management accounts
- Year-end accounts preparation
- Accountant handover

## Data Domain

### Owned Entities

**IRSNL-REC (IRS Nominal Ledger)**
- Business description: Simplified chart of accounts
- Key Attributes:
  - KEY-1 (10 digits: 5 main + 5 sub)
  - TIPE (1 char account type)
  - NL-NAME (24 chars description)
  - DR (debit balance)
  - CR (credit balance)
  - DR-LAST-01-04 (quarterly debits)
  - CR-LAST-01-04 (quarterly credits)
  - AC (active flag Y/N)
- Business Identifiers: Account number
- Lifecycle: Created at setup, permanent, quarterly updates

**IRSDFLT-REC (Posting Defaults)**
- Business description: Pre-defined posting combinations
- Key Attributes:
  - DEF-REC-KEY (01-32)
  - DEF-ACS (5 digit account)
  - DEF-CODES (2 char posting code)
  - DEF-VAT (N/I/O - None/Input/Output)
- Business Identifiers: Default number
- Lifecycle: Setup once, rarely changed

**IRSPOSTING-REC (Transaction Postings)**
- Business description: All financial transactions
- Key Attributes:
  - KEY-4 (5 digit sequential)
  - POST4-CODE (transaction code)
  - POST4-DAT (date YYYYMMDD)
  - POST4-DR (debit account)
  - POST4-CR (credit account)
  - POST4-AMOUNT
  - POST4-LEGEND (description)
  - VAT-AC-DEF4 (VAT default)
  - VAT-AMOUNT4
- Business Identifiers: Posting number
- Lifecycle: Created daily, archived annually

**IRSFINAL-REC (Final Accounts Configuration)**
- Business description: Year-end account mappings
- Key Attributes:
  - Account mappings for statements
  - Report line definitions
  - Calculation rules
- Business Identifiers: Configuration key
- Lifecycle: Setup once, updated for changes

### Referenced Entities
- SYSTEM-REC: VAT rates, company info
- SLPOSTING: Sales postings (read)
- PLPOSTING: Purchase postings (read)

## Interface Contracts

### Inbound Interfaces

| Interface ID | Source | Data Type | Frequency | Business Purpose |
|-------------|--------|-----------|-----------|------------------|
| INT_SL_IRS_001 | SL_MGMT | SLPOSTING file | Daily | Sales entries |
| INT_PL_IRS_001 | PL_MGMT | PLPOSTING file | Daily | Purchase entries |
| INT_MAN_IRS_001 | User | Screen entry | Daily | Manual entries |
| INT_BANK_IRS_001 | Bank import | Transaction file | Daily | Bank entries |

### Outbound Interfaces

| Interface ID | Target | Data Type | Frequency | Business Purpose |
|-------------|--------|-----------|-----------|------------------|
| INT_IRS_RPT_001 | Reports | Financial data | On-demand | Statements |
| INT_IRS_TAX_001 | Tax export | VAT data | Quarterly | VAT returns |
| INT_IRS_ACCT_001 | Archive | Year data | Annual | Accountant file |

### Internal APIs/Services

**Default Posting Service**
- Parameters: Default-Number, Amount, VAT-Type
- Returns: DR/CR accounts, VAT amount, Success/Fail
- Purpose: Generate full posting from default
- Validation: Valid default, amount > 0
- Error Handling: Invalid default, VAT calculation error

**Balance Inquiry Service**
- Parameters: Account-Number, Period
- Returns: DR-Balance, CR-Balance, Net-Movement
- Purpose: Get account balances
- Validation: Valid account, valid period
- Error Handling: Account not found

**VAT Summary Service**
- Parameters: Date-Range, VAT-Type
- Returns: Total-VAT, Net-Amount, Transaction-Count
- Purpose: VAT return preparation
- Validation: Valid dates
- Error Handling: No data found

## Business Rules Engine

### Validation Rules
- **VAL-IRS-001**: Posting must have valid default or accounts
- **VAL-IRS-002**: VAT must be N, I, or O
- **VAL-IRS-003**: Date must be in open period
- **VAL-IRS-004**: Amount must be positive
- **VAL-IRS-005**: Account must exist and be active

### Calculation Rules
- **CALC-IRS-001**: VAT = Net amount × VAT rate
- **CALC-IRS-002**: If default used, generate contra entry
- **CALC-IRS-003**: Net position = DR - CR balances
- **CALC-IRS-004**: Quarter totals accumulate monthly
- **CALC-IRS-005**: P&L balance to capital account

### Workflow Rules
- **WF-IRS-001**: Entry → Validation → Posting → Update
- **WF-IRS-002**: No complex batch processing
- **WF-IRS-003**: Direct posting without approval
- **WF-IRS-004**: Period close rolls balances

## Operational Characteristics

### Processing Patterns
- **Real-time Processing**:
  - Transaction entry
  - Balance inquiry
  - Default lookups
- **Batch Processing**:
  - SL/PL integration: Daily
  - Period close: Monthly
  - Report generation: On-demand
- **Peak Periods**:
  - Month-end
  - VAT return dates
  - Year-end

### Data Volumes
- Transaction Volume:
  - Daily: 10-50 postings
  - Monthly: 200-1,000 postings
  - Yearly: 3,000-15,000 postings
- Data Growth Rate:
  - Transactions: 5% annually
  - Accounts: Minimal growth
- Retention Requirements:
  - Online: Current year
  - Archive: 7 years

## Dependencies

### Upstream Dependencies
- SL_MGMT: Sales postings
- PL_MGMT: Purchase postings
- SYS_ADMIN: VAT rates, parameters
- User: Manual entries

### Downstream Dependencies
- RPT_ENGINE: Financial reports
- Tax systems: VAT returns
- External accountants: Year-end

### External Dependencies
- Tax authority: Compliance rules
- Bank: Statement imports

## Quality Attributes

### Performance Requirements
- Response Time:
  - Posting entry: < 2 seconds
  - Balance inquiry: < 1 second
  - Report generation: < 30 seconds
- Throughput: 50 postings per hour
- Batch Windows: 30 minutes for integration

### Reliability Requirements
- Availability: 99% business hours
- Recovery Time: 4 hours RTO
- Recovery Point: Daily backup

### Compliance Requirements
- Tax regulations: Full VAT compliance
- Small company: Simplified reporting
- Audit trail: Basic requirements
- Data retention: Legal minimums

## Evolution Potential

### Enhancement Opportunities
- Bank feed integration: Auto-import
- Cloud backup: Automatic protection
- Mobile app: On-the-go entry
- Receipt scanning: Digital records
- Automated VAT returns: Direct submission

### Modernization Candidates
- Web interface: Browser-based
- Cloud deployment: SaaS model
- API access: Accountant integration
- Digital receipts: Paperless
- Auto-categorization: ML-based

### Known Limitations
- No multi-company
- Basic reporting only
- No multi-currency
- No approval workflow
- Limited analysis
- No budgeting

## Risk Assessment

### Technical Risks
- Simple structure may limit growth
- No audit controls
- Limited validation
- Basic security

### Business Risks
- May outgrow capabilities
- Compliance changes
- Limited controls
- Error prone without validation

### Mitigation Strategies
- Regular accountant review
- Frequent backups
- Training materials
- Upgrade path to GL
- External audit checks

## Special Considerations

### Target Market
- Sole traders
- Small partnerships
- Simple businesses
- Non-VAT registered (optional)
- Service businesses

### Upgrade Path
- Clear migration to GL_CORE
- Data conversion tools
- Training materials
- Phased approach
- Parallel running option

### Integration Simplicity
- Minimal configuration
- Pre-set defaults
- Common scenarios built-in
- Help text throughout
- Example entries

---

Document Version: 1.0
Subsystem Version: IRS v3.02
Analysis Date: December 2024