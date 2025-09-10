# ACAS Accounting-Specific Analysis

## 1. Compliance and Controls

### 1.1 Segregation of Duties Implementation

The ACAS system implements segregation of duties through its modular design and menu structure:

#### Module-Based Segregation
- **Sales Functions**: Order entry separate from cash receipts
- **Purchase Functions**: Order creation separate from payment processing  
- **General Ledger**: Journal entry separate from posting
- **System Administration**: Parameter setup separate from transaction processing

#### Process Controls
- **Invoice Entry**: Can be separated from posting (sl910 vs sl060)
- **Payment Selection**: Separate from payment execution (pl080 vs pl100)
- **Batch Processing**: Entry, proofing, and posting as distinct steps

### 1.2 Audit Trail Completeness

#### Transaction Tracking
Every transaction maintains:
- **Creation Date**: When entered into system
- **Posting Date**: When posted to ledger
- **Batch Number**: For grouping and control
- **Source Document**: Invoice/payment reference
- **User ID**: Limited (system-wide rather than user-specific)

#### Stock Audit Trail
- Every movement recorded in AUDIT-REC
- Source type (sales, purchase, adjustment)
- Date, quantity, and value changes
- Running balances maintained

#### Posting Audit
- All GL/IRS postings retain:
  - Original transaction details
  - Account codes (debit and credit)
  - Amounts including VAT breakdown
  - Transaction narrative/legend

### 1.3 Data Validation Rules

#### Master File Validation
- **Customer/Supplier Codes**: 7-character with check digit validation
- **Account Numbers**: Must exist in Chart of Accounts
- **Stock Codes**: 13-character unique identifiers
- **VAT Codes**: Limited to configured options

#### Transaction Validation
- **Date Validation**: 
  - Must be valid calendar date
  - Cannot be before last period end
  - Warning if future date
- **Amount Validation**:
  - Non-negative amounts required
  - Credit notes require existing invoice
  - Payments cannot exceed invoice amount
- **Batch Balancing**:
  - Debits must equal credits
  - VAT calculations verified
  - Control totals maintained

### 1.4 Approval Workflows

Current system limitations:
- No built-in electronic approval workflows
- Manual approval processes assumed
- Batch control provides review point
- Posting step acts as approval gate

### 1.5 Security Controls

#### Current Implementation
- File-level access control (OS dependent)
- No user authentication within application
- No role-based permissions
- Limited password protection

#### Audit Recommendations
- Implement user authentication
- Add role-based access control
- Enable transaction-level user tracking
- Implement password policies

### 1.6 Regulatory Compliance Features

#### UK VAT Compliance
- Multiple VAT rates supported
- Separate Input/Output VAT accounts
- VAT return preparation data
- Invoice VAT breakdown
- VAT-inclusive/exclusive calculations

#### Financial Reporting Standards
- Double-entry bookkeeping enforced
- Period-based accounting
- Accruals concept supported
- Going concern basis
- Consistency principle

## 2. Calculation Engine Documentation

### 2.1 VAT Calculations

#### VAT Calculation Methods

**From Net Amount**:
```
VAT Amount = Net Amount × (VAT Rate ÷ 100)
Gross Amount = Net Amount + VAT Amount
```

**From Gross Amount**:
```
VAT Amount = Gross Amount × (VAT Rate ÷ (100 + VAT Rate))
Net Amount = Gross Amount - VAT Amount
```

#### VAT Codes and Rates
- **Standard Rate**: Configured in system parameters (e.g., 20%)
- **Reduced Rate**: Configured separately (e.g., 5%)
- **Zero Rate**: 0% but VAT-registered transaction
- **Exempt**: No VAT applicable

#### VAT Posting Logic
```
Sales Invoice:
  DR Customer Account     (Gross Amount)
  CR Sales Account       (Net Amount)
  CR Output VAT Account  (VAT Amount)

Purchase Invoice:
  DR Purchase Account    (Net Amount)
  DR Input VAT Account   (VAT Amount)
  CR Supplier Account    (Gross Amount)
```

### 2.2 Discount Calculations

#### Trade Discounts
Applied at line level:
```
Line Net = (Quantity × Unit Price) × (1 - Discount% ÷ 100)
```

#### Settlement Discounts
Applied at payment:
```
If Payment Date <= Invoice Date + Discount Days Then
  Discount = Invoice Amount × (Settlement Discount% ÷ 100)
  Payment Required = Invoice Amount - Discount
End If
```

#### Early Payment Discount VAT Adjustment
```
VAT Adjustment = Original VAT × (Discount ÷ Original Gross)
```

### 2.3 Currency Handling

Current system capabilities:
- Single currency per company
- No multi-currency support
- All amounts in 2 decimal places
- Maximum amount: 99,999,999.99

### 2.4 Pricing Logic

#### Customer-Specific Pricing
```
Price Selection Hierarchy:
1. Customer-specific price (if exists)
2. Customer discount % from list price
3. Standard list price
4. Cost plus markup (if configured)
```

