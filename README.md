# project-olly
[![All Contributors](https://img.shields.io/badge/all_contributors-3-orange.svg?style=flat-square)](#contributors)

# Installation - without Docker
1. Clone the repository! You need the code, it won't just magically work without it.
2. Install requirements - ensure you already have python3 installed on your machine. We recommend the latest python3.7 build
```pip install -r requirements.txt``` (run that command, assuming you are in the main directory
3. Get a secret key! By default there is no secret key, so be sure to put a secret key in settings.py -
the following lines will have django create a new key for you
`from django.core.management.utils import get_random_secret_key`
`get_random_secret_key()`
4. Apply database migrations by running ```python3 manage.py migrate``` (assuming your database options are set as you'd like in settings.py)
5. If you are utilizing AWS for storage, make sure you obtain the required keys and put them in settings.py
6. If you are looking to enable CAPTCHA for logins, make sure you obtain the required keys and put them in settings.py 
as well as profiles/templates/captcha.html - and uncomment the lines in profiles.views that pertain to form verification of the captcha success
7. Be sure to set SMTP email settings in settings.py so account activation emails can be sent out to new users
8. Create a django admin/super user account - ```python manage.py createsuperuser```
9. Give your new superuser account staff panel access by modifying the database row in the `profiles_userprofile` table - set
`user_verified` to `1` and set `user_type` to `superadmin` or `admin`
9. Create a StaticInfo object, if you don't every page will throw an error telling you that it can't access the StaticInfo - easiest
way to make a staticinfo object is through the django admin at /admin

# Docker Instalation

# Configuration
You can and probably should configure things to however you'd like! As a general project we try to make things as flexible as possible
but sometimes we just can't have it do everything in the world :(

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
