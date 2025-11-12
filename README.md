# ITCS-6190 Assignment 3: AWS Data Processing Pipeline

This project demonstrates an end-to-end serverless data processing pipeline on AWS. The process involves ingesting raw data into S3, using a Lambda function to process it, cataloging the data with AWS Glue, and finally, querying and visualizing the results on a dynamic webpage hosted on an EC2 instance.

## 1. Amazon S3 Bucket Structure 🪣

First, set up an S3 bucket with the following folder structure to manage the data workflow:

* **`bucket-name/`**
    * **`raw/`**: For incoming raw data files.
    * **`processed/`**: For cleaned and filtered data output by the Lambda function.
    * **`enriched/`**: For storing athena query results.

---
<img width="1918" height="1053" alt="image" src="https://github.com/user-attachments/assets/2ff16504-9720-47b2-8b06-5707576d19cb" />
<img width="1910" height="1051" alt="image" src="https://github.com/user-attachments/assets/a5ace5bd-952e-4388-bda7-8cc2511d0402" />



## 2. IAM Roles and Permissions 🔐

Create the following IAM roles to grant AWS services the necessary permissions to interact with each other securely.

### Lambda Execution Role

1.  Navigate to **IAM** -> **Roles** and click **Create role**.
2.  **Trusted entity type**: Select **AWS service**.
3.  **Use case**: Select **Lambda**.
4.  **Add Permissions**: Attach the following managed policies:
    * `AWSLambdaBasicExecutionRole`
    * `AmazonS3FullAccess`
5.  Give the role a descriptive name (e.g., `Lambda-S3-Processing-Role`) and create it.


   <img width="1917" height="1045" alt="image" src="https://github.com/user-attachments/assets/7a6ee6e4-41e8-4cae-b43e-b085563d743a" />


### Glue Service Role

1.  Create another IAM role for **AWS service** with the use case **Glue**.
2.  **Add Permissions**: Attach the following policies:
    * `AmazonS3FullAccess`
    * `AWSGlueConsoleFullAccess`
    * `AWSGlueServiceRole`
3.  Name the role (e.g., `Glue-S3-Crawler-Role`) and create it.

<img width="1907" height="1035" alt="image" src="https://github.com/user-attachments/assets/2d7bd3a4-a48c-42e6-9d98-908aa6af4ac8" />


### EC2 Instance Profile

1.  Create a final IAM role for **AWS service** with the use case **EC2**.
2.  **Add Permissions**: Attach the following policies:
    * `AmazonS3FullAccess`
    * `AmazonAthenaFullAccess`
3.  Name the role (e.g., `EC2-Athena-Dashboard-Role`) and create it.

---
<img width="1912" height="1037" alt="image" src="https://github.com/user-attachments/assets/ce8f49e5-8ab3-4d5f-8843-24ccbcfc2def" />

## 3. Create the Lambda Function ⚙️

This function will automatically process files uploaded to the `raw/` S3 folder.

1.  Navigate to the **Lambda** service in the AWS Console.
2.  Click **Create function**.
3.  Select **Author from scratch**.
4.  **Function name**: `FilterAndProcessOrders`
5.  **Runtime**: Select **Python 3.9** (or a newer version).
6.  **Permissions**: Expand *Change default execution role*, select **Use an existing role**, and choose the **Lambda Execution Role** you created.
7.  Click **Create function**.
8.  In the **Code source** editor, replace the default code with LambdaFunction.py code for processing the raw data.

---
<img width="1917" height="1046" alt="image" src="https://github.com/user-attachments/assets/73631247-7b3f-4519-8a04-447599c79b59" />


## 4. Configure the S3 Trigger ⚡

Set up the S3 trigger to invoke your Lambda function automatically.

1.  In the Lambda function overview, click **+ Add trigger**.
2.  **Source**: Choose **S3**.
3.  **Bucket**: Select your S3 bucket.
4.  **Event types**: Choose **All object create events**.
5.  **Prefix (Required)**: Enter `raw/`. This ensures the function only triggers for files in this folder.
6.  **Suffix (Recommended)**: Enter `.csv`.
7.  Check the acknowledgment box and click **Add**.

--- 
<img width="1911" height="1032" alt="image" src="https://github.com/user-attachments/assets/5573a7e5-8398-4ad6-a4c4-8f2ba0886170" />

**Start Processing of Raw Data**: Now upload the Orders.csv file into the `raw/` folder of the S3 Bucket. This will automatically trigger the Lambda function.
---
<img width="1911" height="1052" alt="image" src="https://github.com/user-attachments/assets/ba85a38e-dc6c-4dd7-9960-b6c005d168a4" />

## 5. Create a Glue Crawler 🕸️

The crawler will scan your processed data and create a data catalog, making it queryable by Athena.

1.  Navigate to the **AWS Glue** service.
2.  In the left pane, select **Crawlers** and click **Create crawler**.
3.  **Name**: `orders_processed_crawler`.
4.  **Data source**: Point the crawler to the `processed/` folder in your S3 bucket.
5.  **IAM Role**: Select the **Glue Service Role** you created earlier.
6.  **Output**: Click **Add database** and create a new database named `orders_db`.
7.  Finish the setup and run the crawler. It will create a new table in your `orders_db` database.

