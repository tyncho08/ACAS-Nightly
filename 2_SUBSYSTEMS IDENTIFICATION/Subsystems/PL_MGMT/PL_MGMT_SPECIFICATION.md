# Subsystem: PL_MGMT - Purchase Ledger Management

## Executive Summary
- **Purpose**: Comprehensive accounts payable management covering supplier relationships, purchase ordering, goods receipt, invoice processing, and payment management
- **Business Value**: Optimizes cash flow through payment timing, ensures supplier relationships, controls purchasing spend, maintains audit compliance
- **Key Users**: Purchasing agents, accounts payable clerks, warehouse receiving, finance managers
- **Criticality**: HIGH - Controls organizational spending and supplier relationships

## Functional Capabilities

### Core Functions

1. **Supplier Master Management**
   - Description: Maintain complete supplier records with banking details
   - Business Rules:
     - Supplier code: 7 characters with check digit
     - Bank details validation (sort code + account)
     - Payment terms and methods
     - Settlement discount terms
     - Multiple delivery addresses
   - Triggers: New supplier onboarding, updates
   - Outcomes: Validated supplier ready for transactions

2. **Purchase Order Processing**
   - Description: Create and manage purchase orders with approval tracking
   - Business Rules:
     - Sequential order numbering
     - Automatic supplier item linkage
     - Delivery date tracking
     - Multi-line orders
     - Order amendment controls
   - Triggers: Purchase requisition, reorder point
   - Outcomes: Approved PO sent to supplier

3. **Goods Receipt Processing**
   - Description: Record receipt of goods/services against orders
   - Business Rules:
     - Match to purchase order
     - Partial receipt handling
     - Over/under delivery tolerance
     - Quality acceptance flags
     - Automatic stock updates
   - Triggers: Physical goods arrival
   - Outcomes: Updated stock, accrual creation

4. **Invoice Matching and Posting**
   - Description: Three-way matching of order, receipt, and invoice
   - Business Rules:
     - Price variance tolerance
     - Quantity matching
     - VAT validation
     - Automatic accrual reversal
     - Approval routing
   - Triggers: Supplier invoice receipt
   - Outcomes: Approved invoice posted to ledger

5. **Payment Processing**
   - Description: Payment selection, approval, and execution
   - Business Rules:
     - Due date calculation
     - Settlement discount optimization
     - Payment method selection
     - Cheque/BACS generation
     - Remittance production
   - Triggers: Payment run schedule, due dates
   - Outcomes: Payments executed, suppliers paid

### Business Processes Supported
- Procure-to-pay cycle
- Supplier onboarding
- Purchase requisition management
- Three-way matching
- Payment optimization
- Supplier performance tracking
- Spend analysis
- Standing order management

## Data Domain

### Owned Entities

**PULEDGER (Supplier Master)**
- Business description: Complete supplier information with payment details
- Key Attributes:
  - Purch-Key (7 chars, check digit)
  - Purch-Name (30 chars)
  - Purch-Current/30/60/90 (aged balances)
  - Credit-Limit (supplier gives us)
  - Credit-Period (payment terms)
  - Discount-Percent (settlement)
  - Discount-Days (early payment)
  - Bank-Sort-Code (6 digits)
  - Bank-Account (8 digits)
  - Date fields (created, last invoice, last payment)
- Business Identifiers: Supplier code
- Lifecycle: Created at onboarding, permanent record

**PUINVOICE (Purchase Orders/Invoices)**
- Business description: Purchase order and invoice records
- Key Attributes:
  - Order number (sequential)
  - Supplier code
  - Order date
  - Required date
  - Line items (code, qty, price)
  - Receipt status
  - Invoice matching
  - Authorization flags
- Business Identifiers: Order number
- Lifecycle: Created, received, matched, posted, archived

**PUITM5 (Open Items)**
- Business description: Unpaid supplier invoices
- Key Attributes:
  - OI5-KEY (Supplier + Invoice)
  - Original amount
  - Paid amount
  - Outstanding balance
  - Due date
  - Payment terms
- Business Identifiers: Supplier + Invoice
- Lifecycle: Created at posting, cleared at payment

**PLPOSTING (GL Interface)**
- Business description: Purchase postings to GL/IRS
- Key Attributes:
  - Posting codes (PI, PC, PP)
  - Account numbers
  - Amounts and VAT
  - Descriptions
- Business Identifiers: Sequential
- Lifecycle: Created at posting, consumed by GL

**PUAUTOGEN (Standing Orders)**
- Business description: Recurring purchase orders
- Key Attributes:
  - Template definition
  - Frequency rules
  - Next generation date
  - Active flag
- Business Identifiers: Template code
- Lifecycle: Created, generates orders, maintained

### Referenced Entities
- STOCK: For item details and updates
- ANALYSIS: Expense categorization
- SYSTEM: Parameters and controls
- PAYMENTS: Shared payment file
- DELIVERY: Alternative addresses

## Interface Contracts

### Inbound Interfaces

| Interface ID | Source | Data Type | Frequency | Business Purpose |
|-------------|--------|-----------|-----------|------------------|
| INT_REQ_PL_001 | Users | Requisitions | Daily | Purchase requests |
| INT_SINV_PL_001 | Suppliers | Invoice data | Daily | Invoice receipt |
| INT_REORD_PL_001 | ST_CTRL | Reorder data | Daily | Stock replenishment |
| INT_EDI_PL_001 | EDI system | Orders/Invoices | Real-time | Electronic trading |

### Outbound Interfaces

