# HI HENRY

![Splash Image](splash.jpg)

## Introduction

## Install

## Usage

The application provides a command line interface and supports the following four commands:

| Command  | Description                                                         |
|----------|---------------------------------------------------------------------|
| create   | creates a new configuration which can be used used to generate code |
| delete   | deletes a previously created configuration                          |
| generate | generates code based on a configuration                             |
| clear    | deletes previously generated code                                   |

### create

This command defines a new configuration that can be used to connect to a database and extract its schema.  The 
command accepts the following parametrs:

| Parameter | Description                                               | Required | Default   |
|-----------|-----------------------------------------------------------|----------|-----------|
| database  | The name of the database to use in generating code        | Yes      |           |
| user      | The name of the database to use in generating code        | Yes      |           | 
| passport  | The user password to use to connect to the database       | Yes      |           |
| driver    | The database management system (DBMS) hostig the database | No       | mysql     |
| host      | The host where which the DBMS is running                  | No       | 127.0.0.1 | 
| port      | The port on which the DMBS is listening                   | No       | 3306      |

The driver parameter currently only supports one option - mysql, others may be added later.

### delete

This command deletes a configuration, previously created with the creaet command.  The command requires the following 
parameter:

| Parameter | Description                                               | Required | Default   |
|-----------|-----------------------------------------------------------|----------|-----------|
| database  | The name of the database to use in generating code        | Yes      |           |

### generate

This command generaets the code. The command supports the following parameter:

| Parameter | Description                                          | Required | Default |
|-----------|------------------------------------------------------|----------|---------|
| database  | The name of the database to use in generating code   | Yes      |         |
| folder    | If provided, code will be generated in this folder   | No       |         |

### clear

This command deletes the contents of the folder where the generated code was stored.  Optionally the default folder can 
be overwritten.

| Parameter | Description                                          | Required | Default |
|-----------|------------------------------------------------------|----------|---------|
| folder    | If provided, code will be generated in this folder   | No       |         |

## Design

### Configuration

### Schema Moodel

### Data Types

### Code Generation
