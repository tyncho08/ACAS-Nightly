# Target System Migration Questionnaire Generator

## Context
You must access to:
1. The original COBOL source code of the ACAS legacy system
2. The functional documentation in `1_FUNCTIONAL DOCUMENTATION/` folder
3. The subsystem analysis in `2_SUBSYSTEMS DOCUMENTATION/` folder

You must save results in `3_AI ASK ABOUT TARGET/` folder

Your task is to generate a comprehensive questionnaire that will gather all necessary information about the target system environment, migration strategy, and business requirements to ensure a successful migration from the legacy COBOL system to a modern architecture.

## Objective
Create a structured set of questions organized by domain that will:
- Clarify target architecture preferences and constraints
- Identify business priorities and migration drivers
- Uncover technical requirements and limitations
- Define success criteria and risk tolerance
- Establish timeline and resource parameters
- Determine integration and coexistence needs

## Question Generation Framework

### Instructions for Question Design
```
Each question should be:
- SPECIFIC: Avoid ambiguous or overly broad questions
- ACTIONABLE: Answers should directly inform migration decisions
- MEASURABLE: Include options for quantifiable responses where possible
- CONTEXTUAL: Reference specific findings from the legacy system analysis
- PRIORITIZED: Mark questions as [CRITICAL], [IMPORTANT], or [NICE-TO-HAVE]

Format each question with:
- Question ID: [DOMAIN-###]
- Priority: [CRITICAL|IMPORTANT|NICE-TO-HAVE]
- Type: [MULTIPLE_CHOICE|OPEN_TEXT|NUMERIC|YES_NO|SCALE]
- Dependencies: [Which questions must be answered first]
- Impact: [What migration decisions this affects]
```

## Section 1: Business Context and Drivers

### 1.1 Strategic Alignment
```markdown
## Business Strategy Questions

[BUS-001] [CRITICAL] [OPEN_TEXT]
**What are the top 3 business drivers for migrating from the current COBOL system?**
- Options to consider: Cost reduction, scalability, talent availability, compliance, innovation enablement
- Impact: Determines migration approach and success metrics

[BUS-002] [CRITICAL] [SCALE]
**How critical is the ACAS system to daily business operations?**
- Scale: 1 (Can tolerate week+ downtime) to 5 (Zero downtime tolerance)
- Impact: Defines migration strategy (big bang vs phased)

[BUS-003] [IMPORTANT] [NUMERIC]
**What is the expected business growth rate over the next 5 years?**
- Provide percentage annual growth
- Impact: Influences scalability requirements

[BUS-004] [CRITICAL] [MULTIPLE_CHOICE]
**What is the acceptable timeframe for complete migration?**
- [ ] 6 months
- [ ] 12 months
- [ ] 18 months
- [ ] 24 months
- [ ] 36+ months
- Impact: Determines phasing and resource allocation

[BUS-005] [IMPORTANT] [YES_NO]
**Are there any upcoming regulatory changes that the new system must address?**
- If yes, specify requirements and deadlines
- Impact: May prioritize certain subsystem migrations
```

### 1.2 Current Pain Points
```markdown
## Legacy System Issues

[BUS-006] [CRITICAL] [OPEN_TEXT]
**Based on the subsystem analysis, which of these identified subsystems cause the most operational issues?**
- List subsystems: GL_CORE, AR_MGMT, AP_MGMT, INV_CTRL, IRS_PROC
- Describe specific problems
- Impact: Prioritizes migration sequence

[BUS-007] [IMPORTANT] [MULTIPLE_CHOICE]
**What are the biggest limitations of the current COBOL system?** (Select all that apply)
- [ ] Performance/speed issues
- [ ] Lack of real-time processing
- [ ] Limited reporting capabilities
- [ ] Poor integration with modern systems
- [ ] User interface limitations
- [ ] Maintenance complexity
- [ ] Lack of skilled COBOL developers
- Impact: Defines key requirements for target system

[BUS-008] [IMPORTANT] [NUMERIC]
**How many business workarounds exist due to system limitations?**
- Provide count and brief descriptions
- Impact: Identifies hidden requirements
```

## Section 2: Target Architecture Preferences

