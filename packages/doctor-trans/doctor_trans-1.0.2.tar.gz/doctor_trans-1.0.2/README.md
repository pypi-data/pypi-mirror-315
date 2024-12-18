# Doctor Trans

Doctor Trans is a powerful Python package for translating large datasets in a DataFrame format. It process multiple columns simultaneously, translating text data from one language to another while preserving data integrity. The package outputs the translated DataFrame, making it perfect for large-scale multilingual data processing in business and research.

## Features
- **Automatic Language Detection**: Automatically detects the source language if not specified.
- **Multiple Language Support**: Supports translation to and from any language available in Google Translate.
- **Error Handling and Logging**: Provides detailed logging to track translation status and handle errors effectively.

## Installation
To use Doctor Trans, ensure the following packages are installed:
```bash
pip install pandas requests openpyxl
```
If Microsoft Visual C++ 14.0 is not installed, you can download it here:
https://visualstudio.microsoft.com/visual-cpp-build-tools/

```python
import pandas as pd
from doctor_trans import trans

# Sample data
data = {
    'Name': ['Hola', 'Bonjour', 'Ciao'],
    'Description': ['Buenos días', 'Bonne journée', 'Buona giornata']
}
df = pd.DataFrame(data)

# Translate the DataFrame to English and return translated DataFrame
df = trans(df, input_lang='auto', output_lang='en')

df.to_excel("translated_file.xlsx", index=False)
```

## Parameters
- **df:** The DataFrame containing text data to translate.
- **input_lang:** (optional) The source language code. Default is 'auto' for automatic detection.
- **output_lang:** (optional) The target language code. Default is 'en' for English.


Make multilingual data processing effortless with Doctor Trans. If you find this package helpful, please refer to your developer friends! 🙂