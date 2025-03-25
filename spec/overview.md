# Open Restaurant Feed Specification (ORFS) Overview

## Introduction

The Open Restaurant Feed Specification (ORFS) is a standardized data format that allows restaurants to publish information about their establishments, menus, dishes, tables, and ingredients in both static and real-time formats. ORFS is designed to be a comprehensive, flexible, and interoperable standard that can be used across various restaurant management systems, third-party applications, and aggregator platforms.

## Purpose

ORFS addresses the fragmentation in restaurant data interchange by providing:

1. **Standardized Data Model**: A consistent way to represent restaurant information
2. **Real-time Updates**: Mechanisms for broadcasting changes to menu availability, table status, etc.
3. **Interoperability**: Allow systems from different vendors to communicate seamlessly
4. **Data Quality**: Validation tools to ensure data integrity and compliance

## Core Concepts

ORFS is built around the following core entities:

- **Restaurant**: The establishment providing food services
- **Menu**: A collection of dishes available at specific times
- **Dish**: Food/beverage items with pricing, ingredients, and customization options
- **Table**: Physical seating arrangements with capacity and availability status
- **Ingredient**: Components of dishes with allergen information

## Feed Types

ORFS supports two types of feeds:

1. **Static Feed** (JSON): Complete snapshot of restaurant data that changes infrequently
2. **Real-time Feed** (Protocol Buffers): Updates about dynamic aspects like table availability and dish stock levels

## Implementation

Implementation of ORFS involves:

1. Generating ORFS-compliant feeds from your restaurant management system
2. Publishing these feeds through APIs or file exports
3. Validating feeds using the official tools
4. Consuming feeds in applications through standard libraries

## Benefits

- **For Restaurants**: Increased visibility across platforms with reduced integration effort
- **For Developers**: Consistent data structure across different restaurant sources
- **For Consumers**: More accurate and up-to-date information about restaurants

## Getting Started

Refer to the [technical reference](technical_reference.md) for detailed specifications and the [implementation guide](implementation_guide.md) for practical steps to implement ORFS in your systems.
