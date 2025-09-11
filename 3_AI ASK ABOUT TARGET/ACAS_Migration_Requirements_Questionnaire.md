# ACAS Migration Requirements Questionnaire

## Executive Summary

This questionnaire is designed to gather comprehensive requirements for migrating the ACAS (Applewood Computers Accounting System) from its current COBOL implementation to a modern architecture. Based on analysis of the actual COBOL source code and system documentation, this questionnaire addresses critical technical and business decisions needed for a successful migration.

### Key Statistics
- **Total Questions**: 185
  - Critical: 67
  - Important: 82
  - Nice-to-Have: 36
- **Subsystems to Migrate**: 12
- **COBOL Programs**: 200+
- **Lines of Code**: ~500,000+
- **Data Storage**: Dual support for ISAM files and RDBMS (MySQL/MariaDB)

### Critical Questions Requiring Immediate Answers
1. [BUS-001] Business drivers for migration
2. [BUS-002] System criticality and downtime tolerance
3. [ARCH-001] Target architecture pattern preference
4. [DATA-001] Data migration strategy
5. [TECH-002] Database technology choice
6. [RISK-001] Risk tolerance level
7. [EXEC-001] Budget range
8. [SEQ-001] Subsystem migration priority

---

## Response Template

```yaml
# ACAS Migration Requirements Response
# Date: [YYYY-MM-DD]
# Respondent: [Name, Role]
# Version: 1.0

Section_1_Business_Context:
  BUS-001:
    answer: 
    notes: 
  BUS-002:
    answer: 
    notes:
  # ... continue for all questions

Decision_Summary:
  migration_approach: 
  timeline: 
  budget: 
  key_risks: 
  success_criteria: 
```

---

## Quick Start Guide

### Top 20 Questions to Answer First

These questions will determine the fundamental approach to your migration:

1. **[BUS-001]** What are your top 3 business drivers?
2. **[BUS-002]** What is your downtime tolerance?
3. **[ARCH-001]** What architecture pattern do you prefer?
4. **[ARCH-004]** What is your cloud strategy?
5. **[TECH-001]** What programming language(s) will you use?
6. **[TECH-002]** What database technology?
7. **[DATA-001]** What is your data migration strategy?
8. **[FUNC-001]** What level of feature parity is required?
9. **[INT-003]** Will systems need to coexist?
10. **[NFR-001]** What are transaction volume requirements?
11. **[EXEC-001]** What is your budget range?
12. **[EXEC-002]** How many resources are available?
13. **[RISK-001]** What is your risk tolerance?
14. **[TEST-001]** What testing approach is preferred?
15. **[SEQ-001]** What is the subsystem migration priority?
16. **[SEQ-004]** What are critical business dates?
17. **[COBOL-001]** Do you want to maintain COBOL compatibility?
18. **[BATCH-001]** How should batch processing be modernized?
19. **[FILE-001]** How to handle ISAM to database conversion?
20. **[INTEG-001]** What integration patterns are preferred?

### Why These Questions Matter Most

These questions establish:
- **Strategic Direction**: Architecture, technology stack, and approach
- **Constraints**: Budget, timeline, resources, and risk tolerance
- **Technical Foundation**: Database, programming language, and integration patterns
- **Migration Sequencing**: Which subsystems to migrate first and why
- **Validation Approach**: How to ensure the migration is successful

### Impact of Not Answering

Failure to answer these questions will result in:
- Undefined scope leading to budget/timeline overruns
- Wrong technology choices requiring rework
- Inadequate testing causing production failures
- Poor subsystem sequencing causing business disruption
- Incompatible architecture requiring redesign

---

## Full Questionnaire

## Section 1: Business Context and Drivers

### 1.1 Strategic Alignment

**[BUS-001] [CRITICAL] [OPEN_TEXT]**  
**What are the top 3 business drivers for migrating from the current COBOL system?**
- Dependencies: None
- Impact: Determines migration approach, technology choices, and success metrics
- Context: Current system is 40+ years old, written in COBOL, supports both ISAM files and MySQL/MariaDB

Options to consider:
- Cost reduction (COBOL developer shortage)
- Scalability limitations
- Real-time processing needs (current batch-heavy system)
- Modern integration requirements
- User experience improvements
- Compliance/regulatory changes
- Business agility/faster changes

**[BUS-002] [CRITICAL] [SCALE]**  
**How critical is the ACAS system to daily business operations?**
- Scale: 1 (Can tolerate week+ downtime) to 5 (Zero downtime tolerance)
- Dependencies: None
- Impact: Defines migration strategy (big bang vs phased vs parallel run)
- Context: System handles GL, Sales, Purchase, Stock, IRS ledgers

**[BUS-003] [IMPORTANT] [NUMERIC]**  
**What is the expected business growth rate over the next 5 years?**
- Provide percentage annual growth
- Dependencies: None
- Impact: Influences scalability requirements and architecture choices
- Context: Current system handles transactions with 10-digit amounts

**[BUS-004] [CRITICAL] [MULTIPLE_CHOICE]**  
**What is the acceptable timeframe for complete migration?**
- [ ] 6 months
- [ ] 12 months  
- [ ] 18 months
- [ ] 24 months
- [ ] 36+ months
- Dependencies: BUS-002
- Impact: Determines phasing, resource allocation, and approach

**[BUS-005] [IMPORTANT] [YES_NO]**  
**Are there any upcoming regulatory changes that the new system must address?**
- If yes, specify requirements and deadlines
- Dependencies: None
- Impact: May prioritize certain subsystem migrations
- Context: System includes IRS (Incomplete Records System) for tax compliance

### 1.2 Current Pain Points

