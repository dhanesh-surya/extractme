#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "==> Starting build process..."

# Install dependencies
echo "==> Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Run migrations
echo "==> Running database migrations..."
python manage.py migrate

# Collect static files
echo "==> Collecting static files..."
python manage.py collectstatic --no-input

echo "==> Build completed successfully!"
