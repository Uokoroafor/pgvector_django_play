import os

# Define defaults
default_values = """
OPENAI_API_KEY=""
DB_NAME="vector_db"
DB_USER="postgres"
DB_PASSWORD="password"
DB_HOST="localhost"
DB_PORT=5432
"""

# Check if .env file exists
env_file_path = ".env"

if not os.path.exists(env_file_path):
    print(f"{env_file_path} does not exist. Creating with default values...")
    with open(env_file_path, "w") as env_file:
        env_file.write(default_values)
else:
    print(f"{env_file_path} already exists. Skipping creation.")