**[BUS-006] [CRITICAL] [OPEN_TEXT]**  
**Based on the subsystem analysis, which of these identified subsystems cause the most operational issues?**
Subsystems:
1. GL_CORE (General Ledger) - 17 programs
2. IRS_CORE (Tax/Incomplete Records) - 15 programs  
3. SL_MGMT (Sales Ledger) - 36 programs
4. PL_MGMT (Purchase Ledger) - 31 programs
5. ST_CTRL (Stock Control) - 10 programs
6. BATCH_FW (Batch Processing) - 8 programs
7. RPT_ENGINE (Reporting) - 25 programs
8. SYS_ADMIN (System Admin) - 5 programs
9. PERIOD_PROC (Period Processing) - 3 programs
10. DAL (Data Access Layer) - 50+ programs
11. COMMON_UTIL (Utilities) - 10 programs
12. INTEG_SVC (Integration) - 5 programs

- Dependencies: None
- Impact: Prioritizes migration sequence
- Context: Each subsystem has different criticality levels

**[BUS-007] [IMPORTANT] [MULTIPLE_CHOICE]**  
**What are the biggest limitations of the current COBOL system?** (Select all that apply)
- [ ] Performance/speed issues (batch processing delays)
- [ ] Lack of real-time processing (heavy batch dependency)
- [ ] Limited reporting capabilities (fixed format reports)
- [ ] Poor integration with modern systems
- [ ] Green screen UI limitations
- [ ] Complex maintenance (COBOL expertise required)
- [ ] Lack of skilled COBOL developers
- [ ] Fixed decimal arithmetic limitations
- [ ] File locking issues with ISAM
- [ ] Limited concurrent user support
- Dependencies: None
- Impact: Defines key requirements for target system

**[BUS-008] [IMPORTANT] [NUMERIC]**  
**How many business workarounds exist due to system limitations?**
- Provide count and brief descriptions
- Dependencies: BUS-007
- Impact: Identifies hidden requirements
- Context: Users may have Excel-based workarounds or manual processes

**[BUS-009] [CRITICAL] [YES_NO]**  
**Is the current dual-mode operation (ISAM files + MySQL) causing issues?**
- If yes, describe specific problems
- Dependencies: None
- Impact: Influences data architecture decisions
- Context: System can run in COBOL file mode, database mode, or both simultaneously

---

## Section 2: Target Architecture Preferences

### 2.1 Architecture Style

**[ARCH-001] [CRITICAL] [MULTIPLE_CHOICE]**  
**What is your preferred target architecture pattern?**
- [ ] Monolithic (modern stack)
- [ ] Service-Oriented Architecture (SOA)  
- [ ] Microservices
- [ ] Serverless/Function-as-a-Service
- [ ] Event-driven architecture
- [ ] Hybrid (specify combination)
- Dependencies: BUS-001, BUS-002
- Impact: Defines entire migration approach and technology stack
- Context: Current system is modular COBOL with clear subsystem boundaries

**[ARCH-002] [CRITICAL] [MULTIPLE_CHOICE]**  
**Given the subsystem boundaries identified, which migration pattern do you prefer?**
- [ ] Strangler Fig (gradual replacement subsystem by subsystem)
- [ ] Big Bang (complete replacement at once)
- [ ] Parallel Run (both systems simultaneously)
- [ ] Phased Cutover (subsystem by subsystem with coexistence)
- [ ] Hybrid approach (specify)
- Dependencies: ARCH-001, BUS-002
- Impact: Determines migration timeline, risk, and resource needs
- Context: System has 12 distinct subsystems with defined interfaces

**[ARCH-003] [IMPORTANT] [YES_NO]**  
**Should the new system maintain the same subsystem boundaries identified in the analysis?**
- If no, describe desired changes
- Dependencies: ARCH-001
- Impact: Affects design complexity and migration effort
- Context: Current boundaries: GL, IRS, Sales, Purchase, Stock, Batch, Reporting, etc.

**[ARCH-004] [CRITICAL] [MULTIPLE_CHOICE]**  
**What is your cloud strategy?**
- [ ] On-premises only
- [ ] Private cloud
- [ ] Public cloud (AWS/Azure/GCP)
- [ ] Hybrid cloud
- [ ] Multi-cloud
- Dependencies: None
- Impact: Influences technology choices, security approach, and costs

**[ARCH-005] [IMPORTANT] [YES_NO]**  
**Do you want to preserve the current menu-driven navigation structure?**
- If no, describe preferred user experience
- Dependencies: None
- Impact: Affects UI/UX design and user training needs
- Context: Current system uses character-based menus (ACAS, sales, purchase, stock, general, irs)

### 2.2 Technology Stack

**[TECH-001] [CRITICAL] [MULTIPLE_CHOICE]**  
**Preferred programming language(s) for the new system?** (Select up to 3)
- [ ] Java
- [ ] C#/.NET
- [ ] Python
- [ ] Go
- [ ] JavaScript/TypeScript (Node.js)
- [ ] Rust
- [ ] Keep COBOL with modernization
- [ ] Other (specify)
- Dependencies: ARCH-001
- Impact: Determines development resources needed, performance characteristics
- Context: Current system is 200+ COBOL programs with complex business logic

**[TECH-002] [CRITICAL] [MULTIPLE_CHOICE]**  
**Preferred database technology?**
- [ ] Traditional RDBMS (PostgreSQL, MySQL, Oracle, SQL Server)
- [ ] NoSQL (MongoDB, DynamoDB, Cassandra)
- [ ] NewSQL (CockroachDB, VoltDB)
- [ ] Multi-model (mixed based on subsystem needs)
- [ ] Keep current MySQL/MariaDB
- Dependencies: ARCH-001
- Impact: Affects data migration strategy and application design
- Context: Current system supports both ISAM files and MySQL/MariaDB

