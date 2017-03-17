# hugo-go webserver

A very simple Go webserver.  Works great with Hugo sites.  http://test.billyc.io was deployed using it.

For example, to deploy a Hugo generated blog:


- Run the `hugo` command:

```
cd /path/to/hugo
./hugo
```
- Symlink whatever you're trying to deploy to `./public` (from this directory):

```
ln -s /path/to/hugo/public public
```

- Test the site (you will need the GCloud SDK):

```
dev_appserver.py --port=9999 app.yaml
```

- If everything looks good, deploy! You'll need to configure your Google Cloud account and GCloud SDK first though...:

```
gcloud app deploy --quiet
``
