# prezo
Presentation Management

### Theme
Don't be left 'on-prem'. [https://www.linkedin.com/pulse/im-interested-networking-anymore-joel-w-king/](https://www.linkedin.com/pulse/im-interested-networking-anymore-joel-w-king/)

The goal of this project is to enable sharing of PowerPoint presentations while using metadata to locate relevant content.

### Components
Some of the tools used in this solution include the following.

#### Minio
Minio is an open source object storage system which provides a consistent view of data regardless of where it resides in Google, Microsoft or Amazon's cloud, in your private cloud or in a co-location service. Data that resides in AWS today may be in a co-location tomorrow, and in your private data center. The Minio Python SDK is used to upload PowerPoint presentations from a laptop to an Amazon S3 bucket

#### python-pptx
The Python library *python-pptx* is used to extract the text and tags from each PowerPoint presentation.

#### Rapid Automatic Keyword Extraction algorithm
The Python library *rake-nltk* (Rapid Automatic Keyword Extraction algorithm) to determine key phrases and loading them as metadata to the object.

#### FuzzyWuzzy
After the objects are loaded in their target bucket(s), we use the MinIO Python SDK to query the metadata of all the objects and use the FuzzyWuzzy Python library for string matching.

### Installation

TODO

### Loading presentation to an object store

TODO

### Environment Variables

#### Upload

To upload files, program `upload.py` uses these environment variables to learn the bucket name, secret and access key, and the filename of the input file.

When using AWS S3 buckets, navigate to the IAM menu, create (or select a user) which has the policy of `AmazonS3FullAccess` and under the `security credentials` tab. The access keys allow you to use the AWS CLI, and these programs using the MinIO SDK. You can have a maximum of two access keys (active or inactive) at a time.

You can create the bucket either by using the AWS console (GUI) or the AWS CLI. Enable `Block all public access` to the bucket. You can enable `Bucket Versioning` to maintain multiple copies of objects with the same name.

```shell
export PZ_BUCKET="bucket_name"
export PZ_ACCESS_KEY="your_access_key"
export PZ_SECRET_KEY="your_secret_key"
export PZ_PPTX_FILES="file_name_of_input_file"
```

#### Query

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

#### Logging level

By default the program logs at the INFO (20) level, to modify the level, specify an integer value corresponding to the desired level.

>Note: DEBUG=10 INFO=20 WARNING=30 ERROR=40 CRITICAL=50

For example:
```shell
export PZ_DEBUG=10
```
The output will be logged in the following format with the date, time and the log message:

```log
2021-08-19 21:11:47,824 - query - INFO - RESULTS:
```

### References
[Presentation Management, the New Strategy for Content Management - Chapter 1](https://www.linkedin.com/pulse/presentation-management-new-strategy-content-chapter-james-ontra/)

[Presentation Management: The New Strategy for Enterprise Content (First release)](https://www.amazon.com/Presentation-Management-Strategy-Enterprise-Content-ebook/dp/B07MMV7MJ2)

### Author
Joel W. King @joelwking