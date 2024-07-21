## Setup Instructions

1. **Extract the ZIP file**:

   ```bash
   unzip Phonebook-Spam-Detector-API.zip
   cd Phonebook-Spam-Detector-API
   ```
2. **Create a Virtual Environment**: 
   ```bash
   python -m venv venv
    ```
3. **Activate Virtual Environment**:

   -On Windows
   ```bash
   venv\Scripts\activate
   ```
   -On macOS/Linux
   ```bash
   source venv/bin/activate
   ```
**Make sure you are inside phonebook_spam_detector directory**

4. **Install Requirements:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Run Development Server:**
   ```bash
   python manage.py runserver
   ```
   
6. **Create Dummy Data (optional, for testing):**
   ```bash
   python manage.py populate_data
   ```