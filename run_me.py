from pathlib import Path
import logging
import re
import webbrowser
from time import sleep

import docker
from docker.errors import ImageNotFound
from requests.exceptions import ConnectionError

from download_data import download

# TODO: fix docker.errors.APIError: 409 Client Error: Conflict ("Conflict. The container name "/mastering-pyspark-ml"
#  is already in use by container "5e645605bbef237ecabe3366dd512de182ac76505e3ff1cff16fb3d5af748cdf". You have to
#  remove (or rename) that container to be able to reuse that name.")

logging.basicConfig(
    level=logging.DEBUG, format="%(levelname)-7s  %(name)-19s  %(message)s", style="%"
)
logger = logging.getLogger("CourseHandler")


def re_search(pattern, text, plural=False):
    """Regex helper to find strings in a body of text"""
    match = [m.group(1) for m in re.finditer(pattern, text)]
    if plural:
        return match
    else:
        if match:
            return match[0]


def look_ahead(iter_item):
    """
    This function can be used to determine if there are items left after the current
    value in the iterable. It passes through all values from the given iterable,
    augmented by the information if there are more values to come after the current
    one. The data is enumerated as to provide an index key as well.

     Passes through all values from the given iterable augmented with a index number
     (i) and a boolean that determines if the current value is the last value.
              - (False) if there are more values after the current one
              - (True) if it is the last value

    :param iter_item: iterable item
    :return: yields index, value, last_flag

    Code example:
    >>> for i, v, last in look_ahead(["this","is","a","test"]):
    ...     print(i, v, last)
    ...     if last:
    ...         print("The End")
    0 this False
    1 is False
    2 a False
    3 test True
    The End

    Inspired by: (http://stackoverflow.com/questions/1630320/what-is-the-pythonic-way-to
    -detect-the-last-element-in-a-python-for-loop)
    """
    # Get an iterator and pull the first value (we are starting from the second value
    ii = iter(iter_item)
    last_value = next(ii)
    last_i = 0

    # Run the iterator to exhaustion. As long as loop is running we have not reached
    # the last value yet
    for i, value in enumerate(ii):
        # Report the *previous* value
        yield i, last_value, False
        last_value = value
        last_i = i + 1

    # Report the last value. Since the loop has finished we have reached the last value
    yield last_i, last_value, True


