# Subsystem: DAL - Data Access Layer

## Executive Summary
- **Purpose**: Provides abstraction layer between business logic and data storage, supporting both COBOL files and RDBMS with transparent switching capability
- **Business Value**: Enables database flexibility, simplifies migration paths, provides consistent data access patterns, supports modernization without business logic changes
- **Key Users**: All ACAS modules (indirect), system developers, database administrators
- **Criticality**: CRITICAL - Foundation layer for all data operations

## Functional Capabilities

### Core Functions

1. **Unified Data Access Interface**
   - Description: Single API for all data operations regardless of storage
   - Business Rules:
     - Consistent calling conventions
     - Storage-agnostic operations
     - Automatic storage detection
     - Transaction semantics
     - Error standardization
   - Triggers: Any data operation from business layer
   - Outcomes: Data retrieved/stored transparently

2. **File Handler Management**
   - Description: COBOL file operations through handlers
   - Business Rules:
     - ISAM file support
     - Sequential file support
     - Record locking
     - Key management (1-3 keys)
     - File status mapping
   - Triggers: File-based storage active
   - Outcomes: Traditional file operations

3. **Database Operations**
   - Description: RDBMS operations through SQL
   - Business Rules:
     - MySQL/MariaDB support
     - Prepared statements
     - Connection pooling
     - Transaction control
     - Cursor management
   - Triggers: RDBMS storage active
   - Outcomes: Database operations

4. **Dual-Mode Processing**
   - Description: Simultaneous file and database operations
   - Business Rules:
     - Write to both storages
     - Read from primary (DB)
     - Synchronization checking
     - Migration support
     - Consistency validation
   - Triggers: Dual mode configuration
   - Outcomes: Parallel data maintenance

5. **Data Migration Utilities**
   - Description: Move data between storage types
   - Business Rules:
     - Load programs (*LD)
     - Unload programs (*UNL)
     - Restore programs (*RES)
     - Validation routines
     - Progress tracking
   - Triggers: Migration requirements
   - Outcomes: Data transferred between storages

### Business Processes Supported
- All data read operations
- All data write operations
- Transaction management
- Data migration
- Backup and restore
- Performance optimization
- Storage abstraction
- Multi-storage support

## Data Domain

### Owned Entities

**File Handlers (acas000-acas032)**
- Business description: COBOL file operation programs
- Key Components:
  - acas000: System/defaults handler
  - acas005: Sales ledger handler
  - acas006: Purchase ledger handler
  - acas007: Stock file handler
  - acas008: SL posting handler
  - Others for each file type
- Business Purpose: Traditional file access
- Lifecycle: Called per operation

**DAL Modules (*MT programs)**
- Business description: Database operation programs
- Key Components:
  - salesMT: Sales ledger DAL
  - purchMT: Purchase ledger DAL
  - stockMT: Stock file DAL
  - nominalMT: GL ledger DAL
  - systemMT: System file DAL
  - 40+ other modules
- Business Purpose: Database access
- Lifecycle: Called per operation

**Migration Utilities**
- Business description: Data movement programs
- Categories:
  - *LD: Load from file to database
  - *UNL: Unload from database to file
  - *RES: Restore operations
- Business Purpose: Storage migration
- Lifecycle: Run during migrations

### Referenced Entities
- All business data files/tables
- System configuration
- Connection parameters

## Interface Contracts

### Inbound Interfaces

| Interface ID | Source | Data Type | Frequency | Business Purpose |
|-------------|--------|-----------|-----------|------------------|
| INT_DAL_READ_001 | All modules | Read request | Continuous | Data retrieval |
| INT_DAL_WRITE_001 | All modules | Write request | Continuous | Data storage |
| INT_DAL_START_001 | All modules | Position request | Per batch | Sequential access |
| INT_DAL_DELETE_001 | All modules | Delete request | As needed | Record removal |

### Standard DAL Call Interface
```cobol
CALL "handler" USING 
    System-Record
    Data-Record
    File-Access
    File-Defs
    DAL-Common-Data
```

**Parameters**:
- System-Record: System configuration
- Data-Record: Business data
- File-Access: Operation specification
- File-Defs: File/table definitions
- DAL-Common-Data: Status and control

### File-Access Structure
```cobol
01  File-Access.
    03  File-Function    PIC X.
        88  Fa-Open-Input     VALUE "1".
        88  Fa-Open-I-O       VALUE "2".
        88  Fa-Open-Output    VALUE "3".
        88  Fa-Close          VALUE "9".
        88  Fa-Read           VALUE "R".
        88  Fa-Write          VALUE "W".
        88  Fa-Rewrite        VALUE "U".
        88  Fa-Delete         VALUE "D".
        88  Fa-Start          VALUE "S".
    03  File-Key-No      PIC 9.
    03  Access-Type      PIC 9.
    03  Fs-Reply         PIC XX.
```

### Internal APIs/Services

**Open Service**
- Parameters: File-Mode (Input/I-O/Output)
- Returns: Success/Failure, File-Handle
- Purpose: Initialize file/table access
- Validation: File exists, permissions
- Error Handling: File not found, locked

**Read Service**
- Parameters: Key-Number, Key-Value
- Returns: Record-Data, Status
- Purpose: Retrieve specific record
- Validation: Valid key, record exists
- Error Handling: Not found, read error

