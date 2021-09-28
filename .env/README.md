README
------

This is the format of the `.env/debug.env` file specified in the `.vscode/launch.json` debug configuration:

```
PZ_ACCESS_KEY=AKXXXXXXXC4PLERT
PZ_SECRET_KEY="2WOz2345678hnowi0EWSS"
PZ_BUCKET= "foobar"
```
The file `run.env` is a sample input environment variable file for use when initiating the code with a stand-along container. Use the argument `--env-file .env/run.env` to specify the file.