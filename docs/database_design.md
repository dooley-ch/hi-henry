# Database Design

## Introduction

This application comes with a set of templates that can be used to generate Python code for accessing an MySQL 
database.  There are many database design patters that can be implemented using the features provided by this 
application.  This document outlines the pattern underlying the set of templates provided as a default with this 
application.

## Enum

```mermaid
    classDiagram
   
        class action {
            <<Enum>>
            +Insert
            +Update
            +Delete
        }

```
## Versioning

```mermaid
    erDiagram
        version {
            int ID
            int major
            int minor
            int build
            varchar comment
            enum status
            timestamp created_at
        }
        
        version_step {
            int ID
            varchar step
            varchar comment
            int version_id
            timestamp created_at
        }
        
        version ||--o{ version_step : has
```

## Data Table

```mermaid
    erDiagram
        data_table {
            int ID
            int lock_version
            timestamp created_at
            timestamp updated_at
        }
        
        xxx_data_table {
            int ID
            timestamp logged_at
            enum action
            int record_id
            int record_lock_version
        }
        
        data_table ||--o{ xxx_data_table : has
```

## Summary
