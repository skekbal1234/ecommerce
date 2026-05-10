# Leather Ecommerce Website

This repository contains a sample ecommerce application for leather goods like bags, belts, and accessories.

## Project Structure

- `backend/` - Flask API server serving product data, checkout simulation, and static HTML/CSS/JS files
- `requirements.txt` - Python dependencies

## Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the environment:
   - Windows PowerShell:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the Flask app:
   ```bash
   python backend/app.py
   ```

The app will run on `http://localhost:5000` and serve the HTML interface.

## Features

- Product listing for leather bags, belts, and accessories
- Add to cart, quantity adjustment, and remove item support
- Checkout flow with order total calculation

## Notes

Images are loaded from placeholder URLs in the sample data. Replace them with your own product visuals to match your leather brand.

## CI/CD Deployment

This repo includes GitHub Actions for CI/CD in `.github/workflows/deploy.yml`.

Secrets required for deploy:
- `EC2_HOST` – EC2 public IP or hostname
- `EC2_USER` – SSH username (`ec2-user`, `ubuntu`, etc.)
- `EC2_SSH_KEY` – private SSH key for the EC2 host
- `EC2_SSH_PORT` – SSH port (usually `22`)
- `EC2_APP_PATH` – deployment directory on EC2 (for example `/home/ubuntu/leather-ecommerce`)

The workflow will:
1. Run Python dependency install and syntax check
2. Build the Docker image
3. Copy repository files to EC2
4. Build and restart the Docker container on EC2

## Deploying with Your Own Domain

The project now supports an HTTP front-facing server via Nginx on EC2. This means you can point your domain name at your EC2 instance and serve the app over port 80.

### Steps to use your domain

1. Set your domain's DNS A record to your EC2 public IP.
2. Ensure the EC2 security group allows inbound traffic on port `80`.
3. Run deployment on EC2:

```bash
cd /path/to/your/app
chmod +x deploy_ec2.sh
./deploy_ec2.sh
```

The script will:
- install Nginx if needed
- create an Nginx reverse proxy config for your domain
- restart Nginx
- run the Docker container on port `5000`
- serve the app on port `80`

### GitHub Actions

The GitHub workflow will copy the repository to EC2 and then run `deploy_ec2.sh` remotely. To use your domain, you can set the `DOMAIN` environment variable on the EC2 host or in the SSH command.

If you want, I can also update the workflow to pass the domain as a secret and deploy it automatically with the correct domain name.