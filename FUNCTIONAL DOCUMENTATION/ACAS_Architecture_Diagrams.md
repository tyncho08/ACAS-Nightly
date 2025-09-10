# ACAS System Architecture Diagrams

## 1. System Overview - Module Architecture

```mermaid
graph TB
    %% Main Entry Points
    ACAS[ACAS Main Menu]
    
    %% Sub-system Entry Points
    IRS[IRS Menu<br/>Incomplete Records]
    SL[Sales Ledger Menu<br/>Accounts Receivable]
    PL[Purchase Ledger Menu<br/>Accounts Payable]
    ST[Stock Control Menu<br/>Inventory Mgmt]
    GL[General Ledger Menu<br/>Full Accounting]
    
    %% System Components
    SYS[System Parameters<br/>sys002/acas000]
    DAL[Data Access Layer]
    
    %% Main connections
    ACAS --> IRS
    ACAS --> SL
    ACAS --> PL
    ACAS --> ST
    ACAS --> GL
    ACAS --> SYS
    
    %% System Parameter connections
    IRS --> SYS
    SL --> SYS
    PL --> SYS
    ST --> SYS
    GL --> SYS
    
    %% DAL connections
    IRS --> DAL
    SL --> DAL
    PL --> DAL
    ST --> DAL
    GL --> DAL
    
    %% Data Storage
    DAL --> FILES[COBOL Files<br/>ISAM/Sequential]
    DAL --> DB[(MySQL/MariaDB<br/>Database)]
    
    style ACAS fill:#e1f5e1
    style IRS fill:#fff2e6
    style SL fill:#e6f3ff
    style PL fill:#ffe6f0
    style ST fill:#f0e6ff
    style GL fill:#e6ffe6
    style SYS fill:#ffffe6
    style DAL fill:#f0f0f0
```

## 2. Data Access Layer (DAL) Architecture

```mermaid
graph TD
    %% Application Programs
    APPS[Application Programs<br/>sl*, pl*, st*, gl*, ir*]
    
    %% File Handlers
    APPS --> FH[COBOL File Handlers<br/>acas0xx series]
    
    %% Decision Point
    FH --> DEC{RDBMS<br/>Enabled?}
    
    %% File Path
    DEC -->|No| FILES[COBOL Files<br/>Direct Access]
    
    %% Database Path
    DEC -->|Yes| MT[MT Modules<br/>DAL Layer]
    MT --> DB[(Database)]
    
    %% Dual Mode
    DEC -->|Dual Mode| BOTH[Write to Both<br/>Read from DB]
    BOTH --> FILES
    BOTH --> MT
    
    %% MT Module Examples
    MT --> MTX[salesMT<br/>purchMT<br/>stockMT<br/>nominalMT<br/>systemMT<br/>etc.]
    
    style APPS fill:#e6f3ff
    style FH fill:#fff2e6
    style MT fill:#e1f5e1
    style DEC fill:#ffffe6
```

## 3. Transaction Flow - Sales to GL/IRS

```mermaid
sequenceDiagram
    participant User
    participant SL as Sales Ledger
    participant ST as Stock Control
    participant POST as Posting File
    participant GL as General Ledger
    participant IRS as IRS System
    
    User->>SL: Enter Invoice (sl910)
    SL->>ST: Check Stock Availability
    ST-->>SL: Stock Status
    SL->>SL: Calculate VAT & Totals
    SL->>SL: Create Invoice Record
    
    User->>SL: Post Invoice (sl060)
    SL->>POST: Create Posting Records
    Note over POST: DR: Customer Account<br/>CR: Sales Account<br/>CR: VAT Account
    
    alt GL Mode
        POST->>GL: Transfer to GL Batch
        GL->>GL: Update Account Balances
    else IRS Mode
        POST->>IRS: Transfer to IRS Posting
        IRS->>IRS: Update Nominal Accounts
    else Both Mode
        POST->>GL: Transfer to GL
        POST->>IRS: Transfer to IRS
    end
    
    SL->>ST: Update Stock Quantities
    SL->>SL: Update Customer Balance
```

## 4. File Access Matrix

```mermaid
graph LR
    %% Define files
    subgraph "Data Files"
        SYS[System.dat]
        SALES[Sales Ledger]
        PURCH[Purchase Ledger]
        STOCK[Stock File]
        NOM[Nominal Ledger]
        POST[Posting File]
        ANAL[Analysis File]
    end
    
    %% Define program groups
    subgraph "IRS Programs"
        IRS1[irs010<br/>CoA]
        IRS2[irs020<br/>Defaults]
        IRS3[irs030<br/>Posting]
        IRS4[irs040<br/>Trial Bal]
    end
    
    subgraph "Sales Programs"
        SL1[sl010<br/>Customer]
        SL2[sl910<br/>Invoice]
        SL3[sl060<br/>Posting]
        SL4[sl080<br/>Payment]
    end
    
    subgraph "Stock Programs"
        ST1[st010<br/>Items]
        ST2[st020<br/>Movement]
        ST3[st030<br/>Reports]
    end
    
    %% IRS connections
    IRS1 --> NOM
    IRS2 --> NOM
    IRS3 --> NOM
    IRS3 --> POST
    IRS4 --> NOM
    
    %% Sales connections
    SL1 --> SALES
    SL2 --> SALES
    SL2 --> STOCK
    SL2 --> ANAL
    SL3 --> SALES
    SL3 --> POST
    SL4 --> SALES
    
    %% Stock connections
    ST1 --> STOCK
    ST1 --> ANAL
    ST1 --> PURCH
    ST2 --> STOCK
    ST3 --> STOCK
    
    %% System file connections
    IRS1 --> SYS
    SL1 --> SYS
    ST1 --> SYS
```

