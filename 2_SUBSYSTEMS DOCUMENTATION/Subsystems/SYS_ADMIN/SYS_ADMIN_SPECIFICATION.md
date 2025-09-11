# Subsystem: SYS_ADMIN - System Administration

## Executive Summary
- **Purpose**: Central configuration, parameter management, and system control providing foundational settings for all ACAS subsystems
- **Business Value**: Ensures system-wide consistency, enables business configuration without code changes, maintains security and control settings
- **Key Users**: System administrators, finance managers, implementation consultants
- **Criticality**: CRITICAL - System cannot operate without proper configuration

## Functional Capabilities

### Core Functions

1. **System Parameter Management**
   - Description: Maintain global system configuration
   - Business Rules:
     - Single source of truth for all parameters
     - Version control for changes
     - Validation of parameter values
     - Dependency checking
     - Change audit trail
   - Triggers: Initial setup, business changes, period updates
   - Outcomes: Consistent system-wide configuration

2. **Company Information Management**
   - Description: Maintain legal entity and business details
   - Business Rules:
     - Company name and address
     - Registration numbers (VAT, company)
     - Contact information
     - Bank details
     - Multi-company support (via profit centers)
   - Triggers: Company setup, regulatory changes
   - Outcomes: Accurate company data for reports

3. **Period and Date Control**
   - Description: Manage accounting periods and system dates
   - Business Rules:
     - 12 monthly periods + adjustments
     - Period open/close status
     - Date validation ranges
     - Year-end rollover
     - Multi-year history
   - Triggers: Month-end, year-end, daily operations
   - Outcomes: Controlled period management

4. **VAT Configuration**
   - Description: Maintain tax rates and rules
   - Business Rules:
     - Multiple VAT rates (up to 5)
     - Effective dating
     - VAT account mappings
     - Exemption rules
     - Report parameters
   - Triggers: Tax law changes, rate updates
   - Outcomes: Accurate tax calculations

5. **Master Data Administration**
   - Description: Manage shared reference data
   - Business Rules:
     - Analysis codes maintenance
     - Delivery address management
     - System-wide defaults
     - Code validation rules
     - Cross-reference tables
   - Triggers: Business requirement changes
   - Outcomes: Consistent reference data

### Business Processes Supported
- System initialization
- Period management
- Tax compliance
- Multi-entity configuration
- Security administration
- Integration configuration
- Master data governance
- System health monitoring

## Data Domain

### Owned Entities

**SYSTEM-REC (System Parameters)**
- Business description: Core system configuration and parameters
- Key Attributes:
  - System version info
  - VAT rates (1-5)
  - Period/cycle info
  - Company details
  - Print/email settings
  - Module activation flags
  - RDBMS configuration
  - Processing options
- Business Identifiers: Single record file
- Lifecycle: Created at install, continuously maintained

**ANALYSIS-REC (Analysis Codes)**
- Business description: Product/service categorization
- Key Attributes:
  - PA-CODE (3 chars)
  - PA-GL (GL account link)
  - PA-DESC (description)
  - PA-PRINT (report flag)
- Business Identifiers: Analysis code
- Lifecycle: Created as needed, rarely deleted

**DELIVERY-REC (Delivery Addresses)**
- Business description: Alternative delivery locations
- Key Attributes:
  - DELIV-KEY (8 chars)
  - DELIV-NAME
  - DELIV-ADDRESS
- Business Identifiers: Entity + sequence
- Lifecycle: Created per customer/supplier

**System Control Tables**
- Business description: Various control parameters
- Including:
  - Profit center definitions
  - Report parameters
  - Security settings
  - Interface configurations
- Business Identifiers: Various
- Lifecycle: Setup and maintenance

### Referenced Entities
- None (this is the root configuration)

## Interface Contracts

### Inbound Interfaces

| Interface ID | Source | Data Type | Frequency | Business Purpose |
|-------------|--------|-----------|-----------|------------------|
| INT_PARAM_001 | Users | Parameter updates | As needed | Configuration |
| INT_PERIOD_001 | Period close | Period advance | Monthly | Period control |
| INT_TAX_001 | Tax updates | Rate changes | Legislative | VAT compliance |
| INT_MASTER_001 | Various | Master data | As needed | Reference data |

### Outbound Interfaces

| Interface ID | Target | Data Type | Frequency | Business Purpose |
|-------------|--------|-----------|-----------|------------------|
| INT_SYS_ALL_001 | All modules | Parameters | Every operation | Configuration |
| INT_SYS_VAT_001 | SL/PL/GL | VAT rates | Per transaction | Tax calculation |
| INT_SYS_PERIOD_001 | All | Period info | Per validation | Date control |
| INT_SYS_COMPANY_001 | Reports | Company data | Per report | Headers/footers |

### Internal APIs/Services

**Parameter Retrieval Service**
- Parameters: Parameter-Group, Parameter-Name
- Returns: Parameter-Value, Effective-Date
- Purpose: Get configuration values
- Validation: Valid parameter name
- Error Handling: Default values, missing parameter

**Period Control Service**
- Parameters: Operation-Type, Target-Period
- Returns: Success/Failure, New-Period
- Purpose: Manage period operations
- Validation: Sequential periods, prerequisites
- Error Handling: Period gaps, future periods