**Write Service**
- Parameters: Record-Data
- Returns: Success/Failure
- Purpose: Create new record
- Validation: Unique key, valid data
- Error Handling: Duplicate, write error

**Update Service**
- Parameters: Record-Data
- Returns: Success/Failure
- Purpose: Modify existing record
- Validation: Record exists, valid changes
- Error Handling: Not found, lock conflict

## Business Rules Engine

### Access Rules
- **ACC-DAL-001**: Check storage mode before operation
- **ACC-DAL-002**: Validate operation permissions
- **ACC-DAL-003**: Enforce record locking
- **ACC-DAL-004**: Maintain operation sequence
- **ACC-DAL-005**: Preserve transaction boundaries

### Translation Rules
- **TRANS-DAL-001**: COBOL status to standard codes
- **TRANS-DAL-002**: SQL errors to file status
- **TRANS-DAL-003**: Data type conversions
- **TRANS-DAL-004**: Key format adaptations
- **TRANS-DAL-005**: Character set handling

### Performance Rules
- **PERF-DAL-001**: Connection pooling for DB
- **PERF-DAL-002**: Cursor management
- **PERF-DAL-003**: Batch operation optimization
- **PERF-DAL-004**: Index usage enforcement
- **PERF-DAL-005**: Lock duration minimization

## Operational Characteristics

### Processing Patterns
- **File Operations**:
  - Direct ISAM access
  - Record-level locking
  - Sequential processing
  - Key-based retrieval
- **Database Operations**:
  - SQL generation
  - Result set handling
  - Transaction management
  - Connection pooling
- **Dual Mode**:
  - Parallel writes
  - Primary reads from DB
  - Consistency checking

### Performance Metrics
- Operation Volume:
  - Reads: 10,000+/hour
  - Writes: 5,000+/hour
  - Updates: 3,000+/hour
- Response Times:
  - File read: < 10ms
  - DB read: < 20ms
  - Write: < 50ms
- Resource Usage:
  - Connections: 10-50
  - Memory: Minimal
  - CPU: Low

## Dependencies

### Upstream Dependencies
- All business modules (callers)
- System configuration (storage mode)
- File system (for files)
- Database system (for RDBMS)

### Downstream Dependencies
- Operating system (file I/O)
- Database engine (SQL processing)
- Storage systems (disk access)

### External Dependencies
- MySQL/MariaDB client libraries
- Network (for remote DB)
- File system permissions

## Quality Attributes

### Performance Requirements
- Latency:
  - Local file: < 10ms
  - Local DB: < 20ms
  - Remote DB: < 50ms
- Throughput:
  - 1000 operations/second
  - Scales with hardware
- Concurrency:
  - Multi-user support
  - Lock management

### Reliability Requirements
- Availability: 99.99% (critical path)
- Recovery: Automatic reconnection
- Integrity: ACID compliance
- Durability: Persistent storage

### Compatibility Requirements
- COBOL file formats
- MySQL/MariaDB protocols
- Character encodings
- Platform independence

## Evolution Potential

### Enhancement Opportunities
- NoSQL support: Document stores
- Cloud storage: S3, Azure Blob
- Caching layer: Redis/Memcached
- Async operations: Non-blocking I/O
- Sharding support: Horizontal scaling

### Modernization Candidates
- Microservice adapters: REST APIs
- GraphQL interface: Flexible queries
- Event streaming: Kafka integration
- Containerization: Docker support
- Observability: Metrics/tracing

### Known Limitations
- Two storage types only
- No distributed transactions
- Limited connection pooling
- Basic error handling
- No query optimization
- Synchronous only

## Risk Assessment

### Technical Risks
- Storage corruption
- Connection failures
- Lock timeouts
- Performance degradation

### Business Risks
- Data inconsistency
- Operation failures
- Migration errors
- Availability issues

### Mitigation Strategies
- Regular integrity checks
- Connection retry logic
- Lock timeout handling
- Performance monitoring
- Backup procedures

## Storage Mode Configuration

### File-Only Mode
```cobol
RDBMS-Name = SPACES
File-Duplicates = "N"
```
- Traditional COBOL files
- No database required
- Fastest performance
- Limited scalability

### Database-Only Mode
```cobol
RDBMS-Name = "MySQL"
File-Duplicates = "N"
```
- All data in database
- Better scalability
- Network capability
- Richer queries

### Dual Mode (Migration)
```cobol
RDBMS-Name = "MySQL"
File-Duplicates = "Y"
```
- Writes to both
- Reads from database
- Migration support
- Performance impact

## Error Handling

### Standard Error Codes
| Code | Meaning | Action |
|------|---------|--------|
| 00 | Success | Continue |
| 10 | End of file | Normal termination |
| 21 | Invalid key | Check key value |
| 22 | Duplicate key | Use update instead |
| 23 | Not found | Check existence |
| 99 | General error | Check specifics |

### Database-Specific Errors
- Connection failures (911)
- Lock timeouts (910)
- SQL errors (mapped to 99)
- Permission denied (99)

## Migration Procedures

### File to Database
1. Run verification (*UNL test)
2. Load data (*LD programs)
3. Verify counts
4. Switch to dual mode
5. Validate operations
6. Switch to DB-only

### Database to File
1. Unload data (*UNL programs)
2. Verify integrity
3. Switch modes
4. Validate operations

---

Document Version: 1.0
Subsystem Version: DAL v3.02
Analysis Date: December 2024