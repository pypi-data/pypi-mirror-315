# download_pbi_xmla

**Version:** 0.4  
**Description:** A Python package to fetch and save Power BI tables via the XMLA endpoint using DAX queries. The package allows data to be saved in either Parquet or CSV format.  

## Table of Contents
1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Setup](#setup)
5. [Usage](#usage)
6. [Running the Scripts](#running-the-scripts)
7. [Troubleshooting](#troubleshooting)
8. [Contributing](#contributing)
9. [License](#license)

## Overview
The `download_pbi_xmla` package is designed to connect to a Power BI XMLA endpoint, execute DAX queries, and save the results in either Parquet or CSV formats. This tool is specifically for use in a Windows environment due to its dependency on `.NET` assemblies and the `pythonnet` library.

## System Requirements
- **Operating System:** Windows
- **Python Version:** 3.9 to 3.12
- **Required Software:** .NET Framework and Power BI Pro or Premium capacity access with XMLA endpoint enabled.
- **Authentication:** The package currently only supports authentication using the Microsoft Authentication Library (MSAL) to obtain an access token, supporting Multi-Factor Authentication (MFA).

### Python Version Compatibility

The `download_pbi_xmla` package requires Python version **3.9, 3.10, 3.11, or 3.12**. 

#### Important Note:

- The package is **not compatible** with Python 3.13 or any versions above it due to a dependency on `pythonnet`, which only supports Python versions up to 3.12.
- If you are using Python 3.13 or higher, please switch to a compatible Python version (3.9 to 3.12) to install and use this package.

#### Instructions for Checking and Changing Your Python Version

1. **Check Your Python Version:**
   
   Run the following command in your terminal or command prompt to check your current Python version:

   ```sh
   python --version
   ```
## Installation

### Prerequisites
1. **Install Python**  
   Ensure you have Python 3.9 to 3.12 installed. You can download it from [python.org](https://www.python.org/downloads/).

2. **Install .NET Framework**  
   Install the required .NET Framework runtime from [Microsoft's website](https://dotnet.microsoft.com/download).

3. **Install Poetry** (optional)  
   [Poetry](https://python-poetry.org/docs/#installation) is a dependency manager for Python that simplifies package installation and management. Follow the instructions on their website to install it.

### Steps to Install the Package

#### Option 1: Using Poetry

If you have Poetry installed, you can add the package to your environment by running:

```bash
poetry add download_pbi_xmla
```

#### Option 2: Using pip

Alternatively, you can install the package directly using pip:

```bash
pip install download_pbi_xmla
```

## Setup

1. **Run the Setup Script**  
   This script copies example configuration files and prompts you to edit them.

   - **Using Poetry:**
     ```bash
     poetry run setup-files
     ```

   - **Using pip:**
     ```bash
     python -m download_pbi_xmla.setup_files
     ```

2. **Edit the Configuration Files**  
   After running the setup script, two configuration files (`.env` and `config.json`) will be created in your project's root directory. You need to update these files with your credentials and specific configurations.

   - **.env File Example:**  
     Open the newly created `.env` file and provide your credentials and other necessary settings:
    ```plaintext
    CLIENT_ID=your-client-id
    CLIENT_SECRET=your-client-secret
    TENANT_ID=your-tenant-id
    CONFIG_FILE=config.json
    SAVE_PATH=./data
    ```
   - **config.json File Example:**  
     Modify the `config.json` file to specify the Power BI server, database, DAX queries, and output formats:
    ```json
    {
      "server": "your-server-url",
      "database": "your-database-name",
      "dax_queries": [
        {
          "query": "Add your DAX query here",
          "output_file": "Your filename here.parquet",
          "format": "parquet"
        },
        {
          "query": "Add your second DAX query here (or delete this section)",
          "output_file": "Your second filename here.csv",
          "format": "csv"
        }
      ]
    }
    ```

## Usage

To use the package, you can execute the provided scripts to fetch data from Power BI XMLA endpoints and save it in your desired format.

### Fetch and Save Data
You can run the main download script using either Poetry or pip:

- **Using Poetry:**
  ```bash
  poetry run run-download
  ```

- **Using pip:**
  ```bash
  python -m download_pbi_xmla.run_download
  ```

## Running the Scripts

### 1. Fetch Tables Script
This script downloads tables and saves them using the specified configurations:

- **Using Poetry:**
  ```bash
  poetry run fetch-tables
  ```

- **Using pip:**
  ```bash
  python -m download_pbi_xmla.fetch_tables
  ```

### 2. Setup Environment Script
To set up your environment by creating necessary configuration files:

- **Using Poetry:**
  ```bash
  poetry run setup-environment
  ```

- **Using pip:**
  ```bash
  python -m download_pbi_xmla.setup_environment
  ```

## Troubleshooting

### Common Issues

1. **.NET Assemblies Not Found**
   Ensure you have the correct version of the .NET runtime installed on your machine. The `pythonnet` library only works on Windows systems.

2. **Invalid Credentials**
   Double-check that your credentials in the `.env` file are correct and that your Azure AD app registration has the necessary permissions to access the Power BI XMLA endpoint.

3. **Data Save Errors**
   Ensure that the specified output paths and formats are correct. The script supports saving data as either Parquet or CSV files.

## Contributing

If you'd like to contribute to this project, please fork the repository and create a pull request with your changes. Ensure that all tests pass before submitting.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.