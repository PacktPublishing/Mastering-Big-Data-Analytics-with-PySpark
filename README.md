## $5 Tech Unlocked 2021!
[Buy and download this Video for only $5 on PacktPub.com](https://www.packtpub.com/product/mastering-big-data-analytics-with-pyspark-video/9781838640583)
-----
*The $5 campaign         runs from __December 15th 2020__ to __January 13th 2021.__*

# Mastering Big Data Analytics with PySpark [Video]
This is the code repository for [Mastering Big Data Analytics with PySpark [Video]]( https://www.packtpub.com/data/mastering-big-data-analytics-with-pyspark-video), published by [Packt](https://www.packtpub.com/?utm_source=github ). It contains all the supporting project files necessary to work through the video course from start to finish.<br/>
Authored by: [Danny Meijer](https://www.linkedin.com/in/dannydatascientist)

## About the Video Course
PySpark helps you perform data analysis at-scale; it enables you to build more scalable analyses and pipelines. This course starts by introducing you to PySpark's potential for performing effective analyses of large datasets. You'll learn how to interact with Spark from Python and connect Jupyter to Spark to provide rich data visualizations. After that, you'll delve into various Spark components and its architecture.

You'll learn to work with Apache Spark and perform ML tasks more smoothly than before. Gathering and querying data using Spark SQL, to overcome challenges involved in reading it. You'll use the DataFrame API to operate with Spark MLlib and learn about the Pipeline API. Finally, we provide tips and tricks for deploying your code and performance tuning.

By the end of this course, you will not only be able to perform efficient data analytics but will have also learned to use PySpark to easily analyze large datasets at-scale in your organization. <br/>

<H2>What You Will Learn</H2>
<DIV class>

<UL>
• Gain a solid knowledge of vital Data Analytics concepts via practical use cases<br/>
• Create elegant data visualizations using Jupyter<br/>
• Run, process, and analyze large chunks of datasets using PySpark<br/>
• Utilize Spark SQL to easily load big data into DataFrames<br/>
• Create fast and scalable Machine Learning applications using MLlib with Spark<br/>
• Perform exploratory Data Analysis in a scalable way<br/>
• Achieve scalable, high-throughput and fault-tolerant processing of data streams using Spark Streaming<br/>
</LI></UL></DIV>

## Instructions and Navigation
### Assumed Knowledge
This course will greatly appeal to data science enthusiasts, data scientists, or anyone who is familiar with Machine Learning concepts and wants to scale out his/her work to work with big data.

If you find it difficult to analyze large datasets that keep growing, then this course is the perfect guide for you!

A working knowledge of Python assumed.

## Technical Requirements <br/>
#### Minimum Hardware Requirements
For successful completion of this course, students will require the computer systems with at least the following:

OS: Windows, Mac, or Linux<br/>
Processor: Any processor from the last few years<br/>
Memory: 2GB RAM<br/>
Storage: 300MB for the Integrated Development Environment (IDE) and 1GB for cache<br/>

#### Recommended Hardware Requirements <br/>
For an optimal experience with hands-on labs and other practical activities, we recommend the following configuration:

OS: Windows, Mac, or Linux<br/>
Processor: Core i5 or better (or AMD equivalent)<br/>
Memory: 8GB RAM or better<br/>
Storage:  2GB free for build caches and dependencies<br/>

#### Software Requirements<br/>

Operating system: Windows, Mac, or Linux<br/>

Docker<br/>

## Follow the instructions below to download the data belonging to the course as well as
 setting up your interactive development environment.

### Downloading Data for this Course

Once you have cloned this repository locally, simply navigate to the folder you have
 stored the repo in and run:
```python download_data.py```

This will populate the `data-sets` folder in your repo with a number of data sets that
 will be used throughout the course.

### Docker Image Bundled with the Course

### About

The Docker Image bundled with this course (see `Dockerfile`) is based on the
`pyspark-notebook`, distributed and maintained by Jupyter
> [Github link](https://github.com/jupyter/docker-stacks/blob/master/pyspark-notebook/Dockerfile)
> Original copyright (c) Jupyter Development Team. Distributed under the terms of the
Modified BSD License.

This Course's Docker image extends the `pyspark-notebook` with the following additions:
- enables Jupyter Lab by default
- exposes correct ports for JupyterLab and SparkUI
- sets numerous default settings to improve Quality of Life for the user
- installs numerous add-ons (such as `pyspark-stubs` and `blackcellmagic`) using
  `jupyter_contrib_nbextensions`

### Instructions for use

There are 2 ways to access the Docker container in this course:
1. Through the bundled `run_me.py` script (recommended to use)
2. Through the Docker CLI (only for advanced users)

#### Using the bundled script to run the container

The easiest way to run the container that belongs to this course is by running
 ```python run_me.py``` from the course's repository. This will automatically
 build the Docker image, set up the Docker container, download the data, and set up the
 necessary volume mounts.

#### Using Docker CLI

If you rather start the Docker container manually, use the following instructions:

1. __Downlad the data__
    ```bash
    python download_data.py
    ```

2. __Build the image__
    ```bash
    docker build --rm -f "Dockerfile" -t mastering_pyspark_ml:latest .
    ```

3. __Run the image__
Ensure that you replace `/path/to/mastering_pyspark_ml/repo/` in the following command, and run it in a terminal or command prompt:
    ```bash
    docker run  -v /path/to/mastering_pyspark_ml/repo/:/home/jovyan/ --rm -d -p 8888:8888 -p 4040:4040 --name mastering_pyspark_ml mastering_pyspark_ml .
    ```

4. __Open Jupyter lab once Docker image is running__
Navigate to [http://localhost:8888/lab](http://localhost:8888/lab?token=masteringpysparkml)

#### To Stop the Docker Image
Once you are ready to shutdown the Docker container, you can use the following command:
```bash
docker stop mastering_pyspark_ml
```

## Related Products
* [Hands-On Continuous Integration and Delivery with Jenkins X and Kubernetes [Video]](https://www.packtpub.com/cloud-networking/hands-on-continuous-integration-and-delivery-with-jenkins-x-and-kubernetes-video)

* [Mastering Palo Alto Networks [Video]](https://www.packtpub.com/networking-and-servers/mastering-palo-alto-networks-video)

* [Hands-On Systems Programming with Rust [Video]](https://www.packtpub.com/programming/hands-on-systems-programming-with-rust-video)
