#!/bin/bash

# Exit if any command fails
set -e

PROJECT_DIR="/home/ubuntu/B2CBackend"
VENV_DIR="$PROJECT_DIR/b2cEnv"
MANAGE_PY="$PROJECT_DIR/manage.py"
ENV_FILE="$PROJECT_DIR/.env"

echo "🔄 Starting deployment..."

# Go to project directory
cd $PROJECT_DIR

# Load environment variables (if .env file exists)
if [ -f "$ENV_FILE" ]; then
  echo "🌍 Loading environment variables from .env..."
  export $(grep -v '^#' $ENV_FILE | xargs)
fi

# Pull latest code
echo "📥 Pulling latest code from Git..."
git fetch origin main
git reset --hard origin/main   # ensures exact match with remote

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source $VENV_DIR/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run mamke migrations
echo "🗄️ Running Django make migrations..."
python $MANAGE_PY makemigrations --noinput


# Run migrations
echo "🗄️ Running Django migrations..."
python $MANAGE_PY migrate --noinput

# Collect static files
echo "🎨 Collecting static files..."
python $MANAGE_PY collectstatic --noinput

# Restart services
echo "🔁 Restarting Gunicorn..."
sudo systemctl restart gunicorn

echo "🔄 Reloading Nginx..."
sudo systemctl reload nginx

echo "✅ Deployment complete!"


# #!/bin/bash

# # Exit if any command fails
# set -e

# PROJECT_DIR="/home/ubuntu/B2CBackend"
# VENV_DIR="$PROJECT_DIR/b2cEnv"
# MANAGE_PY="$PROJECT_DIR/manage.py"

# echo "🔄 Starting deployment..."

# # Go to project directory
# cd $PROJECT_DIR

# # Pull latest code
# echo "📥 Pulling latest code from Git..."
# git fetch origin main
# git reset --hard origin/main   # ensures exact match with remote

# # Activate virtual environment
# echo "🐍 Activating virtual environment..."
# source $VENV_DIR/bin/activate

# # Install dependencies
# echo "📦 Installing dependencies..."
# pip install --upgrade pip
# pip install -r requirements.txt

# # Run migrations
# echo "🗄️ Running Django migrations..."
# python $MANAGE_PY migrate --noinput

# # Collect static files
# echo "🎨 Collecting static files..."
# python $MANAGE_PY collectstatic --noinput

# # Restart services
# echo "🔁 Restarting Gunicorn..."
# sudo systemctl restart gunicorn

# echo "🔄 Reloading Nginx..."
# sudo systemctl reload nginx

# echo "✅ Deployment complete!"
