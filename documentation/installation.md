Installation Instructions
-------------------------
First create a copy of this repository on your local system.

```shell
git clone https://github.com/joelwking/prezo.git
cd prezo
```

Then build the Docker image and verify.

```shell
docker build -f ./Dockerfile -t joelwking/prezo:1.0 .
docker images joelwking/prezo
```

Input Files
-----------
Identify the files you wish to upload. You can specify either a directory, or an input file.

The easy method is to copy all your Powerpoint files to a directory (`cp -p ` will preserve the timestamp) and then specify the directory name using the environment variable `PZ_PPTX_FILES`. Any file ending with '.pptx' are uploaded.

There is a sample Bash script `copy_files.sh` to assist in locating all the presentation files on your hard drive and copy them to a USB drive.

Dot Underscore Files
--------------------
If you specify a directory rather than input file, the [Dot Underscore](
https://apple.stackexchange.com/questions/14980/why-are-dot-underscore-files-created-and-how-can-i-avoid-them) files (files beginning with a `._`) should be ignored or removed from the source directory. If you have copied your presentation files to a USB drive, you can remove these files either manually or by using the following command:

```shell
/Volumes/KINGSTON/data % find . -type f -name '._*' -delete
```

If you do not remove these files, they will be uploaded, but the metadata for the RAKE keywords will contain the string `error extracting text`.

Alternately, you can create an input file to inventory the presentations you wish to upload. In `NOTES_TIPS.md` there is an explaination on how to create the input file. Because we are running in a container, the best approach is to copy all the presentation to a directory, and mount that directory to the container. 

Run the Image
-------------
Run the image, mapping the directory to the container.

```shell
docker run --volume /home/administrator/prezo/data:/opt/powerpoint:ro -it joelwking/prezo:1.0  /bin/bash

```
> Note: to exit the container, leaving the container running, detach from the running container, use ^P^Q (hold Ctrl , press P , press Q , release Ctrl ).

You will be attached to the container, in the work directory of `/prezo`. Your Powerpoint files are at `/opt/powerpoint`.

Loading presentation to an object store
---------------------------------------
Loading the presentation files to an object store requires specifiying several environment variables for authentication, logging and setting options for program execution.

Environment Variables
---------------------
We use a number of environment variables to specify credentials and other configuration options.

These can be specified on the `docker run` command by using `--env-file .env/run.env`

Upload
------
To upload files, program `upload.py` uses these environment variables to learn the bucket name, secret and access key, and the directory or filename of the input file.

Create the Target Bucket
------------------------
When using AWS S3 buckets, navigate to the IAM menu, create (or select a user) which has the policy of `AmazonS3FullAccess` and under the `security credentials` tab. The access keys allow you to use the AWS CLI, and these programs using the MinIO SDK. You can have a maximum of two access keys (active or inactive) at a time.

You can create the bucket either by using the AWS console (GUI) or the AWS CLI. Enable `Block all public access` to the bucket. You can enable `Bucket Versioning` to maintain multiple copies of objects with the same name.

Specify the bucket name and secret and access key values.

```shell
export PZ_BUCKET="bucket_name"
export PZ_ACCESS_KEY="your_access_key"
export PZ_SECRET_KEY="your_secret_key"
```

Specify either the name of an input file or the directory where your files are located.

```shell
export PZ_PPTX_FILES="/opt/powerpoint/upload.file"
```

```shell
export PZ_PPTX_FILES="/opt/powerpoint/
```

Logging
-------
To create a log output file, create the directory path and specify the name of a log file using the environment variable.

```shell
export PZ_LOG_FILE="/prezo/log/prezo.log"
```

By default the program logs at the INFO (20) level, to modify the level, specify an integer value corresponding to the desired level.

>Note: DEBUG=10 INFO=20 WARNING=30 ERROR=40 CRITICAL=50

For example:
```shell
export PZ_DEBUG=10
```
The output will be logged in the following format with the date, time and the log message:

```log
2021-08-25 20:13:41,714 - upload - ERROR - MAIN: [Errno 2] No such file or directory:'E-SERIES_VMS_Validation_Program_Verint.pptx' E-SERIES_VMS_Validation_Program_Verint.pptx
2021-08-25 20:13:41,715 - upload - ERROR - MAIN: [Errno 2] No such file or directory: 'E-SERIES_VMS_Validation_Program_Milestone.pptx' E-SERIES_VMS_Validation_Program_Milestone.pptx
2021-08-25 20:13:41,716 - upload - ERROR - MAIN: [Errno 2] No such file or directory: 'E-SERIES_VMS_Validation_Program.pptx' E-SERIES_VMS_Validation_Program.pptx
2021-08-25 20:15:59,592 - upload - ERROR - MAIN: [Errno 2] No such file or directory: '/opt/powerpoing/E-SERIES_VMS_Validation_Program_Verint.pptx' /opt/powerpoing/E-SERIES_VMS_Validation_Program_Verint.pptx
2021-08-25 20:16:02,413 - upload - INFO - MAIN: etag:0d49761777d4574572ddb4d90691ab5e filepath:/opt/powerpoint/E-SERIES_VMS_Validation_Program_Milestone.pptx
2021-08-25 20:16:04,734 - upload - INFO - MAIN: etag:884d42c8454df56bba9a5a2c4f29dc08 filepath:/opt/powerpoint/E-SERIES_VMS_Validation_Program.pptx

```

Tags
----
Each object may have up to 10 associate *tags*, or key, value pairs for grouping objects with the same tag and value. The tag key can be up to 128 bytes, the value up to 256 bytes. To associate *tags* with the uploaded presentations, create a JSON file of key, value pairs and specify the name of the file in the environment variable `PZ_TAGs`.

```shell
export PZ_TAGS='data/tags.json'
```
All uploaded file(s) will contain the specified tags. To apply specify tags to a subset of your files, segregate the files in separate directories and create a `tags.json` file for each directory. Execute the upload for each directory.

Upload files
------------
Execute the `upload.py` program to extract keywords and upload the files.

```shell
cd /prezo
python3 library/upload.py
```

>Note: If you configured the filename of a log file you can view it: `cat /prezo/log/prezo.log`

Query Files
-----------
To query files, program `query.py` uses the environment variables above, sans `PZ_PPTX_FILES`.

You can use the `-h` switch to display the command line arguments.
```
usage: query.py [-h] [-u] [-s SEARCH_STRING]

Query metadata of object store

optional arguments:
  -h, --help        show this help message and exit
  -u                display download URL
  -s SEARCH_STRING  search string (use lowercase)
```

If you wish to search on presentations which contain the keywords `meetup king', run a query as shown:

```shell
python library/query.py -u -s 'meetup king'
```
The results of the query is a YAML formatted list of presentations.

```yaml
- credibility: 4.4
  etag: 6f6027223eeedfb34b294af9a79ea604-4
  last_modified: '2021-08-19T18:26:21+00:00'
  metadata:
  - King, Joel
  - Meetup Overview
  - King, Joel
  - Meetup_Overview.pptx
  object_name: Meetup_Overview.pptx
  url: '... specify the -u argument for a download URL'
```

Author
------
Joel W. King  @joelwking