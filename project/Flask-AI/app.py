from flask import Flask, request, jsonify
from llm import *

app = Flask(__name__)

@app.post("/generate")
def generate():
    data = request.json
    prompt = data.get("prompt", "")
    response = generate_prompt(prompt)
    
    return jsonify({"response": response})

@app.get("/schemas")
def schemas():
    dbname = request.args.get("dbname", "flask_db")
    user = request.args.get("user", "admin")
    password = request.args.get("password", "secret")
    
    schemas_md = get_db_schema(dbname, user, password)
    return jsonify({"schema": schemas_md})
    
@app.post("/analyze")
def analyze():
    data = request.json
    question = data.get("question", "")
    dbname = request.args.get("dbname", "flask_db")
    user = request.args.get("user", "admin")
    password = request.args.get("password", "secret")
    
    response = analyze_response(question, dbname, user, password)
    analysis = response_analysis(question, response)
    return analysis
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)