## 5. Accounting Module Interactions

```mermaid
graph TD
    %% Customer/Vendor facing modules
    subgraph "External Facing"
        CUST[Customers]
        VEND[Vendors]
    end
    
    %% Transaction modules
    subgraph "Transaction Processing"
        SL[Sales Ledger<br/>AR]
        PL[Purchase Ledger<br/>AP]
        ST[Stock Control]
    end
    
    %% Accounting modules
    subgraph "Financial Accounting"
        IRS[IRS<br/>Simple Books]
        GL[General Ledger<br/>Full Books]
    end
    
    %% Reporting
    subgraph "Reporting"
        FS[Financial<br/>Statements]
        MR[Management<br/>Reports]
    end
    
    %% External interactions
    CUST -->|Invoices| SL
    SL -->|Payments| CUST
    VEND -->|Bills| PL
    PL -->|Payments| VEND
    
    %% Internal flows
    SL -->|Stock Issues| ST
    PL -->|Stock Receipts| ST
    
    SL -->|Postings| IRS
    SL -->|Postings| GL
    PL -->|Postings| IRS
    PL -->|Postings| GL
    ST -->|Adjustments| IRS
    ST -->|Adjustments| GL
    
    IRS --> FS
    GL --> FS
    ST --> MR
    SL --> MR
    PL --> MR
    
    style CUST fill:#e6f3ff
    style VEND fill:#ffe6f0
    style SL fill:#cce5ff
    style PL fill:#ffccdd
    style ST fill:#e6ccff
    style IRS fill:#fff5cc
    style GL fill:#ccffcc
```

## 6. Program Call Hierarchy

```mermaid
graph TD
    %% Menu level
    MENU[sales/purchase/irs/stock/general<br/>Main Menu Programs]
    
    %% Start of day
    MENU --> SOD[*000 Programs<br/>Start of Day]
    SOD --> MAPS04[maps04<br/>Date Conversion]
    
    %% Maintenance programs
    MENU --> MAINT[*010 Programs<br/>Master File Maintenance]
    MAINT --> MAPS09[maps09<br/>Check Digits]
    MAINT --> DAL1[*MT DAL Modules]
    
    %% Transaction programs
    MENU --> TRANS[*020-*090 Programs<br/>Transactions & Reports]
    TRANS --> DAL2[*MT DAL Modules]
    
    %% System utilities
    MENU --> SYS[sys002<br/>System Parameters]
    MENU --> ACAS000[acas000<br/>System File Handler]
    ACAS000 --> SYSMT[systemMT<br/>System DAL]
    
    %% Common utilities
    DAL1 --> FHLOG[fhlogger<br/>File Access Logger]
    DAL2 --> FHLOG
    
    %% Database layer
    DAL1 --> DB[(Database<br/>Operations)]
    DAL2 --> DB
    SYSMT --> DB
    
    style MENU fill:#e1f5e1
    style SOD fill:#fff2e6
    style MAINT fill:#e6f3ff
    style TRANS fill:#ffe6f0
```

## 7. Batch Processing Flow

```mermaid
stateDiagram-v2
    [*] --> Entry: Transaction Entry
    Entry --> Batch: Create/Select Batch
    Batch --> Validation: Enter Transactions
    
    state Validation {
        [*] --> CheckBalance: Check Dr/Cr Balance
        CheckBalance --> CheckVAT: Validate VAT
        CheckVAT --> CheckAccounts: Verify Accounts Exist
        CheckAccounts --> [*]: All Valid
    }
    
    Validation --> Proof: Generate Proof Report
    Proof --> Modify: Errors Found?
    Modify --> Validation: Fix Errors
    Proof --> Post: No Errors
    
    state Post {
        [*] --> UpdateBalances: Update Account Balances
        UpdateBalances --> CreateAudit: Create Audit Trail
        CreateAudit --> UpdateBatch: Mark Batch Posted
        UpdateBatch --> [*]: Complete
    }
    
    Post --> Archive: Period End
    Archive --> [*]: Transaction Complete
```

## 8. Database Schema Overview

```mermaid
erDiagram
    SYSTEM ||--|| PARAMETERS : contains
    SALES ||--o{ SAINVOICE : has
    SALES ||--o{ SAITM3 : has
    PURCHASE ||--o{ PUINVOICE : has
    PURCHASE ||--o{ PUITM5 : has
    STOCK ||--o{ AUDIT : tracks
    NOMINAL ||--o{ POSTING : receives
    
    SALES {
        char7 Customer_Code PK
        char30 Name
        decimal Credit_Limit
        decimal Balance
        int Credit_Days
    }
    
    PURCHASE {
        char7 Supplier_Code PK
        char30 Name
        decimal Credit_Limit
        decimal Balance
        int Payment_Terms
    }
    
    STOCK {
        char13 Stock_Code PK
        char32 Description
        decimal Qty_Held
        decimal Reorder_Level
        decimal Cost
        decimal Sell_Price
    }
    
    NOMINAL {
        int8 Account_Number PK
        char32 Account_Name
        decimal DR_Balance
        decimal CR_Balance
        char1 Account_Type
    }
    
    POSTING {
        int Batch_Number
        int Post_Number
        int DR_Account
        int CR_Account
        decimal Amount
        decimal VAT_Amount
    }
```

These diagrams provide a comprehensive view of the ACAS system architecture, showing:
1. The modular structure with five main subsystems
2. The flexible DAL architecture supporting both files and databases
3. Transaction flows from source documents to financial records
4. File access patterns showing which programs access which data
5. Integration between accounting modules
6. Program call hierarchies
7. Batch processing workflows
8. Key database relationships

The system demonstrates a well-structured accounting solution with clear separation of concerns and flexible deployment options.