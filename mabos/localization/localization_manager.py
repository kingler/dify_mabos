# mabos/localization/localization_manager.py
class LocalizationManager:
    def __init__(self, translations):
        self.translations = translations
        # Initialize other attributes and components
        self.default_language = 'en'  # Set the default language
        self.supported_languages = list(translations.keys())  # Get the list of supported languages
        self.date_formatters = {}  # Dictionary to store date formatters for each language
        self.number_formatters = {}  # Dictionary to store number formatters for each language
        self.user_language_preferences = {}  # Dictionary to store user language preferences

    def get_translation(self, key, language):
        # Retrieve the translation for a specific key in a given language
        if language in self.translations and key in self.translations[language]:
            return self.translations[language][key]
        elif self.default_language in self.translations and key in self.translations[self.default_language]:
            return self.translations[self.default_language][key]
        else:
            return key  # Return the key as fallback if no translation is found

    def set_user_language(self, user, language):
        # Set the preferred language for a user
        if language in self.supported_languages:
            self.user_language_preferences[user] = language
        else:
            raise ValueError(f"Unsupported language: {language}")

    def format_date(self, date, language):
        # Format a date according to the specified language
        if language not in self.date_formatters:
            # Create a new date formatter for the language if it doesn't exist
            self.date_formatters[language] = self._create_date_formatter(language)
        
        # Use the date formatter for the specified language to format the date
        formatted_date = self.date_formatters[language].format(date)
        
        return formatted_date

    def format_number(self, number, language):
        # Format a number according to the specified language
        if language not in self.number_formatters:
            # Create a new number formatter for the language if it doesn't exist
            self.number_formatters[language] = self._create_number_formatter(language)
        
        # Use the number formatter for the specified language to format the number
        formatted_number = self.number_formatters[language].format(number)
        
        return formatted_number
