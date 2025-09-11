# Subsystem: COMMON_UTIL - Common Utilities

## Executive Summary
- **Purpose**: Provides shared utility functions used across all ACAS subsystems including date handling, validation routines, check digit algorithms, and system functions
- **Business Value**: Ensures consistency in common operations, reduces code duplication, provides tested and reliable utility functions
- **Key Users**: All ACAS modules (indirect), developers maintaining the system
- **Criticality**: HIGH - Core functions required by all modules

## Functional Capabilities

### Core Functions

1. **Date and Time Management (maps04)**
   - Description: Comprehensive date validation and conversion
   - Business Rules:
     - Multiple date format support (UK/US/ISO)
     - Leap year validation
     - Working day calculations
     - Period date validation
     - Date arithmetic functions
   - Triggers: Any date field processing
   - Outcomes: Validated, formatted dates

2. **Check Digit Algorithms (maps09)**
   - Description: Generate and validate check digits
   - Business Rules:
     - Modulus 11 algorithm
     - Customer/supplier codes
     - Self-checking codes
     - Error detection
     - Standard compliance
   - Triggers: Master record creation/validation
   - Outcomes: Valid check-digit codes

3. **Encryption/Decryption (maps01)**
   - Description: Basic data encryption services
   - Business Rules:
     - Password encryption
     - Sensitive data masking
     - Reversible encryption
     - Key management
     - Compliance support
   - Triggers: Security requirements
   - Outcomes: Protected data

4. **File Access Logging (fhlogger)**
   - Description: Track all file operations for debugging
   - Business Rules:
     - Operation logging
     - Performance metrics
     - Error tracking
     - Configurable levels
     - Rotation policies
   - Triggers: Testing flag enabled
   - Outcomes: Detailed operation log

5. **Error Handling Utilities**
   - Description: Standardized error management
   - Business Rules:
     - Error code mapping
     - Message formatting
     - Stack traces (cobdump)
     - Recovery suggestions
     - Logging integration
   - Triggers: Error conditions
   - Outcomes: Consistent error handling

### Business Processes Supported
- Date validation across all modules
- Customer/supplier code generation
- Security and compliance
- System debugging and testing
- Error diagnosis and recovery
- Email communications
- Data conversion operations

## Data Domain

### Owned Entities

**Utility Work Areas**
- Business description: Temporary data for calculations
- Key Attributes:
  - Date conversion fields
  - Check digit work areas
  - Encryption buffers
  - Error message areas
- Business Identifiers: N/A (transient)
- Lifecycle: Per operation

**Log Files**
- Business description: Operation tracking files
- Key Attributes:
  - Timestamp
  - Operation type
  - Module/program
  - User ID
  - Results
  - Performance data
- Business Identifiers: Timestamp + sequence
- Lifecycle: Created continuously, rotated

### Referenced Entities
- System parameters (date formats)
- Error message catalog
- Security configuration

## Interface Contracts

### Standard Utility Interfaces

**Date Conversion Service (maps04)**
```cobol
CALL "maps04" USING
    Date-Function
    Input-Date
    Output-Date
    Date-Format
    Return-Status
```

**Check Digit Service (maps09)**
```cobol
CALL "maps09" USING
    Check-Function
    Input-Code
    Check-Digit
    Return-Status
```

**Encryption Service (maps01)**
```cobol
CALL "maps01" USING
    Crypt-Function
    Input-Data
    Output-Data
    Key-Data
    Return-Status
```

### Function Codes

**Date Functions**:
- 1: Validate date
- 2: Convert format
- 3: Calculate days between
- 4: Add/subtract days
- 5: Get day of week
- 6: Working days calculation

**Check Digit Functions**:
- 1: Generate check digit
- 2: Validate with check digit
- 3: Strip check digit
- 4: Repair if possible

### Internal APIs/Services

**Date Validation Service**
- Parameters: Date-String, Format-Type
- Returns: Valid/Invalid, Formatted-Date
- Purpose: Ensure valid calendar dates
- Validation: Format, range, leap years
- Error Handling: Invalid format, impossible date

**Working Days Service**
- Parameters: Start-Date, End-Date, Calendar
- Returns: Working-Days-Count
- Purpose: Business day calculations
- Validation: Date order, calendar exists
- Error Handling: Invalid dates, no calendar

**Error Formatting Service**
- Parameters: Error-Code, Context-Data
- Returns: Formatted-Message, Severity
- Purpose: Consistent error messages
- Validation: Valid error code
- Error Handling: Unknown error code

## Business Rules Engine

### Date Rules
- **DATE-001**: Accept DD/MM/YY or DD/MM/YYYY
- **DATE-002**: Handle US format MM/DD/YYYY
- **DATE-003**: Support ISO format YYYY-MM-DD
- **DATE-004**: Validate leap years correctly
- **DATE-005**: Reject impossible dates

