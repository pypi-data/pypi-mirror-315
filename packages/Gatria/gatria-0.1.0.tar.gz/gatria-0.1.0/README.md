# Gatria - Employee Management System

**Gatria** is a comprehensive employee management system designed to streamline workforce management through a versatile and extensible platform. It offers multiple framework adapters, database integrations, and advanced features such as asynchronous operations and machine learning analytics.

---

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Basic Usage](#basic-usage)
- [Installation Options](#installation-options)
- [Documentation](#documentation)
- [Examples](#examples)
  - [Web Framework Integration](#web-framework-integration)
  - [Database Operations](#database-operations)
  - [Asynchronous Operations](#asynchronous-operations)
  - [Machine Learning Analytics](#machine-learning-analytics)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Features

- 🚀 **Multi-framework support**: Seamlessly integrate with Flask, Django, and FastAPI.
- 📊 **Database flexibility**: Support for SQLAlchemy, MongoDB, and Redis databases.
- ⚡ **Asynchronous capabilities**: Enable high-performance operations with async support.
- 🤖 **Machine Learning-powered analytics**: Leverage ML algorithms for workforce insights.
- 🛠 **Extensible architecture**: Easily extend and customize the system to fit specific needs.

## Getting Started

### Prerequisites

- **Python**: Version 3.8 or higher
- **pip**: Package installer for Python
- **Virtual Environment**: Recommended for dependency management

### Installation

Install Gatria using `pip`:

```bash
pip install Gatria
```

### Basic Usage

Create a simple employee management script:

```python
from Gatria import EmployeeManager

# Initialize the EmployeeManager with default settings
manager = EmployeeManager()

# Create a new employee
employee_data = {
    "name": "John Doe",
    "position": "Software Engineer",
    "department": "Engineering",
    "email": "john.doe@example.com",
    "phone": "+1-555-0100",
    "date_hired": "2022-01-15"
}

employee = manager.create_employee(employee_data)

# Retrieve employee information
retrieved_employee = manager.get_employee(employee.id)
print(retrieved_employee.to_dict())

# Update employee data
updated_data = {"position": "Senior Software Engineer"}
manager.update_employee(employee.id, updated_data)

# Delete an employee
manager.delete_employee(employee.id)
```

---

## Installation Options

Select the features you require by installing specific option packages:

```bash
# Full installation with all features
pip install Gatria[all]
```

### Optional Feature Installations

#### Web Framework Support

```bash
pip install Gatria[web]
```

Includes:

- **Flask**: For building lightweight web applications.
- **Django**: A high-level Python web framework.
- **FastAPI**: For building APIs with high performance.

#### Database Integrations

```bash
pip install Gatria[database]
```

Includes:

- **SQLAlchemy**: SQL toolkit and ORM.
- **PyMongo**: Official MongoDB driver for Python.
- **Redis**: Python client for Redis key-value store.

#### Asynchronous Support

```bash
pip install Gatria[async]
```

Includes:

- **aiohttp**: Asynchronous HTTP client/server framework.
- **asyncio**: Library to write concurrent code.
- **websockets**: For building WebSocket servers and clients.

#### Machine Learning Features

```bash
pip install Gatria[ml]
```

Includes:

- **Scikit-learn**: Machine learning library.
- **TensorFlow**: End-to-end open-source platform for ML.
- **PyTorch**: Deep learning platform.
- **NumPy**: Fundamental package for numerical computations.
- **Pandas**: Data analysis and manipulation tool.

---

## Documentation

For detailed documentation, refer to:

- [Installation Guide](./docs/installation.md): Step-by-step instructions to install Gatria.
- [Configuration Guide](./docs/configuration.md): Instructions for configuring Gatria.
- [API Reference](./docs/api.md): Comprehensive details of all classes and methods.
- [Examples and Tutorials](./docs/examples.md): Practical examples to get you started.
- [Contributing Guide](./docs/contributing.md): Guidelines for contributing to the project.

---

## Examples

### Web Framework Integration

#### Flask Example

```python
from flask import Flask
from Gatria.adapters.flask import FlaskAdapter

app = Flask(__name__)
FlaskAdapter.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
```

#### Django Example

```python
# In your urls.py
from django.urls import path, include
from Gatria.adapters.django import DjangoAdapter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('employees/', include(DjangoAdapter.get_urls())),
]
```

### Database Operations

#### Using SQLAlchemy

```python
from Gatria.database.sqlalchemy import SQLAlchemyDatabase
from Gatria import EmployeeManager

db = SQLAlchemyDatabase('sqlite:///employees.db')
manager = EmployeeManager(database=db)

# Perform database operations
```

#### Using MongoDB

```python
from Gatria.database.mongodb import MongoDBDatabase
from Gatria import EmployeeManager

db = MongoDBDatabase('mongodb://localhost:27017/', 'Gatria_db')
manager = EmployeeManager(database=db)

# Perform database operations
```

### Asynchronous Operations

```python
import asyncio
from Gatria import EmployeeManager

async def main():
    manager = EmployeeManager(async_mode=True)
    employee = await manager.create_employee_async({
        "name": "Jane Smith",
        "position": "Data Scientist",
        "department": "Analytics",
    })
    print(await manager.get_employee_async(employee.id))

asyncio.run(main())
```

### Machine Learning Analytics

```python
from Gatria.ml.analytics import EmployeeAnalytics

analytics = EmployeeAnalytics()
report = analytics.generate_performance_report(department='Engineering')
print(report)
```

---

## Configuration

Gatria can be configured using a configuration file or environment variables. Refer to the [Configuration Guide](./docs/configuration.md) for detailed instructions on customizing settings such as database connections, logging levels, and third-party integrations.

---

## Contributing

We welcome contributions from the community. Please read the [Contributing Guide](./docs/contributing.md) to learn about our development process, coding standards, and how to propose improvements.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for full details.

---

## Contact

For questions or support, please contact the project maintainer:

- **Author**: Pradyumn Tandon
- **Email**: pradyumn.tandon@hotmail.com
- **GitHub**: [Canopus-Development/Gatria](https://github.com/Canopus-Development/Gatria)