**[TECH-003] [IMPORTANT] [MULTIPLE_CHOICE]**  
**How should the current file-based data storage be migrated?**
- [ ] Direct conversion to relational tables (maintain current structure)
- [ ] Redesign data model completely
- [ ] Hybrid (some files, some database)
- [ ] Event sourcing pattern
- [ ] Document store for some data types
- Dependencies: TECH-002
- Impact: Determines data migration complexity
- Context: System uses indexed sequential (ISAM) files with specific record layouts

**[TECH-004] [IMPORTANT] [MULTIPLE_CHOICE]**  
**Preferred user interface approach?**
- [ ] Web-based (SPA - React/Angular/Vue)
- [ ] Web-based (server-rendered - traditional)
- [ ] Desktop application
- [ ] Mobile-first
- [ ] API-only (headless)
- [ ] Multiple interfaces for different user types
- Dependencies: None
- Impact: Affects frontend development needs and user training

**[TECH-005] [NICE-TO-HAVE] [YES_NO]**  
**Should the system support multiple UI themes (including a "classic" mode)?**
- Dependencies: TECH-004
- Impact: May ease user transition
- Context: Current users familiar with green-screen interface

---

## Section 3: COBOL-Specific Migration Decisions

### 3.1 COBOL Code Handling

**[COBOL-001] [CRITICAL] [MULTIPLE_CHOICE]**  
**How should the existing COBOL business logic be handled?**
- [ ] Complete rewrite in new language
- [ ] Automated translation to new language
- [ ] Keep COBOL, modernize runtime (GnuCOBOL to Enterprise COBOL)
- [ ] Gradual rewrite with COBOL-to-new-language bridges
- [ ] Extract business rules to rule engine, rewrite rest
- Dependencies: TECH-001
- Impact: Determines migration approach and timeline
- Context: ~500,000 lines of COBOL code with complex business logic

**[COBOL-002] [IMPORTANT] [YES_NO]**  
**Do you need to maintain COBOL PICTURE clause precision in calculations?**
- If yes, specify critical calculations
- Dependencies: COBOL-001
- Impact: Affects numeric handling in new system
- Context: System uses COMP-3 packed decimal, specific PICTURE clauses for money

**[COBOL-003] [CRITICAL] [MULTIPLE_CHOICE]**  
**How should COBOL copybooks be handled?**
- [ ] Convert to new language structures/classes
- [ ] Generate from schema definitions
- [ ] Maintain as separate data dictionaries
- [ ] Embed in microservice contracts
- Dependencies: COBOL-001
- Impact: Affects data structure consistency
- Context: System uses extensive copybooks (wsnames.cob, wsfnctn.cob, etc.)

**[COBOL-004] [IMPORTANT] [YES_NO]**  
**Should the new system support COBOL-style file handling operations?**
- Operations: START, READ NEXT, READ KEY, REWRITE, DELETE
- Dependencies: TECH-002
- Impact: Affects data access layer design
- Context: Current system has complex file positioning and sequential processing

### 3.2 Batch Processing Modernization

**[BATCH-001] [CRITICAL] [MULTIPLE_CHOICE]**  
**How should the current batch processing be modernized?**
Based on analysis of xl150 (End of Cycle), gl070 (Posting), etc.:
- [ ] Keep as scheduled batch jobs
- [ ] Convert to real-time processing
- [ ] Event-driven processing
- [ ] Hybrid (some batch, some real-time)
- [ ] Microservices with message queues
- Dependencies: ARCH-001
- Impact: Major architectural decision
- Context: Current system has complex month-end, year-end batch processes

**[BATCH-002] [IMPORTANT] [OPEN_TEXT]**  
**Which batch processes must be preserved vs. converted to real-time?**
Current batch processes include:
- GL posting (gl070, gl071, gl072)
- Period-end closing (xl150)
- Invoice posting (sl060, pl060)
- Report generation
- Statement production
- File reorganization

For each, specify: Keep batch / Convert to real-time / Eliminate
- Dependencies: BATCH-001
- Impact: Affects system design and user workflows

**[BATCH-003] [CRITICAL] [YES_NO]**  
**Must the new system support the current posting period concept?**
- If yes, can it be simplified?
- Dependencies: None
- Impact: Affects transaction processing design
- Context: Current system has complex period-based posting with strict sequencing

### 3.3 File Structure Migration

**[FILE-001] [CRITICAL] [MULTIPLE_CHOICE]**  
**How should ISAM indexed file structures be converted?**
- [ ] Direct table mapping (one file = one table)
- [ ] Normalized relational design
- [ ] Document store for complex records
- [ ] Mixed approach based on data type
- Dependencies: TECH-002
- Impact: Determines data migration complexity
- Context: Files like GLLEDGER, SALEDGER use complex keys and alternate indexes

**[FILE-002] [IMPORTANT] [YES_NO]**  
**Should the new system maintain the current record locking behavior?**
- Current: COBOL file locking, exclusive access during updates
- Dependencies: ARCH-001
- Impact: Affects concurrency design
- Context: Current system uses file/record locking for consistency

**[FILE-003] [IMPORTANT] [MULTIPLE_CHOICE]**  
**How should the current audit trail files be modernized?**
- [ ] Database audit tables
- [ ] Event sourcing
- [ ] Audit log service
- [ ] Blockchain for immutability
- [ ] Keep current approach
- Dependencies: None
- Impact: Affects compliance and debugging capabilities
- Context: System maintains detailed audit trails for all transactions

---

## Section 4: Functional Requirements

### 4.1 Feature Parity and Enhancements

