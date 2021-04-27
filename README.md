# Project Olly
[![Build Status](https://jenkins.nightfury.pw/buildStatus/icon?job=Project-Olly-Multibranch%2Fmaster)](https://jenkins.nightfury.pw/job/Project-Olly-Multibranch/job/master/)
[![All Contributors](https://img.shields.io/badge/all_contributors-3-orange.svg?style=flat-square)](#contributors)
<a href="https://discord.gg/5dp8x2t">
    <img src="https://img.shields.io/badge/discord-join-7289DA.svg?logo=discord&longCache=true&style=flat" />
</a>

# About the project
Project Olly is an online esports tournament hosting platform written in Python 3 using the Django web framework. It began as a closed source commercial product until November 2019 when it was re-released under the MPL2.0 license (see license.md)

# Roadmap

- Single Eliminations Tournaments (Live - improvements coming soon)
- Leagues (Live - improvements coming soon)
- UserProfiles (completed)
- Support Tickets (completed)
- News Posts (completed)
- Match System (Live - improvements coming soon)
- Team system - team invites, captains (completed - improvements coming soon)
- PayPal Store for processing some payments (completed)
- Double Elimination Tournaments (planned)
- Ladders (planned)

# Installation

1. Clone the repository! You need the code, it won't just magically work without it. `git clone https://github.com/NFM-Studios/project-olly.git`
2. Install docker and docker-compose. Follow the instructions [here](https://docs.docker.com/install/linux/docker-ce/ubuntu/) and [here](https://docs.docker.com/compose/install/)
3. Copy `.env.example` to `.env` and edit using the guidance in the file
4. Copy `Caddyfile.example` to `Caddyfile` and change `example.com` to your domain and `email.example.com` to your email address
5. Run `docker-compose up -d`
6. A user was automatically created with the username `admin` and the password `ChangeMe!` **DON'T FORGET TO CHANGE THE PASSWORD!**
7. How easy was that!?

# Designs and Template
Project Olly allows you to throw in your front end templates without having to mess with any backend code! It's simple!

Use our templates in project-templates as a base, then set `template_path` in `.env` to wherever you stored your custom templates

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/mulveyben1"><img src="https://avatars1.githubusercontent.com/u/22732775?v=4?s=100" width="100px;" alt=""/><br /><sub><b>mulveyben1</b></sub></a><br /><a href="https://github.com/NFM-Studios/project-olly/commits?author=mulveyben1" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/tkenney124"><img src="https://avatars.githubusercontent.com/u/29129110?v=4?s=100" width="100px;" alt=""/><br /><sub><b>tkenney124</b></sub></a><br /><a href="https://github.com/NFM-Studios/project-olly/commits?author=tkenney124" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
