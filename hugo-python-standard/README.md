# hugo-python-standard

A Hugo Google App Engine webserver, with the added twist of posting Google Analytics stats from the server side.

# Installation

- Install the Python requirements:

```
virtualenv env
source env/bin/activate
pip install -t lib -r requirements.txt
```

- Edit the `app.yaml` file and configure the Google Analytics tracker and the site name:

```
env_variables:
    GA_TRACKING_ID: TRACKING-ID-NUMBER
    SITE_HOSTNAME: example.org
```

- This particular Google App Engine Standard is designed for use with a static site generator, specifically Hugo.  It will need a symlink to your static directory:

```
ln -s /path/to/your/hugo/public static
```

# To Test Locally

- Run the dev server:

```
dev_appserver.py --port=9999 app.yaml
```

- Connect to http://localhost:9999.  You may get prompted about allowing inbound connections. Test and develop accordingly.
- Once tested, to deploy:

```
gcloud app deploy --quiet
```