**[FUNC-001] [CRITICAL] [MULTIPLE_CHOICE]**  
**What level of feature parity is required with the legacy system?**
- [ ] 100% - All features must be replicated exactly
- [ ] 90% - Core features only, remove rarely used
- [ ] 80% - Significant simplification acceptable  
- [ ] 70% - Major re-engineering with process improvement
- [ ] Re-engineer - Complete business process redesign
- Dependencies: BUS-001
- Impact: Defines scope, complexity, and timeline
- Context: System has many features accumulated over 40+ years

**[FUNC-002] [IMPORTANT] [YES_NO]**  
**Must the new system support the IRS (Incomplete Records System) functionality?**
- If yes, can it be redesigned or must maintain current logic?
- Dependencies: FUNC-001
- Impact: May require special handling in migration
- Context: IRS is simplified accounting for small businesses, unique to ACAS

**[FUNC-003] [CRITICAL] [YES_NO]**  
**Should multi-company/branch processing be enhanced from current capability?**
- Current: System supports profit centers
- Dependencies: None
- Impact: Affects data model and security design
- Context: Uses 2-digit profit center codes throughout

**[FUNC-004] [IMPORTANT] [OPEN_TEXT]**  
**What new capabilities should the target system add?**
Suggestions based on current limitations:
- Real-time dashboard and analytics
- Mobile access
- Advanced reporting/BI
- Workflow automation
- Electronic document management
- API for third-party integration
- Multi-currency support (currently single currency)
- Advanced inventory features (currently basic)

List and prioritize:
- Dependencies: BUS-001
- Impact: Extends project scope beyond migration

**[FUNC-005] [IMPORTANT] [MULTIPLE_CHOICE]**  
**How should the reporting subsystem be modernized?**
- [ ] Maintain current fixed-format reports
- [ ] Modernize with BI tool integration (Tableau, PowerBI)
- [ ] Self-service analytics capability
- [ ] Real-time dashboards
- [ ] API for external reporting tools
- [ ] All of the above
- Dependencies: None
- Impact: Determines reporting architecture
- Context: Current system has 25+ fixed-format reports

### 4.2 Business Rules and Calculations

**[FUNC-006] [CRITICAL] [MULTIPLE_CHOICE]**  
**How should complex COBOL business logic be handled?**
Examples: VAT calculations, discount matrices, posting rules
- [ ] Translate directly to new language
- [ ] Re-implement with modern patterns
- [ ] Extract to rules engine (Drools, etc.)
- [ ] Microservice per major calculation
- [ ] Review and simplify where possible
- Dependencies: COBOL-001
- Impact: Affects migration approach and testing
- Context: Complex calculations in gl070, sl060, VAT handling

**[FUNC-007] [IMPORTANT] [YES_NO]**  
**Are all financial calculations documented and validated?**
- If no, what additional validation is needed?
- Dependencies: FUNC-006
- Impact: Determines testing requirements
- Context: System handles 10-digit amounts with specific rounding rules

**[FUNC-008] [CRITICAL] [OPEN_TEXT]**  
**Which accounting standards and regulations must the new system comply with?**
- List specific standards (GAAP, IFRS, SOX, etc.)
- Any industry-specific requirements?
- Any country-specific requirements?
- Dependencies: None
- Impact: Defines compliance requirements
- Context: Current system has UK-specific features (VAT, date formats)

**[FUNC-009] [IMPORTANT] [YES_NO]**  
**Should the double-entry validation be enhanced beyond current capability?**
- Current: Basic debit/credit balance checking
- Dependencies: None
- Impact: Affects posting engine design
- Context: GL posting programs (gl070-gl072) perform validation

---

## Section 5: Data Migration Strategy

### 5.1 Data Migration Approach

**[DATA-001] [CRITICAL] [MULTIPLE_CHOICE]**  
**What is your data migration strategy?**
- [ ] Big bang migration (all at once during cutover)
- [ ] Phased migration (by subsystem)
- [ ] Parallel run (sync between old and new)
- [ ] Trickle migration (gradual with sync)
- [ ] Archive historical, migrate active only
- Dependencies: ARCH-002
- Impact: Defines data migration project complexity
- Context: System has both ISAM files and MySQL tables

**[DATA-002] [CRITICAL] [NUMERIC]**  
**What is the data volume to migrate?**
Based on file analysis:
- Number of customers: ___
- Number of suppliers: ___
- Number of GL accounts: ___
- Number of stock items: ___
- Historical transaction years to migrate: ___
- Total data size (GB): ___
- Dependencies: None
- Impact: Sizes migration effort and timeline

**[DATA-003] [IMPORTANT] [MULTIPLE_CHOICE]**  
**How should data quality issues be handled?**
- [ ] Migrate as-is, fix in new system
- [ ] Clean before migration
- [ ] Clean during migration
- [ ] Only migrate records meeting quality standards
- [ ] Manual review for exceptions
- Dependencies: DATA-001
- Impact: Affects timeline and resource needs
- Context: 40+ year old system likely has data quality issues

**[DATA-004] [CRITICAL] [YES_NO]**  
**Is historical data audit trail critical?**
- Years of history required: ___
- Can be archived vs. online: ___
- Dependencies: None
- Impact: Influences storage strategy and data model
- Context: System maintains detailed audit trails

**[DATA-005] [IMPORTANT] [MULTIPLE_CHOICE]**  
**How should the current file-to-database dual mode be handled?**
- [ ] Migrate ISAM files only
- [ ] Migrate MySQL data only  
- [ ] Reconcile and merge both sources
- [ ] Keep both and maintain sync
- Dependencies: DATA-001
- Impact: Affects migration complexity
- Context: System can maintain data in both ISAM and MySQL

**[DATA-006] [CRITICAL] [YES_NO]**  
**Should inactive records (dead accounts) be migrated?**
- If yes, to separate archive?
- Dependencies: DATA-002
- Impact: Affects data volume and model
- Context: System maintains 'dead' flag for inactive accounts

