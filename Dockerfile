ARG PYTHON_VERSION=3.12-slim-bullseye
FROM python:${PYTHON_VERSION}

# Create a venv
RUN python3 -m venv --copies /opt/.venv

# Set the Virtual Environment as current location
ENV PATH=/opt/.venv/bin:$PATH

# Upgrade pip and install poetry
RUN pip install --upgrade pip && pip install uv

# Set Python-related environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Ensure wget is available in the container (if using it)
RUN apt-get update && apt-get install -y wget


# Create the mini vm's code directory
RUN mkdir -p /code

# Set the working directory to that same code directory
WORKDIR /code

# Copy the poetry files to install depedencies and cache
COPY uv.lock pyproject.toml /code/

# Export the dependencies to requirements.txt
RUN uv lock --check && uv export --no-dev --format requirements-txt --no-hashes -o proj_requirements.txt
RUN pip install --no-cache-dir -r proj_requirements.txt

# copy the project code into the container's working directory
COPY ./django-proj /code

# Clean up apt cache to reduce image size
RUN apt-get remove --purge -y \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Run the Django project via the runtime script
# when the container starts
COPY ./entrypoint.sh /
COPY generate_env.py /
# make the bash script executable
RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh", "/entrypoint.sh"]