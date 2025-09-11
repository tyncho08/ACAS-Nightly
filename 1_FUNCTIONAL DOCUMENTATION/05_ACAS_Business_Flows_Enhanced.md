# ACAS Business Flows Documentation

## Overview
This document describes the end-to-end business processes implemented in the ACAS system, including decision trees for complex logic, accounting period processing, and year-end procedures.

## Table of Contents
1. [Sales Cycle (Order to Cash)](#sales-cycle)
2. [Purchase Cycle (Procure to Pay)](#purchase-cycle)
3. [Inventory Management](#inventory-management)
4. [Financial Closing Process](#financial-closing)
5. [System Setup and Initialization](#system-setup)
6. [Integration Workflows](#integration-workflows)

---

## 1. Sales Cycle (Order to Cash)

### 1.1 Customer Setup Flow

```mermaid
flowchart TD
    Start([START]) --> sl010[sl010<br/>Customer Maintenance]
    sl010 --> Decision{New or<br/>Existing?}
    
    Decision -->|New Customer| NewCust[New Customer Setup]
    NewCust --> Code[Enter Customer Code<br/>7 characters]
    Code --> Credit[Set Credit Limit]
    Credit --> Terms[Define Payment Terms<br/>Days]
    Terms --> Discount[Set Discount %]
    Discount --> Late[Configure Late Charges]
    Late --> Delivery[Add Delivery Addresses]
    Delivery --> End1([END])
    
    Decision -->|Existing Customer| ExistCust[Existing Customer]
    ExistCust --> ViewMod[View/Modify Details]
    ViewMod --> CheckCredit[Check Credit Status]
    CheckCredit --> UpdateContact[Update Contact Info]
    UpdateContact --> End2([END])
    
    style Start fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
    style End1 fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
    style End2 fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
    style sl010 fill:#e6f3ff,stroke:#4a9eff,stroke-width:2px
    style Decision fill:#fff5cc,stroke:#ffc107,stroke-width:2px
```

### 1.2 Sales Order and Invoicing Flow

```mermaid
flowchart TD
    Order([Customer Order<br/>Received]) --> sl910[sl910/sl900<br/>Invoice Entry]
    
    sl910 --> Validate[Validate Customer]
    Validate --> CheckExists[Check Exists]
    CheckExists --> VerifyCredit[Verify Credit Limit]
    VerifyCredit --> CheckPayment[Check Payment Status]
    
    CheckPayment --> LineItems[Enter Line Items]
    LineItems --> StockCheck[Validate Stock<br/>Availability]
    StockCheck --> Pricing[Apply Pricing/<br/>Discounts]
    Pricing --> VAT[Calculate VAT]
    VAT --> BackOrder{Back Orders<br/>Needed?}
    
    BackOrder -->|Yes| HandleBO[Handle Back Orders]
    BackOrder -->|No| SaveInv[Save Invoice]
    HandleBO --> SaveInv
    
    SaveInv --> PrintMode{Print Mode?}
    PrintMode -->|Immediate| sl910Print[sl910<br/>Immediate Print]
    PrintMode -->|Batch| sl900Batch[sl900<br/>Batch Processing]
    
    sl910Print --> sl055[sl055<br/>Invoice Proof]
    sl900Batch --> sl055
    
    sl055 --> ValidateTotals[Validate Totals]
    ValidateTotals --> CheckCodes[Check Analysis Codes]
    CheckCodes --> ReviewErrors[Review for Errors]
    
    ReviewErrors --> sl060[sl060<br/>Invoice Posting]
    sl060 --> UpdateCust[Update Customer<br/>Balance]
    UpdateCust --> OpenItems[Create Open Items]
    OpenItems --> UpdateStock[Update Stock<br/>Quantities]
    UpdateStock --> GLPost[Generate GL/IRS<br/>Postings]
    
    GLPost --> Entries[["DR: Customer Account<br/>CR: Sales Account<br/>CR: VAT Account"]]
    
    style Order fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
    style sl910 fill:#e6f3ff,stroke:#4a9eff,stroke-width:2px
    style sl055 fill:#e6f3ff,stroke:#4a9eff,stroke-width:2px
    style sl060 fill:#e6f3ff,stroke:#4a9eff,stroke-width:2px
    style BackOrder fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style PrintMode fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style Entries fill:#e1f5e1,stroke:#4caf50,stroke-width:2px
```

### 1.3 Customer Payment Processing

```mermaid
flowchart TD
    Payment([Payment<br/>Received]) --> sl080[sl080<br/>Payment Entry]
    
    sl080 --> SelectCust[Select Customer]
    SelectCust --> PayDetails[Enter Payment Details]
    
    PayDetails --> Amount[Amount]
    Amount --> CheckRef[Check/Reference<br/>Number]
    CheckRef --> PayDate[Payment Date]
    
    PayDate --> Allocate[Allocate to Invoices]
    Allocate --> AllocMethod{Allocation<br/>Method?}
    
    AllocMethod -->|Automatic| AutoAlloc[Oldest First]
    AllocMethod -->|Manual| ManualSelect[Manual Selection]
    
    AutoAlloc --> DiscountCheck{Early Payment<br/>Discount?}
    ManualSelect --> DiscountCheck
    
    DiscountCheck -->|Yes| CalcDiscount[Calculate Discount]
    DiscountCheck -->|No| sl085[sl085<br/>Payment Proof]
    CalcDiscount --> ApplyDiscount[Apply if Within Terms]
    ApplyDiscount --> sl085
    
    sl085 --> VerifyAlloc[Verify Allocations]
    VerifyAlloc --> CheckTotals[Check Totals]
    
    CheckTotals --> sl100[sl100<br/>Cash Posting]
    sl100 --> ClearInv[Clear Paid Invoices]
    ClearInv --> UpdateBal[Update Customer<br/>Balance]
    UpdateBal --> PostGL[Post to GL/IRS]
    
    PostGL --> CashEntries[["DR: Bank Account<br/>CR: Customer Account"]]
    
    style Payment fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
    style sl080 fill:#e6f3ff,stroke:#4a9eff,stroke-width:2px
    style sl085 fill:#e6f3ff,stroke:#4a9eff,stroke-width:2px
    style sl100 fill:#e6f3ff,stroke:#4a9eff,stroke-width:2px
    style AllocMethod fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style DiscountCheck fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style CashEntries fill:#e1f5e1,stroke:#4caf50,stroke-width:2px
```

### 1.4 Credit Control Decision Tree

```mermaid
flowchart TD
    Start([Monthly Credit Review]) --> sl120[sl120<br/>Aged Debtors Report]
    
    sl120 --> Aging{Account<br/>Age?}
    
    Aging -->|0-30 Days| Current[Current]
    Current --> NoAction1[No Action Required]
    NoAction1 --> End1([END])
    
    Aging -->|30-60 Days| Days30[30-60 Days Overdue]
    Days30 --> Statement1[Generate Statement<br/>sl110]
    Statement1 --> End2([END])
    
    Aging -->|60-90 Days| Days60[60-90 Days Overdue]
    Days60 --> Statement2[Generate Statement]
    Statement2 --> FirstLetter[First Dunning Letter<br/>sl190]
    FirstLetter --> End3([END])
    
    Aging -->|90+ Days| Days90[90+ Days Overdue]
    Days90 --> FinalLetter[Final Dunning Letter]
    FinalLetter --> LateCheck{Balance ><br/>Minimum?}
    
    LateCheck -->|Yes| ApplyCharges[Apply Late Charges]
    LateCheck -->|No| CreditHold{Charges ><br/>Threshold?}
    
    ApplyCharges --> CreditHold
    CreditHold -->|Yes| HoldAccount[Consider Credit Hold]
    CreditHold -->|No| End4([END])
    HoldAccount --> End5([END])
    
    style Start fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
    style sl120 fill:#e6f3ff,stroke:#4a9eff,stroke-width:2px
    style Aging fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style LateCheck fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style CreditHold fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style Current fill:#e1f5e1,stroke:#4caf50,stroke-width:2px
    style Days30 fill:#fff2e6,stroke:#ff9800,stroke-width:2px
    style Days60 fill:#ffe6f0,stroke:#e91e63,stroke-width:2px
    style Days90 fill:#ffcccc,stroke:#f44336,stroke-width:2px
```

---

## 2. Purchase Cycle (Procure to Pay)

### 2.1 Supplier Setup Flow

```mermaid
flowchart TD
    Start([START]) --> pl010[pl010<br/>Supplier Maintenance]
    
    pl010 --> NewSupp[New Supplier Setup]
    NewSupp --> SuppCode[Enter Supplier Code<br/>7 characters]
    SuppCode --> BankDetails[Bank Details]
    BankDetails --> SortCode[Sort Code]
    SortCode --> AccNumber[Account Number]
    AccNumber --> CreditTerms[Credit Terms]
    CreditTerms --> PayDiscount[Payment Discount %]
    PayDiscount --> ContactInfo[Contact Information]
    
    ContactInfo --> LinkStock{Link to<br/>Stock Items?}
    LinkStock -->|Yes| st010[st010<br/>Stock Maintenance]
    LinkStock -->|No| End1([END])
    st010 --> LinkSupp[Link up to 3<br/>Suppliers per Item]
    LinkSupp --> End2([END])
    
    style Start fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
    style pl010 fill:#ffe6f0,stroke:#e91e63,stroke-width:2px
    style st010 fill:#e6ccff,stroke:#9c27b0,stroke-width:2px
    style LinkStock fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style End1 fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
    style End2 fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
```

### 2.2 Purchase Order Flow

```mermaid
flowchart TD
    Requirement([Purchase<br/>Requirement]) --> pl020[pl020/pl900<br/>Order Entry]
    
    pl020 --> SelectSupp[Select Supplier]
    SelectSupp --> OrderDetails[Enter Order Details]
    
    OrderDetails --> OrderDate[Order Date]
    OrderDate --> ReqDate[Required Date]
    ReqDate --> DelivInstr[Delivery Instructions]
    
    DelivInstr --> AddItems[Add Line Items]
    AddItems --> ProdCode[Product/Service Code]
    ProdCode --> Quantity[Quantity]
    Quantity --> UnitPrice[Unit Price]
    UnitPrice --> VATCode[VAT Code]
    
    VATCode --> SaveOrder[Save Order]
    SaveOrder --> PrintOpt{Print Option?}
    
    PrintOpt -->|Immediate| pl910[pl910<br/>Print Immediately]
    PrintOpt -->|Batch| pl900[pl900<br/>Batch Processing]
    
    pl910 --> pl025[pl025<br/>Goods Receipt]
    pl900 --> pl025
    
    pl025 --> MatchOrder[Match to Order]
    MatchOrder --> RecDate[Record Receipt Date]
    RecDate --> UpdateQty[Update Quantities<br/>Received]
    UpdateQty --> FlagPay[Flag for Payment]
    
    FlagPay --> pl050[pl050<br/>Proof Report]
    pl050 --> Review[Review Before Posting]
    
    Review --> pl060[pl060<br/>Invoice Posting]
    pl060 --> UpdateSupp[Update Supplier<br/>Balance]
    UpdateSupp --> CreatePay[Create Payable Items]
    CreatePay --> StockUpdate{Update<br/>Stock?}
    
    StockUpdate -->|Yes| UpdateInv[Update Inventory]
    StockUpdate -->|No| PostGL[Post to GL/IRS]
    UpdateInv --> PostGL
    
    PostGL --> PurchEntries[["DR: Purchase/Expense Account<br/>DR: VAT Account<br/>CR: Supplier Account"]]
    
    style Requirement fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
    style pl020 fill:#ffe6f0,stroke:#e91e63,stroke-width:2px
    style pl025 fill:#ffe6f0,stroke:#e91e63,stroke-width:2px
    style pl050 fill:#ffe6f0,stroke:#e91e63,stroke-width:2px
    style pl060 fill:#ffe6f0,stroke:#e91e63,stroke-width:2px
    style PrintOpt fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style StockUpdate fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style PurchEntries fill:#e1f5e1,stroke:#4caf50,stroke-width:2px
```

### 2.3 Payment Processing Flow

```mermaid
flowchart TD
    Due([Payment Due]) --> pl080[pl080<br/>Payment Selection]
    
    pl080 --> AutoSelect[Auto-select by<br/>Due Date]
    AutoSelect --> DiscountConsider{Consider<br/>Discounts?}
    
    DiscountConsider -->|Yes| CheckTerms[If Paid Within Terms]
    DiscountConsider -->|No| CashReq[Review Cash<br/>Requirements]
    CheckTerms --> CashReq
    
    CashReq --> pl085[pl085<br/>Payment Amendment]
    pl085 --> AdjustSel[Adjust Selections]
    AdjustSel --> SetPayDate[Set Payment Date]
    
    SetPayDate --> pl095[pl095<br/>Check Printing]
    pl095 --> PrintChecks[Print Checks]
    PrintChecks --> RemitAdvice[Generate<br/>Remittance Advice]
    
    RemitAdvice --> pl100[pl100<br/>Payment Posting]
    pl100 --> ClearInv[Clear Paid Invoices]
    ClearInv --> UpdateSupp[Update Supplier<br/>Balance]
    UpdateSupp --> PostEntries[Post to GL/IRS]
    
    PostEntries --> PayEntries[["DR: Supplier Account<br/>CR: Bank Account"]]
    
    style Due fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
    style pl080 fill:#ffe6f0,stroke:#e91e63,stroke-width:2px
    style pl085 fill:#ffe6f0,stroke:#e91e63,stroke-width:2px
    style pl095 fill:#ffe6f0,stroke:#e91e63,stroke-width:2px
    style pl100 fill:#ffe6f0,stroke:#e91e63,stroke-width:2px
    style DiscountConsider fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style PayEntries fill:#e1f5e1,stroke:#4caf50,stroke-width:2px
```

---

## 3. Inventory Management

### 3.1 Stock Item Setup

```mermaid
flowchart TD
    Start([START]) --> st010[st010<br/>Stock Maintenance]
    
    st010 --> ItemIdent[Item Identification]
    ItemIdent --> StockCode[Stock Code<br/>13 characters]
    StockCode --> Description[Description]
    Description --> Location[Location]
    
    Location --> Valuation[Valuation]
    Valuation --> CostPrice[Cost Price]
    CostPrice --> SellPrice[Selling Price]
    SellPrice --> ValMethod[Valuation Method]
    
    ValMethod --> ReorderParams[Reorder Parameters]
    ReorderParams --> ReorderLevel[Reorder Level]
    ReorderLevel --> ReorderQty[Reorder Quantity]
    ReorderQty --> LeadTime[Lead Time]
    
    LeadTime --> SuppLinks[Supplier Links]
    SuppLinks --> Supp3[Up to 3 Suppliers]
    Supp3 --> End([END])
    
    style Start fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
    style st010 fill:#e6ccff,stroke:#9c27b0,stroke-width:2px
    style End fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
```

### 3.2 Stock Movement Flow

```mermaid
flowchart TD
    Trigger([Movement<br/>Trigger]) --> Type{Movement<br/>Type?}
    
    Type -->|Sales| SalesAuto[Automatic from<br/>Invoice Posting]
    Type -->|Purchases| PurchAuto[Automatic from<br/>Goods Receipt]
    Type -->|Manual| st020[st020<br/>Stock Movements]
    
    SalesAuto --> UpdateProc[Stock Update<br/>Process]
    PurchAuto --> UpdateProc
    st020 --> UpdateProc
    
    UpdateProc --> ValidateQty[Validate Quantity<br/>Available]
    ValidateQty --> UpdateLevels[Update Stock Levels]
    
    UpdateLevels --> OnHand[Quantity on Hand]
    OnHand --> Allocated[Allocated Quantity]
    Allocated --> Available[Available Quantity]
    
    Available --> CalcValue[Calculate New Value]
    CalcValue --> AvgCost[Average Cost Method]
    
    AvgCost --> CreateAudit[Create Audit Record]
    CreateAudit --> DateTime[Date/Time]
    DateTime --> MovType[Movement Type]
    MovType --> SourceDoc[Source Document]
    SourceDoc --> QtyValue[Quantity/Value]
    QtyValue --> End([END])
    
    style Trigger fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
    style Type fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style st020 fill:#e6ccff,stroke:#9c27b0,stroke-width:2px
    style UpdateProc fill:#e1f5e1,stroke:#4caf50,stroke-width:2px
    style End fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
```

### 3.3 Reorder Decision Process

```mermaid
flowchart TD
    Start([Daily Review]) --> st030[st030<br/>Reorder Report]
    
    st030 --> Loop{For Each<br/>Item}
    
    Loop --> CheckQty{Available Qty <<br/>Reorder Level?}
    
    CheckQty -->|YES| GenReorder[Generate Reorder]
    CheckQty -->|NO| NextItem1[Next Item]
    
    GenReorder --> SuggestQty[Suggested Qty =<br/>Reorder Qty]
    SuggestQty --> CheckOnOrder[Check On-Order Qty]
    CheckOnOrder --> SelectSupp[Select Supplier]
    
    SelectSupp --> Consider[Consider Factors]
    Consider --> LeadTime[Lead Time]
    LeadTime --> Seasonal[Seasonal Adjustments]
    Seasonal --> BackOrders[Back Orders Pending]
    
    BackOrders --> NextItem2[Next Item]
    NextItem1 --> Loop
    NextItem2 --> Loop
    
    Loop -->|All Items<br/>Processed| Report[Generate<br/>Reorder Report]
    Report --> End([END])
    
    style Start fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
    style st030 fill:#e6ccff,stroke:#9c27b0,stroke-width:2px
    style Loop fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style CheckQty fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style Report fill:#e1f5e1,stroke:#4caf50,stroke-width:2px
    style End fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
```

---

## 4. Financial Closing Process

### 4.1 Daily Closing

```mermaid
flowchart LR
    subgraph "Start of Day"
        ModStart[Each Module<br/>Start of Day] --> Programs[*000 Programs]
        Programs --> SetDate[Set System Date]
        SetDate --> ValidSeq[Validate Date<br/>Sequence]
        ValidSeq --> InitOps[Initialize Daily<br/>Operations]
    end
    
    subgraph "End of Day"
        CompTrans[Complete All<br/>Transactions] --> RunProof[Run Proof<br/>Reports]
        RunProof --> PostBatch[Post All<br/>Batches]
        PostBatch --> Backup[Backup<br/>Manual/Scripted]
    end
    
    InitOps -.-> CompTrans
    
    style ModStart fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
    style Backup fill:#e1f5e1,stroke:#4caf50,stroke-width:2px
```

### 4.2 Period End Processing

```mermaid
flowchart TD
    Start([Period End]) --> Modules{Select<br/>Module}
    
    Modules -->|Sales| SalesPE[Sales Ledger<br/>Period End]
    Modules -->|Purchase| PurchPE[Purchase Ledger<br/>Period End]
    Modules -->|Stock| StockPE[Stock<br/>Period End]
    Modules -->|GL| GLPE[General Ledger<br/>Period End]
    
    %% Sales Period End
    SalesPE --> sl120A[sl120<br/>Aged Debtors]
    sl120A --> AgeAll[Age All Balances]
    AgeAll --> CalcLate[Calculate Late Charges]
    CalcLate --> sl110A[sl110<br/>Statements]
    sl110A --> GenState[Generate for<br/>All/Selected]
    GenState --> PrintEmail1[Print/Email]
    PrintEmail1 --> sl130A[sl130<br/>Product Analysis]
    sl130A --> SalesProd[Sales by<br/>Product/Service]
    SalesProd --> UpdateSales[Update Period<br/>Totals]
    
    %% Purchase Period End
    PurchPE --> pl120A[pl120<br/>Aged Creditors]
    pl120A --> ReviewPay[Review Payment<br/>Obligations]
    ReviewPay --> pl130A[pl130<br/>Product Analysis]
    pl130A --> PurchCat[Purchases by<br/>Category]
    PurchCat --> UpdatePurch[Update Period<br/>Totals]
    
    %% Stock Period End
    StockPE --> st040A[st040<br/>End of Cycle]
    st040A --> ClearMove[Clear Period<br/>Movements]
    ClearMove --> Add[Additions]
    Add --> Ded[Deductions]
    Ded --> Adj[Adjustments]
    Adj --> UpdateMonth[Update Month-<br/>in-Year Totals]
    UpdateMonth --> st030A[st030<br/>Valuation Report]
    st030A --> DocValue[Document Ending<br/>Inventory Value]
    
    %% GL Period End
    GLPE --> gl080A[gl080<br/>End of Cycle]
    gl080A --> VerifyBatch[Verify All<br/>Batches Posted]
    VerifyBatch --> Archive[Archive<br/>Transactions]
    Archive --> SeqFile[To Sequential File]
    SeqFile --> ClearPost[Clear Posting File]
    ClearPost --> UpdateQuart[Update Quarterly<br/>Totals]
    UpdateQuart --> gl090A[gl090<br/>Trial Balance]
    gl090A --> VerifyBal[Verify<br/>Debits = Credits]
    VerifyBal --> FinState[gl100/105<br/>Financial Statements]
    FinState --> PL[Profit & Loss]
    PL --> BS[Balance Sheet]
    
    UpdateSales --> Complete1([Complete])
    UpdatePurch --> Complete2([Complete])
    DocValue --> Complete3([Complete])
    BS --> Complete4([Complete])
    
    style Start fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
    style Modules fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style SalesPE fill:#e6f3ff,stroke:#4a9eff,stroke-width:2px
    style PurchPE fill:#ffe6f0,stroke:#e91e63,stroke-width:2px
    style StockPE fill:#e6ccff,stroke:#9c27b0,stroke-width:2px
    style GLPE fill:#e6ffe6,stroke:#4caf50,stroke-width:2px
```

### 4.3 Year End Processing

```mermaid
flowchart TD
    subgraph "Pre-Year End Checklist"
        Check1[Complete All<br/>Period Ends] --> Check2[Run Year-End<br/>Reports]
        Check2 --> Reports[Annual P&L<br/>Balance Sheet<br/>Analysis Reports<br/>Stock Valuation]
        Reports --> Check3[Full System<br/>Backup]
        Check3 --> Check4[Archive Current<br/>Year Data]
    end
    
    Check4 --> xl150[xl150<br/>End of Cycle<br/>All Modules]
    
    xl150 --> SLYear[Sales Ledger<br/>Year End]
    xl150 --> PLYear[Purchase Ledger<br/>Year End]
    xl150 --> STYear[Stock Control<br/>Year End]
    xl150 --> GLYear[General Ledger<br/>Year End]
    
    SLYear --> SLTasks[Clear Quarterly Totals<br/>Move Current to Last Year<br/>Reset YTD Counters]
    PLYear --> PLTasks[Similar to Sales]
    STYear --> STTasks[Clear YTD Movements<br/>Carry Forward Balances]
    GLYear --> GLTasks[Close P&L Accounts<br/>Post to Retained Earnings<br/>Carry Forward BS Accounts]
    
    xl150 --> IRSSpec{IRS Special<br/>Process?}
    IRSSpec -->|Yes| irs090[irs090<br/>End of Period]
    irs090 --> ClearOpt{Clear<br/>Transactions?}
    ClearOpt -->|Yes| AfterArch[After Archiving]
    ClearOpt -->|No| CarryFwd[Carry Forward<br/>Balances]
    AfterArch --> CarryFwd
    CarryFwd --> ResetCount[Reset Period<br/>Counters]
    
    SLTasks --> Complete([Year End<br/>Complete])
    PLTasks --> Complete
    STTasks --> Complete
    GLTasks --> Complete
    ResetCount --> Complete
    IRSSpec -->|No| Complete
    
    style Check1 fill:#fff2e6,stroke:#ff9800,stroke-width:2px
    style xl150 fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
    style IRSSpec fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style ClearOpt fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style Complete fill:#e1f5e1,stroke:#4caf50,stroke-width:2px
```

---

## 5. System Setup and Initialization

### 5.1 Initial System Setup Flow

```mermaid
flowchart TD
    Install([New Installation]) --> CreateSys[Create system.dat]
    
    CreateSys --> CompInfo[Company Information]
    CompInfo --> VATReg[VAT Registration]
    VATReg --> FinYear[Financial Year Dates]
    FinYear --> ModActive[Module Activation]
    
    ModActive --> EachMod{For Each<br/>Active Module}
    
    EachMod -->|IRS| IRSSetup[IRS Setup]
    IRSSetup --> irs010A[irs010<br/>Chart of Accounts]
    irs010A --> irs020A[irs020<br/>Posting Defaults]
    
    EachMod -->|GL| GLSetup[GL Setup]
    GLSetup --> gl030A[gl030<br/>Chart of Accounts]
    gl030A --> gl020A[gl020<br/>Default Accounts]
    
    EachMod -->|Sales| SalesSetup[Sales Setup]
    SalesSetup --> SLControl[Set Control Accounts]
    SLControl --> InvNumber[Invoice Numbering]
    InvNumber --> CreditDef[Credit Defaults]
    
    EachMod -->|Purchase| PurchSetup[Purchase Setup]
    PurchSetup --> PLControl[Set Control Accounts]
    PLControl --> PayTerms[Payment Terms]
    
    EachMod -->|Stock| StockSetup[Stock Setup]
    StockSetup --> ValMethod[Valuation Method]
    ValMethod --> MoveTrack[Movement Tracking]
    
    irs020A --> Ready1([Module Ready])
    gl020A --> Ready2([Module Ready])
    CreditDef --> Ready3([Module Ready])
    PayTerms --> Ready4([Module Ready])
    MoveTrack --> Ready5([Module Ready])
    
    style Install fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
    style EachMod fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style IRSSetup fill:#fff2e6,stroke:#ff9800,stroke-width:2px
    style GLSetup fill:#e6ffe6,stroke:#4caf50,stroke-width:2px
    style SalesSetup fill:#e6f3ff,stroke:#4a9eff,stroke-width:2px
    style PurchSetup fill:#ffe6f0,stroke:#e91e63,stroke-width:2px
    style StockSetup fill:#e6ccff,stroke:#9c27b0,stroke-width:2px
```

### 5.2 Data Migration Flow

```mermaid
flowchart TD
    Legacy([Legacy System<br/>Data]) --> Prep[File Preparation]
    
    Prep --> Export[Export to<br/>CSV/Text]
    Export --> MapFields[Map Field<br/>Relationships]
    
    MapFields --> LoadProg[Load Programs<br/>*LD series]
    
    LoadProg --> CustData[Customer Data<br/>→ salesLD]
    LoadProg --> SuppData[Supplier Data<br/>→ purchLD]
    LoadProg --> StockData[Stock Items<br/>→ stockLD]
    LoadProg --> CoAData[Chart of Accounts<br/>→ nominalLD]
    LoadProg --> OpenBal[Opening Balances<br/>→ Manual Entry]
    
    CustData --> Valid[Validation]
    SuppData --> Valid
    StockData --> Valid
    CoAData --> Valid
    OpenBal --> Valid
    
    Valid --> RunTB[Run Trial Balance]
    RunTB --> VerifyTotals[Verify Control<br/>Totals]
    VerifyTotals --> TestTrans[Test Transactions]
    TestTrans --> Complete([Migration<br/>Complete])
    
    style Legacy fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
    style LoadProg fill:#e1f5e1,stroke:#4caf50,stroke-width:2px
    style Valid fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style Complete fill:#e1f5e1,stroke:#4caf50,stroke-width:2px
```

---

## 6. Integration Workflows

### 6.1 Sales to Stock Integration

```mermaid
flowchart TD
    InvEntry([Invoice Line<br/>Item Entry]) --> CheckStock{Check Stock<br/>Availability}
    
    CheckStock -->|Available| AllocQty[Allocate Quantity]
    CheckStock -->|Not Available| CreateBO[Create Back Order]
    CreateBO --> FlagFulfill[Flag for<br/>Fulfillment]
    
    AllocQty --> InvPost[Invoice Posting]
    FlagFulfill --> InvPost
    
    InvPost --> ReduceStock[Reduce Stock<br/>Quantity]
    ReduceStock --> UpdateHand[Update On-Hand]
    UpdateHand --> CreateMove[Create Movement<br/>Record]
    CreateMove --> RecalcValue[Recalculate Value]
    RecalcValue --> Complete([Complete])
    
    style InvEntry fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
    style CheckStock fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style Complete fill:#e1f5e1,stroke:#4caf50,stroke-width:2px
```

### 6.2 Purchase to Stock Integration

```mermaid
flowchart TD
    GoodsRec([Goods Receipt]) --> UpdateOrder[Update On-Order<br/>Quantity]
    UpdateOrder --> IncreaseHand[Increase On-Hand<br/>Quantity]
    IncreaseHand --> UpdateCost[Update Last Cost]
    UpdateCost --> RecalcAvg[Recalculate<br/>Average Cost]
    
    RecalcAvg --> CheckBO{Check Back<br/>Orders}
    CheckBO -->|Stock Available| AllocBO[Allocate to<br/>Back Orders]
    CheckBO -->|No BO| Complete([Complete])
    
    AllocBO --> NotifySales[Notify Sales]
    NotifySales --> Complete
    
    style GoodsRec fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
    style CheckBO fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style Complete fill:#e1f5e1,stroke:#4caf50,stroke-width:2px
```

### 6.3 Subsidiary to General Ledger Flow

```mermaid
flowchart TD
    Trans([Transaction Entry<br/>Any Module]) --> PostProc[Posting Process]
    
    PostProc --> CreateRec[Create Posting<br/>Records]
    CreateRec --> AccCodes[Account Codes]
    AccCodes --> Amounts[Amounts]
    Amounts --> VATDetails[VAT Details]
    
    VATDetails --> CheckParam{System<br/>Parameter<br/>Check}
    
    CheckParam -->|GL Only| PostGL[Post to GL]
    CheckParam -->|IRS Only| PostIRS[Post to IRS]
    CheckParam -->|Both| PostBoth[Post to Both]
    
    PostBoth --> PostGL
    PostBoth --> PostIRS
    
    PostGL --> GLUpdate[Update GL<br/>Accounts]
    PostIRS --> IRSUpdate[Update IRS<br/>Accounts]
    
    GLUpdate --> Complete([Complete])
    IRSUpdate --> Complete
    
    style Trans fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
    style CheckParam fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style Complete fill:#e1f5e1,stroke:#4caf50,stroke-width:2px
```

### 6.4 VAT Processing Flow

```mermaid
flowchart TD
    TransVAT([Transaction<br/>with VAT]) --> DetermineCode[Determine<br/>VAT Code]
    
    DetermineCode --> CodeType{VAT Code<br/>Type}
    CodeType -->|Standard| StdRate[Standard Rate]
    CodeType -->|Reduced| RedRate[Reduced Rate]
    CodeType -->|Zero/Exempt| ZeroRate[Zero/Exempt]
    
    StdRate --> CalcVAT[Calculate VAT]
    RedRate --> CalcVAT
    ZeroRate --> NoVAT[No VAT Calc]
    
    CalcVAT --> FromWhat{Calculate<br/>From?}
    FromWhat -->|Net| FromNet[From Net Amount]
    FromWhat -->|Gross| FromGross[From Gross Amount]
    
    FromNet --> PostVAT[Post VAT]
    FromGross --> PostVAT
    NoVAT --> Continue[Continue<br/>Processing]
    
    PostVAT --> VATType{VAT Type?}
    VATType -->|Input| InputVAT[Input VAT<br/>To Account 31]
    VATType -->|Output| OutputVAT[Output VAT<br/>To Account 32]
    
    InputVAT --> PeriodEnd[Period End VAT]
    OutputVAT --> PeriodEnd
    Continue --> PeriodEnd
    
    PeriodEnd --> VATReturn[VAT Return<br/>Preparation]
    VATReturn --> InVsOut[Input vs Output]
    InVsOut --> PayRefund[Payment/Refund<br/>Calculation]
    
    style TransVAT fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
    style CodeType fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style FromWhat fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style VATType fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style PayRefund fill:#e1f5e1,stroke:#4caf50,stroke-width:2px
```

### 6.5 Multi-Company Processing

```mermaid
flowchart LR
    SysStart([System Start]) --> SelectCo{Select<br/>Company}
    
    SelectCo -->|Single| LoadSingle[Load Company<br/>Parameters]
    SelectCo -->|Multiple| SelectWhich[Select Which<br/>Company]
    
    SelectWhich --> LoadParams[Load Company<br/>Parameters]
    LoadSingle --> Trans[Transactions]
    LoadParams --> Trans
    
    Trans --> UsePC[All Use Profit<br/>Center Codes]
    UsePC --> SepByCo[Separate by<br/>Company]
    
    SepByCo --> Reporting[Reporting]
    Reporting --> ReportType{Report<br/>Type}
    
    ReportType -->|By PC| ByPC[By Profit Center]
    ReportType -->|Consolidated| Consol[Consolidated Option]
    ReportType -->|Inter-Co| InterCo[Inter-Company<br/>Eliminations]
    
    style SysStart fill:#4a9eff,stroke:#2a3f5f,stroke-width:2px,color:#fff
    style SelectCo fill:#fff5cc,stroke:#ffc107,stroke-width:2px
    style ReportType fill:#fff5cc,stroke:#ffc107,stroke-width:2px
```

## Key Business Rules

### Credit Management
- Credit limit checked on order entry
- Overdue accounts flagged in red
- Automatic late charge calculation
- Payment terms enforcement

### Inventory Control  
- No negative stock allowed
- FIFO for physical movement
- Average cost for valuation
- Automatic reorder point monitoring

### Financial Control
- Batches must balance (DR = CR)
- Periods locked after closing
- Audit trail mandatory
- No deletion after posting

### VAT Compliance
- Correct VAT code required
- VAT calculated automatically
- Separate VAT accounts maintained
- VAT return data available

This document provides the essential business flows. Each flow can be customized through system parameters and business rules embedded in the programs.