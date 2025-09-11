# Subsystem: SL_MGMT - Sales Ledger Management

## Executive Summary
- **Purpose**: Complete accounts receivable management including customer master data, invoicing, credit control, payment processing, and sales analysis
- **Business Value**: Optimizes cash flow through efficient billing and collection, maintains customer relationships, provides sales insights
- **Key Users**: Sales staff, credit controllers, accounts receivable clerks, customer service
- **Criticality**: HIGH - Direct revenue impact, customer-facing

## Functional Capabilities

### Core Functions

1. **Customer Master Management**
   - Description: Maintain comprehensive customer records
   - Business Rules:
     - Customer code: 7 characters with check digit
     - Credit limit enforcement
     - Payment terms (days)
     - Discount percentages
     - Late charge flags
   - Triggers: New customer setup, credit review
   - Outcomes: Active customer account ready for transactions

2. **Invoice Generation and Management**
   - Description: Create, validate, and post sales invoices
   - Business Rules:
     - Sequential invoice numbering
     - Stock availability check
     - Credit limit validation
     - VAT calculation by line item
     - Automatic discount application
   - Triggers: Sales order, delivery completion
   - Outcomes: Posted invoice, updated AR, stock deduction

3. **Payment Processing and Allocation**
   - Description: Record and allocate customer payments
   - Business Rules:
     - FIFO allocation (oldest first)
     - Early payment discount calculation
     - Partial payment handling
     - Foreign payment tracking
   - Triggers: Payment receipt, bank statement
   - Outcomes: Cleared invoices, updated balances, cash posting

4. **Credit Control and Collections**
   - Description: Monitor and manage customer credit
   - Business Rules:
     - Aging buckets: Current, 30, 60, 90+ days
     - Automatic late charge calculation
     - Credit hold triggers
     - Dunning letter generation
   - Triggers: Period-end aging, payment delays
   - Outcomes: Collection actions, credit decisions

5. **Sales Analysis and Reporting**
   - Description: Analyze sales by customer, product, period
   - Business Rules:
     - Product category analysis
     - Customer profitability
     - Period comparisons
     - Sales trends
   - Triggers: Management requests, period-end
   - Outcomes: Sales insights, performance metrics

### Business Processes Supported
- Order-to-cash cycle
- Credit management
- Customer onboarding
- Revenue recognition
- Cash application
- Customer communications
- Sales performance analysis
- Standing order processing

## Data Domain

### Owned Entities

**SALEDGER (Customer Master)**
- Business description: Complete customer information and balances
- Key Attributes:
  - Sales-Key (7 chars, check digit)
  - Sales-Name (30 chars)
  - Sales-Current/30/60/90 (aged balances)
  - Credit-Limit
  - Credit-Period (payment terms)
  - Discount-Percent
  - Email flags and addresses
- Business Identifiers: Customer code
- Lifecycle: Created at setup, permanent, continuous updates

**SAINVOICE (Invoice Headers)**
- Business description: Sales invoice master records
- Key Attributes:
  - SINVOICE-KEY (8 digit invoice + 2)
  - IH-CUSTOMER (customer code)
  - IH-DATE (invoice date)
  - IH-NET/VAT (amounts)
  - IH-STATUS (posted Y/N)
  - IH-TYPE (1=Invoice, 2=Credit)
- Business Identifiers: Invoice number
- Lifecycle: Created at entry, posted, paid, archived

**SAINV-LINES (Invoice Details)**
- Business description: Line item details for invoices
- Key Attributes:
  - IL-LINE-KEY (Invoice + line)
  - IL-PRODUCT (stock code)
  - IL-QTY (quantity)
  - IL-UNIT (price)
  - IL-NET/VAT (amounts)
  - IL-DISCOUNT
- Business Identifiers: Invoice + Line number
- Lifecycle: Created with invoice, deleted after payment

**SAITM3 (Open Items)**
- Business description: Unpaid invoice tracking
- Key Attributes:
  - OI3-KEY (Customer + Invoice + Type)
  - OI3-AMOUNT (original)
  - OI3-PAID (applied)
  - OI3-BALANCE (outstanding)
  - OI3-DAYS (terms)
- Business Identifiers: Customer + Invoice
- Lifecycle: Created at posting, updated with payments, deleted when paid

**SLPOSTING (GL Interface)**
- Business description: Accounting entries for GL/IRS
- Key Attributes:
  - Posting codes (SI, SC, SR)
  - Account numbers
  - Amounts and VAT
  - Descriptions
- Business Identifiers: Sequential within batch
- Lifecycle: Created at posting, consumed by GL, deleted

### Referenced Entities
- STOCK: Inventory availability and pricing
- ANALYSIS: Product/service categories
- SYSTEM: VAT rates, parameters
- DELIVERY: Alternative addresses
- PAYMENTS: Shared payment records

## Interface Contracts

### Inbound Interfaces

| Interface ID | Source | Data Type | Frequency | Business Purpose |
|-------------|--------|-----------|-----------|------------------|
| INT_CUST_001 | External | Customer data | As needed | New customer setup |
| INT_ORDER_001 | Order system | Order details | Real-time | Invoice generation |
| INT_BANK_001 | Bank files | Payment data | Daily | Payment import |

### Outbound Interfaces

| Interface ID | Target | Data Type | Frequency | Business Purpose |
|-------------|--------|-----------|-----------|------------------|
| INT_SL_GL_001 | GL_CORE | Posting file | Daily | Revenue posting |
| INT_SL_ST_001 | ST_CTRL | Stock updates | Real-time | Inventory deduction |
| INT_SL_DOC_001 | Print/Email | Documents | On-demand | Invoice/statement output |