### 2.1 Architecture Style
```markdown
## Architecture Decisions

[ARCH-001] [CRITICAL] [MULTIPLE_CHOICE]
**What is your preferred target architecture pattern?**
- [ ] Monolithic (modern stack)
- [ ] Service-Oriented Architecture (SOA)
- [ ] Microservices
- [ ] Serverless/Function-as-a-Service
- [ ] Hybrid (specify combination)
- Impact: Defines entire migration approach

[ARCH-002] [CRITICAL] [MULTIPLE_CHOICE]
**Given the subsystem boundaries identified, which migration pattern do you prefer?**
- [ ] Strangler Fig (gradual replacement)
- [ ] Big Bang (complete replacement)
- [ ] Parallel Run (both systems simultaneously)
- [ ] Phased Cutover (subsystem by subsystem)
- Impact: Determines migration timeline and risk

[ARCH-003] [IMPORTANT] [YES_NO]
**Should the new system maintain the same subsystem boundaries identified in the analysis?**
- If no, describe desired changes
- Impact: Affects design and migration complexity

[ARCH-004] [CRITICAL] [MULTIPLE_CHOICE]
**What is your cloud strategy?**
- [ ] On-premises only
- [ ] Private cloud
- [ ] Public cloud (AWS/Azure/GCP)
- [ ] Hybrid cloud
- [ ] Multi-cloud
- Impact: Influences technology choices and costs
```

### 2.2 Technology Stack
```markdown
## Technology Preferences

[TECH-001] [CRITICAL] [MULTIPLE_CHOICE]
**Preferred programming language(s) for the new system?** (Select up to 3)
- [ ] Java
- [ ] C#/.NET
- [ ] Python
- [ ] Go
- [ ] JavaScript/TypeScript (Node.js)
- [ ] Rust
- [ ] Keep COBOL with modernization
- [ ] Other (specify)
- Impact: Determines development resources needed

[TECH-002] [CRITICAL] [MULTIPLE_CHOICE]
**Preferred database technology?**
- [ ] Traditional RDBMS (PostgreSQL, MySQL, Oracle, SQL Server)
- [ ] NoSQL (MongoDB, DynamoDB, Cassandra)
- [ ] NewSQL (CockroachDB, VoltDB)
- [ ] Multi-model (mixed based on subsystem needs)
- Impact: Affects data migration strategy

[TECH-003] [IMPORTANT] [MULTIPLE_CHOICE]
**How should the current file-based data storage be migrated?**
- [ ] Direct conversion to relational tables
- [ ] Redesign data model completely
- [ ] Hybrid (some files, some database)
- [ ] Event sourcing pattern
- Impact: Determines data migration complexity

[TECH-004] [IMPORTANT] [MULTIPLE_CHOICE]
**Preferred user interface approach?**
- [ ] Web-based (SPA)
- [ ] Web-based (server-rendered)
- [ ] Desktop application
- [ ] Mobile-first
- [ ] API-only (headless)
- [ ] Multiple interfaces
- Impact: Affects frontend development needs
```

## Section 3: Functional Requirements

### 3.1 Feature Parity and Enhancements
```markdown
## Functional Expectations

[FUNC-001] [CRITICAL] [MULTIPLE_CHOICE]
**What level of feature parity is required with the legacy system?**
- [ ] 100% - All features must be replicated
- [ ] 90% - Core features only, remove rarely used
- [ ] 80% - Significant simplification acceptable
- [ ] Re-engineer - Complete business process redesign
- Impact: Defines scope and complexity

[FUNC-002] [IMPORTANT] [OPEN_TEXT]
**Which COBOL batch processes must be preserved vs. converted to real-time?**
- Review batch process list from documentation
- Specify each as: Keep batch / Convert to real-time / Eliminate
- Impact: Affects architecture and processing design

[FUNC-003] [CRITICAL] [YES_NO]
**Must the new system support the IRS (Incomplete Records System) functionality?**
- If yes, can it be redesigned or must maintain current logic?
- Impact: May require special handling in migration

[FUNC-004] [IMPORTANT] [OPEN_TEXT]
**What new capabilities should the target system add that don't exist today?**
- List and prioritize new features
- Impact: Extends project scope beyond migration

[FUNC-005] [IMPORTANT] [MULTIPLE_CHOICE]
**How should the reporting subsystem be modernized?**
- [ ] Maintain current reports as-is
- [ ] Modernize with BI tool integration
- [ ] Self-service analytics capability
- [ ] Real-time dashboards
- [ ] All of the above
- Impact: Determines reporting architecture
```

