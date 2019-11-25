# Project Olly
[![All Contributors](https://img.shields.io/badge/all_contributors-3-orange.svg?style=flat-square)](#contributors)
<a href="https://discord.gg/5dp8x2t">
    <img src="https://img.shields.io/badge/discord-join-7289DA.svg?logo=discord&longCache=true&style=flat" />
</a>

## Please note: this document is currently under construction and is not yet complete.

# About the project
Project Olly is an online esports tournament hosting platform written in Python 3 using the Django web framework. It began as a closed source commercial product until November 2019 when it was re-released under the MPL2.0 license (see license.md)

# Configuration
In `olly/settings.py` fill in the following fields:
- `SECRET_KEY` - This value is used for django's cryptographic signing functions. You can easily generate this by running `from django.core.management.utils import get_random_secret_key` followed by `get_random_secret_key()` in a django shell (`python manage.py shell`)
- `ALLOWED_HOSTS` -  It is strongly recommended to set this to the domain name of your site to prevent HTTP host header attacks
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_S3_ENDPOINT_URL` - Authentication information for AWS S3 compatable object storage. Note: this is not required, however we do not currently have documentation on how to setup with local storage
- `AWS_STORAGE_BUCKET_NAME` - This is simply the name you wish to use for your S3 compatable bucket
- `EMAIL_HOST` - The hostname of your email server (for example `smtp.gmail.com`)
- `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` - the login information for your email account
- `FROM_EMAIL` - The name and email address that will be shown in the "From" field in emails
- `GOOGLE_RECAPTCHA_SECRET_KEY` and `GOOGLE_RECAPTCHA_SITE_KEY` - Authentication information for Google reCAPTCHA
- `DEBUG` and `PAYPAL_TEST` - Set to False
- `DATABASES` section - It is highly recommended to use postgresql rather than sqlite for deployment as it has much higher performance. Replace the existing DATABASES section with the one below and edit the information as instructed in the comments
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase', # The name of the database (must exist)
        'USER': 'mydatabaseuser', # The username you wish to use to connect to the database
        'PASSWORD': 'mypassword', # The password of the user
        'HOST': '127.0.0.1', # The IP address of the database server. If it is the same server, this can be left as is
        'PORT': '5432', # The port the database server is running on. It is unlikely you will need to change this
    }
}
```

# Installation - without Docker
#### Not officially supported. It is possible, but we aren't able to assist with the installation if you choose to do so.

1. Clone the repository! You need the code, it won't just magically work without it.
2. Install requirements - `pip install -r requirements.txt`
3. Configure settings.py
4. Apply database migrations by running `python3 manage.py migrate` (assuming your database options are set as you'd like in settings.py)
5. Create a django admin/super user account - `python manage.py createsuperuser` and follow the prompts
6. Give your new superuser account staff panel access by modifying the database row in the `profiles_userprofile` table - set
`user_verified` to `1` and set `user_type` to `superadmin` or `admin` (hint: you can use django admin at /admin)
7. Create a StaticInfo object, if you don't every page will throw an error telling you that it can't access the StaticInfo - easiest
way to make a staticinfo object is through the django admin at /admin
8. Setup a web server and reverse proxy using industry standard best practices (hint: gunicorn and nginx work well)

# Docker Instalation

1. Clone the repository! You need the code, it won't just magically work without it. (Seems to be a recurring theme)
2. Create the folder for static files by running `sudo mkdir /var/www/static` and transfer ownership by running `sudo chown www-data:www-data /var/www/static`. Feel free to substitute the username, but your reverse proxy must be running as that user
3. Run `docker build .` (take note of the image id) followed by `docker run -d -v /var/www/static:/static -v /tmp:/sock --net=host -u www-data --name project-olly [your image id]`
4. Setup a reverse proxy of your choice (we highly recommend nginx, and have setup instructions	available in [nginx_setup.md](nginx_setup.md))
5. A user was automatically created with the username `admin` and the password `ChangeMe!` **DON'T FORGET TO CHANGE THE PASSWORD!**
6. How easy was that!?

# Designs and Template
Project Olly allows you to throw in your front end templates without having to mess with any backend code! It's simple!
1. Create a Header & Footer template in pages/templates/sitename (if neccessary)
2. Create a base.html in pages/templates - make sure to include the header and footer template that you just made

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore -->
<table>
  <tr>
    <td align="center"><a href="http://mikemadden.me"><img src="https://avatars0.githubusercontent.com/u/19417674?v=4" width="100px;" alt="Mike M."/><br /><sub><b>Mike M.</b></sub></a><br /><a href="https://github.com/mikemaddem/project-olly/commits?author=mikemaddem" title="Tests">⚠️</a> <a href="https://github.com/mikemaddem/project-olly/commits?author=mikemaddem" title="Code">💻</a> <a href="https://github.com/mikemaddem/project-olly/commits?author=mikemaddem" title="Documentation">📖</a> <a href="#ideas-mikemaddem" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://github.com/techlover1"><img src="https://avatars1.githubusercontent.com/u/17421974?v=4" width="100px;" alt="Steven Young"/><br /><sub><b>Steven Young</b></sub></a><br /><a href="#infra-techlover1" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/mikemaddem/project-olly/commits?author=techlover1" title="Code">💻</a> <a href="#ideas-techlover1" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/mikemaddem/project-olly/commits?author=techlover1" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/mulveyben1"><img src="https://avatars1.githubusercontent.com/u/22732775?v=4" width="100px;" alt="mulveyben1"/><br /><sub><b>mulveyben1</b></sub></a><br /><a href="https://github.com/mikemaddem/project-olly/commits?author=mulveyben1" title="Code">💻</a></td>
  </tr>
</table>

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
