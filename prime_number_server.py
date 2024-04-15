import sys
import time
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

class PrimeGenerator:
    def generate_primes(self, start, end):
        pass

class NaivePrimeGenerator(PrimeGenerator):
    def generate_primes(self, start, end):
        primes = []
        for num in range(max(2, start), end + 1):
            if self.is_prime(num):
                primes.append(num)
        return primes
    
    def is_prime(self, n):
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

class SievePrimeGenerator(PrimeGenerator):
    def generate_primes(self, start, end):
        sieve = [True] * (end + 1)
        p = 2
        while p * p <= end:
            if sieve[p]:
                for i in range(p * p, end + 1, p):
                    sieve[i] = False
            p += 1
        primes = [i for i in range(max(2, start), end + 1) if sieve[i]]
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
    prime_generator = get_prime_generator(strategy)
    primes = prime_generator.generate_primes(start, end)
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

def get_prime_generator(strategy):
    if strategy == 'naive':
        return NaivePrimeGenerator()
    elif strategy == 'sieve':
        return SievePrimeGenerator()
    else:
        raise ValueError("Invalid strategy")

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'server':
        app.run(debug=True)
    elif len(sys.argv) == 4:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
        strategy = sys.argv[3]
        prime_generator = get_prime_generator(strategy)
        primes = prime_generator.generate_primes(start, end)
        print(primes)
    else:
        print("Usage: python script.py server")
        print("       python script.py <start> <end> <strategy>")
        print("       Strategies: naive, sieve")
