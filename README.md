## Bettors.ai

This is the git for bettors.ai

#### Password storing

- For secutiry, Bettors.ai uses Vault to store credentials. Reach out to info@bettors.ai for VAULT Credentials to access dev environment.

#### Conda Instructions

```
conda create -n bettors-full python
```

Install all requirements.

```
pip install -r requirements.txt
```

bettors-full/
├─accounts
│ ├─forms
│ ├─models
│ │ └─receivers
│ └─views
│ └─send_mail
├─apps
│ ├─access_security
│ ├─chat
│ ├─inquiry
│ │ ├─models
│ │ │ └─receivers
│ │ └─views
│ └─user_properties
│ ├─models
│ └─views
├─common
│ ├─lib
│ │ ├─axes
│ │ ├─social_core
│ │ └─social_django
│ ├─scripts
│ └─views
├─config
│ ├─acsess_logic
│ ├─admin_protect
│ ├─extra_settings
│ └─security
├─media
├─static
│ ├─apps
│ └─templates
│ ├─base
│ ├─common
│ │ ├─css
│ │ ├─func
│ │ └─lib
│ ├─meta_image
│ └─pages
│ ├─apps
│ │ └─chat
│ │ └─css
│ └─home
├─templates
│ ├─accounts
│ │ ├─AccountDelete
│ │ ├─AccountLock
│ │ ├─EmailChange
│ │ │ └─mail_template
│ │ ├─LogIn
│ │ ├─PasswordChange
│ │ ├─PasswordReset
│ │ │ └─mail_template
│ │ └─SignUp
│ │ └─mail_template
│ ├─apps
│ │ ├─chat
│ │ │ └─room
│ │ │ └─include
│ │ ├─inquiry
│ │ │ └─inquiry_form
│ │ │ └─notice_admin_mail_template
│ │ └─user_properties
│ │ ├─asset
│ │ └─Settings
│ ├─common
│ │ ├─asset
│ │ └─debug
│ └─pages
│ ├─general
│ └─home
└─templatetags

```

```
