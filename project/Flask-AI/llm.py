import requests 
import psycopg2

def get_db_schema(dbname, user, password, host='localhost', port=5433):
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cursor = conn.cursor()
        
        query = """
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return "No tables found in the database."
        
        markdown = "|Table name | Column name | Data type |\n| --------- | ----------- | ---------- | \n"
        
        for row in rows:
            markdown += f"|{row[0]} | {row[1]} | {row[2]} |\n"
            
        return markdown
        
    except Exception as e:
        return f"Error: {e}"
    
def generate_prompt(prompt, model="llama3.2", host="http://localhost:11434/"):
    url = f"{host}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()["response"]
        return data
        
    except Exception as e:
        return f"Error: {e}"
    
def generate_sql(question):
    dbname, user, password = "flask_db", "admin", "secret"
    
    schema = get_db_schema(dbname, user, password)
    
    prompt = f"""
        Act as Data Analyst senior, you will help junior on providing SQL queries.
        
        Generate a SQL query that answer the following question:
        
        {question}
        
        Use the following database schema:
        
        {schema} 
        
        Return only SQL query in plain text
    """
    
    response = generate_prompt(prompt)
    return response
    
def analyze_response(question, dbname, user, password):
    query = generate_sql(question)
    
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host='localhost', port=5433)
        cursor = conn.cursor()
        
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        field_name = [i[0] for i in cursor.description]
        table = "| " + " | ".join(field_name) + " |\n"
        table += "| " + " | ".join(["-" * len(name) for name in field_name]) + " |\n"
        
        for row in rows:
            table += "| " + " | ".join(map(str, row)) + " |\n"
            
        return table
        
    except Exception as e:
        return f"Error: {e}"
    
    
def response_analysis(question, response):
    query = f"""
        Act as Senio Data Analyst, provide your analysis from following question: 
        
        {question}
        
        Given the data after query from database:
        
        {response}    
    """
    
    return generate_prompt(query)
    
if __name__ == "__main__":
 
    dbname, user, password = "flask_db", "admin", "secret"
    question = "What are the customer name?"
    # schema_markdown = get_db_schema(dbname, user, password)
    # print(schema_markdown)

    # print(generate_prompt("Explain the theory of relativity in simple terms."))
    result = analyze_response(question, dbname, user, password)
    print(response_analysis(question, result))