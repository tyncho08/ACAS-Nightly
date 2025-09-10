# ACAS Data Dictionary

## Overview
This data dictionary documents all files and database tables in the ACAS system, providing field-level documentation, business meanings, and validation rules.

## Table of Contents
1. [System-Wide Files](#system-wide)
2. [Sales Ledger Files](#sales-ledger)
3. [Purchase Ledger Files](#purchase-ledger)
4. [Stock Control Files](#stock-control)
5. [General Ledger Files](#general-ledger)
6. [IRS Files](#irs-files)
7. [Common Code Values](#code-values)

---

## 1. System-Wide Files {#system-wide}

### SYSTEM.DAT / SYSTEM-REC
**Purpose**: Central configuration and control file
**Key**: Single record file
**Size**: 1024 bytes

| Field Name | Type | Size | Description | Validation |
|-----------|------|------|-------------|-----------|
| Company-Name | CHAR | 30 | Company legal name | Required |
| Company-Add1-4 | CHAR | 30×4 | Company address lines | Required |
| Coy-Phone | CHAR | 14 | Company phone | Optional |
| Coy-Fax | CHAR | 14 | Company fax | Optional |
| Coy-Email | CHAR | 48 | Company email | Email format |
| Coy-WebSite | CHAR | 48 | Company website | URL format |
| Coy-Vat-Reg-No | CHAR | 14 | VAT registration | Valid VAT number |
| Vat-Rate | DEC | 2.2 | Standard VAT % | 0-99.99 |
| Reduced-Vat | DEC | 2.2 | Reduced VAT % | 0-99.99 |
| EOM-DD | NUM | 2 | End of month day | 1-31 |
| Preserve-Batch | CHAR | 1 | Keep batch numbers | Y/N |
| RDBMS-Name | CHAR | 10 | Database type | MySQL/MariaDB/None |
| RDBMS-Version | CHAR | 3.3 | Database version | Numeric |
| DB-Data-Source | CHAR | 48 | Database DSN | Valid DSN |
| Invoicer-Type | NUM | 1 | Invoice module | 1=Internal, 2=External |
| IRS-Both-Used | CHAR | 1 | IRS+GL active | Y/N |
| Testing-X flags | CHAR | 1×8 | Debug flags | 0/1 each |

### ANALYSIS-REC
**Purpose**: Product/service analysis codes for reporting
**Key**: PA-CODE (3 chars)
**Used By**: Sales, Purchase, Stock

| Field Name | Type | Size | Description | Validation |
|-----------|------|------|-------------|-----------|
| PA-CODE | CHAR | 3 | Analysis code | Unique, required |
| PA-GL | NUM | 6 | GL account link | Valid GL account |
| PA-DESC | CHAR | 24 | Description | Required |
| PA-PRINT | CHAR | 3 | Print on reports | YES/NO |

### DELIVERY-REC
**Purpose**: Additional delivery addresses
**Key**: DELIV-KEY (8 chars)
**Used By**: Sales, Purchase

| Field Name | Type | Size | Description | Validation |
|-----------|------|------|-------------|-----------|
| DELIV-KEY | CHAR | 8 | Cust/Supp + seq | Required |
| DELIV-NAME | CHAR | 30 | Delivery name | Required |
| DELIV-ADDRESS | CHAR | 96 | Full address | Required |

---

## 2. Sales Ledger Files {#sales-ledger}

### SALEDGER-REC
**Purpose**: Customer master file
**Key**: Sales-Key (7 chars)
**Record Size**: 300 bytes

| Field Name | Type | Size | Description | Validation |
|-----------|------|------|-------------|-----------|
| Sales-Key | CHAR | 7 | Customer code | Unique, check digit |
| Sales-Name | CHAR | 30 | Customer name | Required |
| Sales-Add-1-4 | CHAR | 30×4 | Address lines | Required |
| Sales-Add-5 | CHAR | 10 | Country/region | Optional |
| Sales-PC | CHAR | 10 | Postal code | Format check |
| Sales-Phone | CHAR | 14 | Phone number | Optional |
| Sales-Fax | CHAR | 14 | Fax number | Optional |
| Sales-Contact | CHAR | 20 | Contact person | Optional |
| Sales-Current | DEC | 9.2 | Current balance | Calculated |
| Sales-30-60-90 | DEC | 9.2×3 | Aged balances | Calculated |
| Sales-Last | DEC | 9.2 | Previous balance | Calculated |
| Sales-Q1-4 | DEC | 9.2×4 | Quarterly sales | Accumulated |
| Credit-Limit | DEC | 9.2 | Credit limit | >= 0 |
| Credit-Period | NUM | 3 | Payment terms | Days |
| Discount-Percent | DEC | 2.2 | Trade discount | 0-99.99 |
| Late-Charge-YN | CHAR | 1 | Apply late fees | Y/N |
| Email-Invoice | CHAR | 1 | Email invoices | Y/N |
| Email-Statement | CHAR | 1 | Email statements | Y/N |
| Email-Dunning | CHAR | 1 | Email reminders | Y/N |
| Email-Address | CHAR | 48 | Customer email | Email format |
| Allow-Part-Ship | CHAR | 1 | Partial shipment | Y/N |
| Allow-BO | CHAR | 1 | Back orders OK | Y/N |
| Date-Created | NUM | 8 | Creation date | YYYYMMDD |
| Date-Last-Inv | NUM | 8 | Last invoice | YYYYMMDD |
| Date-Last-Pay | NUM | 8 | Last payment | YYYYMMDD |
| Sales-Analysis | CHAR | 3 | Analysis code | Valid code |
| Status-Flag | CHAR | 1 | Active/Hold | A/H/D |

### SAINVOICE-REC
**Purpose**: Sales invoice header
**Key**: SINVOICE-KEY (10 chars: 8-digit invoice + 2)
**Links**: Customer, Stock, Analysis

| Field Name | Type | Size | Description | Validation |
|-----------|------|------|-------------|-----------|
| SINVOICE-KEY | CHAR | 10 | Invoice + type | Unique |
| IH-INVOICE | NUM | 8 | Invoice number | Sequential |
| IH-TEST | NUM | 2 | Type code | 01-99 |
| IH-CUSTOMER | CHAR | 7 | Customer code | Must exist |
| IH-DAT | NUM | 8 | Invoice date | Valid date |
| IH-ORDER | CHAR | 10 | Order reference | Optional |
| IH-TYPE | NUM | 1 | 1=Inv, 2=Credit | 1-2 |
| IH-REF | CHAR | 10 | Customer ref | Optional |
| IH-NET | DEC | 9.2 | Net amount | Calculated |
| IH-VAT | DEC | 9.2 | VAT amount | Calculated |
| IH-STATUS | CHAR | 1 | Posted flag | Y/N |
| IH-DAYS | NUM | 3 | Credit terms | From customer |
| IH-LINES | NUM | 2 | Line count | 1-99 |

### SAINV-LINES-REC
**Purpose**: Sales invoice detail lines
**Key**: IL-LINE-KEY (10 chars)
**Parent**: SAINVOICE-REC

| Field Name | Type | Size | Description | Validation |
|-----------|------|------|-------------|-----------|
| IL-LINE-KEY | CHAR | 10 | Invoice + line | Unique |
| IL-INVOICE | NUM | 8 | Invoice number | Must exist |
| IL-LINE | NUM | 2 | Line number | Sequential |
| IL-PRODUCT | CHAR | 13 | Stock code | Valid item |
| IL-PA | CHAR | 2 | Analysis code | Valid code |
| IL-QTY | NUM | 6 | Quantity | > 0 |
| IL-TYPE | CHAR | 1 | Line type | S=Stock, N=Non |
| IL-DESCRIPTION | CHAR | 32 | Line text | Required |
| IL-NET | DEC | 9.2 | Line total | Calculated |
| IL-UNIT | DEC | 9.2 | Unit price | > 0 |
| IL-DISCOUNT | DEC | 4.2 | Discount % | 0-99.99 |
| IL-VAT | DEC | 9.2 | VAT amount | Calculated |
| IL-VAT-CODE | NUM | 1 | VAT type | 0-3 |

### SAITM3-REC
**Purpose**: Sales open items (unpaid invoices)
**Key**: OI3-KEY (15 chars)

| Field Name | Type | Size | Description | Validation |
|-----------|------|------|-------------|-----------|
| OI3-KEY | CHAR | 15 | Cust+Inv+Type | Unique |
| OI3-CUSTOMER | CHAR | 7 | Customer code | Must exist |
| OI3-INVOICE | NUM | 8 | Invoice number | Must exist |
| OI3-DATE | NUM | 8 | Invoice date | Valid date |
| OI3-AMOUNT | DEC | 9.2 | Original amt | > 0 |
| OI3-PAID | DEC | 9.2 | Amount paid | >= 0 |
| OI3-DISCOUNT | DEC | 9.2 | Discount taken | >= 0 |
| OI3-BALANCE | DEC | 9.2 | Outstanding | Calculated |
| OI3-DAYS | NUM | 3 | Credit terms | Days |
| OI3-TYPE | CHAR | 1 | I=Inv, C=Credit | I/C |

---

## 3. Purchase Ledger Files {#purchase-ledger}

### PULEDGER-REC
**Purpose**: Supplier master file
**Key**: Purch-Key (7 chars)
**Record Size**: 302 bytes

| Field Name | Type | Size | Description | Validation |
|-----------|------|------|-------------|-----------|
| Purch-Key | CHAR | 7 | Supplier code | Unique, check digit |
| Purch-Name | CHAR | 30 | Supplier name | Required |
| Purch-Add-1-4 | CHAR | 30×4 | Address lines | Required |
| Purch-PC | CHAR | 10 | Postal code | Format check |
| Purch-Phone | CHAR | 14 | Phone number | Optional |
| Purch-Fax | CHAR | 14 | Fax number | Optional |
| Purch-Contact | CHAR | 20 | Contact person | Optional |
| Purch-Current | DEC | 9.2 | Current balance | Calculated |
| Purch-30-60-90 | DEC | 9.2×3 | Aged balances | Calculated |
| Purch-Last | DEC | 9.2 | Previous balance | Calculated |
| Purch-Q1-4 | DEC | 9.2×4 | Quarterly purch | Accumulated |
| Credit-Limit | DEC | 9.2 | Credit allowed | >= 0 |
| Credit-Period | NUM | 3 | Payment terms | Days |
| Discount-Percent | DEC | 2.2 | Settlement disc | 0-99.99 |
| Discount-Days | NUM | 3 | Discount period | Days |
| Bank-Sort-Code | NUM | 6 | Bank routing | Valid code |
| Bank-Account | NUM | 8 | Account number | Valid account |
| Date-Created | NUM | 8 | Creation date | YYYYMMDD |
| Date-Last-Inv | NUM | 8 | Last invoice | YYYYMMDD |
| Date-Last-Pay | NUM | 8 | Last payment | YYYYMMDD |
| Purch-Analysis | CHAR | 3 | Analysis code | Valid code |
| Status-Flag | CHAR | 1 | Active/Hold | A/H/D |

### PUITM5-REC
**Purpose**: Purchase open items (unpaid invoices)
**Key**: OI5-KEY (15 chars)
**Structure**: Similar to SAITM3-REC but for purchases

---

## 4. Stock Control Files {#stock-control}

### STOCK-REC
**Purpose**: Inventory master file
**Key**: Stock-Code (13 chars)
**Alt Key**: Stock-Abbrev (7 chars)
**Record Size**: 400 bytes

| Field Name | Type | Size | Description | Validation |
|-----------|------|------|-------------|-----------|
| Stock-Code | CHAR | 13 | Item code | Unique |
| Stock-Abbrev | CHAR | 7 | Short code | Unique |
| Stock-Desc | CHAR | 32 | Description | Required |
| Stock-Location | CHAR | 8 | Bin/location | Optional |
| Stock-Anal | CHAR | 3 | Analysis code | Valid code |
| Service-Item | CHAR | 1 | Non-physical | Y/N |
| Supp-1-3 | CHAR | 7×3 | Suppliers | Valid suppliers |
| Qty-Held | DEC | 9.2 | On hand | >= 0 |
| Qty-On-Order | DEC | 9.2 | On PO | >= 0 |
| Qty-BO | DEC | 9.2 | Back ordered | >= 0 |
| Qty-WIP | DEC | 9.2 | Work in progress | >= 0 |
| Reorder-Level | DEC | 9.2 | Min stock | >= 0 |
| Reorder-Qty | DEC | 9.2 | Order quantity | > 0 |
| Cost-Price | DEC | 9.2 | Unit cost | >= 0 |
| Sell-Price | DEC | 9.2 | Retail price | >= 0 |
| Stock-Value | DEC | 9.2 | Total value | Calculated |
| Last-Cost | DEC | 9.2 | Last purchase | >= 0 |
| Avg-Cost | DEC | 9.2 | Average cost | Calculated |
| Date-Created | NUM | 8 | Creation date | YYYYMMDD |
| Date-Last-Rcpt | NUM | 8 | Last receipt | YYYYMMDD |
| Date-Last-Sale | NUM | 8 | Last sale | YYYYMMDD |
| Date-On-Order | NUM | 8 | Order placed | YYYYMMDD |
| Period-Add | DEC | 9.2×2 | Period receipts | Qty + Value |
| Period-Ded | DEC | 9.2×2 | Period issues | Qty + Value |
| YTD-Add | DEC | 9.2×2 | Year receipts | Qty + Value |
| YTD-Ded | DEC | 9.2×2 | Year issues | Qty + Value |

### AUDIT-REC
**Purpose**: Stock movement history
**Key**: Sequential/Date+Time
**Links**: Stock-Code

| Field Name | Type | Size | Description | Validation |
|-----------|------|------|-------------|-----------|
| Batch-Number | NUM | 6 | Batch control | Sequential |
| Movement-Date | NUM | 8 | Transaction date | Valid date |
| Movement-Time | NUM | 6 | HHMMSS | Valid time |
| Stock-Code | CHAR | 13 | Item moved | Must exist |
| Movement-Type | CHAR | 1 | A=Add, D=Deduct | A/D/T |
| Movement-Qty | DEC | 9.2 | Quantity | != 0 |
| Movement-Value | DEC | 9.2 | Value | Calculated |
| Source-Type | CHAR | 2 | SI=Sale,PI=Purch | Valid type |
| Source-Ref | CHAR | 10 | Document ref | Required |
| User-ID | CHAR | 8 | Who did it | System/User |

---

## 5. General Ledger Files {#general-ledger}

### GLLEDGER-REC / NOMINAL-REC
**Purpose**: Chart of Accounts
**Key**: LEDGER-KEY (8 digits: 6 + 2 profit center)

| Field Name | Type | Size | Description | Validation |
|-----------|------|------|-------------|-----------|
| LEDGER-KEY | NUM | 8 | Account + PC | Unique |
| LEDGER-TYPE | NUM | 1 | 1=BS, 2=PL, 9=Head | 1/2/9 |
| LEDGER-PLACE | CHAR | 1 | Report position | A-Z |
| LEDGER-LEVEL | NUM | 1 | Hierarchy level | 1-9 |
| LEDGER-NAME | CHAR | 32 | Account name | Required |
| LEDGER-BALANCE | DEC | 10.2 | Current balance | Calculated |
| LEDGER-LAST | DEC | 10.2 | Prior period | Historical |
| LEDGER-Q1-4 | DEC | 10.2×4 | Quarterly moves | Accumulated |

### GLBATCH-REC
**Purpose**: GL batch control
**Key**: BATCH-KEY (6 digits)

| Field Name | Type | Size | Description | Validation |
|-----------|------|------|-------------|-----------|
| BATCH-KEY | NUM | 6 | Batch number | Sequential |
| ITEMS | NUM | 2 | Entry count | > 0 |
| BATCH-STATUS | NUM | 1 | 0=Open,1=Proof,2=Post | 0-2 |
| ENTERED | NUM | 8 | Entry date | Valid date |
| POSTED | NUM | 8 | Posting date | Valid date |
| INPUT-GROSS | DEC | 14.2 | Header total | Required |
| ACTUAL-GROSS | DEC | 14.2 | Detail total | Must balance |
| DESCRIPTION | CHAR | 24 | Batch description | Required |

### GLPOSTING-REC
**Purpose**: GL transaction details
**Key**: POST-RRN (relative record)

| Field Name | Type | Size | Description | Validation |
|-----------|------|------|-------------|-----------|
| POST-RRN | NUM | 5 | Record number | Sequential |
| POST-KEY | NUM | 10 | Batch+Seq | Unique |
| POST-CODE | CHAR | 2 | Transaction code | Valid code |
| POST-DAT | CHAR | 8 | Posting date | Valid date |
| POST-DR | NUM | 6 | Debit account | Must exist |
| DR-PC | NUM | 2 | Debit PC | Valid PC |
| POST-CR | NUM | 6 | Credit account | Must exist |
| CR-PC | NUM | 2 | Credit PC | Valid PC |
| POST-AMOUNT | DEC | 10.2 | Amount | > 0 |
| POST-LEGEND | CHAR | 32 | Description | Required |
| VAT-AC | NUM | 6 | VAT account | If VAT |
| VAT-AMOUNT | DEC | 10.2 | VAT amount | Calculated |

---

## 6. IRS Files {#irs-files}

### IRSNL-REC
**Purpose**: IRS nominal ledger (simplified GL)
**Key**: KEY-1 (10 digits: 5 main + 5 sub)

| Field Name | Type | Size | Description | Validation |
|-----------|------|------|-------------|-----------|
| KEY-1 | NUM | 10 | Account number | Unique |
| TIPE | CHAR | 1 | Account type | A-Z |
| NL-NAME | CHAR | 24 | Account name | Required |
| DR | DEC | 10.2 | Debit balance | >= 0 |
| CR | DEC | 10.2 | Credit balance | >= 0 |
| DR-LAST-01-04 | DEC | 10.2×4 | Quarterly DR | Historical |
| CR-LAST-01-04 | DEC | 10.2×4 | Quarterly CR | Historical |
| AC | CHAR | 1 | Active flag | Y/N |
| REC-POINTER | NUM | 5 | Record link | Internal |

### IRSDFLT-REC
**Purpose**: IRS posting defaults
**Key**: DEF-REC-KEY (2 digits)

| Field Name | Type | Size | Description | Validation |
|-----------|------|------|-------------|-----------|
| DEF-REC-KEY | NUM | 2 | Default number | 01-32 |
| DEF-ACS | NUM | 5 | GL account | Must exist |
| DEF-CODES | CHAR | 2 | Posting code | AA-ZZ |
| DEF-VAT | CHAR | 1 | VAT type | N/I/O |

### IRSPOSTING-REC
**Purpose**: IRS transaction postings
**Key**: KEY-4 (5 digits)

| Field Name | Type | Size | Description | Validation |
|-----------|------|------|-------------|-----------|
| KEY-4 | NUM | 5 | Posting number | Sequential |
| POST4-CODE | CHAR | 2 | Transaction code | Valid code |
| POST4-DAT | CHAR | 8 | Posting date | Valid date |
| POST4-DR | NUM | 5 | Debit account | Must exist |
| POST4-CR | NUM | 5 | Credit account | Must exist |
| POST4-AMOUNT | DEC | 9.2 | Amount | > 0 |
| POST4-LEGEND | CHAR | 32 | Description | Required |
| VAT-AC-DEF4 | NUM | 2 | VAT default | If VAT |
| VAT-AMOUNT4 | DEC | 9.2 | VAT amount | Calculated |

---

## 7. Common Code Values {#code-values}

### Transaction Codes (POST-CODE)
| Code | Description | Usage |
|------|-------------|-------|
| SI | Sales Invoice | Sales posting |
| SC | Sales Credit | Sales return |
| SR | Sales Receipt | Payment received |
| PI | Purchase Invoice | Purchase posting |
| PC | Purchase Credit | Purchase return |
| PP | Purchase Payment | Payment made |
| JE | Journal Entry | Manual GL entry |
| ST | Stock Transfer | Inventory movement |
| SA | Stock Adjustment | Inventory correction |

### VAT Codes
| Code | Description | Rate |
|------|-------------|------|
| 0 | Zero rated | 0% |
| 1 | Standard rate | System parameter |
| 2 | Reduced rate | System parameter |
| 3 | Exempt | No VAT |

### Account Types (TIPE)
| Code | Description | Balance Type |
|------|-------------|--------------|
| A | Assets | Debit normal |
| L | Liabilities | Credit normal |
| C | Capital | Credit normal |
| I | Income | Credit normal |
| E | Expenses | Debit normal |
| H | Header | No balance |

### Status Flags
| Code | Description | Usage |
|------|-------------|-------|
| A | Active | Normal status |
| H | Hold | Temporary stop |
| D | Dormant | Inactive |
| C | Closed | Permanently closed |

### Period Codes
| Code | Description | Days |
|------|-------------|------|
| W | Weekly | 7 |
| M | Monthly | 30/31 |
| Q | Quarterly | 90 |
| Y | Yearly | 365 |

### Movement Types
| Code | Description | Effect |
|------|-------------|---------|
| A | Addition | Increase stock |
| D | Deduction | Decrease stock |
| T | Transfer | Move location |
| R | Return | Reverse movement |

### Batch Status
| Code | Description | Next Action |
|------|-------------|-------------|
| 0 | Open | Continue entry |
| 1 | Proofed | Ready to post |
| 2 | Posted | Complete |
| 3 | Error | Needs correction |

## Field Naming Conventions

### Prefixes
- **Sales-**: Sales ledger fields
- **Purch-**: Purchase ledger fields
- **Stock-**: Inventory fields
- **IH-**: Invoice header
- **IL-**: Invoice lines
- **OI-**: Open items
- **POST-**: Posting fields

### Suffixes
- **-Key**: Primary key field
- **-Date**: Date field (YYYYMMDD)
- **-Amount**: Monetary value
- **-Code**: Reference code
- **-Flag**: Yes/No indicator
- **-PC**: Profit center

## Data Integrity Rules

### Referential Integrity
- Customer/Supplier codes must exist before use
- Stock codes must exist for stock transactions
- GL accounts must exist before posting
- Analysis codes must be predefined

### Business Rules
- Debits must equal credits in batches
- No negative stock quantities
- Payments cannot exceed invoice amounts
- Period dates must be sequential
- VAT calculations must balance

### Validation Patterns
- Check digits on customer/supplier codes
- Date format validation (YYYYMMDD)
- Email format checking where applicable
- Numeric fields right-justified, zero-filled
- Character fields left-justified, space-filled

This data dictionary provides the foundation for understanding ACAS data structures and supports data migration, integration, and reporting initiatives.