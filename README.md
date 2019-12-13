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

### Author
joel.king@wwt.com GitHub / GitLab: @joelwking