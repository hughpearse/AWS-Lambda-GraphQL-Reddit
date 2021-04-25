
```bash
foo@bar$ pipenv --rm
foo@bar$ pipenv install --three
foo@bar$ pipenv shell
```

You can test the lambda code:

```bash
foo@bar$ lambda init # dev purposes only
foo@bar$ lambda invoke
```

Or you can run the web server

```
foo@bar$ export FLASK_APP=service.py
foo@bar$ flask run
```


