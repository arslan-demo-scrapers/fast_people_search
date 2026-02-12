# Web Scraper Setup On New System, Quick Guide

- **Install IDE**  
- **Create Virtual Environment**  
- **Install MYSQL Server**  
- **Install MYSQL WorkBench**  
- **Create Database & Tables**  
- **Add Spiders Configuration**  

---

# Web Scraper Usage Guide

## Prerequisites

- **Python Version:** Ensure you have Python 3.9 or later installed.
- **IDE Recommendation:** Download and install [PyCharm Community Edition](https://www.jetbrains.com/pycharm/download/) for managing Python projects.

---

## Step 1: Setup the Environment

1. **Install PyCharm** and open the project folder.
2. Navigate to `Project Interpreter` and create a new virtual environment.

   Alternatively, check this guide for setting up a virtual environment on [Windows/Linux](https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/?ref=lbp).

3. **Upgrade pip** to the latest version by running:

   ```sh
   pip install --upgrade pip
   ```

4. **Install required dependencies:**
   
   ```sh
   pip install -r requirements.txt
   ```
   
   Or install them individually:

   ```sh
   pip install Scrapy==2.13.4
   pip install scrapeops-scrapy
   pip install mysql-connector-python~=8.0.28
   pip install twilio
   ```

---

## Step 2: Running the Script

1. Open the terminal/command prompt and navigate to the project directory:

   ```sh
   cd "fast_people_search/fast_people_search/spiders"
   ```

2. Run the script using syntax:

   ```sh
   scrapy crawl <spider-name>
   ```

   **OR**

   Open `fast_people_search_spider.py` in PyCharm, right-click on it, and select the `Run` option.

**Note:**

Make sure you are in the project spiders directory:

```
/fast_people_search/fast_people_search/spiders/
```

---

## Step 3: Output Location

After successful execution, the script will search, extract, filter and store the results in JSON file, located in `ouput` folder.

---

### Need Help?

If you have any questions regarding the script, please inbox me. I'd be happy to assist you!

**Many thanks!**

**Best**, Arslan