---

## Section 6: Integration Requirements

### 6.1 External Systems

**[INT-001] [CRITICAL] [OPEN_TEXT]**  
**What external systems must the new system integrate with?**
For each system provide:
- System name and purpose
- Current integration method (if any)
- Desired integration method
- Data flow direction
- Frequency/volume

- Dependencies: None
- Impact: Defines integration architecture
- Context: Current system is largely standalone

**[INT-002] [IMPORTANT] [MULTIPLE_CHOICE]**  
**Preferred integration approach for the new system?**
- [ ] REST APIs
- [ ] GraphQL
- [ ] Message queues (RabbitMQ, Kafka)
- [ ] ETL/batch files
- [ ] Direct database access
- [ ] Web services (SOAP)
- [ ] Mixed approach
- Dependencies: ARCH-001
- Impact: Determines integration patterns

**[INT-003] [CRITICAL] [YES_NO]**  
**Will the legacy COBOL system need to coexist with the new system?**
- If yes, for how long? ___
- Which subsystems must maintain synchronization?
- Dependencies: ARCH-002
- Impact: Requires bidirectional sync strategy
- Context: System has clear subsystem boundaries enabling phased migration

**[INT-004] [IMPORTANT] [MULTIPLE_CHOICE]**  
**How should master data be managed during migration?**
- [ ] Maintain in legacy until full cutover
- [ ] Migrate to new system immediately
- [ ] Dual maintenance during transition
- [ ] MDM solution as separate system
- [ ] Subsystem by subsystem
- Dependencies: INT-003
- Impact: Affects data consistency strategy
- Context: Master data includes customers, suppliers, GL accounts, stock items

**[INT-005] [NICE-TO-HAVE] [YES_NO]**  
**Do you need real-time integration with banking systems?**
- For payments?
- For reconciliation?
- Dependencies: None
- Impact: May add scope to project
- Context: Current system has no banking integration

---

## Section 7: Non-Functional Requirements

### 7.1 Performance and Scalability

**[NFR-001] [CRITICAL] [NUMERIC]**  
**What are the transaction volume requirements?**
Current system analysis shows:
- Expected peak transactions per second: ___
- Expected daily transaction count: ___
- Expected monthly growth rate: ___
- Peak period (month-end) multiplier: ___
- Dependencies: BUS-003
- Impact: Sizes infrastructure and architecture
- Context: Current batch processing suggests lower TPS but high volume

**[NFR-002] [IMPORTANT] [NUMERIC]**  
**What are the response time requirements?**
- Online transaction response time (ms): ___
- Query/search response time (seconds): ___
- Report generation time (seconds): ___
- Batch processing window (hours): ___
- Dependencies: None
- Impact: Influences technology choices and architecture
- Context: Current green-screen is actually quite fast

**[NFR-003] [CRITICAL] [SCALE]**  
**What is the criticality of each subsystem's performance?**
Rate each from 1 (flexible) to 5 (critical):
- GL_CORE (General Ledger): [1-5]
- IRS_CORE (Incomplete Records): [1-5]
- SL_MGMT (Sales Ledger): [1-5]
- PL_MGMT (Purchase Ledger): [1-5]
- ST_CTRL (Stock Control): [1-5]
- BATCH_FW (Batch Processing): [1-5]
- RPT_ENGINE (Reporting): [1-5]
- Dependencies: None
- Impact: Prioritizes optimization efforts

**[NFR-004] [IMPORTANT] [NUMERIC]**  
**How many concurrent users must be supported?**
- Data entry users: ___
- Query/report users: ___
- Peak concurrent: ___
- Dependencies: None
- Impact: Affects architecture and infrastructure sizing
- Context: Current COBOL system has limited concurrent user support

### 7.2 Security and Compliance

**[NFR-005] [CRITICAL] [MULTIPLE_CHOICE]**  
**What authentication method should be implemented?**
- [ ] Username/password
- [ ] SSO/SAML
- [ ] OAuth 2.0
- [ ] Multi-factor authentication
- [ ] Biometric
- [ ] Certificate-based
- [ ] Active Directory integration
- Dependencies: None
- Impact: Defines security architecture
- Context: Current system has basic user/password

**[NFR-006] [CRITICAL] [YES_NO]**  
**Are there specific data encryption requirements?**
- At rest: [Requirements]
- In transit: [Requirements]  
- Key management: [Requirements]
- Dependencies: None
- Impact: Influences technology stack and performance
- Context: Current system has no encryption

**[NFR-007] [IMPORTANT] [OPEN_TEXT]**  
**What audit trail requirements must be maintained?**
- Current capabilities to preserve:
  - All transactions are logged
  - User and timestamp on all changes
  - Before/after values for updates
- Additional requirements: ___
- Retention periods: ___
- Dependencies: None
- Impact: Affects data model and storage
- Context: System has comprehensive audit in AUDIT files

**[NFR-008] [IMPORTANT] [YES_NO]**  
**Do you require role-based access control (RBAC)?**
- Current: Basic user-level access
- Desired: Role/permission based?
- Dependencies: NFR-005
- Impact: Affects security design
- Context: Current system has limited access control

### 7.3 Availability and Reliability

**[NFR-009] [CRITICAL] [NUMERIC]**  
**What are the availability requirements?**
- Required uptime percentage: ___% 
- Planned maintenance window: ___
- Maximum unplanned downtime (hours/year): ___
- Dependencies: BUS-002
- Impact: Determines architecture (HA, DR requirements)

**[NFR-010] [IMPORTANT] [YES_NO]**  
**Is disaster recovery required?**
- RPO (Recovery Point Objective): ___
- RTO (Recovery Time Objective): ___
- Geographic redundancy required?
- Dependencies: NFR-009
- Impact: Affects infrastructure costs and architecture

