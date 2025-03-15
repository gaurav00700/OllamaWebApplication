import os, sys
sys.path.append(os.path.abspath(os.path.join(__file__, '../..')))

from streamlit.testing.v1 import AppTest
at = AppTest.from_file("frontend/app.py")

# TODO: Add more tests to cover the frontend logic
# at.run()
# at.text_input["Enter your prompt:"] = "Hello World!"
# assert not at.exception