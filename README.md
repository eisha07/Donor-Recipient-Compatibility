# Donor-Recipient-Compatibility

## Setup

### 1. Download HLA Database (One-time setup)

Run the setup script to download the HLA FASTA database to your system cache. This only needs to be done once:

```bash
python setup_hla_database.py
```

This will:
- Download the HLA FASTA database from EBI (~100 MB)
- Cache it in your system's cache directory (platform-specific)
- Store the path in a config file for reuse

**Cache locations:**
- **Linux/Mac**: `~/.cache/hai_def/hla_prot.fasta`
- **Windows**: `~/AppData/Local/hai_def_cache/hla_prot.fasta`

### 2. Use in Notebook

In your notebook, use the cached database path:

```python
from setup_hla_database import load_hla_path

hla_fasta_path = load_hla_path()
# Use hla_fasta_path in your HLASequenceCache or directly in your code
```

## Benefits

✅ **No repeated downloads** - The database is cached after the first run  
✅ **Minimal disk space** - Shared cache location, not duplicated per project  
✅ **Fast execution** - Subsequent runs use the cached file instantly  
✅ **Cross-platform** - Works on Linux, Mac, and Windows