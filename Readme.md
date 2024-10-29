# Topology Manager

Modular Multi-Agent LLM Orchestration and Retrieval-Augmented Generation (RAG) System

## Description
This project is a Python-based system designed to orchestrate multiple Large Language Models (LLMs) in a configurable, directed acyclic graph (DAG) topology, supporting both on-device and API-based LLMs. By leveraging OpenRouter API and local execution tools such as LMStudio, the system provides an abstraction layer to manage and execute tasks across various LLMs.

In addition, the system implements agentic RAG using LanceDB, enabling efficient retrieval of relevant information from web-scraped data to enhance response generation. The project’s configuration module offers flexibility by reading from an infrastructure file that specifies LLM configurations and validates their DAG structure, ensuring a robust setup before deployment.

## System Design
The system architecture, as depicted in the diagram, is organized into two primary flows:

### 1. Configuration and Initialization Flow
- The **Configuration File** specifies LLM interactions, node types, and dependencies, which the **Topology Manager** reads and validates.
- The Topology Manager then instantiates each LLM based on the provided **LLM Instruction Template** and arranges them according to the defined graph structure.

### 2. Execution Flow
- When a user query is received, it is directed to the **Instruction Executor**, which uses memory snapshots from the **Memory** module to ensure context continuity.
- The Instruction Executor sends the query to each LLM along with specific memory information and receives processed responses based on the RAG-enhanced LLM outputs.

## Implementation Details

### Modules
- **config**: Responsible for reading the infrastructure file that outlines LLM specifications and interactions. It includes validation logic to ensure that LLM configurations adhere to a proper graph structure, confirming the DAG formation.
- **core**: Contains the fundamental logic for LLM interaction and memory management, allowing for the storage and retrieval of context to improve response coherence.
- **db**: Manages data scraping and retrieval tasks. Using LanceDB, this module performs RAG by indexing web-scraped data, which LLMs can access as part of the response generation process.
- **manager**: Serves as the core orchestrator, integrating `config`, `models`, and `db` modules. It checks for acyclicity in the LLM arrangement and verifies the configuration before initializing LLM instances.
- **models**: Provides an abstraction layer over API-based and on-device LLMs. This module interacts with the OpenRouter API and LMStudio to handle both cloud-based and local LLM execution, supporting versatile deployment environments.

### LLM Abstraction and Execution
The `models` module encapsulates LLM functionality by offering a unified interface for both API-based and on-device LLMs. This enables the system to switch seamlessly between different types of LLMs based on the configuration file.

### Memory Management
The system uses a memory snapshot mechanism to retain context for ongoing conversations. This ensures that the **Instruction Executor** can provide coherent and contextually relevant responses, enhancing user experience.

### Graph Validation
Before any execution, the configuration is validated to confirm that the LLM arrangement forms a valid, acyclic DAG. This prevents circular dependencies and ensures reliable orchestration of tasks across the LLM hierarchy.

## Conclusion
This project provides a flexible, extensible framework for orchestrating LLMs in complex topologies, supporting agentic RAG for enhanced retrieval-based response generation. With its modular design, this system can be adapted for various LLM architectures, making it a powerful tool for multi-agent LLM deployments.

## LLM