**Configuration Update Service**
- Parameters: Parameter-Name, New-Value, Effective-Date
- Returns: Success/Failure, Previous-Value
- Purpose: Update system parameters
- Validation: Value ranges, dependencies
- Error Handling: Invalid values, locked parameters

## Business Rules Engine

### Configuration Rules
- **CFG-001**: VAT rates between 0 and 99.99
- **CFG-002**: Period must advance sequentially
- **CFG-003**: Company VAT number format validation
- **CFG-004**: Analysis codes must be unique
- **CFG-005**: RDBMS config requires connection test

### Validation Rules
- **VAL-SYS-001**: Email addresses must be valid format
- **VAL-SYS-002**: Dates must be valid calendar dates
- **VAL-SYS-003**: Numeric parameters within ranges
- **VAL-SYS-004**: Required fields cannot be empty
- **VAL-SYS-005**: Dependent parameters consistency

### Security Rules
- **SEC-SYS-001**: Parameter changes require admin role
- **SEC-SYS-002**: Period close requires authorization
- **SEC-SYS-003**: Audit trail for all changes
- **SEC-SYS-004**: No deletion of historical parameters
- **SEC-SYS-005**: Sensitive data encryption required

## Operational Characteristics

### Processing Patterns
- **Real-time Access**:
  - Parameter reads: Continuous
  - Validation checks: Per transaction
  - Configuration queries: On-demand
- **Batch Processing**:
  - Period roll: Monthly
  - Parameter broadcast: After changes
  - Cleanup routines: Weekly
- **Maintenance Windows**:
  - Parameter updates: Scheduled
  - Period operations: Month-end
  - System verification: Daily

### Data Volumes
- Configuration Data:
  - System parameters: ~500 settings
  - Analysis codes: 50-200 codes
  - Delivery addresses: 100-1000
- Access Patterns:
  - Parameter reads: 1000s/day
  - Updates: 10-50/month
- Growth Rate:
  - Minimal (configuration stable)

## Dependencies

### Upstream Dependencies
- Installation process (initial setup)
- Business requirements (configuration needs)
- Regulatory changes (tax updates)

### Downstream Dependencies
- ALL MODULES depend on SYS_ADMIN
- Critical parameters:
  - System.dat availability
  - VAT rates accuracy
  - Period control
  - Company information

### External Dependencies
- Operating system (file permissions)
- Database system (if RDBMS)
- Backup systems (configuration protection)

## Quality Attributes

### Performance Requirements
- Response Time:
  - Parameter read: < 100ms
  - Configuration update: < 2 seconds
  - Validation check: < 500ms
- Availability:
  - 99.99% for reads
  - 99.9% for updates
- Caching:
  - Parameters cached per session
  - Invalidation on update

### Reliability Requirements
- Availability: 99.99% (system critical)
- Recovery Time: 15 minutes RTO
- Recovery Point: Last backup
- Data Integrity: Checksums on critical data

### Compliance Requirements
- Change control: All updates logged
- Authorization: Role-based access
- Audit trail: Complete history
- Data protection: Encryption for sensitive data

## Evolution Potential

### Enhancement Opportunities
- Web-based configuration UI
- Multi-tenant support
- Dynamic parameter reload
- Configuration templates
- Automated compliance updates

### Modernization Candidates
- REST API for configuration
- Cloud parameter store
- Version control integration
- Infrastructure as code
- Zero-downtime updates

### Known Limitations
- Single parameter file
- No real-time reload
- Limited validation rules
- Character interface only
- No parameter inheritance
- Basic security model

## Risk Assessment

### Technical Risks
- Single point of failure
- File corruption impact
- No redundancy
- Limited scalability

### Business Risks
- Incorrect configuration affects all
- Period errors block operations
- VAT errors cause compliance issues
- Parameter loss requires rebuild

### Mitigation Strategies
- Regular backups of system.dat
- Parameter validation routines
- Change control procedures
- Configuration documentation
- Disaster recovery plan

## Critical Parameters

### System-Wide Impact Parameters
| Parameter | Description | Impact if Wrong |
|-----------|-------------|-----------------|
| VAT Rates | Tax percentages | All calculations wrong |
| Current Period | Active accounting period | Cannot post transactions |
| RDBMS Config | Database connection | No data access |
| Company Name | Legal entity name | All reports wrong |
| GL/IRS Flag | Which ledger active | Wrong accounting system |

### Module Activation Flags
| Flag | Controls | Default |
|------|----------|---------|
| Level-1 | GL active | 1 (Yes) |
| Level-2 | PL active | 1 (Yes) |
| Level-3 | SL active | 1 (Yes) |
| Level-4 | Stock active | 1 (Yes) |
| Level-5 | IRS active | 0 (No) |

### Integration Parameters
- Print spool configuration
- Email server settings
- File path definitions
- Date format settings
- Currency symbols

## Administration Procedures

### Daily Tasks
- Monitor system.dat accessibility
- Check parameter read errors
- Verify period date consistency

### Monthly Tasks
- Period advancement
- Parameter backup
- Configuration review
- Usage analysis

### Annual Tasks
- Year-end rollover
- Parameter cleanup
- Configuration documentation
- Compliance review

---

Document Version: 1.0
Subsystem Version: SYS_ADMIN v3.02
Analysis Date: December 2024