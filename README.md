# VNPAY Entry Test - Part 2: Data & Coding

## Setup Evironment:

1. Create a Virtual Environment

```bash
python3 -m venv venv
```

1. Activate the Virtual Environment

```bash
source venv/bin/activate
```

1. Install dependencies

```bash
pip install -r requirements.txt
```

## Part 1: Weather Data Crawling Using Visual Crossing API

The weather data is retrieved using the **Visual Crossing API**, which provides access to historical weather data. The API request fetches weather data based on the **location** (e.g., district names in Hanoi) and the **date** for which the data is required.

**API Request URL Structure:**

```

https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{date}?key={api_key}&include=hours
```

Where:

- `{location}`: The city/district for which weather data is requested (e.g., "Hoan Kiem, Hanoi, Vietnam").
- `{date}`: The specific date to retrieve data for (e.g., "2023-03-25").
- `{api_key}`: The key used to authenticate and access the API.

The response from the API is in **JSON** format, which contains detailed information about the weather conditions, including humidity, precipitation, and other hourly metrics. //Link_example_respon

You can view the complete code for crawling weather data using the Visual Crossing API in the following //link to code.

### **Code Explanation**

1. **API Request and Fetch Data:**
The function `fetch_weather_data()` constructs the API URL using the `location` and `date` as parameters. It sends a **GET** request to the API and checks if the request was successful by checking the status code. If successful, it returns the weather data in JSON format.
2. **Extracting Useful Information:**
The `extract_info()` function processes the raw JSON data by looping through the hourly data for each day. It extracts key weather parameters.
    
    This function stores the extracted data in a structured format (list of dictionaries).
    
3. **Saving Data to File:**
The function `save_data_to_local()` saves the processed weather data to a CSV file and a JSON file, with each row representing hourly weather data. The filename includes the date of the data being saved (e.g., `weather_data_2023-03-25.csv`). 
4. Link code. 

### **Optional Enhancement: Schedule the Script to Run Daily**

To automate the process of crawling weather data daily, we can use **cron jobs**. This allows you to run the Python script automatically at specific times without needing to keep the script running continuously.

1. **Open the Cron Tab for Editing:**
Open the terminal and run:
    
    ```bash
    crontab -e
    ```
    
2. **Add a Cron Job to Run Daily at 07:00 AM:**
Add the following line to run your Python script at 07:00 AM every day:
    
    ```bash
    0 7 * * * /usr/bin/python3 /absolute_path/to/crawl.py
    ```
    
    - `0 7 * * *`: This specifies that the script will run **daily** at **07:00 AM**.
    - `/usr/bin/python3`: The full path to the Python interpreter (you can check it by running `which python3`).
    - `/absolute_path/to/crawl.py`: The full path to the Python script you want to run.
3. **Save and Exit:**
After adding the cron job, save and exit the editor:
    - In `vim`: Press `Esc`, type `:wq`, and hit `Enter`
    - In `nano`: Press `CTRL + X`, then press `Y`, and hit `Enter`.
4. **Verify the Cron Job:**
You can verify that the cron job was added successfully by running:
    
    ```bash
    crontab -l
    ```
    

---

## Part 2: EDA

### Q1. Clean data and filter Outliers

**Data description:**

- **UserId** - It is a unique ID for all User Id
- **TransactionId** - It contains unique Transactions ID
- **TransactionTime** - It contains Transaction Time
- **ItemCode** - It contains item code that item will be purchased
- **ItemDescription** - It contains Item description
- **NumberOfItemPurchased** - It contains total number of items Purchased
- **CostPerltem** - Cost per item Purchased
- **Country** - Country where item purchased

**Step 1: Drop Duplicates. Handle Missing Values**

- Removed duplicate rows to ensure data quality and reduce dataset size. The dataset size was reduced from 1,083,818 rows to 536,572 rows by eliminating redundant entries.
- The `ItemDescription` column has a small proportion of missing values (0.27% of the data). Since the dataset contains a relatively small number of missing rows, the decision is to fill these missing values with the placeholder 'N/A'.
- Other columns have no missing values -> No action required

**Step 2: Correct Data Types**

Final Data Types:

- UserId: `str`
- TransactionId: `str`
- TransactionTime: `datetime`
- ItemCode: `str`
- ItemDescription: `str`
- NumberOfItemsPurchased: `int`
- CostPerItem: `float`
- Country: `str`

**Step 3: Filter and Treat Outliers**

- Remove rows with UserId = -1
- Negative Values:
    - NumberOfItemsPurchased: Min = -242,985 (illogical).
    - CostPerItem: Min = -15,265.64 (unrealistic).
- Extreme Outliers:
    - NumberOfItemsPurchased: Max = 242,985, far higher than the mean (28.66), with a high standard deviation (657.43).
    - CostPerItem: Max = 1,696,285.5, much larger than the mean (9.39), with a high standard deviation (2,476.45).
- Outlier Removal: Used IQR (Interquartile Range) method to remove extreme outliers and improve data quality.

### Q2. Calculate the number of Items purchased and prices in each month

This script calculates the total number of items purchased and the total price for each month. The results are aggregated by month and stored in an output file.

**Steps:**

1. The data is first processed to extract the year and month from the `TransactionTime`.
2. The total number of items purchased and the total price (calculated as `NumberOfItemsPurchased * CostPerItem`) are then calculated for each month.

**Code**: Link to Code

**Output File**: Link to Output File

### Q3. Calculate the number of items purchased for each userID in 30 days for each day

This script calculates the total number of items purchased by each `UserID` for each day over a 30-day period. The results are aggregated by `UserID` and `TransactionTime` (date-wise).

**Steps:**

1. The data is processed to filter transactions within the last 30 days.
2. The number of items purchased by each `UserID` is summed for each day.

**Code**: Link to Code

**Output File**: Link to Output File

### Q4. Recommendation system with the goal of purchasing more items

**Hybrid Approach Strategy:**

1. **Content-Based Filtering (CBF)**: This will provide recommendations based on item similarity derived from product descriptions.
2. **Collaborative Filtering (SVD)**: This will provide recommendations based on user-item interaction patterns (e.g., purchases).
3. **Hybrid Model**: Combine the recommendations from both models by taking a weighted average of the two approaches' recommendations.

We'll assign weights to both methods (e.g., 0.5 for each method), and then generate a final recommendation list for each user based on both approaches. The final recommendation will be the union of the top N products from both models.

**Steps:**

1. Train both the **Content-Based Filtering (CBF)** model and **SVD-based Collaborative Filtering** model.
2. Combine the recommendations from both models based on weighted averages.
3. Evaluate the hybrid model using precision and recall.

→ The **Hybrid Recommender System** combines the strengths of both **Content-Based Filtering** (good when item metadata is available) and **Collaborative Filtering (SVD)** (good when user-item interaction data is available). The weighted combination of the two methods often results in better recommendations, as it leverages both content-based and collaborative signals.

**Result:**

→ The **Hybrid Model** combines multiple methods, and the higher precision and better top-K accuracy suggest that it is performing better than either of the individual models. However, since the recall is still 1.0, it may still be recommending at least one relevant item, but the precision is low, meaning it’s also recommending many irrelevant items.

**Issues:**

- Data-Related:
    - Small Sample Size: Limited data results in overfitting and poor generalization.
    - Cold Start Problem: Lack of data for new items or users.
    - Sparsity: Missing interactions between users and items, especially in collaborative filtering.
- Model-Related:
    - Overfitting: Especially in small datasets, models may memorize the data rather than generalize.
    - Limited Diversity: Content-based models may only recommend similar items, leading to narrow suggestions.
    - Performance Issues: SVD-based models struggle with sparse data or small sample sizes.

### Suggestions for Improvement:

- Data-Related:
    - Data Augmentation: Use implicit feedback (views, clicks) to enrich the dataset.
    - Hybridize Content-Based & Collaborative: Combine strengths of both to handle cold start and sparsity.
    - Cross-Validation: Apply k-fold validation to reduce overfitting and make the most of small data.
- Model-Related:
    - Regularization: Apply regularization to avoid overfitting, especially in matrix factorization.
    - Better Feature Engineering: Use more sophisticated item features (e.g., embeddings, categories).