#### Quantity Breaks
- Not implemented in current system
- All pricing is per unit basis

### 2.5 Interest/Late Charge Computation

#### Late Charge Calculation
```
If enabled in parameters:
  Days Overdue = Current Date - Due Date
  If Days Overdue > Grace Period Then
    If Balance > Minimum Late Balance Then
      Late Charge = Balance × (Monthly Rate ÷ 100)
      Subject to Maximum Late Charge
    End If
  End If
```

#### Application Timing
- Calculated during statement production
- Posted as separate transaction
- Can be waived manually

### 2.6 Cost and Valuation Methods

#### Average Cost Calculation
```
When receiving stock:
  Total Cost = (Existing Qty × Existing Avg Cost) + 
               (Receipt Qty × Receipt Cost)
  New Avg Cost = Total Cost ÷ (Existing Qty + Receipt Qty)
```

#### Stock Valuation
```
Stock Value = Quantity on Hand × Average Cost
Total Inventory Value = Sum of all Stock Values
```

#### FIFO Principle
- Physical stock movements assumed FIFO
- Cost calculation uses average method
- No specific cost tracking by batch

### 2.7 Depreciation Methods

Not implemented in current system. Fixed assets would require:
- Manual journal entries
- External calculation
- Period posting to GL/IRS

### 2.8 Tax Calculations Beyond VAT

#### Other Tax Considerations
- System designed for UK VAT only
- No sales tax matrices
- No withholding tax
- No multi-jurisdiction support

## 3. Period and Year-End Calculations

### 3.1 Aging Calculations

#### Standard Aging Buckets
```
Current: 0-30 days from invoice date
30 Days: 31-60 days overdue
60 Days: 61-90 days overdue  
90+ Days: Over 90 days overdue
```

#### Aging Logic
```
Days Outstanding = Report Date - Invoice Date
If Payment Terms = 30 Then
  Days Overdue = Days Outstanding - 30
Else
  Days Overdue = Days Outstanding - Payment Terms
End If
```

### 3.2 Period Accumulations

#### Sales/Purchase Ledger
- Current period transactions
- Four quarterly totals (Q1-Q4)
- Year-to-date calculations
- Last year comparatives

#### Stock Movements
- Period additions/deductions
- Month-within-year totals
- Year-to-date movements
- Quantity and value tracking

### 3.3 Financial Statement Calculations

#### Profit & Loss Compilation
```
For each P&L Account:
  If Credit Balance Then
    Add to Income
  Else
    Add to Expenses
  End If
End For
Net Profit = Total Income - Total Expenses
```

#### Balance Sheet Balancing
```
Total Assets = Fixed Assets + Current Assets
Total Liabilities = Long Term + Current Liabilities
Total Equity = Capital + Reserves + Current P&L
Verification: Assets = Liabilities + Equity
```

### 3.4 Year-End Closing Calculations

#### P&L Account Closure
```
For each P&L Account:
  Transfer Balance to Retained Earnings
  Set Account Balance to Zero
End For
```

#### Balance Sheet Carry Forward
```
For each BS Account:
  Prior Year Balance = Current Balance
  Clear Period Movements
  Maintain Running Balance
End For
```

## 4. Control and Reconciliation Features

### 4.1 Batch Controls
- Header totals vs detail totals
- Item count verification
- Net and VAT reconciliation
- Posting validation

### 4.2 Control Accounts
- Sales Control (Debtors)
- Purchase Control (Creditors)
- VAT Control accounts
- Stock Control account
- Must reconcile to subsidiary ledgers

### 4.3 Period Locks
- Prevent posting to closed periods
- Require supervisor override
- Maintain period integrity
- Support audit requirements

## 5. Compliance Gap Analysis

### 5.1 Current Strengths
- ✓ Complete audit trail
- ✓ Double-entry enforcement
- ✓ VAT compliance
- ✓ Period controls
- ✓ Batch balancing

### 5.2 Compliance Gaps
- ✗ User-level audit trail
- ✗ Electronic approvals
- ✗ Role-based security
- ✗ Automated controls testing
- ✗ Data encryption

### 5.3 Recommendations for Compliance Enhancement
1. Implement user authentication and tracking
2. Add approval workflow capabilities
3. Enhance security with encryption
4. Implement automated compliance reports
5. Add data retention policies
6. Enable real-time monitoring

## 6. Calculation Accuracy and Rounding

### 6.1 Rounding Rules
- All monetary amounts: 2 decimal places
- Quantities: 0-2 decimals per configuration
- Percentages: 2 decimal places
- VAT calculations: Round at line level

### 6.2 Calculation Precision
- Internal calculations: COBOL COMP-3
- Display format: Standard decimal
- No floating-point arithmetic
- Banker's rounding applied

This analysis confirms ACAS implements fundamental accounting principles with room for enhancement in security, compliance automation, and modern regulatory requirements.