class Course:
    """Class that constructs the environment for this course"""

    author = "Danny Meijer"
    copyright = 2020

    find_me_on_the_web = {
        "LinkedIn": "https://www.linkedin.com/in/dannydatascientist/",
        "GitHub": "https://github.com/dannymeijer",
        "Email": "chilltake@gmail.com",
    }

    @staticmethod
    def close(self):
        print("Thank you!")

    repo_path = Path(__file__).resolve().parent

    Dockerfile = open(repo_path / "Dockerfile", "r").read()

    author = re_search('ARG AUTHOR="(.+)"', Dockerfile)
    version = re_search('ARG VERSION="([\w-]+)"', Dockerfile)
    container_name = re_search('ARG CONTAINER_NAME="([\w-]+)"', Dockerfile)
    full_name = re_search('ARG COURSE_NAME="([\w\s]+)"', Dockerfile)
    short_name = full_name.lower().replace(" ", "_")
    repo_name = Path(repo_path).name
    home = Path(re_search('ENV HOME="(.+)"', Dockerfile))
    ports = re_search("EXPOSE ([0-9/tcudp]+)", Dockerfile, plural=True)
    tag = "{tag}:{target}".format(tag=container_name, target=version)

    client = None
    image = None
    container = None

    def __init__(self):
        self._client()
        self._image()
        self._container()

    @property
    def volumes(self):
        """volumes property dynamically builds volume configuration based on the
        course Sections, expecting a data-sets folder and creating a work folder
        :return: dictionary to configure volumes mounted inside the container
        """
        return {
            # Mount data-sets
            self.repo_path / "data-sets": {
                "bind": (self.home / "data-sets").as_posix(),
                "mode": "rw",
            },
            # Mount work folder
            self.repo_path / "work": {
                "bind": (self.home / "work").as_posix(),
                "mode": "rw",
            },
            # Mount each section
            **{
                section_path: {
                    "bind": (self.home / self.short_name / section_path.name).as_posix(),
                    "mode": "rw",
                }
                for section_path in list(self.repo_path.glob("Section*"))
            },
        }

    def _client(self):
        """Initiates a Docker client
        :returns: DockerClient
        """
        try:
            logger.info("Connecting to Docker API")
            if not self.client:
                self.client = docker.from_env()
            return self.client
        except ConnectionError:
            raise RuntimeError(
                "Something went wrong. Unable to connect to Docker. Please verify that "
                "the Docker Desktop Client is running"
            )

    def get_image(self, tag):
        try:
            self.image = self.client.images.get(tag)
        except docker.errors.ImageNotFound:
            self.image = None
        logger.debug("image value: %s", self.image)
        return self.image

    def remove_image(self, tag):
        # FOR DEBUG AND DEVELOPMENT PURPOSES ONLY
        try:
            self.client.images.remove(tag)
            logger.info("Successfully removed image, %s", tag)
        except docker.errors.ImageNotFound:
            logger.warning("Unable to remove image, ImageNotFound %s", tag)

    def build_image(self):
        """Equivalent of `docker build --rm -f "Dockerfile" -t $COURSE_NAME .`
        :return: None
        """
        logger.info("Building Docker image")
        build_logger = logging.getLogger("docker.api.build")
        progress_log = dict()

        # Using low level Docker API to be able to report status
        # Builds can take a while!
        build_logger.info("Initiating (this might take a few moments)")
        for i, log, last in look_ahead(
            self.client.api.build(
                tag=self.tag,
                path=str(self.repo_path),
                dockerfile="Dockerfile",
                rm=True,
                decode=True,
            )
        ):
            if i == 0:
                build_logger.info("Build process started...")

            # Retrieve status from stream
            status = log.get("status")
            progress_detail = log.get("progressDetail")
            i_d = log.get("id", None)
            if i_d:
                if status in ["Downloading", "Extracting"] and progress_detail:
                    progress_log[i_d] = {
                        "status": status,
                        "total": progress_detail.get("total", 1),
                        "current": progress_detail.get("current", 0),
                    }

            # Report progress every few lines from the stream
            if (last or (i + 1) % 100 == 0) and progress_log.__len__() > 0:
                # Construct log message
                build_logger.info(
                    " {total_progress} | {total} Packages, {downloading} Downloading, "
                    "{extracting} Extracted".format(
                        downloading=len(
                            [
                                log
                                for log in progress_log.values()
                                if log.get("status") == "Downloading"
                            ]
                        ),
                        extracting=len(
                            [
                                log
                                for log in progress_log.values()
                                if log.get("status") == "Extracting"
                            ]
                        ),
                        total_progress="{0:.2f}%".format(
                            (
                                float(sum([v["current"] for v in progress_log.values()]))
                                / float(sum([v["total"] for v in progress_log.values()]))
                            )
                            * 100
                        ),
                        total=progress_log.__len__(),
                    )
                )

        build_logger.info("Image was built successfully")
        self.image = self.get_image(self.tag)
        logger.info("Image ID: %s", self.image.id)

    def _image(self):
        """Retrieves docker image (if available)
        :return: docker image object
        """
        logger.info("Checking if Docker image is already set-up")
        if self.get_image(self.tag):
            self.image.reload()
        else:
            logger.warning("Docker image has not been built yet")
            self.build_image()

        logger.info("Image looks good!")
        return self.image

    def get_container(self, tag):
        try:
            self.container = self.client.containers.get(tag)
        except docker.errors.NotFound:
            self.container = None
        return self.container

    def run_container(self):
        """This method is responsible for running the container.

        Functionally similar to running Docker CLI command:
        ```docker run -v ${volumes} --rm -d -p ${ports} --name ${name} ${image}```

        The following things are set/handled
        - ensures the container is using the correct image version and that it is named
          correctly
        - exposes ports as set up by the port_map property
        - mounts the correct volumes inside of the container as per the volumes property
        - detach=True ensures that Container runs in detached head mode
        - remove=True ensures that the Container is removed once it is stopped

        :return: docker container object
        """
        # TODO: check if ports are available
        # TODO: dynamic port mapping
        port_map = {"{}/tcp".format(p): ("127.0.0.1", p) for p in self.ports}

        self.container = self.client.containers.run(
            ports=port_map,
            volumes=self.volumes,
            image=self.tag,
            name=self.container_name,
            detach=True,
            remove=True,
        )
        # TODO: handle docker.errors.APIError

        return self.container

    def _container(self):
        """Retrieves docker container (if available)
        :return: docker container object
        """
        logger.info("Checking if course container is running already")
        if not self.get_container(self.tag):
            logger.warning("Course's Docker container is not running yet")
            self.run_container()

        return self.container


if __name__ == "__main__":
    logger.info("Welcome to '%s' by %s", Course.full_name, Course.author)
    logger.info("Course Version: %s", Course.version)
    logger.info("Course Name: %s", Course.full_name)
    logger.info("Container Name: %s", Course.container_name)

    logger.debug("Ports that will be Exposed: %s", Course.ports)
    logger.debug("Container Tag: %s", Course.tag)

    logger.info("Downloading the data")
    download()

    # Set up the course
    course = Course()

    course_url = "http://localhost:{port}/lab?token={token}".format(
        port=8888, token=re_search('ENV JUPYTER_TOKEN "([\w-]+)"', course.Dockerfile)
    )

    logger.info(
        "The Course environment is available at [%s] \nIt will automatically "
        "open in your web browser within the next 15 seconds",
        course_url,
    )
    sleep(12)
    logger.info("Enjoy the Course!")
    webbrowser.open(course_url)
