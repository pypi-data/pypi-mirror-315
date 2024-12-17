"""Command-line interface for MistralVDB."""

import os
import argparse
from .api import start_server

def run_server():
    """Run the MistralVDB API server."""
    parser = argparse.ArgumentParser(description="Start MistralVDB API server")
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to run the server on (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the server on (default: 8000)"
    )
    parser.add_argument(
        "--storage-dir",
        help="Custom storage directory (optional)"
    )
    parser.add_argument(
        "--jwt-secret",
        help="JWT secret key (optional, will generate if not provided)"
    )
    
    args = parser.parse_args()
    
    # Get API key from environment
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError(
            "MISTRAL_API_KEY environment variable must be set. "
            "Get your API key from https://console.mistral.ai/"
        )
    
    # Generate JWT secret if not provided
    if not args.jwt_secret:
        import secrets
        args.jwt_secret = secrets.token_urlsafe(32)
        print(f"Generated JWT secret key: {args.jwt_secret}")
    
    print(f"Starting server on {args.host}:{args.port}")
    if args.storage_dir:
        print(f"Using storage directory: {args.storage_dir}")
    
    start_server(
        host=args.host,
        port=args.port,
        mistral_api_key=api_key,
        jwt_secret_key=args.jwt_secret
    )
