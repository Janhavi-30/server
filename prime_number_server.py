import sys
import time
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Prime number generator functions

def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes_range(start, end, strategy='naive'):
    """Generate prime numbers within a given range."""
    primes = []
    if strategy == 'naive':
        for num in range(max(2, start), end + 1):
            if is_prime(num):
                primes.append(num)
    elif strategy == 'sieve':
        sieve = [True] * (end + 1)
        p = 2
        while p * p <= end:
            if sieve[p]:
                for i in range(p * p, end + 1, p):
                    sieve[i] = False
            p += 1
        primes = [i for i in range(max(2, start), end + 1) if sieve[i]]
    else:
        raise ValueError("Invalid strategy")
    return primes

# Database setup
conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS executions 
             (timestamp INTEGER, start INTEGER, end INTEGER, strategy TEXT, time_elapsed REAL, num_primes INTEGER)''')

# API endpoints
@app.route('/generate_primes', methods=['GET'])
def generate_primes():
    start = int(request.args.get('start'))
    end = int(request.args.get('end'))
    strategy = request.args.get('strategy', 'naive')
    
    start_time = time.time()
    primes = generate_primes_range(start, end, strategy)
    end_time = time.time()
    time_elapsed = end_time - start_time
    
    c.execute("INSERT INTO executions (timestamp, start, end, strategy, time_elapsed, num_primes) VALUES (?, ?, ?, ?, ?, ?)",
              (int(time.time()), start, end, strategy, time_elapsed, len(primes)))
    conn.commit()
    
    return jsonify({'primes': primes, 'time_elapsed': time_elapsed, 'num_primes': len(primes)})


@app.route('/executions', methods=['GET'])
def get_executions():
    c.execute("SELECT * FROM executions")
    executions = [{'timestamp': row[0], 'start': row[1], 'end': row[2], 'strategy': row[3], 'time_elapsed': row[4], 'num_primes': row[5]} for row in c.fetchall()]
    return jsonify(executions)


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'server':
        app.run(debug=True)
    elif len(sys.argv) == 4:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
        strategy = sys.argv[3]
        primes = generate_primes_range(start, end, strategy)
        print(primes)
    else:
        print("Usage: python script.py server")
        print("       python script.py <start> <end> <strategy>")
        print("       Strategies: naive, sieve")
