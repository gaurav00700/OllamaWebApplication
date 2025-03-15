import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__, '../..')))
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_homepage():
    """Test the homepage of backend API endpoint."""

    response = client.get('/') # Send a GET request to the homepage endpoint
    response_data = response.json() # Convert the response to JSON format

    assert response.status_code == 200, "The API did not return a successful status code."
    assert 'name' and 'description' in response_data, "The response data is missing expected fields."
    
# if __name__ == '__main__':
#     test_homepage()