| Interface ID | Target | Data Type | Frequency | Business Purpose |
|-------------|--------|-----------|-----------|------------------|
| INT_PL_GL_001 | GL/IRS | Posting file | Daily batch | Expense posting |
| INT_PL_ST_001 | ST_CTRL | Stock updates | Real-time | Goods receipt |
| INT_PL_BANK_001 | Bank | Payment file | Weekly | BACS payments |
| INT_PL_PRINT_001 | Print/Email | Documents | On-demand | Orders/remittances |

### Internal APIs/Services

**Supplier Validation Service**
- Parameters: Supplier-Code
- Returns: Valid/Invalid, Status, Balance, Terms
- Purpose: Validate supplier status
- Validation: Active supplier, credit available
- Error Handling: Invalid code, inactive supplier

**Order Generation Service**
- Parameters: Items[], Supplier, Delivery-Date
- Returns: Order-Number, Success/Failure
- Purpose: Create purchase order
- Validation: Valid items, supplier, future date
- Error Handling: Invalid data, system limits

**Three-Way Match Service**
- Parameters: Order, Receipt, Invoice
- Returns: Match-Status, Variances[], Approval-Needed
- Purpose: Validate invoice for payment
- Validation: Quantities, prices, totals
- Error Handling: Variances exceed tolerance

## Business Rules Engine

### Validation Rules
- **VAL-PL-001**: Supplier must exist and be active
- **VAL-PL-002**: Order quantity must be positive
- **VAL-PL-003**: Receipt cannot exceed order + tolerance
- **VAL-PL-004**: Invoice must match receipt
- **VAL-PL-005**: Payment cannot exceed invoice

### Calculation Rules
- **CALC-PL-001**: Due date = Invoice date + Payment terms
- **CALC-PL-002**: Settlement = Invoice × Discount % if paid early
- **CALC-PL-003**: Net payable = Invoice - Credits - Discounts
- **CALC-PL-004**: VAT = Net amount × VAT rate
- **CALC-PL-005**: Supplier balance = Previous + Invoices - Payments

### Workflow Rules
- **WF-PL-001**: Requisition → Approval → Order → Supplier
- **WF-PL-002**: Receipt → Inspection → Stock update → Accrual
- **WF-PL-003**: Invoice → Matching → Approval → Posting
- **WF-PL-004**: Due invoices → Selection → Approval → Payment

## Operational Characteristics

### Processing Patterns
- **Real-time Processing**:
  - Order entry
  - Goods receipt
  - Stock updates
  - Inquiry functions
- **Batch Processing**:
  - Invoice posting: Daily
  - Payment runs: Weekly
  - Statement reconciliation: Monthly
  - Aged creditors: Weekly
- **Peak Periods**:
  - Month-end ordering
  - Payment run days
  - Year-end accruals

### Data Volumes
- Transaction Volume:
  - Daily: 50-200 orders/receipts
  - Weekly: 100-500 invoices
  - Monthly: 500-2,000 transactions
- Data Growth Rate:
  - Suppliers: 2-5% annually
  - Transactions: 10-15% annually
- Retention Requirements:
  - Orders/Invoices: 7 years
  - Suppliers: Permanent
  - Payments: 7 years

## Dependencies

### Upstream Dependencies
- ST_CTRL: Reorder requirements
- Requisition system: Purchase requests
- SYS_ADMIN: Parameters, VAT rates
- Approval system: Authorization

### Downstream Dependencies
- GL_CORE/IRS_CORE: Expense postings
- ST_CTRL: Stock receipts
- Bank systems: Payment execution
- Suppliers: Orders and payments

### External Dependencies
- Supplier portals: Electronic invoices
- Banks: Payment processing
- Transportation: Delivery tracking

## Quality Attributes

### Performance Requirements
- Response Time:
  - Supplier inquiry: < 2 seconds
  - Order entry: < 5 seconds
  - Receipt processing: < 3 seconds
  - Payment run: < 30 minutes
- Throughput:
  - 50 orders per hour
  - 100 receipts per hour
- Batch Windows: 2 hours for payment processing

### Reliability Requirements
- Availability: 99.5% business hours
- Recovery Time: 2 hours RTO
- Recovery Point: Last completed transaction

### Compliance Requirements
- Tax compliance: VAT reporting
- Audit trail: Complete purchase history
- Approval controls: Segregation of duties
- Data retention: Legal requirements

## Evolution Potential

### Enhancement Opportunities
- Supplier portal: Self-service invoicing
- Electronic ordering: EDI/API
- Dynamic discounting: Early payment optimization
- Automated matching: AI-powered
- Spend analytics: Advanced reporting

### Modernization Candidates
- Web interface: Modern UI
- Mobile approvals: Anywhere access
- Cloud deployment: Scalability
- P-cards integration: Card transactions
- Blockchain: Supply chain transparency

### Known Limitations
- Character interface only
- Manual three-way matching
- Limited payment methods
- No workflow engine
- Basic approval routing
- No contract management

## Risk Assessment

### Technical Risks
- Manual processes error-prone
- Limited integration options
- Batch processing delays
- Scalability constraints

### Business Risks
- Duplicate payments
- Missed discounts
- Maverick spending
- Supplier relationship issues

### Mitigation Strategies
- Automated controls
- Regular reconciliations
- Supplier statement matching
- Payment approval limits
- Duplicate invoice checking

## Special Features

### Standing Orders
- Recurring purchase automation
- Template-based generation
- Frequency options
- Automatic price updates
- Volume adjustments

### Multi-Level Approvals
- Amount-based routing
- Category-based rules
- Delegation handling
- Audit trail complete
- Override capabilities

### Supplier Performance
- On-time delivery tracking
- Quality metrics
- Price variance analysis
- Preferred supplier flags
- Performance reporting

---

Document Version: 1.0
Subsystem Version: PL v3.02
Analysis Date: December 2024