---
<img width="1917" height="1093" alt="image" src="https://github.com/user-attachments/assets/c87b4e2d-d6aa-4a0f-810d-49632d34c94a" />
<img width="1910" height="1047" alt="image" src="https://github.com/user-attachments/assets/3b9fe3f6-7d8d-4aec-ae56-15b655eda501" />
<img width="1918" height="1047" alt="image" src="https://github.com/user-attachments/assets/a8dda254-2fe2-4156-b4ad-e1e4e7b2c329" />
<img width="1910" height="1083" alt="image" src="https://github.com/user-attachments/assets/b76e327c-7b74-44a5-999c-ab70d06b641a" />
<img width="1908" height="1047" alt="image" src="https://github.com/user-attachments/assets/cceb0ab0-a454-481c-bd74-83134cf6a81d" />





## 6. Query Data with Amazon Athena 🔍

Navigate to the **Athena** service. Ensure your data source is set to `AwsDataCatalog` and the database is `orders_db`. You can now run SQL queries on your processed data.

**Queries to be executed:**
* **Total Sales by Customer**: Calculate the total amount spent by each customer.
<img width="1903" height="1032" alt="image" src="https://github.com/user-attachments/assets/992a20eb-ec15-4e70-85f7-c9c047c4d35b" />
<img width="1907" height="1032" alt="image" src="https://github.com/user-attachments/assets/1f12a81c-ff8c-45cf-bcd7-2a6e690fa763" />


* **Monthly Order Volume and Revenue**: Aggregate the number of orders and total revenue per month.
<img width="1897" height="1047" alt="image" src="https://github.com/user-attachments/assets/48e9a88f-ded1-4741-9fa2-87fba49e1f87" />

* **Order Status Dashboard**: Summarize orders based on their status (`shipped` vs. `confirmed`).
<img width="1902" height="1060" alt="image" src="https://github.com/user-attachments/assets/93a57b3b-6a06-4360-aa70-5a56bd4d89ee" />
<img width="1908" height="1053" alt="image" src="https://github.com/user-attachments/assets/9ef5d3ec-73f4-4b3d-9179-c0bae587ffd3" />


* **Average Order Value (AOV) per Customer**: Find the average amount spent per order for each customer.

* **Top 10 Largest Orders in February 2025**: Retrieve the highest-value orders from a specific month.

---
<img width="1903" height="1042" alt="image" src="https://github.com/user-attachments/assets/a7ebb661-986c-4d27-bb03-49ef491bce04" />



## 7. Launch the EC2 Web Server 🖥️

This instance will host a simple web page to display the Athena query results.

1.  Navigate to the **EC2** service and click **Launch instance**.
2.  **Name**: `Athena-Dashboard-Server`.
3.  **Application and OS Images**: Select **Amazon Linux 2023 AMI**.
4.  **Instance type**: Choose **t2.micro** (Free tier eligible).
5.  **Key pair (login)**: Create and download a new key pair. **Save the `.pem` file!**
6.  **Network settings**: Click **Edit** and configure the security group:
    * **Rule 1 (SSH)**: Type: `SSH`, Port: `22`, Source: `My IP`.
    * **Rule 2 (Web App)**: Click **Add security group rule**.
        * Type: `Custom TCP`
        * Port Range: `5000`
        * Source: `Anywhere` (`0.0.0.0/0`)
7.  **Advanced details**: Scroll down and for **IAM instance profile**, select the **EC2 Instance Profile** you created.
8.  Click **Launch instance**.

---

## 8. Connect to Your EC2 Instance

1.  From the EC2 dashboard, select your instance and copy its **Public IPv4 address**.
2.  Open a terminal or SSH client and connect using your key pair:

    ```bash
    ssh -i /path/to/your-key-file.pem ec2-user@YOUR_PUBLIC_IP_ADDRESS
    ```

---

## 9. Set Up the Web Environment

Once connected via SSH, run the following commands to install the necessary software.

1.  **Update system packages**:
    ```bash
    sudo yum update -y
    ```
2.  **Install Python and Pip**:
    ```bash
    sudo yum install python3-pip -y
    ```
3.  **Install Python libraries (Flask & Boto3)**:
    ```bash
    pip3 install Flask boto3
    ```

---

## 10. Create and Configure the Web Application

1.  Create the application file using the `nano` text editor:
    ```bash
    nano app.py
    ```
2.  Copy and paste your Python web application code (`EC2InstanceNANOapp.py`) into the editor.

3.  ‼️ **Important**: Update the placeholder variables at the top of the script:
    * `AWS_REGION`: Your AWS region (e.g., `us-east-1`).
    * `ATHENA_DATABASE`: The name of your Glue database (e.g., `orders_db`).
    * `S3_OUTPUT_LOCATION`: The S3 URI for your Athena query results (e.g., `s3://your-athena-results-bucket/`).

4.  Save the file and exit `nano` by pressing `Ctrl + X`, then `Y`, then `Enter`.

---

## 11. Run the App and View Your Dashboard! 🚀

1.  Execute the Python script to start the web server:
    ```bash
    python3 app.py
    ```
    You should see a message like `* Running on http://0.0.0.0:5000/`.

2.  Open a web browser and navigate to your instance's public IP address on port 5000:
    ```
    http://YOUR_PUBLIC_IP_ADDRESS:5000
    ```
    You should now see your Athena Orders Dashboard!

---

## Important Final Notes

* **Stopping the Server**: To stop the Flask application, return to your SSH terminal and press `Ctrl + C`.
* **Cost Management**: This setup uses free-tier services. To prevent unexpected charges, **stop or terminate your EC2 instance** from the AWS console when you are finished.
