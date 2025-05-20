# Navigate to your project directory
```bash
cd /Users/kurtik/Projects/crypto-app
```

# Run your backend with nohup in the background
```bash
cd backend
nohup python run.py > ../backend_log.txt 2>&1 &
```

# Note the process ID that will be shown (you'll need it to kill the process later)
# Example output: [1] 1234

# Monitor file size changes in real time
```bash
watch -n 5 "ls -la /Users/kurtik/Projects/crypto-app/backend/app/external/utilities/*.csv"
```

# Check the most recent lines written to a specific CSV file
```bash
tail -f /Users/kurtik/Projects/crypto-app/backend/app/external/utilities/crypto_arbitrage_3_*.csv
```

# List running Python processes
```bash
ps aux | grep python
```

# Kill the background process when you're done (replace 1234 with your process ID)
```bash
kill 1234
```