# Secure Home using Blockchain: Decentralized IoT Management

## Project Summary

This project demonstrates a proof-of-concept for securing an Internet of Things (IoT) environment by integrating a custom-built blockchain and a smart contract. The blockchain is used as a tamper-proof ledger to immutably record critical IoT sensor data, ensuring data integrity. The smart contract provides decentralized governance, enforcing logical rules for device control based on the recorded sensor inputs.

## GRC & Security-by-Design Focus

This architecture showcases critical competencies in data governance, security, and process control:

* Data Integrity (Immutability): The use of a blockchain ledger guarantees that sensor readings, once recorded, cannot be retrospectively altered or deleted, which is essential for audit trails and forensic analysis.

* Decentralized Access Control: The Solidity smart contract enforces predefined logical controls over physical devices. This removes reliance on a single central server, making the system highly resilient and transparent.

* Chain of Custody: Every data entry is timestamped, hashed, and linked in the blockchain, providing a robust, cryptographically secured chain of custody for all device telemetry.

* Zero-Trust Principles: Control logic (like turning a fan ON/OFF based on PIR/UDS sensors) is codified and externally verifiable, aligning with zero-trust principles where rules are immutable.

## Technical Scope & Components 

The project utilizes a hybrid architecture combining Python for the ledger and Solidity for device logic:

* Data Layer: Custom-built Blockchain implementing basic Proof-of-Work (PoW) consensus.

* Control Layer: Solidity Smart Contract (device contract) defining physical device states and state transition logic.

* Integration: The Python blockchain records data with fields for deviceID, deviceType, location, and data (representing sensor readings).

* APIs: Flask REST API endpoints for mining blocks, adding data, validating the chain, and decentralized peer-to-peer syncing.
