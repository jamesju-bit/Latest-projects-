

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

class Parent:
    def __init__(self, phone_number, id_details):
        self.phone_number = phone_number
        self.id_details = id_details

class KidAccount:
    def __init__(self, name, balance, parent):
        self.name = name
        self.balance = balance
        self.parent = parent

parents = {}  # Dictionary to store parent information
kid1 = KidAccount("Alice", 100, None)
kid2 = KidAccount("Bob", 50, None)

def verify_parent(phone_number, id_details):
    # In a real app, you would perform more robust verification (e.g., against a database)
    return phone_number in parents and parents[phone_number].id_details == id_details

@app.route('/register_parent', methods=['POST'])
def register_parent():
    data = request.get_json()
    phone_number = data.get('phone_number')
    id_details = data.get('id_details')
    
    if not phone_number or not id_details:
        return jsonify({"error": "Invalid input"}), 400

    parents[phone_number] = Parent(phone_number, id_details)
    return jsonify({"message": "Parent registered successfully."})

@app.route('/transfer', methods=['POST'])
def transfer_money():
    data = request.get_json()
    phone_number = data.get('phone_number')
    id_details = data.get('id_details')
    amount = float(data.get('amount', 0))

    if not phone_number or not id_details or amount <= 0:
        return jsonify({"error": "Invalid input"}), 400

    if verify_parent(phone_number, id_details):
        kid1.balance -= amount
        kid2.balance += amount
        return jsonify({"message": f"Transfer successful! {kid1.name} sent {amount} to {kid2.name}."})
    else:
        return jsonify({"error": "Parent verification failed."}), 401

if __name__ == '__main__':
    app.run(debug=True)
```

