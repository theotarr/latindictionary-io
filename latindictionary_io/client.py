import requests
from latindictionary_io.exceptions import APIException, RequestException

class Client:
    API_URL = 'https://www.latindictionary.io/api/v1/'
    
    def request(self, method, endpoint, params=None):
        url = self.API_URL + endpoint
        try:
            response = requests.request(method, url, params=params)
        except requests.exceptions.RequestException as e:
            raise RequestException(e)
        if response.status_code != 200:
            raise APIException(response.status_code, response.text)
        return response.json()
    
    def analyze_word(self, word):
        """Parses the forms and english definitions of a Latin word.

        Args:
            word (str): a Latin word.

        Returns:
            json: json response from the API.
        """
        return self.request('GET', 'analyze/' + word)
    
    def get_concordance(self, word):
        """Get examples of the word in anchient latin texts.

        Args:
            word (str): a Latin word.

        Returns:
            json: json response from the API.
        """
        return self.request('GET', 'concordance/' + word)
    
    def get_definition(self, word):
        """Get the english definition of a Latin word.
        
        Args:
            word (str): a Latin word.
        
        Returns:
            json: json response from the API.
        """
        return self.request('GET', 'definition/' + word)
    
    def get_word_of_the_day(self, date=None):
        """Get the word of the day.
        
        Args:
            date (str): date in the format YYYY-MM-DD.
        
        Returns:
            json: json response from the API with the Word of the Day from the specified date.
        """
        # return self.request('GET', 'wordoftheday/')