### 3.2 Business Rules and Calculations
```markdown
## Business Logic Handling

[FUNC-006] [CRITICAL] [MULTIPLE_CHOICE]
**How should complex COBOL business logic be handled?**
- [ ] Translate directly to new language
- [ ] Re-implement with modern patterns
- [ ] Extract to rules engine
- [ ] Microservice per major calculation
- [ ] Review and simplify where possible
- Impact: Affects migration approach and testing

[FUNC-007] [IMPORTANT] [YES_NO]
**Are all financial calculations documented and validated?**
- Reference calculation documentation from analysis
- If no, what additional validation is needed?
- Impact: Determines testing requirements

[FUNC-008] [CRITICAL] [OPEN_TEXT]
**Which accounting standards and regulations must the new system comply with?**
- List specific standards (GAAP, IFRS, SOX, etc.)
- Any industry-specific requirements?
- Impact: Defines compliance requirements
```

## Section 4: Integration Requirements

### 4.1 External Systems
```markdown
## Integration Landscape

[INT-001] [CRITICAL] [OPEN_TEXT]
**What external systems must the new system integrate with?**
- List each system with:
  - System name and purpose
  - Current integration method
  - Desired integration method
  - Data flow direction
- Impact: Defines integration architecture

[INT-002] [IMPORTANT] [MULTIPLE_CHOICE]
**Preferred integration approach for the new system?**
- [ ] REST APIs
- [ ] GraphQL
- [ ] Message queues (RabbitMQ, Kafka)
- [ ] ETL/batch files
- [ ] Direct database access
- [ ] Mixed approach
- Impact: Determines integration patterns

[INT-003] [CRITICAL] [YES_NO]
**Will the legacy COBOL system need to coexist with the new system?**
- If yes, for how long?
- Which subsystems must maintain synchronization?
- Impact: Requires bidirectional sync strategy

[INT-004] [IMPORTANT] [MULTIPLE_CHOICE]
**How should master data be managed during migration?**
- [ ] Maintain in legacy until full cutover
- [ ] Migrate to new system immediately
- [ ] Dual maintenance during transition
- [ ] MDM solution as separate system
- Impact: Affects data consistency strategy
```

## Section 5: Non-Functional Requirements

### 5.1 Performance and Scalability
```markdown
## Performance Expectations

[NFR-001] [CRITICAL] [NUMERIC]
**What are the transaction volume requirements?**
Based on current analysis showing [X transactions/day]:
- Expected peak transactions per second:
- Expected daily transaction count:
- Expected monthly growth rate:
- Impact: Sizes infrastructure and architecture

[NFR-002] [IMPORTANT] [NUMERIC]
**What are the response time requirements?**
- Online transaction response time (ms):
- Report generation time (seconds):
- Batch processing window (hours):
- Impact: Influences technology choices

[NFR-003] [CRITICAL] [SCALE]
**What is the criticality of each subsystem's performance?**
Rate each from 1 (flexible) to 5 (critical):
- GL_CORE: [1-5]
- AR_MGMT: [1-5]
- AP_MGMT: [1-5]
- INV_CTRL: [1-5]
- IRS_PROC: [1-5]
- Impact: Prioritizes optimization efforts
```

### 5.2 Security and Compliance
```markdown
## Security Requirements

[NFR-004] [CRITICAL] [MULTIPLE_CHOICE]
**What authentication method should be implemented?**
- [ ] Username/password
- [ ] SSO/SAML
- [ ] OAuth 2.0
- [ ] Multi-factor authentication
- [ ] Biometric
- [ ] Certificate-based
- Impact: Defines security architecture

[NFR-005] [CRITICAL] [YES_NO]
**Are there specific data encryption requirements?**
- At rest: [Requirements]
- In transit: [Requirements]
- Key management: [Requirements]
- Impact: Influences technology stack

[NFR-006] [IMPORTANT] [OPEN_TEXT]
**What audit trail requirements must be maintained?**
- Current COBOL audit capabilities from analysis
- Additional requirements for new system
- Retention periods
- Impact: Affects data model and storage
```

## Section 6: Migration Execution