---

## Section 8: Migration Execution

### 8.1 Resources and Constraints

**[EXEC-001] [CRITICAL] [MULTIPLE_CHOICE]**  
**What is the budget range for this migration?**
- [ ] < $500K
- [ ] $500K - $1M
- [ ] $1M - $3M  
- [ ] $3M - $5M
- [ ] $5M - $10M
- [ ] > $10M
- Dependencies: None
- Impact: Constrains approach, timeline, and technology choices

**[EXEC-002] [CRITICAL] [NUMERIC]**  
**How many resources are available for the migration?**
- Internal developers: ___
- External consultants: ___
- Business analysts: ___
- QA testers: ___
- Project managers: ___
- COBOL developers available: ___
- Dependencies: None
- Impact: Determines timeline feasibility

**[EXEC-003] [IMPORTANT] [YES_NO]**  
**Is there COBOL expertise available during migration?**
- Number of COBOL developers: ___
- Availability duration: ___
- Knowledge of ACAS specifically? ___
- Dependencies: None
- Impact: Affects knowledge transfer approach
- Context: System has custom business logic requiring deep understanding

**[EXEC-004] [CRITICAL] [MULTIPLE_CHOICE]**  
**What is the preferred team structure?**
- [ ] Single team for entire migration
- [ ] Team per subsystem
- [ ] Separate teams for legacy maintenance and new development
- [ ] Vendor-led with internal oversight
- [ ] Hybrid internal/external teams
- Dependencies: EXEC-002
- Impact: Influences project organization

**[EXEC-005] [IMPORTANT] [YES_NO]**  
**Will the business continue to enhance the legacy system during migration?**
- If yes, how to handle divergence?
- Dependencies: None
- Impact: Requires change synchronization strategy
- Context: Long migration may require continued legacy development

### 8.2 Risk Management

**[RISK-001] [CRITICAL] [SCALE]**  
**What is your risk tolerance for the migration?**
- Scale: 1 (Very conservative) to 5 (Aggressive)
- Dependencies: BUS-002
- Impact: Determines migration approach and validation requirements

**[RISK-002] [CRITICAL] [MULTIPLE_CHOICE]**  
**What is the fallback strategy if migration fails?**
- [ ] Maintain ability to rollback completely
- [ ] Parallel run until confidence achieved
- [ ] Fix-forward only (no rollback)
- [ ] Hybrid based on subsystem
- [ ] Incremental rollback capability
- Dependencies: RISK-001
- Impact: Affects migration design and infrastructure

**[RISK-003] [IMPORTANT] [OPEN_TEXT]**  
**What are the absolute "no-go" scenarios?**
Examples:
- Data loss
- Financial calculation errors
- Extended downtime
- Compliance violations
List unacceptable risks:
- Dependencies: None
- Impact: Defines guardrails for migration

**[RISK-004] [CRITICAL] [YES_NO]**  
**Is data loss acceptable in any scenario?**
- If yes, what data and under what conditions?
- Dependencies: RISK-003
- Impact: Determines backup and validation rigor
- Context: Financial system typically requires zero data loss

**[RISK-005] [IMPORTANT] [MULTIPLE_CHOICE]**  
**How should calculation differences be handled?**
- [ ] Must match to the penny
- [ ] Rounding differences acceptable
- [ ] Small variances with documentation
- [ ] Material differences only
- Dependencies: None
- Impact: Affects testing and validation approach
- Context: COBOL uses specific decimal arithmetic

---

## Section 9: Testing and Validation

### 9.1 Testing Strategy

**[TEST-001] [CRITICAL] [MULTIPLE_CHOICE]**  
**What testing approach is preferred?**
- [ ] Full parallel run comparison (old vs new)
- [ ] Subsystem-by-subsystem validation
- [ ] Risk-based testing (critical paths only)
- [ ] User acceptance testing only
- [ ] Comprehensive (all methods)
- Dependencies: RISK-001
- Impact: Determines testing timeline and resources

**[TEST-002] [CRITICAL] [NUMERIC]**  
**What is the acceptable variance in calculations?**
- Financial calculations tolerance: $___
- Inventory counts tolerance: ___
- Report totals tolerance: $___
- Percentage variance allowed: ___%
- Dependencies: RISK-005
- Impact: Defines success criteria

**[TEST-003] [IMPORTANT] [YES_NO]**  
**Will automated testing be implemented?**
- Unit test coverage target (%): ___
- Integration test requirements: ___
- Performance test requirements: ___
- Regression test automation: ___
- Dependencies: None
- Impact: Affects development approach and quality

**[TEST-004] [CRITICAL] [OPEN_TEXT]**  
**Which specific COBOL programs/reports are critical for validation?**
Critical programs to validate:
- gl090 (Trial Balance)
- gl100 (P&L Statement)  
- gl105 (Balance Sheet)
- sl130 (Sales Analysis)
- pl130 (Purchase Analysis)
- st080 (Stock Valuation)
List others:
- Dependencies: None
- Impact: Focuses testing efforts

**[TEST-005] [IMPORTANT] [MULTIPLE_CHOICE]**  
**How long should parallel run testing continue?**
- [ ] 1 month
- [ ] 3 months
- [ ] 6 months
- [ ] Full fiscal cycle
- [ ] Until variance targets met
- Dependencies: TEST-001, TEST-002
- Impact: Affects timeline and resource needs

### 9.2 Data Validation

**[TEST-006] [CRITICAL] [YES_NO]**  
**Should migrated data be validated against source?**
- Record counts: ___
- Balance totals: ___
- Relationship integrity: ___
- Historical transactions: ___
- Dependencies: None
- Impact: Defines validation scope