### Check Digit Rules
- **CHECK-001**: Use modulus 11 algorithm
- **CHECK-002**: Customer codes: 6 digits + 1 check
- **CHECK-003**: Supplier codes: 6 digits + 1 check
- **CHECK-004**: X represents check digit 10
- **CHECK-005**: Reject invalid check digits

### Logging Rules
- **LOG-001**: Log when testing flag set
- **LOG-002**: Include timestamp, program, user
- **LOG-003**: Rotate logs at size limit
- **LOG-004**: Mask sensitive data
- **LOG-005**: Performance metrics optional

## Operational Characteristics

### Processing Patterns
- **Real-time Utilities**:
  - Called synchronously
  - Immediate response
  - No state maintained
  - Thread-safe operations
- **Logging Operations**:
  - Asynchronous possible
  - Buffered writes
  - Rotation handling

### Performance Metrics
- Operation Volume:
  - Date validations: 1000s/hour
  - Check digits: 100s/hour
  - Logging: Continuous
- Response Times:
  - Date functions: < 1ms
  - Check digit: < 1ms
  - Encryption: < 10ms
- Resource Usage:
  - CPU: Minimal
  - Memory: Small buffers
  - I/O: Logging only

## Dependencies

### Upstream Dependencies
- All ACAS modules (callers)
- System configuration (formats)

### Downstream Dependencies
- Operating system (date/time)
- File system (logging)

### External Dependencies
- System clock accuracy
- Locale settings
- File permissions

## Quality Attributes

### Performance Requirements
- Response Time:
  - Utility calls: < 5ms
  - No blocking operations
  - Efficient algorithms
- Availability:
  - Always available
  - No external dependencies
  - Failsafe operation

### Reliability Requirements
- Accuracy: 100% for algorithms
- Consistency: Same results always
- Error Handling: Never crash caller

### Compatibility Requirements
- COBOL standards compliance
- Platform independence
- Character set handling
- Date windowing (Y2K)

## Evolution Potential

### Enhancement Opportunities
- Extended date formats: More international
- Stronger encryption: Modern algorithms
- Enhanced logging: Structured logs
- Performance monitoring: Built-in metrics
- Utility library: More functions

### Modernization Candidates
- Web service utilities: REST calls
- JSON handling: Data exchange
- UUID generation: Unique IDs
- Hash functions: Data integrity
- Async operations: Non-blocking

### Known Limitations
- Basic encryption only
- Limited date formats
- No timezone handling
- English messages only
- Synchronous only
- No external integration

## Risk Assessment

### Technical Risks
- Algorithm errors affect all
- Performance degradation
- Logging disk full
- Date overflow (2038)

### Business Risks
- Check digit failure
- Date miscalculation
- Encryption weakness
- Logging gaps

### Mitigation Strategies
- Comprehensive testing
- Algorithm validation
- Log rotation
- Regular updates
- Performance monitoring

## Utility Catalog

### Date Utilities (maps04)
| Function | Description | Usage |
|----------|-------------|-------|
| Validate | Check date validity | All date inputs |
| Convert | Change date format | Display/storage |
| Difference | Days between dates | Aging, terms |
| Add/Subtract | Date arithmetic | Due dates |
| Day of Week | Get weekday | Scheduling |
| Working Days | Business days | Payment terms |

### Check Digit Utilities (maps09)
| Function | Description | Usage |
|----------|-------------|-------|
| Generate | Create check digit | New codes |
| Validate | Verify check digit | Code entry |
| Strip | Remove check digit | Internal use |
| Repair | Fix if possible | Error recovery |

### System Utilities
| Utility | Description | Usage |
|---------|-------------|-------|
| cobdump | COBOL dump handler | Error diagnosis |
| fhlogger | File operation logger | Testing/debug |
| send-some-mail | Email sender | Notifications |

## Error Messages

### Standard Error Returns
| Code | Meaning | Action |
|------|---------|--------|
| 0 | Success | Continue |
| 1 | Invalid input | Check data |
| 2 | Format error | Check format |
| 3 | Range error | Check limits |
| 4 | System error | Check system |

### Date-Specific Errors
- Invalid day (1-31)
- Invalid month (1-12)
- Invalid year (range)
- Invalid format
- Impossible date (Feb 30)

### Check Digit Errors
- Invalid length
- Non-numeric data
- Check digit mismatch
- Algorithm failure

## Best Practices

### When to Use Utilities
1. **Always Use For**:
   - Date validation
   - Check digit operations
   - Error formatting
   - Standardized operations

2. **Consider For**:
   - Performance logging
   - Data encryption
   - Complex calculations

3. **Don't Use For**:
   - Business logic
   - Data storage
   - External integration

### Integration Guidelines
- Include proper error handling
- Check return codes
- Pass correct parameters
- Don't assume success
- Log errors appropriately

---

Document Version: 1.0
Subsystem Version: UTIL v3.02
Analysis Date: December 2024