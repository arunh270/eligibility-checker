from flask import Flask, request, jsonify, render_template  # Moved render_template import here

app = Flask(__name__)

# Example AST Node
class Node:
    def __init__(self, node_type: str, left=None, right=None, value=None):
        self.node_type = node_type
        self.left = left
        self.right = right
        self.value = value

    def evaluate(self, user_data):
        if self.node_type == "operator":
            if self.value == "AND":
                return self.left.evaluate(user_data) and self.right.evaluate(user_data)
            elif self.value == "OR":
                return self.left.evaluate(user_data) or self.right.evaluate(user_data)
        elif self.node_type == "operand":
            field, operator, target_value = self.value["field"], self.value["operator"], self.value["value"]
            user_value = user_data.get(field)
            if operator == ">":
                return user_value > target_value
            elif operator == "<":
                return user_value < target_value
            elif operator == "==":
                return user_value == target_value
            elif operator == ">=":
                return user_value >= target_value
            elif operator == "<=":
                return user_value <= target_value
            elif operator == "!=":
                return user_value != target_value
        return False

# Define the default rule (AST example)
rules = Node(
    node_type="operator",
    value="AND",
    left=Node(node_type="operand", value={"field": "age", "operator": ">", "value": 18}),
    right=Node(
        node_type="operator",
        value="OR",
        left=Node(node_type="operand", value={"field": "income", "operator": ">=", "value": 50000}),
        right=Node(node_type="operand", value={"field": "department", "operator": "==", "value": "engineering"})
    )
)

@app.route('/check-eligibility', methods=['POST'])
def check_eligibility():
    user_data = request.json
    
    # Convert age and income to the appropriate types
    user_data['age'] = int(user_data['age'])  # Ensure age is an integer
    user_data['income'] = int(user_data['income'])  # Ensure income is an integer

    eligibility = rules.evaluate(user_data)
    return jsonify({"eligible": eligibility})


@app.route('/modify-rule', methods=['POST'])
def modify_rule():
    global rules
    new_rule = request.json
    rules = parse_ast(new_rule)
    return jsonify({"message": "Rule updated successfully"})

def parse_ast(data):
    if data['node_type'] == 'operator':
        return Node(node_type=data['node_type'], value=data['value'], left=parse_ast(data['left']), right=parse_ast(data['right']))
    elif data['node_type'] == 'operand':
        return Node(node_type=data['node_type'], value=data['value'])
    return None

@app.route('/')  # Route for the homepage
def home():
    return render_template('index.html')  # Ensure this matches your HTML file name

if __name__ == '__main__':
    app.run(debug=True)  # Start the Flask app
