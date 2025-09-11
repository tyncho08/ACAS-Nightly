# Subsystem: ST_CTRL - Stock Control System

## Executive Summary
- **Purpose**: Comprehensive inventory management providing real-time stock control, valuation, movement tracking, and reorder management
- **Business Value**: Optimizes inventory investment, prevents stockouts, ensures accurate costing, maintains audit trail for compliance
- **Key Users**: Warehouse staff, purchasing agents, inventory controllers, management
- **Criticality**: HIGH - Directly impacts sales fulfillment and working capital

## Functional Capabilities

### Core Functions

1. **Stock Item Master Maintenance**
   - Description: Maintain comprehensive inventory item records
   - Business Rules:
     - Stock code: 13 characters (unique identifier)
     - Abbreviated code: 7 characters (quick reference)
     - Multiple supplier links (up to 3)
     - Service items flag (non-physical)
     - Location tracking
   - Triggers: New product introduction, supplier changes
   - Outcomes: Active stock record ready for transactions

2. **Stock Movement Processing**
   - Description: Record all inventory movements with full audit trail
   - Business Rules:
     - Movement types: Addition, Deduction, Transfer
     - Source tracking (SI=Sales, PI=Purchase, etc.)
     - Real-time quantity updates
     - Automatic cost recalculation
     - Audit record creation
   - Triggers: Sales transactions, purchase receipts, adjustments
   - Outcomes: Updated quantities, cost values, audit trail

3. **Inventory Valuation**
   - Description: Calculate and maintain inventory values
   - Business Rules:
     - Average cost method
     - Real-time value updates
     - Include WIP in valuation
     - Period movement tracking
     - Cost price maintenance
   - Triggers: Any stock movement, cost changes
   - Outcomes: Current inventory value, cost of goods sold

4. **Reorder Management**
   - Description: Monitor stock levels and suggest reorders
   - Business Rules:
     - Reorder level monitoring
     - Reorder quantity calculation
     - Lead time consideration
     - Preferred supplier selection
     - Seasonal adjustments
   - Triggers: Stock below reorder level, periodic review
   - Outcomes: Reorder suggestions, purchase requisitions

5. **Stock Analysis and Reporting**
   - Description: Comprehensive inventory reporting
   - Business Rules:
     - Stock valuation reports
     - Movement analysis
     - Reorder reports
     - Stock take variance
     - ABC analysis capability
   - Triggers: On-demand, period-end, stock take
   - Outcomes: Management insights, control reports

### Business Processes Supported
- Inventory receipt and put-away
- Order fulfillment and picking
- Stock transfers between locations
- Physical inventory counts
- Cycle counting
- Inventory valuation
- Reorder point management
- Supplier performance tracking

## Data Domain

### Owned Entities

**STOCK (Inventory Master)**
- Business description: Complete item information and balances
- Key Attributes:
  - Stock-Code (13 chars, primary key)
  - Stock-Abbrev (7 chars, alternate key)
  - Stock-Desc (32 chars description)
  - Stock-Location (8 chars)
  - Stock-Anal (3 char analysis code)
  - Service-Item (Y/N flag)
  - Qty-Held (on hand)
  - Qty-On-Order (outstanding POs)
  - Qty-BO (backordered)
  - Qty-WIP (work in progress)
  - Reorder-Level
  - Reorder-Qty
  - Cost-Price (current average)
  - Sell-Price (retail)
  - Stock-Value (qty × cost)
  - Supp-1/2/3 (supplier codes)
  - Date fields (created, last receipt, last sale)
  - Period/YTD movements (add/deduct with qty and value)
- Business Identifiers: Stock code or abbreviated code
- Lifecycle: Created at setup, continuous updates, permanent record

**AUDIT (Stock Movement History)**
- Business description: Complete audit trail of all stock movements
- Key Attributes:
  - Batch-Number (6 digits)
  - Movement-Date (YYYYMMDD)
  - Movement-Time (HHMMSS)
  - Stock-Code (item moved)
  - Movement-Type (A=Add, D=Deduct, T=Transfer)
  - Movement-Qty
  - Movement-Value
  - Source-Type (SI=Sales Invoice, etc.)
  - Source-Ref (document number)
  - User-ID
- Business Identifiers: Date + Time + Stock Code
- Lifecycle: Created at movement, retained per policy, archived

**TMP-STOCK (Work File)**
- Business description: Temporary processing file
- Used for: Sorts, reports, calculations
- Lifecycle: Created as needed, deleted after use

### Referenced Entities
- PULEDGER: Supplier information (read)
- SALEDGER: Customer for special pricing (potential)
- ANALYSIS: Stock categorization
- SYSTEM: Costing parameters

## Interface Contracts

### Inbound Interfaces

| Interface ID | Source | Data Type | Frequency | Business Purpose |
|-------------|--------|-----------|-----------|------------------|
| INT_SL_ST_001 | SL_MGMT | Stock update call | Real-time | Sales deductions |
| INT_PL_ST_001 | PL_MGMT | Stock update call | Real-time | Purchase receipts |
| INT_MAN_ST_001 | User | Movement entry | As needed | Adjustments |
| INT_COUNT_001 | Stock take | Count data | Periodic | Physical inventory |

### Outbound Interfaces

| Interface ID | Target | Data Type | Frequency | Business Purpose |
|-------------|--------|-----------|-----------|------------------|
| INT_ST_GL_001 | GL/IRS | Adjustment posting | Batch | Inventory adjustments |
| INT_ST_PL_001 | PL_MGMT | Reorder data | Daily | Purchase suggestions |
| INT_ST_VAL_001 | Reports | Valuation data | Period-end | Stock valuation |