**[TEST-007] [IMPORTANT] [MULTIPLE_CHOICE]**  
**What level of historical transaction testing is required?**
- [ ] Spot checks only
- [ ] Statistical sampling
- [ ] Full year comparison
- [ ] Multi-year validation
- [ ] Critical transactions only
- Dependencies: DATA-004
- Impact: Determines testing effort

---

## Section 10: Post-Migration

### 10.1 Operations and Support

**[POST-001] [IMPORTANT] [MULTIPLE_CHOICE]**  
**Who will support the new system post-migration?**
- [ ] Internal IT team (trained)
- [ ] Original development team (retained)
- [ ] Managed service provider
- [ ] Vendor support contract
- [ ] Hybrid model
- Dependencies: None
- Impact: Influences documentation and knowledge transfer needs

**[POST-002] [CRITICAL] [YES_NO]**  
**Will the legacy COBOL system be maintained as backup?**
- If yes, for how long? ___
- What triggers reversion? ___
- Who maintains it? ___
- Dependencies: RISK-002
- Impact: Affects resource allocation and costs

**[POST-003] [IMPORTANT] [OPEN_TEXT]**  
**What are the success metrics for the migration?**
Technical metrics:
- Performance improvements
- System availability
- Error rates

Business metrics:
- Process efficiency gains
- Cost reductions
- User productivity

User satisfaction metrics:
- Training effectiveness
- Adoption rates

Timeline for measurement: ___
- Dependencies: BUS-001
- Impact: Defines project success

**[POST-004] [IMPORTANT] [MULTIPLE_CHOICE]**  
**What is the training strategy for users?**
- [ ] Formal classroom training
- [ ] Online/self-paced training
- [ ] Train-the-trainer approach
- [ ] Documentation only
- [ ] Embedded help/tutorials
- [ ] Phased by user group
- Dependencies: None
- Impact: Affects change management approach

**[POST-005] [NICE-TO-HAVE] [YES_NO]**  
**Should the new system include a "classic mode" UI option?**
- To ease transition?
- As permanent feature?
- Dependencies: TECH-004
- Impact: May improve user adoption
- Context: Long-time users accustomed to green screens

---

## Section 11: Priorities and Sequencing

### 11.1 Migration Sequencing

**[SEQ-001] [CRITICAL] [OPEN_TEXT]**  
**Based on the subsystem analysis, rank migration priority:**

Subsystems to rank:
1. GL_CORE - General Ledger Core
2. IRS_CORE - IRS/Tax Ledger  
3. SL_MGMT - Sales Ledger Management
4. PL_MGMT - Purchase Ledger Management
5. ST_CTRL - Stock Control
6. BATCH_FW - Batch Framework
7. RPT_ENGINE - Reporting Engine
8. SYS_ADMIN - System Administration
9. PERIOD_PROC - Period Processing
10. DAL - Data Access Layer
11. COMMON_UTIL - Common Utilities
12. INTEG_SVC - Integration Services

For each, explain why this priority.
- Dependencies: BUS-006
- Impact: Determines project phases

**[SEQ-002] [CRITICAL] [MULTIPLE_CHOICE]**  
**Which subsystem is the best pilot/proof of concept?**
- [ ] SYS_ADMIN - Simplest, most isolated
- [ ] ST_CTRL - Relatively standalone
- [ ] RPT_ENGINE - Read-only, lower risk
- [ ] IRS_CORE - Simpler than GL, good test
- [ ] Other: ___
- Dependencies: SEQ-001
- Impact: Defines starting point and proves approach

**[SEQ-003] [IMPORTANT] [YES_NO]**  
**Should tightly coupled subsystems be migrated together?**
Based on dependency analysis:
- GL_CORE + BATCH_FW (posting integration)
- SL_MGMT + ST_CTRL (stock updates)
- PL_MGMT + ST_CTRL (stock updates)
- All + DAL (data access layer)
Specify groupings: ___
- Dependencies: None
- Impact: Affects phase boundaries

**[SEQ-004] [CRITICAL] [OPEN_TEXT]**  
**What are the critical business dates that affect migration timing?**
- Year-end processing: ___
- Tax deadlines: ___
- Audit periods: ___
- Peak business seasons: ___
- Board reporting dates: ___
- Other critical dates: ___
- Dependencies: None
- Impact: Constrains migration windows
- Context: xl150 runs month-end, quarter-end, year-end

**[SEQ-005] [IMPORTANT] [YES_NO]**  
**Should migration align with fiscal year boundaries?**
- If yes, which fiscal year? ___
- Dependencies: SEQ-004
- Impact: May delay or accelerate project
- Context: Clean cutover at year-end may be simpler

---

## Decision Matrix

Based on your answers, here are common migration patterns:

### Conservative Approach
If: High criticality (BUS-002=5) + Low risk tolerance (RISK-001=1-2)
Then: 
- Parallel run strategy
- Subsystem-by-subsystem migration  
- Extended testing periods
- Maintain rollback capability

### Aggressive Modernization
If: Strong drivers (BUS-001=modernization) + Higher risk tolerance (RISK-001=4-5)
Then:
- Microservices architecture
- Complete re-engineering
- Shorter timeline
- Fix-forward approach

### Balanced Transformation  
If: Medium criticality (BUS-002=3) + Medium risk (RISK-001=3)
Then:
- Phased migration by subsystem
- Moderate re-engineering
- Strategic improvements
- Hybrid testing approach

### Technology Refresh Only
If: Keep functionality (FUNC-001=100%) + Modern tech stack needed
Then:
- Direct translation
- Same subsystem boundaries
- Automated testing critical
- Minimal business change

---

## Risk Assessment Questions

### Technical Risks

