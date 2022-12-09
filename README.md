mocap structure
==============================
We are looking for anyone who feels as passionate about using tech for good. Fork it or reach out to us to join our team.

Confluence Home: https://humangestures.atlassian.net/wiki/spaces/MOC/overview
Discord?
Slack: https://join.slack.com/share/enQtNDQ5MDI1NDIwNDI0NS0xN2VhNWYyNWMxZWI4YTRlZjBmOWNiOTZjMzdkY2Y4MGY4YjZjZjczZGY2MWVjMWEyYjJiZmI5MmI5NWI5Njcx

Project Organization
------------

    ├── LICENSE
    ├── .pylintrc          <- Python style guidance
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── env                <- CI configuration
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │   └── streaming      <- Streaming collected from our WatchOS app
    │
    ├── docs               <- Empty for now
    │
    ├── models             <- Models are still in Notebooks to be productionized. We tries restnet, timedistributed 1dconv
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    |                         Due to the merge issues we have included notebooks in the ignore list use -f to push
    │
    ├── references         <- Placeholder for the whitepapers etc.
    │
    ├── reports            <- Empty
    │   └── figures        <- Empty
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── mocap              <- Source code for use in this project.
    │   ├── __init__.py    <- Makes mocap a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │    
    │   ├── utils          <- Allows to easily change config settings for a personalized env
    │   │   └── params.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Empty
    │       └── visualize.py
    ├── 



--------