### Internal APIs/Services

**Customer Validation Service**
- Parameters: Customer-Code
- Returns: Valid/Invalid, Credit-Status, Balance-Info
- Purpose: Validate customer and credit
- Validation: Active customer, credit check
- Error Handling: Invalid customer, credit exceeded

**Invoice Posting Service**
- Parameters: Invoice-Number
- Returns: Success/Failure, Posting-Details
- Purpose: Post invoice to accounts
- Validation: Stock availability, credit limit
- Error Handling: Insufficient stock, credit issues

**Payment Allocation Service**
- Parameters: Customer, Amount, Invoices[]
- Returns: Allocated[], Unallocated-Balance
- Purpose: Apply payment to invoices
- Validation: Invoice ownership, amounts
- Error Handling: Over-allocation, invalid invoice

## Business Rules Engine

### Validation Rules
- **VAL-SL-001**: Customer must exist and be active
- **VAL-SL-002**: Invoice total = sum of lines + VAT
- **VAL-SL-003**: Payment amount > 0
- **VAL-SL-004**: Credit limit check on new invoices
- **VAL-SL-005**: Stock availability for physical items

### Calculation Rules
- **CALC-SL-001**: VAT = Net amount × VAT rate
- **CALC-SL-002**: Line total = Qty × Unit price - Discount
- **CALC-SL-003**: Early payment discount if within terms
- **CALC-SL-004**: Late charges = Balance × Rate × Days/365
- **CALC-SL-005**: Customer balance = Previous + Invoices - Payments

### Workflow Rules
- **WF-SL-001**: Invoice states: Entry → Validated → Posted
- **WF-SL-002**: Payment: Entry → Allocation → Posted
- **WF-SL-003**: Credit hold if balance > limit
- **WF-SL-004**: Dunning: Statement → Letter1 → Letter2 → Hold

## Operational Characteristics

### Processing Patterns
- **Batch Processing**:
  - Invoice posting: End of day
  - Payment posting: After allocation
  - Statement generation: Monthly
  - Aging analysis: Weekly/monthly
- **Real-time Processing**:
  - Invoice entry
  - Stock availability check
  - Credit validation
  - Payment entry
- **Peak Periods**:
  - Month-end invoicing
  - Payment due dates
  - Statement runs

### Data Volumes
- Transaction Volume:
  - Daily: 50-200 invoices
  - Monthly: 1,000-5,000 invoices
  - Yearly: 15,000-60,000 invoices
- Data Growth Rate:
  - Customers: 5-10% annually
  - Transactions: 10-15% annually
- Retention Requirements:
  - Invoices: 7 years
  - Customers: Permanent
  - Open items: Until paid + 90 days

## Dependencies

### Upstream Dependencies
- ST_CTRL: Stock availability and pricing
- SYS_ADMIN: VAT rates, credit parameters
- Order Entry: Order details (if used)
- Bank systems: Payment files

### Downstream Dependencies
- GL_CORE/IRS_CORE: Revenue postings
- ST_CTRL: Stock deductions
- RPT_ENGINE: Sales reports
- Document delivery: Invoice/statement distribution

### External Dependencies
- Customer communications (email/print)
- Bank payment interfaces
- Credit reference agencies

## Quality Attributes

### Performance Requirements
- Response Time:
  - Customer inquiry: < 2 seconds
  - Invoice entry: < 5 seconds per line
  - Payment allocation: < 10 seconds
  - Statement generation: < 2 minutes per 100
- Throughput: 100 invoices per hour
- Batch Windows: 1-hour for posting

### Reliability Requirements
- Availability: 99.5% business hours
- Recovery Time: 2 hours RTO
- Recovery Point: Last completed transaction

### Compliance Requirements
- Tax regulations: VAT reporting compliance
- Data protection: Customer data security
- Credit regulations: Fair credit reporting
- Audit trail: Complete transaction history

## Evolution Potential

### Enhancement Opportunities
- Online customer portal: Self-service access
- Electronic invoicing: EDI/API integration
- Automated credit decisions: Rules engine
- Mobile payment processing: Field collections
- Advanced analytics: Predictive collections

### Modernization Candidates
- Web-based interface: Replace character UI
- REST APIs: Customer/invoice access
- Cloud deployment: SaaS delivery
- Real-time posting: Eliminate batch delays
- AI/ML: Payment prediction, credit scoring

### Known Limitations
- Character interface only
- Batch posting delays
- Limited payment methods
- No multi-currency
- Manual credit decisions
- No customer portal

## Risk Assessment

### Technical Risks
- File locking issues with concurrent users
- Limited error recovery in batch processes
- No real-time integration capabilities
- Scalability constraints

### Business Risks
- Revenue leakage from billing errors
- Cash flow impact from collection delays
- Customer satisfaction from billing issues
- Compliance failures in tax reporting

### Mitigation Strategies
- Implement validation checkpoints
- Automate credit monitoring
- Regular reconciliation processes
- Enhanced exception reporting
- Backup payment processing options

## Backorder Management

### Special Capability: Backorder Processing
- Tracks items not available at invoice time
- Automatic allocation when stock received
- Customer notification options
- Partial shipment handling
- BO aging and cancellation

### BO Data Structures
- BO table: 500 entries maximum
- Item table: 100 different products
- Links to original invoice
- Priority allocation rules

---

Document Version: 1.0
Subsystem Version: SL v3.02
Analysis Date: December 2024