Project Olly Changelog

# 1.0.0 - YES WE'VE MADE IT
Started in August of 2017, after much delays of life and school 
we're happy to call this a release build of project-olly. Thank you to al our contributors 
that have made this goal possible! The support in all shapes and forms don't go unnoticed!

Please note the substantial and large
changes made in this update may affect compatibility with previous versions databases 
- Add SteamID64 and Discord profile fields
- Add basic stats models (will be built upon further in later updates)
- Added notification system for users
- Rework team invites and team roles entirely (from the backend)
- Fix multiple team list templates to work with new standards
- Improve staff panel teams templates
- Remove some hard coded links
- Add free agents to Leagues
- Allow staff to disable free agent registration for leagues within LeagueSettings
- Implement point system for LeagueMatches
- Basic team checkin process ahead of matches
- Multiple other staff panel league improvements
- Front end league template improvements (standings, and more)
- Complete rework of tournament brackets - no more size restrictions, much more efficient brackets!
- Switched to jenkins for project builds, no more travisci
- Implement map random picking for tournaments and league matches
- Shift to single template tournament brackets
- General code cleanup and improvement  
- DoubleElimination tournaments soon!

# 0.9.0
- Implement leagues functionality

# 0.8.1
- News articles publish date now auto fills with last saved date when editing
- Fix news post fields (fixes a possible 500 error when editing). closes #54
- Fix S3 ACL warnings
- Fix static file 404 warning
- Fix template path from old multi tenant design
- Delete user gear model
- Rename support templates to line up with app name
- Allow pages to load if a SocialInfo object doesn't exist
- Disable S3 querystring auth since B2 doesn't support it (and buckets should be public anyways)
- Add Activision ID to UserProfile, closes #73
- [New feature] FAQ
- [New feature] Front page slides are now object based

# 0.8.0
- Reimplemented ESPORTS_MODE
- Fix CI Tests
- Additional CI Changes
- Fix SocialInfo not working as a context processor
- Add Object Based FAQ questions. Create a FAQ section within the staff panel and answer those common questions!
- Fix not being able to create tournaments within the staff panel
- Adjusted store product deletion, making it easier to delete products.
- Add object based slides, allows for a smoother more dynamic content generation on the front end, while keeping the back-end clean. 
- Fix tournament bracket and tournament detail styling
- Fix issue where tournament ruleset page would not load
- Implement team flags into the bracket template
- Add manage rulesets button on staff nav bar
- Object based map list improvements in staff panel.
- Staff base panel style modifications