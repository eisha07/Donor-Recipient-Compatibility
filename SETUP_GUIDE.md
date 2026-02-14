# HLA Database Setup Guide

## Quick Start

### Step 1: One-time Database Setup

Run this command once to download and cache the HLA database:

```bash
python setup_hla_database.py
```

Expected output:
```
======================================================================
🧬 HLA DATABASE SETUP
======================================================================

📂 Cache directory: /home/user/.cache/hai_def

📥 Downloading HLA FASTA database from EBI...
   URL: https://ftp.ebi.ac.uk/pub/databases/ipd/imgt/hla/hla_prot.fasta
   Destination: /home/user/.cache/hai_def/hla_prot.fasta
   Progress: 100.0% (150.5/150.5 MB)
✅ Download complete! File size: 150.5 MB
✓ Configuration saved to: /home/user/.cache/hai_def/config.json

======================================================================
✅ SETUP COMPLETE!
======================================================================

Use this in your notebook:
  from setup_hla_database import load_hla_path
  hla_fasta_path = load_hla_path()
======================================================================
```

### Step 2: Use in Your Notebook

Replace the git clone and manual download code in your notebook with this:

**Before (Old approach - downloads and clones LFS repo):**
```python
# Old code - downloads ~100+ MB, clones large git repo
repo_url = "https://github.com/ANHIG/IMGTHLA/"
os.system(f"git clone {repo_url} {absolute_local_repo_dir}")
```

**After (New approach - uses cached file):**
```python
from setup_hla_database import load_hla_path
from pathlib import Path

hla_fasta_path = load_hla_path()
print(f"Using cached HLA database: {hla_fasta_path}")

# Pass this path to your HLASequenceCache or use directly
```

### Step 3: Modify Your HLASequenceCache Class

Update the `_download_complete_hla_dataset` method to prefer the cached file:

```python
def _download_complete_hla_dataset(self) -> Dict:
    """Load HLA dataset from cached file."""
    from setup_hla_database import load_hla_path
    
    # Try cached location first
    cached_path = load_hla_path()
    if cached_path and cached_path.exists():
        print(f"📥 Loading HLA FASTA from cache: {cached_path}")
        try:
            with open(cached_path, 'r') as f:
                fasta_content = f.read()
            dataset = self._parse_fasta_to_dataset(fasta_content)
            if dataset:
                print(f"✅ Parsed {len(dataset)} unique HLA protein sequences")
                return dataset
        except Exception as e:
            print(f"❌ Error reading cached file: {e}")
    
    # Fallback to EBI
    # ... rest of your download logic
```

## Benefits

| Aspect | Old Approach | New Approach |
|--------|------------|--------------|
| **Download Speed** | Every notebook run | Once, cached forever |
| **Disk Usage** | Multiple copies (one per project) | Single shared copy |
| **Setup Time** | Minutes (git clone) | Seconds (load from cache) |
| **Network** | Repeated downloads | One-time only |
| **Storage Location** | Project folder | System cache folder |

## What Gets Downloaded

- **File**: `hla_prot.fasta` - HLA protein sequences database
- **Size**: ~100-150 MB
- **Source**: EBI IMGT/HLA database
- **Location**: System cache (platform-specific)

## Troubleshooting

### Clear Cache and Re-download

If you need to re-download the database:

```bash
rm -rf ~/.cache/hai_def  # Linux/Mac
# or
rmdir %LOCALAPPDATA%\hai_def_cache  # Windows
python setup_hla_database.py
```

### Check Cache Status

```python
from setup_hla_database import get_cache_dir
from pathlib import Path

cache_dir = get_cache_dir()
config_file = cache_dir / "config.json"

if config_file.exists():
    print("✓ Database is set up")
else:
    print("✗ Database not set up - run: python setup_hla_database.py")
```

## Automation (Optional)

If you want to ensure the database is set up before running notebooks, add this at the notebook start:

```python
from pathlib import Path
from setup_hla_database import load_hla_path

# Check if database is cached
hla_path = load_hla_path()
if not hla_path:
    print("❌ HLA database not cached. Run: python setup_hla_database.py")
    raise RuntimeError("Database setup required")
else:
    print(f"✓ Using cached database: {hla_path}")
```
