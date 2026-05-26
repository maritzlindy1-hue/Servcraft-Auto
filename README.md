# Donovan Local Dashboard

This local dashboard reads the newest Excel file inside the `exports` folder.

## First-time setup

```bash
pip3 install -r requirements.txt
```

## Daily use

1. Run your ServCraft export script.
2. Copy or save the downloaded Excel into this dashboard's `exports` folder.
3. Start the dashboard:

```bash
python3 app.py
```

4. Open this in your browser:

```text
http://127.0.0.1:5000
```

## Important

The dashboard automatically uses the newest Excel file in the `exports` folder.