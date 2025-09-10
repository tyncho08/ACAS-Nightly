# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

ACAS (Applewood Computers Accounting System) is a comprehensive accounting and business management system written in COBOL, originally developed in 1976 and actively maintained. It supports both traditional COBOL indexed files (ISAM) and MySQL/MariaDB databases.

## Build Commands

### Full build with RDBMS support
```bash
./comp-all.sh
```

### Build without RDBMS support
```bash
./comp-all-no-rdbms.sh
```

### Individual subsystem builds
- Common modules: `cd common && ./comp-common.sh`
- General Ledger: `cd general && ./comp-gl.sh`
- IRS (Internal Revenue): `cd irs && ./comp-irs.sh`
- Purchase Ledger: `cd purchase && ./comp-purchase.sh`
- Sales Ledger: `cd sales && ./comp-sales.sh`
- Stock Control: `cd stock && ./comp-stock.sh`

### Installation
First-time: `./install-ACAS.sh`
Updates: `./install-ACAS-preinstalled.sh`

## Running the System

Main menu programs:
- `ACAS` - Main system menu
- `irs` - Internal Revenue System
- `sales` - Sales Ledger
- `purchase` - Purchase Ledger
- `stock` - Stock Control
- `general` - General Ledger

## Architecture

### Directory Structure
```
ACAS-Nightly/
├── common/          # Shared modules, DALs, and utilities
├── copybooks/       # COBOL copybooks (includes, templates)
├── irs/            # IRS modules
├── sales/          # Sales ledger modules
├── purchase/       # Purchase ledger modules
├── stock/          # Stock control modules
├── general/        # General ledger modules
└── mysql/          # Database schema (ACASDB.sql)
```

### Key Components

1. **Menu Programs** - Main entry points (ACAS, irs, sales, etc.)
2. **DAL Modules** - Data Access Layer (*MT.cbl files) abstracting file/database access
3. **FH Modules** - File Handlers for COBOL file operations
4. **Business Logic** - Core accounting programs (sl*, pl*, st*, ir*, gl*)
5. **Load/Unload Programs** - Transfer data between COBOL files and RDBMS

### Data Access Pattern
Programs use a unified interface that can switch between:
- COBOL indexed files (ISAM) - Default for testing
- MySQL/MariaDB tables - When RDBMS is configured

The system always maintains a COBOL parameter file that determines which data storage method is active.

### Compilation Flags
- Module flag (`-m`) for shared libraries (.so files)
- Executable flag (`-x`) for main programs
- RDBMS builds link with MySQL client libraries
- Non-RDBMS builds use dummy-rdbmsMT.cbl for stubs

## Development Notes

- COBOL sources use GnuCOBOL compiler (v3.2+ recommended)
- Terminal must be at least 80x24 characters
- Environment variable COB_SCREEN_ESC must be YES
- File access logging controlled by SW-Testing flag in Test-Data-Flags.cob
- System testing should start with COBOL files before migrating to RDBMS
- Load programs exist to migrate from COBOL files to database tables (not reverse)