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
   pip install Scrapy==2.11.1
   pip install selenium==3.141.0
   pip install webdriver-manager==2.5.1
   pip install undetected-chromedriver==3.0.1
   pip install chromedriver_autoinstaller
   pip install scrapeops-scrapy
   pip install playsound
   pip install twilio
   pip install oauth2client==4.1.3
   pip install gspread
   ```


---

## Step 2: Running the Script

1. Open the terminal/command prompt and navigate to the project directory:

   ```sh
   cd "cesar_scrapers/cesar_scrapers/spiders"
   ```

2. Run the script using syntax:

   ```sh
   scrapy crawl <spider-name>
   ```

   **OR**

   Open `tps_spider.py` in PyCharm, right-click on it, and select the `Run` option.

**Note:**

Make sure you are in the project spiders directory:

```
/cesar_scrapers/cesar_scrapers/spiders/
```

---

## Step 3: Output Location

After successful execution, the script will search, extract, filter and store the matched .
results in database tables.

---

### Need Help?

If you have any questions regarding the script, please inbox me. I'd be happy to assist you!

Many thanks!