### 6.1 Resources and Constraints
```markdown
## Project Parameters

[EXEC-001] [CRITICAL] [MULTIPLE_CHOICE]
**What is the budget range for this migration?**
- [ ] < $500K
- [ ] $500K - $1M
- [ ] $1M - $3M
- [ ] $3M - $5M
- [ ] > $5M
- Impact: Constrains approach and timeline

[EXEC-002] [CRITICAL] [NUMERIC]
**How many resources are available for the migration?**
- Internal developers:
- External consultants:
- Business analysts:
- Testers:
- Project managers:
- Impact: Determines timeline feasibility

[EXEC-003] [IMPORTANT] [YES_NO]
**Is there COBOL expertise available during migration?**
- Number of COBOL developers:
- Availability duration:
- Impact: Affects knowledge transfer approach

[EXEC-004] [CRITICAL] [MULTIPLE_CHOICE]
**What is the preferred team structure?**
- [ ] Single team for entire migration
- [ ] Team per subsystem
- [ ] Separate teams for legacy maintenance and new development
- [ ] Vendor-led with internal oversight
- Impact: Influences project organization
```

### 6.2 Risk Management
```markdown
## Risk Tolerance

[RISK-001] [CRITICAL] [SCALE]
**What is your risk tolerance for the migration?**
- Scale: 1 (Very conservative) to 5 (Aggressive)
- Impact: Determines migration approach

[RISK-002] [CRITICAL] [MULTIPLE_CHOICE]
**What is the fallback strategy if migration fails?**
- [ ] Maintain ability to rollback completely
- [ ] Parallel run until confidence
- [ ] Fix-forward only
- [ ] Hybrid based on subsystem
- Impact: Affects migration design

[RISK-003] [IMPORTANT] [OPEN_TEXT]
**What are the absolute "no-go" scenarios?**
- List unacceptable risks or outcomes
- Impact: Defines guardrails for migration

[RISK-004] [CRITICAL] [YES_NO]
**Is data loss acceptable in any scenario?**
- If yes, what data and under what conditions?
- Impact: Determines backup and validation rigor
```

## Section 7: Data Migration

### 7.1 Data Strategy
```markdown
## Data Migration Approach

[DATA-001] [CRITICAL] [MULTIPLE_CHOICE]
**Based on the data analysis, what is your data migration strategy?**
- [ ] Lift and shift (minimal transformation)
- [ ] Transform and optimize
- [ ] Complete redesign
- [ ] Incremental with continuous sync
- Impact: Defines data migration project

[DATA-002] [CRITICAL] [NUMERIC]
**What is the data volume to migrate?**
Review from documentation:
- Number of master records per entity:
- Historical transaction years to migrate:
- Total data size (GB):
- Impact: Sizes migration effort

[DATA-003] [IMPORTANT] [MULTIPLE_CHOICE]
**How should data quality issues be handled?**
- [ ] Migrate as-is, fix in new system
- [ ] Clean before migration
- [ ] Clean during migration
- [ ] Only migrate clean data
- Impact: Affects timeline and process

[DATA-004] [CRITICAL] [YES_NO]
**Is historical data audit trail critical?**
- Years of history required:
- Can be archived vs. online:
- Impact: Influences storage strategy
```

## Section 8: Testing and Validation

### 8.1 Testing Strategy
```markdown
## Quality Assurance Approach

[TEST-001] [CRITICAL] [MULTIPLE_CHOICE]
**What testing approach is preferred?**
- [ ] Full parallel run comparison
- [ ] Subsystem-by-subsystem validation
- [ ] Risk-based testing
- [ ] User acceptance only
- [ ] Comprehensive (all methods)
- Impact: Determines testing timeline and resources

[TEST-002] [CRITICAL] [NUMERIC]
**What is the acceptable variance in calculations?**
- Financial calculations tolerance:
- Inventory counts tolerance:
- Report totals tolerance:
- Impact: Defines success criteria

[TEST-003] [IMPORTANT] [YES_NO]
**Will automated testing be implemented?**
- Unit test coverage target (%):
- Integration test requirements:
- Performance test requirements:
- Impact: Affects development approach

[TEST-004] [CRITICAL] [OPEN_TEXT]
**Which specific COBOL programs/reports are critical for validation?**
- List programs that must match exactly
- Impact: Focuses testing efforts
```

## Section 9: Post-Migration

