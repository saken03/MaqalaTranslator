# Maqala Translator

A web application that translates Turkish text to Kazakh using ChatGPT-4o model.

## Features

- Web interface for easy text input and file upload
- Supports both direct text input and file uploads (.txt, .docx)
- Real-time translation progress tracking
- Chunk-based translation for handling large texts
- Preserves text formatting and structure
- Supports both Turkish and Kazakh characters

## Requirements

- Python 3.8 or higher
- OpenAI API key (configured for ChatGPT-4o access)
- Internet connection for API access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/MaqalaTranslator.git
cd MaqalaTranslator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
```bash
export OPENAI_API_KEY="your-api-key-here"
export FLASK_SECRET_KEY="your-secret-key-here"  # For session security
```

## Usage

1. Start the web server:
```bash
python run.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Use the web interface to:
   - Enter Turkish text directly in the text area
   - Or upload a .txt or .docx file containing Turkish text
   - Click "Translate" to start the translation
   - Watch the progress bar for translation status
   - View the translated text in real-time

## Configuration

You can modify the following settings in `config.py`:

- `DEFAULT_MODEL`: The model to use (default: "gpt-4o")
- `TEMPERATURE`: Model creativity setting (default: 0.3)
- `MAX_CHUNK_SIZE`: Maximum sentences per chunk (default: 30)
- `SUPPORTED_INPUT_FORMATS`: Supported file formats
- `DEFAULT_ENCODING`: File encoding (default: 'utf-8')

## Error Handling

The application includes comprehensive error handling for:
- Invalid API keys
- Unsupported file formats
- Network issues
- Translation errors
- File processing errors

## Security

- CSRF protection enabled
- Secure file upload handling
- Environment variable based configuration
- Input validation and sanitization

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Deployment

### Option 1: Deploy to Heroku

1. Install the Heroku CLI and login:
```bash
curl https://cli-assets.heroku.com/install.sh | sh
heroku login
```

2. Create a new Heroku app:
```bash
heroku create your-app-name
```

3. Set up environment variables:
```bash
heroku config:set FLASK_SECRET_KEY="your-secret-key-here"
heroku config:set OPENAI_API_KEY="your-openai-api-key-here"
```

4. Deploy to Heroku:
```bash
git push heroku main
```

### Option 2: Deploy to DigitalOcean App Platform

1. Create a new app in DigitalOcean App Platform
2. Connect your GitHub repository
3. Configure environment variables:
   - FLASK_SECRET_KEY
   - OPENAI_API_KEY
4. Select Python as the environment
5. Deploy the application

### Option 3: Deploy to a VPS (e.g., DigitalOcean Droplet)

1. Set up a Ubuntu server
2. Install required packages:
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

3. Clone the repository:
```bash
git clone https://github.com/yourusername/MaqalaTranslator.git
cd MaqalaTranslator
```

4. Set up virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. Create a systemd service file:
```bash
sudo nano /etc/systemd/system/maqala.service
```

Add the following content:
```ini
[Unit]
Description=Maqala Translator
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/path/to/MaqalaTranslator
Environment="PATH=/path/to/MaqalaTranslator/venv/bin"
Environment="FLASK_SECRET_KEY=your-secret-key-here"
Environment="OPENAI_API_KEY=your-openai-api-key-here"
ExecStart=/path/to/MaqalaTranslator/venv/bin/gunicorn run:app -b 0.0.0.0:5000

[Install]
WantedBy=multi-user.target
```

6. Start the service:
```bash
sudo systemctl start maqala
sudo systemctl enable maqala
```

7. Configure Nginx as a reverse proxy:
```bash
sudo nano /etc/nginx/sites-available/maqala
```

Add the following configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

8. Enable the site and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/maqala /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

9. Set up SSL with Let's Encrypt:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Important Deployment Notes

1. Always use environment variables for sensitive information
2. Set up proper logging in production
3. Configure proper security headers
4. Set up monitoring and alerts
5. Regular backups of any persistent data
6. Use a production-grade WSGI server (Gunicorn)
7. Set up proper error tracking (e.g., Sentry)