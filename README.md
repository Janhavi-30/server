This script implements a prime number generator and exposes it through both a command-line interface and a REST API.

Features:
- Prime number generation with two strategies: naive and sieve.
- Command-line interface for generating primes with specified start, end, and strategy.
- REST API endpoints for generating primes within a range and retrieving execution history.
- Execution logging to an in-memory SQLite database.

Sections:
1. Imports: Import necessary libraries for the script.
2. Prime number generator functions: Contains functions for generating prime numbers using two different strategies.
3. Database setup: Creates an in-memory SQLite database for logging executions.
4. API endpoints: Defines routes for the REST API, including prime number generation and execution history retrieval.
5. Unit tests: Contains unit tests for the prime number generator functions.
6. Main block: Handles script execution based on command-line arguments, running the server or generating primes based on input.

Usage:
- To run the script as a server: python script.py server
- To generate primes from the command line: python script.py <start> <end> <strategy>
- Available strategies: naive, sieve