### 9.1 Operations and Support
```markdown
## Operational Readiness

[POST-001] [IMPORTANT] [MULTIPLE_CHOICE]
**Who will support the new system post-migration?**
- [ ] Internal IT team
- [ ] Original development team
- [ ] Managed service provider
- [ ] Hybrid model
- Impact: Influences documentation and training needs

[POST-002] [CRITICAL] [YES_NO]
**Will the legacy COBOL system be maintained as backup?**
- If yes, for how long?
- What triggers reversion?
- Impact: Affects resource allocation

[POST-003] [IMPORTANT] [OPEN_TEXT]
**What are the success metrics for the migration?**
- Technical metrics:
- Business metrics:
- User satisfaction metrics:
- Timeline for measurement:
- Impact: Defines project success

[POST-004] [IMPORTANT] [MULTIPLE_CHOICE]
**What is the training strategy for users?**
- [ ] Formal classroom training
- [ ] Online/self-paced training
- [ ] Train-the-trainer approach
- [ ] Documentation only
- [ ] Embedded help/tutorials
- Impact: Affects change management approach
```

## Section 10: Priorities and Sequencing

### 10.1 Migration Sequencing
```markdown
## Priority Decisions

[SEQ-001] [CRITICAL] [OPEN_TEXT]
**Based on the subsystem analysis, rank migration priority:**
1. First subsystem to migrate: [Why?]
2. Second subsystem: [Why?]
3. Third subsystem: [Why?]
(Continue for all subsystems)
- Impact: Determines project phases

[SEQ-002] [CRITICAL] [MULTIPLE_CHOICE]
**Which subsystem is the best pilot/proof of concept?**
Review subsystem documentation and select based on:
- [ ] Lowest risk
- [ ] Highest business value
- [ ] Most isolated/independent
- [ ] Most problematic currently
- [ ] Simplest technically
- Impact: Defines starting point

[SEQ-003] [IMPORTANT] [YES_NO]
**Should tightly coupled subsystems be migrated together?**
Based on dependency analysis:
- GL_CORE + [coupled subsystems]
- AR_MGMT + [coupled subsystems]
- Impact: Affects phase boundaries

[SEQ-004] [CRITICAL] [OPEN_TEXT]
**What are the critical business dates that affect migration timing?**
- Year-end processing:
- Tax deadlines:
- Audit periods:
- Peak business seasons:
- Impact: Constrains migration windows
```

## Questionnaire Output Format

### Generate the Following Deliverables:

```markdown
# ACAS Migration Requirements Questionnaire

## Executive Summary
- Total questions: [count by priority]
- Critical questions requiring immediate answers: [list]
- Dependencies between sections: [map]

## Response Template
[Provide a structured template for collecting answers]

## Quick Start Guide
- Top 20 questions to answer first
- Why these questions matter most
- Impact of not answering

## Full Questionnaire
[All questions organized by section]

## Decision Matrix
[Table showing how different answer combinations lead to different migration strategies]

## Risk Assessment Questions
[Subset focused on identifying risks]

## Technical Deep Dive Questions
[Detailed technical questions based on specific COBOL patterns found]

## Appendices
A. Glossary of Terms
B. Reference to Original System Documentation
C. Migration Pattern Examples
D. Answer Validation Checklist
```

## Instructions for Using This Questionnaire

1. **Review all documentation first** - Reference specific findings from the COBOL analysis
2. **Customize questions** - Add system-specific questions based on unique features found
3. **Prioritize ruthlessly** - Mark truly critical questions vs nice-to-have
4. **Provide context** - Include relevant metrics/findings from the legacy system
5. **Enable decision-making** - Each answer should drive a specific migration decision
6. **Track dependencies** - Note which questions must be answered in sequence
7. **Version control** - This questionnaire will evolve as answers reveal new questions

## Meta-Questions for the AI

Before generating the questionnaire, consider:
1. What unique COBOL patterns in the code require special attention?
2. Which subsystems have the most complex interdependencies?
3. What technical debt items discovered need explicit decisions?
4. Are there any mysterious or undocumented features that need clarification?
5. What assumptions from the analysis need validation?

Generate a comprehensive yet focused questionnaire that will gather all necessary information to plan and execute a successful migration from the COBOL ACAS system to a modern architecture.

Think ultra mega hard.