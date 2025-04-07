#!/usr/bin/env python3
"""Main entry point for the Turkish to Kazakh translation web application."""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 