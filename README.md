# SwapLocal (API)

SwapLocal is a local item exchange platform where users can trade items with others nearby.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)

## Installation

To get started with this project, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv env
    ```

3. **Activate the virtual environment:**

    - On Windows:

        ```bash
        .\env\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source env/bin/activate
        ```

4. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. **Set up environment variables:**

    Copy the example environment file and update it with your configuration:

    ```bash
    cp .env.example .env
    ```

    Update `.env` with your database settings, secret key, and any other necessary configuration.

2. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

3. **Create a superuser (optional but recommended for admin access):**

    ```bash
    python manage.py createsuperuser
    ```

## Running the Application

Start the development server using:

```bash
python manage.py runserver