### Internal APIs/Services

**Stock Availability Service**
- Parameters: Stock-Code, Required-Qty
- Returns: Available-Qty, On-Order, Lead-Time
- Purpose: Check stock availability
- Validation: Valid item, positive quantity
- Error Handling: Item not found, insufficient stock

**Movement Recording Service**
- Parameters: Stock-Code, Movement-Type, Qty, Source
- Returns: Success/Failure, New-Balance, Audit-Ref
- Purpose: Record stock movement
- Validation: Valid item, movement type, quantity
- Error Handling: Would go negative, invalid type

**Cost Update Service**
- Parameters: Stock-Code, New-Cost, Update-Type
- Returns: Old-Cost, New-Average, Value-Impact
- Purpose: Update item costs
- Validation: Valid item, positive cost
- Error Handling: Invalid cost, calculation overflow

## Business Rules Engine

### Validation Rules
- **VAL-ST-001**: Stock code must be unique
- **VAL-ST-002**: Quantity on hand cannot go negative
- **VAL-ST-003**: Costs must be positive
- **VAL-ST-004**: Reorder level < reorder qty (typically)
- **VAL-ST-005**: Service items have no qty/value

### Calculation Rules
- **CALC-ST-001**: Available = On-Hand - Allocated + On-Order
- **CALC-ST-002**: New avg cost = (Old value + Receipt value) / Total qty
- **CALC-ST-003**: Stock value = Quantity × Average cost
- **CALC-ST-004**: Movement value = Qty × Cost at time
- **CALC-ST-005**: Reorder when Available < Reorder level

### Workflow Rules
- **WF-ST-001**: Receipt → Inspection → Put-away → Available
- **WF-ST-002**: Pick → Pack → Ship → Deduct
- **WF-ST-003**: Count → Variance → Adjustment → Post
- **WF-ST-004**: Below reorder → Suggestion → PO → On-order

## Operational Characteristics

### Processing Patterns
- **Real-time Processing**:
  - Stock queries
  - Movement updates
  - Availability checks
  - Cost calculations
- **Batch Processing**:
  - Reorder analysis: Daily
  - Valuation reports: Period-end
  - Movement reports: Daily/weekly
  - Audit trail: Continuous
- **Peak Periods**:
  - Order processing times
  - Goods receipt times
  - Stock take periods
  - Month-end reporting

### Data Volumes
- Transaction Volume:
  - Daily: 200-1,000 movements
  - Monthly: 5,000-25,000 movements
  - Yearly: 60,000-300,000 movements
- Data Growth Rate:
  - Items: 2-5% annually
  - Movements: 10-15% annually
- Retention Requirements:
  - Stock master: Permanent
  - Movements: Current + 1 year online
  - Audit trail: 3-5 years

## Dependencies

### Upstream Dependencies
- SL_MGMT: Sales transactions trigger deductions
- PL_MGMT: Purchase receipts trigger additions
- SYS_ADMIN: System parameters, analysis codes
- Physical warehouse: Actual stock movements

### Downstream Dependencies
- SL_MGMT: Stock availability for orders
- PL_MGMT: Reorder suggestions
- GL_CORE/IRS_CORE: Inventory valuations
- Management: Inventory reports

### External Dependencies
- Warehouse management: Physical control
- Suppliers: Delivery performance
- Transportation: Receipt timing

## Quality Attributes

### Performance Requirements
- Response Time:
  - Stock inquiry: < 1 second
  - Movement update: < 2 seconds
  - Availability check: < 1 second
  - Valuation report: < 5 minutes
- Throughput: 
  - 500 movements per hour
  - 1000 availability checks per hour
- Batch Windows: Reorder analysis 30 minutes

### Reliability Requirements
- Availability: 99.5% during operation hours
- Recovery Time: 1 hour RTO
- Recovery Point: Last completed movement

### Compliance Requirements
- Audit trail: Complete movement history
- Valuation: GAAP compliance
- Tax: Inventory for tax reporting
- Industry: Lot/serial tracking capability

## Evolution Potential

### Enhancement Opportunities
- Barcode/RFID integration: Automated data capture
- Mobile warehouse app: Real-time floor updates
- Lot/serial tracking: Enhanced traceability
- Multiple locations: Warehouse expansion
- Min/max by season: Dynamic reorder points

### Modernization Candidates
- Web-based interface: Modern UI
- REST APIs: WMS integration
- Cloud deployment: Scalability
- Real-time analytics: Inventory insights
- IoT integration: Automated monitoring

### Known Limitations
- Single location per item
- No lot/serial tracking
- No bin-level control
- Basic reorder logic
- Character interface only
- No barcode support
- Average cost only

## Risk Assessment

### Technical Risks
- File locking with concurrent updates
- Cost calculation precision
- Integration timing issues
- Audit trail gaps

### Business Risks
- Stock-out situations
- Excess inventory costs
- Shrinkage/loss tracking
- Valuation accuracy

### Mitigation Strategies
- Cycle counting program
- Safety stock policies
- Exception reporting
- Regular reconciliation
- Backup stock locations

## Special Considerations

### Service Items
- No quantity tracking
- No stock movements
- Value for reporting only
- Examples: Consultancy, maintenance

### Work in Progress
- Tracks items in production
- Not available for sale
- Included in valuation
- Requires manual updates

### Multi-Supplier Management
- Up to 3 suppliers per item
- Cost comparison capability
- Lead time tracking
- Preferred supplier selection

---

Document Version: 1.0
Subsystem Version: ST v3.02
Analysis Date: December 2024