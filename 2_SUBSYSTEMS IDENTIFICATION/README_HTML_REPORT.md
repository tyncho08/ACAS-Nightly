# ACAS Subsystems HTML Report Generator

## Overview

This directory contains a comprehensive subsystem architecture analysis of the ACAS (Applewood Computers Accounting System) and includes a Python script that generates a unified HTML report from all documentation.

## Generated Report Features

The HTML report (`ACAS_Subsystems_Report.html`) includes:

### 📑 Complete Documentation Set
- **9 Architecture Documents**: Master architecture, inventory, integration patterns, data ownership, etc.
- **12 Subsystem Specifications**: Detailed specifications for each identified subsystem
- **3 Architecture Diagrams**: System context, interactions, and data flows

### 🎨 Visual Features
- **Mermaid Diagrams**: Automatically rendered with interactive features
- **ASCII Art**: Displayed with retro terminal styling
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Navigation**: Fixed sidebar with organized table of contents
- **Smooth Scrolling**: Easy navigation between sections
- **Print-Friendly**: Optimized CSS for printing documentation

## How to Generate the Report

### Prerequisites
```bash
# Python 3.x required
# Install required package:
pip3 install markdown2
```

### Generate Report
```bash
# Make script executable (first time only)
chmod +x create_subsystems_report.py

# Run the script
python3 create_subsystems_report.py
```

### Output
The script generates: `ACAS_Subsystems_Report.html` (~423 KB)

### Updates
- **Fixed Header Issue**: The header is now part of the scrollable content instead of being fixed
- **Improved Navigation**: Dark sidebar with smooth transitions matching the functional documentation style
- **Better Responsive Design**: Optimized for various screen sizes

## Report Contents

### Architecture Documents
1. **Master Subsystem Architecture** - Overview of 12 identified subsystems
2. **Subsystem Inventory** - Mapping of 200+ programs to subsystems
3. **Integration Architecture** - Interface patterns and communication flows
4. **Data Ownership Map** - Clear data boundaries between subsystems
5. **Process Allocation** - Business process to subsystem mapping
6. **Dependency Analysis** - Subsystem coupling and dependencies
7. **Communication Matrix** - Detailed interaction patterns and events
8. **Governance Model** - Change management and impact analysis
9. **Validation Report** - Quality assessment of documentation

### Subsystem Specifications
Each of the 12 subsystems has a complete specification including:
- Executive Summary
- Functional Capabilities
- Data Domain (owned and referenced entities)
- Interface Contracts
- Business Rules
- Quality Attributes
- Evolution Potential
- Risk Assessment

### The 12 Subsystems:
1. **GL_CORE** - General Ledger Core
2. **IRS_CORE** - IRS Ledger Core
3. **SL_MGMT** - Sales Ledger Management
4. **PL_MGMT** - Purchase Ledger Management
5. **ST_CTRL** - Stock Control System
6. **BATCH_FW** - Batch Processing Framework
7. **RPT_ENGINE** - Report Generation Engine
8. **SYS_ADMIN** - System Administration
9. **PERIOD_PROC** - Period Processing
10. **DAL** - Data Access Layer
11. **COMMON_UTIL** - Common Utilities
12. **INTEG_SVC** - Integration Services

## Viewing the Report

1. Open `ACAS_Subsystems_Report.html` in any modern web browser
2. Use the table of contents on the left to navigate
3. Click any section to jump directly to it
4. Mermaid diagrams will render automatically
5. Print using browser's print function (CSS optimized)

## Report Structure

```
ACAS_Subsystems_Report.html
├── Header (Title and generation date)
├── Table of Contents (Fixed sidebar)
│   ├── Architecture Documents
│   ├── Subsystem Specifications
│   └── Architecture Diagrams
├── Main Content Area
│   ├── All documentation sections
│   ├── Rendered diagrams
│   └── Formatted tables and code
└── Footer (Version info)
```

## Technical Notes

- **Mermaid.js**: Used for rendering architecture diagrams
- **Responsive CSS**: Adapts to different screen sizes
- **No external dependencies**: All assets are CDN-hosted
- **Cross-browser compatible**: Works in Chrome, Firefox, Safari, Edge

## Customization

To modify the report generation:
1. Edit `create_subsystems_report.py`
2. Adjust styling in the embedded CSS
3. Modify file ordering in `get_file_order()` method
4. Update Mermaid theme in the JavaScript section

---

Generated with ❤️ for the ACAS Subsystem Architecture Documentation Project