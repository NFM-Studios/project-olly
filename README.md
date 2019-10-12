# project-olly

# Installation
1. Clone the repository! You need the code, it won't just magically work without it.
2. Install requirements - ensure you already have python3 installed on your machine. We recommend the latest python3.7 build
```pip install -r requirements.txt``` (run that command, assuming you are in the main directory
3. Get a secret key! By default there is no secret key, so be sure to put a secret key in settings.py -
the following lines will have django create a new key for you
`from django.core.management.utils import get_random_secret_key`
`get_random_secret_key()`
4. Apply database migrations by running ```python3 manage.py migrate``` (assuming your database options are set as you'd like in settings.py)

# Configuration
You can and probably should configure things to however you'd like! As a general project we try to make things as flexible as possible
but sometimes we just can't have it do everything in the world :(

# Designs and Template
Project Olly allows you to throw in your front end templates without having to mess with any backend code! It's simple!
1. Create a Header & Footer template in pages/templates/sitename (if neccessary)
2. Create a base.html in pages/templates - make sure to include the header and footer template that you just made