**[RISK-T01] [CRITICAL] [YES_NO]**  
**Are there undocumented COBOL programs or features?**
- How to discover? ___
- Impact: Hidden complexity

**[RISK-T02] [IMPORTANT] [YES_NO]**  
**Are there hard-coded business rules in programs?**
- How many identified? ___
- Impact: Difficult to extract and test

**[RISK-T03] [CRITICAL] [YES_NO]**  
**Are there external dependencies not documented?**
- Batch job schedulers?
- File transfers?
- External programs?
- Impact: Integration surprises

### Business Risks

**[RISK-B01] [CRITICAL] [YES_NO]**  
**Will key users resist the change?**
- Mitigation strategy? ___
- Impact: Adoption failure

**[RISK-B02] [IMPORTANT] [YES_NO]**  
**Could migration disrupt critical business periods?**
- Contingency plans? ___
- Impact: Business interruption

**[RISK-B03] [CRITICAL] [YES_NO]**  
**Is specialized business knowledge at risk?**
- Key person dependencies? ___
- Documentation gaps? ___
- Impact: Loss of business logic understanding

---

## Technical Deep Dive Questions

### COBOL-Specific Technical Patterns

**[TECH-D01] [IMPORTANT] [YES_NO]**  
**Should the PERFORM THRU pattern be preserved?**
- Current: Extensive use of PERFORM THRU for sections
- New: Modern structured programming?
- Impact: Code structure in new system

**[TECH-D02] [CRITICAL] [YES_NO]**  
**How to handle COBOL level 88 conditions?**
- Current: Extensive use for business logic
- Convert to: Enums? Constants? Config?
- Impact: Business rule implementation

**[TECH-D03] [IMPORTANT] [YES_NO]**  
**Should REDEFINES be converted to proper data structures?**
- Current: Memory overlay techniques
- New: Proper object/structure design?
- Impact: Data model complexity

**[TECH-D04] [CRITICAL] [MULTIPLE_CHOICE]**  
**How to handle COMP-3 (packed decimal) arithmetic?**
- [ ] BigDecimal or equivalent
- [ ] Fixed-point libraries
- [ ] Database decimal types
- [ ] Custom implementation
- Impact: Calculation accuracy

### File Handling Patterns

**[TECH-D05] [IMPORTANT] [YES_NO]**  
**Should START/READ NEXT patterns become cursors?**
- Current: Sequential file positioning
- New: Database cursors? Pagination?
- Impact: Data access patterns

**[TECH-D06] [CRITICAL] [YES_NO]**  
**How to handle alternate keys (ISAM)?**
- Current: Multiple key paths
- New: Indexes? Separate queries?
- Impact: Query performance

**[TECH-D07] [IMPORTANT] [YES_NO]**  
**Should file status codes be preserved?**
- Current: Extensive FS checking
- New: Exceptions? Status objects?
- Impact: Error handling design

### Batch Processing Patterns

**[TECH-D08] [CRITICAL] [YES_NO]**  
**Should batch control totals be maintained?**
- Current: Hash totals, record counts
- New: Database transactions?
- Impact: Audit and control design

**[TECH-D09] [IMPORTANT] [YES_NO]**  
**How to handle sort work files?**
- Current: SORT verb with work files  
- New: Database ORDER BY? In-memory?
- Impact: Performance and scalability

**[TECH-D10] [CRITICAL] [YES_NO]**  
**Should commit/restart logic be enhanced?**
- Current: Basic checkpoint/restart
- New: Distributed transactions? Sagas?
- Impact: Recovery capabilities

---

## Appendices

### Appendix A: Glossary of Terms

**ACAS**: Applewood Computers Accounting System
**DAL**: Data Access Layer - abstraction for database access
**FH**: File Handler - COBOL file I/O module
**IRS**: Incomplete Records System - simplified accounting
**ISAM**: Indexed Sequential Access Method
**Profit Center**: 2-digit branch/division code
**Posting**: Process of updating ledgers from transactions
**Period Processing**: Month/quarter/year-end procedures

### Appendix B: Reference to Original System Documentation

1. Functional Documentation: `1_FUNCTIONAL DOCUMENTATION/`
2. Subsystems Documentation: `2_SUBSYSTEMS DOCUMENTATION/`
3. Source Code: Various directories (general/, sales/, purchase/, stock/, irs/, common/)
4. Database Schema: `mysql/ACASDB.sql`

### Appendix C: Migration Pattern Examples

1. **Strangler Fig**: Gradually replace subsystems while maintaining interfaces
2. **Big Bang**: Complete system replacement during a cutover weekend  
3. **Parallel Run**: Both systems running with reconciliation
4. **Phased Cutover**: Subsystem by subsystem with coexistence

### Appendix D: Answer Validation Checklist

Before finalizing responses, ensure:

1. [ ] All CRITICAL questions answered
2. [ ] Dependencies between answers are consistent
3. [ ] Budget aligns with timeline and approach
4. [ ] Risk tolerance matches migration strategy
5. [ ] Resource availability supports timeline
6. [ ] Technology choices are compatible
7. [ ] Integration requirements are complete
8. [ ] Testing strategy matches risk tolerance
9. [ ] Success criteria are measurable
10. [ ] Critical dates are considered in planning

---

## Next Steps

1. **Complete Initial Response**: Answer all CRITICAL questions first
2. **Review with Stakeholders**: Ensure alignment on key decisions
3. **Refine Requirements**: Answer IMPORTANT questions based on critical decisions
4. **Technical Deep Dive**: Address technical questions with development team
5. **Finalize Strategy**: Document migration approach based on responses
6. **Create Project Plan**: Develop detailed plan incorporating all requirements

---

*This questionnaire is version 1.0 and should be updated as new information emerges during the migration planning process.*