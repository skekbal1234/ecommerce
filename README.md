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


## Deploying with Your Own Domain

The project supports an HTTP front-facing server via Nginx on EC2. Point your domain name at your EC2 instance and the app will be served on port 80.

### Steps to use your domain

1. Set your domain's DNS A record to your EC2 public IP.
2. Ensure the EC2 security group allows inbound traffic on port `80`.
3. Use the remote deploy script:

```bash
cd /path/to/your/app
chmod +x deploy_ec2.sh
./deploy_ec2.sh
```

Or from your local machine, copy the repo and deploy in one step:

```bash
chmod +x deploy_local_to_ec2.sh
./deploy_local_to_ec2.sh ubuntu@1.2.3.4 /home/ubuntu/leather-ecommerce www.goldhands.com
```

The deploy process will:
- install Nginx if needed
- create an Nginx reverse proxy config for `www.goldhands.com`
- restart Nginx
- run the Docker container on port `5000`
- serve the app on port `80`

### Notes

- Replace `ubuntu@1.2.3.4` with your EC2 username and host.
- Replace `/home/ubuntu/leather-ecommerce` with your desired remote app directory.
- If you run into SSH issues, make sure your local machine has SSH access to the EC2 instance.
