#!/usr/bin/env python3
"""
HLA Database Setup Script
Downloads and caches the HLA FASTA database to avoid repeated downloads and disk space waste.
Run once: python setup_hla_database.py
"""

import os
import sys
import json
from pathlib import Path
import requests
from urllib.parse import urlparse

def get_cache_dir():
    """Get platform-appropriate cache directory."""
    if sys.platform == "win32":
        cache_base = Path.home() / "AppData" / "Local" / "hai_def_cache"
    else:
        cache_base = Path.home() / ".cache" / "hai_def"
    
    return cache_base

def download_hla_fasta(cache_dir: Path, url: str = "https://ftp.ebi.ac.uk/pub/databases/ipd/imgt/hla/hla_prot.fasta") -> Path:
    """Download HLA FASTA file to cache directory."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    fasta_file = cache_dir / "hla_prot.fasta"
    config_file = cache_dir / "config.json"
    
    # Check if file already exists
    if fasta_file.exists():
        print(f"✓ HLA database already cached at: {fasta_file}")
        file_size_mb = fasta_file.stat().st_size / (1024 * 1024)
        print(f"  File size: {file_size_mb:.1f} MB")
        return fasta_file
    
    print(f"📥 Downloading HLA FASTA database from EBI...")
    print(f"   URL: {url}")
    print(f"   Destination: {fasta_file}")
    
    try:
        response = requests.get(url, timeout=300, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        chunk_size = 1024 * 1024  # 1 MB chunks
        
        with open(fasta_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        mb_downloaded = downloaded / (1024 * 1024)
                        mb_total = total_size / (1024 * 1024)
                        print(f"   Progress: {percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)", end='\r')
        
        if total_size > 0:
            print()  # New line after progress
        
        file_size_mb = fasta_file.stat().st_size / (1024 * 1024)
        print(f"✅ Download complete! File size: {file_size_mb:.1f} MB")
        
        # Save config
        config = {
            "hla_fasta_path": str(fasta_file),
            "download_url": url,
            "file_size_mb": file_size_mb
        }
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✓ Configuration saved to: {config_file}")
        
        return fasta_file
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Download failed: {e}")
        if fasta_file.exists():
            fasta_file.unlink()
        sys.exit(1)

def load_hla_path() -> Path | None:
    """Load HLA FASTA path from cache config."""
    cache_dir = get_cache_dir()
    config_file = cache_dir / "config.json"
    
    if not config_file.exists():
        print("❌ HLA database not set up. Run: python setup_hla_database.py")
        return None
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return Path(config['hla_fasta_path'])
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return None

def main():
    """Main setup function."""
    print("="*70)
    print("🧬 HLA DATABASE SETUP")
    print("="*70)
    
    cache_dir = get_cache_dir()
    print(f"\n📂 Cache directory: {cache_dir}\n")
    
    fasta_path = download_hla_fasta(cache_dir)
    
    print("\n" + "="*70)
    print("✅ SETUP COMPLETE!")
    print("="*70)
    print(f"\nUse this in your notebook:")
    print(f"  from setup_hla_database import load_hla_path")
    print(f"  hla_fasta_path = load_hla_path()")
    print("="*70)

if __name__ == "__main__":
    main()
