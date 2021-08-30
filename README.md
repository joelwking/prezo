# prezo

*prezo* - Presentation Management

The goal of this project is to enable sharing of PowerPoint presentations while using metadata to locate relevant content.

I began working on this solution to address my frustration with a lack of a suitable content management system enabling the sharing of presentations and their associated artifacts. [vbrick](https://vbrick.com/) enables a video content management system, which includes storing the associated presentation files, tagging for internal versus external access and analytics.

For published webinars, this is an excellent solution, however, what I need is the ability to share presentation material prior to, and subsequent to the event.

Additional motivations include:

 * developing a better understanding of object storage,
 * understanding of the challenges of programatically extracting text from PowerPoint files,
 * enable intelligent string matching to return relevant results.

What isn't addressed:

 * advice or training on how to create and deliver compelling presentations,
 * developing an enterprise-wide offering [2](README.md#references).

With this aside, let's look at the solution components.

### Theme

I have worked for many years as a Technical Marketing Engineer at several technology companies and more recently, as the organizer for a Meetup group focused on enabling programmability, automation, and Infrastructure as Code to develop NetDevOps skills.

These roles require a technical knowledge the solution components, marketing acumen and communication skills.

Powerpoint is commonly used to foster communication in face-to-face customer meetings, in webinars and video conference meetings. 

Presentations are strategic communications. [1 - Ontra, 2018, p. 24](README.md#references) Unfortunately, outside of a corporate overview deck, most are relegated to the hard drive of the author or scattered across collaboration app (MS Teams, Webex Teams, Slack) channels.

Object storage is popular for used for storing photos, audio files (MP3) and services like DropBox / Box, are used for storing massive amounts of unstructured data. Object storage associates the object with a globally unique ID and the inclusion of metadata and tags to enable searching for object sharing similar characteristics.

Powerpoint files are primarily [3 - unstructured data](README.md#references). These files contain text and images, and also meta-data fields in the Summary / Properties. The meta-data files are typically ignored by most authors, but can be used to document the Title, Subject, Author, Company, Category and Keywords. Applying discipline to update the metadata is recommended.

In this project, we look at using the MinIO Python SDK to upload, search and retrieve objects stored in Amazon S3 (Amazon Simple Storage Service) the object storage service of AWS. This session demonstrates how the open source Python library *python-pptx* and *RAKE* (Rapid Automatic Keyword Extraction) are used to extract and analyze keywords from PowerPoint files providing meta data to these objects stored in S3.

### Components
This solution includes the following tools.

#### Minio
Minio is an open source object storage system which provides a consistent view of data regardless of where it resides in Google, Microsoft or Amazon's cloud, in your private cloud or in a co-location service. Data that resides in AWS today may be in a co-location tomorrow, and in your private data center. The Minio Python SDK is used to upload PowerPoint presentations from a laptop to an Amazon S3 bucket

#### python-pptx
The Python library *python-pptx* is used to extract the text and tags from each PowerPoint presentation.

#### Rapid Automatic Keyword Extraction algorithm
The Python library *rake-nltk* (Rapid Automatic Keyword Extraction algorithm) is used to determine key phrases and loading them as metadata to the object.

#### FuzzyWuzzy
After the objects are loaded in their target bucket(s), we use the MinIO Python SDK to query the metadata of all the objects and use the FuzzyWuzzy Python library for string matching.

### Installation
Installation instructions can be found in `documentation/installation.md`.

### References

[1] AlexAnndra Ontra, James Ontra (2018) [Presentation Management: The New Strategy for Enterprise Content (First release)](https://www.amazon.com/Presentation-Management-Strategy-Enterprise-Content-ebook/dp/B07MMV7MJ2)

[2] [Shufflr](https://shufflrr.com) is a commercial slide library software offering, enabling composing new PowerPoint presentations from existing PowerPoint and other visual content. 

[3][Unstructured Data](https://searchbusinessanalytics.techtarget.com/definition/unstructured-data)

### Author
Joel W. King @joelwking