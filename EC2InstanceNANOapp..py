from flask import Flask, render_template_string
import boto3
import time

app = Flask(__name__)

# Athena + S3 config
ATHENA_DATABASE = "orders_db"
ATHENA_TABLE = "processed"
ATHENA_OUTPUT = "s3://itcs6190-a3-navya-2025/query-results/"

athena = boto3.client("athena", region_name="us-east-1")

def run_athena_query(query):
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={"Database": ATHENA_DATABASE},
        ResultConfiguration={"OutputLocation": ATHENA_OUTPUT},
    )
    
    query_execution_id = response["QueryExecutionId"]
    
    while True:
        result = athena.get_query_execution(QueryExecutionId=query_execution_id)
        state = result["QueryExecution"]["Status"]["State"]

        if state == "SUCCEEDED":
            break
        elif state == "FAILED":
            return None
        
        time.sleep(1)

    result_set = athena.get_query_results(QueryExecutionId=query_execution_id)
    rows = []

    for row in result_set["ResultSet"]["Rows"][1:]:
        rows.append([col.get("VarCharValue", "") for col in row["Data"]])

    return rows


@app.route("/")
def dashboard():
    # 1. Total Sales by Customer
    q1 = """
    SELECT customer, SUM(amount) AS TotalAmountSpent
    FROM orders_db.processed
    GROUP BY customer
    ORDER BY TotalAmountSpent DESC;
    """
    total_sales = run_athena_query(q1)

    # 2. Monthly Order Volume & Revenue
    q2 = """
    SELECT CONCAT(year, '-', LPAD(month, 2, '0')) AS OrderMonth,
           COUNT(*) AS NumberOfOrders,
           SUM(amount) AS MonthlyRevenue
    FROM orders_db.processed
    GROUP BY year, month
    ORDER BY year, month;
    """
    monthly_stats = run_athena_query(q2)

    # 3. Order Status Dashboard
    q3 = """
    SELECT status, COUNT(*) AS OrderCount, SUM(amount) AS TotalAmount
    FROM orders_db.processed
    GROUP BY status;
    """
    order_status = run_athena_query(q3)

    # 4. Average Order Value per Customer
    q4 = """
    SELECT customer, AVG(amount) AS AOV
    FROM orders_db.processed
    GROUP BY customer
    ORDER BY AOV DESC;
    """
    aov = run_athena_query(q4)

    html = """
    <html>
    <head>
        <title>Athena Orders Dashboard</title>
        <style>
            body { font-family: Arial; margin: 20px; }
            h1 { background-color: #444; color: white; padding: 15px; }
            h2 { background-color: #333; color: white; padding: 10px; }
            table { width: 100%; border-collapse: collapse; margin-bottom: 25px; }
            th, td { border: 1px solid #ccc; padding: 10px; text-align: left; }
            th { background-color: #4A90E2; color: white; }
        </style>
    </head>
    <body>

        <h1>Athena Orders Dashboard</h1>

        <h2>1. Total Sales by Customer</h2>
        <table>
            <tr><th>Customer</th><th>TotalAmountSpent</th></tr>
            {% for row in total_sales %}<tr>
                <td>{{ row[0] }}</td><td>{{ row[1] }}</td>
            </tr>{% endfor %}
        </table>

        <h2>2. Monthly Order Volume and Revenue</h2>
        <table>
            <tr><th>OrderMonth</th><th>NumberOfOrders</th><th>MonthlyRevenue</th></tr>
            {% for row in monthly_stats %}<tr>
                <td>{{ row[0] }}</td><td>{{ row[1] }}</td><td>{{ row[2] }}</td>
            </tr>{% endfor %}
        </table>

        <h2>3. Order Status Dashboard</h2>
        <table>
            <tr><th>Status</th><th>OrderCount</th><th>TotalAmount</th></tr>
            {% for row in order_status %}<tr>
                <td>{{ row[0] }}</td><td>{{ row[1] }}</td><td>{{ row[2] }}</td>
            </tr>{% endfor %}
        </table>

        <h2>4. Average Order Value per Customer (AOV)</h2>
        <table>
            <tr><th>Customer</th><th>AOV</th></tr>
            {% for row in aov %}<tr>
                <td>{{ row[0] }}</td><td>{{ row[1] }}</td>
            </tr>{% endfor %}
        </table>

    </body>
    </html>
    """

    return render_template_string(html,
        total_sales=total_sales,
        monthly_stats=monthly_stats,
        order_status=order_status,
        aov=aov
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
