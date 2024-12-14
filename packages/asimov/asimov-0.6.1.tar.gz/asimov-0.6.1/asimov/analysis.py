"""
Code to handle the various kinds of analysis which asimov can handle.

Asimov defintes three types of analysis, depending on the inputs of the analysis.

Simple analyses
  These analyses operate only on a single event,
  and will generally use a very specific set of configuration settings.
  An example of a simple analysis is a bilby or RIFT parameter estimation analysis,
  as these only require access to the data for a single event.
  Before version 0.4 these were called `Productions`.

Event analyses
  These analyses can access the results of all of the simple analyses which have been
  performed on a single event, or a subset of them.
  An example of an event analysis is the production of mixed posterior samples from multiple
  PE analyses.

Project analyses
  These are the most general type of analysis, and have access to the results of all analyses
  on all events, including event and simple analyses.
  This type of analysis is useful for defining a population analysis or analysing multiple events together, for example.

"""

import os
import configparser
from copy import deepcopy
import pathlib

from functools import reduce
import operator

from liquid import Liquid

from asimov import config, logger, LOGGER_LEVEL
from asimov.pipelines import known_pipelines
from asimov.utils import update, diff_dict
from asimov.storage import Store

from .review import Review
from .ini import RunConfiguration

status_map = {
    "cancelled": "light",
    "finished": "success",
    "uploaded": "success",
    "processing": "primary",
    "running": "primary",
    "stuck": "warning",
    "restart": "secondary",
    "ready": "secondary",
    "wait": "light",
    "stop": "danger",
    "manual": "light",
    "stopped": "light",
}

review_map = {
    "deprecated": "warning",
    "none": "default",
    "approved": "success",
    "rejected": "danger",
    "checked": "info",
}


class Analysis:
    """
    The base class for all other types of analysis.
    """

    meta = {}
    meta_defaults = {"scheduler": {}, "sampler": {}, "review": {}, "likelihood": {}}
    _reviews = Review()

    @property
    def review(self):
        """
        Return the review information attached to the analysis.
        """
        if "review" in self.meta:
            if len(self.meta["review"]) > 0:
                self._reviews = Review.from_dict(self.meta["review"], production=self)
                self.meta.pop("review")
        return self._reviews

    def _process_dependencies(self, needs):
        """
        Process the dependencies list for this production.

        The dependencies can be provided either as the name of a production,
        or a query against the analysis's attributes.

        Parameters
        ----------
        needs : list
           A list of all the requirements

        Returns
        -------
        list
           A list of all the requirements processed for evaluation.
        """
        all_requirements = []
        for need in deepcopy(needs):
            try:
                requirement = need.split(":")
                requirement = [requirement[0].split("."), requirement[1]]
            except IndexError:
                requirement = [["name"], need]
            except AttributeError:
                requirement = need
            all_requirements.append(requirement)
        return all_requirements

    @property
    def job_id(self):
        """
        Get the ID number of this job as it resides in the scheduler.
        """
        if "scheduler" in self.meta:
            if "job id" in self.meta["scheduler"]:
                return self.meta["scheduler"]["job id"]
            else:
                return None

    @job_id.setter
    def job_id(self, value):
        if "scheduler" not in self.meta:
            self.meta["scheduler"] = {}
        self.meta["scheduler"]["job id"] = value

    @property
    def dependencies(self):
        """Return a list of analyses which this analysis depends upon."""
        all_matches = []
        if len(self._needs) == 0:
            return []
        else:
            matches = set({})  # set(self.event.analyses)
            # matches.remove(self)
            requirements = self._process_dependencies(deepcopy(self._needs))
            for attribute, match in requirements:
                filtered_analyses = list(
                    filter(
                        lambda x: x.matches_filter(attribute, match),
                        self.event.analyses,
                    )
                )
                matches = set.union(matches, set(filtered_analyses))
            for analysis in matches:
                all_matches.append(analysis.name)

            return all_matches

    @property
    def priors(self):
        if "priors" in self.meta:
            priors = self.meta["priors"]
        else:
            priors = None
        return priors

    @property
    def finished(self):
        finished_states = ["finished", "processing", "uploaded"]
        return self.status in finished_states

    @property
    def status(self):
        return self.status_str.lower()

    @status.setter
    def status(self, value):
        self.status_str = value.lower()

    def matches_filter(self, attribute, match):
        """
        Checks to see if this analysis matches a given filtering
        criterion.

        A variety of different attributes can be used for filtering.
        The primary attributes are

            - review status

            - processing status

            - name

        In addition, any quantity contained in the analysis metadata
        may be used by accessing it in the nested structure of this
        data, with levels of the hierarchy separated with period
        characters.  For example, to access the waveform approximant
        the correct attribute would be `waveform.approximant`.

        Parameters
        ----------
        attribute : str
           The name of the attribute to be tested
        match : str
           The string to be matched against the value of the attribute

        Returns
        -------
        bool
           Returns True if this analysis matches the query,
           otherwise returns False.
        """
        is_review = False
        is_status = False
        is_name = False
        in_meta = False
        if attribute[0] == "review":
            is_review = match.lower() == str(self.review.status).lower()
        elif attribute[0] == "status":
            is_status = match.lower() == self.status.lower()
        elif attribute[0] == "name":
            is_name = match == self.name
        else:
            try:
                in_meta = reduce(operator.getitem, attribute, self.meta) == match
            except KeyError:
                in_meta = False

        return is_name | in_meta | is_status | is_review

    def results(self, filename=None, handle=False, hash=None):
        store = Store(root=config.get("storage", "results_store"))
        if not filename:
            try:
                items = store.manifest.list_resources(self.subject.name, self.name)
                return items
            except KeyError:
                return None
        elif handle:
            return open(
                store.fetch_file(self.subject.name, self.name, filename, hash), "r"
            )
        else:
            return store.fetch_file(self.subject.name, self.name, filename, hash=hash)

    @property
    def rundir(self):
        """
        Return the run directory for this analysis.
        """
        if "rundir" in self.meta:
            return os.path.abspath(self.meta["rundir"])
        elif "working directory" in self.subject.meta:
            value = os.path.join(self.subject.meta["working directory"], self.name)
            self.meta["rundir"] = value
            return os.path.abspath(self.meta["rundir"])
            # TODO: Make sure this is saved back to the ledger
        else:
            return None

    @rundir.setter
    def rundir(self, value):
        """
        Set the run directory.
        """
        if "rundir" not in self.meta:
            self.meta["rundir"] = value
        else:
            self.meta["rundir"] = value

    def get_meta(self, key):
        """
        Get the value of a metadata attribute, or return None if it doesn't
        exist.
        """
        if key in self.meta:
            return self.meta[key]
        else:
            return None

    def set_meta(self, key, value):
        """
        Set a metadata attribute which doesn't currently exist.
        """
        if key not in self.meta:
            self.meta[key] = value
            self.event.ledger.update_event(self.event)
        else:
            raise ValueError

    def make_config(self, filename, template_directory=None, dryrun=False):
        """
        Make the configuration file for this production.

        Parameters
        ----------
        filename : str
           The location at which the config file should be saved.
        template_directory : str, optional
           The path to the directory containing the pipeline config templates.
           Defaults to the directory specified in the asimov configuration file.
        """

        if "template" in self.meta:
            template = f"{self.meta['template']}.ini"

        else:
            template = f"{self.pipeline}.ini"

        pipeline = self.pipeline
        try:
            template_directory = config.get("templating", "directory")
            template_file = os.path.join(f"{template_directory}", template)

        except (configparser.NoOptionError, configparser.NoSectionError):
            if hasattr(pipeline, "config_template"):
                template_file = pipeline.config_template
            else:
                from pkg_resources import resource_filename

                template_file = resource_filename("asimov", f"configs/{template}")

        liq = Liquid(template_file)
        rendered = liq.render(production=self, analysis=self, config=config)
        with open(filename, "w") as output_file:
            output_file.write(rendered)

    def build_report(self):
        if self.pipeline:
            self.pipeline.build_report()

    def html(self):
        """
        An HTML representation of this production.
        """
        production = self

        card = ""

        card += f"<div class='asimov-analysis asimov-analysis-{self.status}'>"
        card += f"<h4>{self.name}"

        if self.comment:
            card += (
                f"""  <small class="asimov-comment text-muted">{self.comment}</small>"""
            )
        card += "</h4>"
        if self.status:
            card += f"""<p class="asimov-status">
  <span class="badge badge-pill badge-{status_map[self.status]}">{self.status}</span>
</p>"""

        if self.pipeline:
            card += f"""<p class="asimov-pipeline-name">{self.pipeline.name}</p>"""

        if self.pipeline:
            # self.pipeline.collect_pages()
            card += self.pipeline.html()

        if self.rundir:
            card += f"""<p class="asimov-rundir"><code>{production.rundir}</code></p>"""
        else:
            card += """&nbsp;"""

        if "approximant" in production.meta:
            card += f"""<p class="asimov-attribute">Waveform approximant:
   <span class="asimov-approximant">{production.meta['approximant']}</span>
</p>"""

        card += """&nbsp;"""
        card += """</div>"""

        if len(self.review) > 0:
            for review in self.review:
                card += review.html()

        return card

    def to_dict(self, event=True):
        """
        Return this production as a dictionary.

        Parameters
        ----------
        event : bool
           If set to True the output is designed to be included nested within an event.
           The event name is not included in the representation, and the production name is provided as a key.
        """
        dictionary = deepcopy(self.meta)
        if not event:
            dictionary["event"] = self.event.name
            dictionary["name"] = self.name

        if isinstance(self.pipeline, str):
            dictionary["pipeline"] = self.pipeline
        else:
            dictionary["pipeline"] = self.pipeline.name.lower()
        dictionary["comment"] = self.comment

        if self.review:
            dictionary["review"] = self.review.to_dicts()

        dictionary["needs"] = self._needs  # self.dependencies

        if "data" in self.meta:
            dictionary["data"] = self.meta["data"]
        if "likelihood" in self.meta:
            dictionary["likelihood"] = self.meta["likelihood"]
        if "quality" in self.meta:
            dictionary["quality"] = self.meta["quality"]
        if "priors" in self.meta:
            dictionary["priors"] = self.meta["priors"]
        if "waveform" in self.meta:
            dictionary["waveform"] = self.meta["waveform"]
        for key, value in self.meta.items():
            dictionary[key] = value

        dictionary["status"] = self.status
        dictionary["job id"] = self.job_id

        # Remove duplicates of pipeline defaults
        if self.pipeline.name.lower() in self.event.ledger.data["pipelines"]:
            defaults = deepcopy(
                self.event.ledger.data["pipelines"][self.pipeline.name.lower()]
            )
        else:
            defaults = {}

        # if "postprocessing" in self.event.ledger.data:
        #     defaults["postprocessing"] = deepcopy(
        #         self.event.ledger.data["postprocessing"]
        #     )

        defaults = update(defaults, deepcopy(self.event.meta))
        dictionary = diff_dict(defaults, dictionary)

        if "repository" in self.meta:
            dictionary["repository"] = self.repository.url
        if "ledger" in dictionary:
            dictionary.pop("ledger")
        if "pipelines" in dictionary:
            dictionary.pop("pipelines")
        if "productions" in dictionary:
            dictionary.pop("productions")

        if not event:
            output = dictionary
        else:
            output = {self.name: dictionary}
        return output


class SimpleAnalysis(Analysis):
    """
    A single subject, single pipeline analysis.
    """

    def __init__(self, subject, name, pipeline, status=None, comment=None, **kwargs):

        self.ledger = kwargs.get("ledger", None)

        self.event = self.subject = subject
        self.name = name

        pathlib.Path(
            os.path.join(config.get("logging", "directory"), self.event.name, name)
        ).mkdir(parents=True, exist_ok=True)

        self.logger = logger.getChild("analysis").getChild(
            f"{self.event.name}/{self.name}"
        )
        self.logger.setLevel(LOGGER_LEVEL)

        # fh = logging.FileHandler(logfile)
        # formatter = logging.Formatter("%(asctime)s - %(message)s", "%Y-%m-%d %H:%M:%S")
        # fh.setFormatter(formatter)
        # self.logger.addHandler(fh)

        if status:
            self.status_str = status.lower()
        else:
            self.status_str = "none"

        self.meta = deepcopy(self.meta_defaults)

        # Start by adding pipeline defaults
        if "pipelines" in self.event.ledger.data:
            if pipeline in self.event.ledger.data["pipelines"]:
                self.meta = update(
                    self.meta, deepcopy(self.event.ledger.data["pipelines"][pipeline])
                )

        if "postprocessing" in self.event.ledger.data:
            self.meta["postprocessing"] = deepcopy(
                self.event.ledger.data["postprocessing"]
            )

        # self.meta["pipeline"] = pipeline

        # Update with the subject defaults
        self.meta = update(self.meta, deepcopy(self.subject.meta))
        if "productions" in self.meta:
            self.meta.pop("productions")
        self.meta = update(self.meta, deepcopy(kwargs))

        self.pipeline = pipeline.lower()
        self.pipeline = known_pipelines[pipeline.lower()](self)

        if "needs" in self.meta:
            self._needs = self.meta.pop("needs")
        else:
            self._needs = []

        self.comment = kwargs.get("comment", None)

    def _previous_assets(self):
        assets = {}
        if self.dependencies:
            productions = {}
            for production in self.event.productions:
                productions[production.name] = production
            for previous_job in self.dependencies:
                assets.update(productions[previous_job].pipeline.collect_assets())
        return assets

    @classmethod
    def from_dict(cls, parameters, subject=None, ledger=None):
        parameters = deepcopy(parameters)
        # Check that pars is a dictionary
        if not {"pipeline", "name"} <= parameters.keys():
            raise ValueError(
                f"Some of the required parameters are missing."
                f"Found {parameters.keys()}"
            )
        if "status" not in parameters:
            parameters["status"] = "ready"
        if "event" in parameters:
            parameters.pop("event")
        pipeline = parameters.pop("pipeline")
        name = parameters.pop("name")
        if "comment" not in parameters:
            parameters["comment"] = None
        if "ledger" in parameters:
            ledger = parameters.pop("ledger")

        return cls(
            name=name, pipeline=pipeline, ledger=ledger, subject=subject, **parameters
        )


class SubjectAnalysis(Analysis):
    """
    A single subject analysis which requires results from multiple pipelines.
    """

    def __init__(self, subject, name, pipeline, status=None, comment=None, **kwargs):
        self.event = self.subject = subject
        self.name = name

        self.category = "subject_analyses"

        self.logger = logger.getChild("event").getChild(f"{self.name}")
        self.logger.setLevel(LOGGER_LEVEL)

        if status:
            self.status_str = status.lower()
        else:
            self.status_str = "none"

        self.meta = deepcopy(self.meta_defaults)
        self.meta = update(self.meta, deepcopy(self.subject.meta))
        self.meta = update(self.meta, deepcopy(kwargs))

        self._analysis_spec = self.meta.get("needs")

        if self._analysis_spec:
            requirements = self._process_dependencies(self._analysis_spec)
            self.analyses = []
            for attribute, match in requirements:
                matches = set(self.subject.analyses)
                filtered_analyses = list(
                    filter(
                        lambda x: x.matches_filter(attribute, match), subject.analyses
                    )
                )
                matches = set.intersection(matches, set(filtered_analyses))

                for analysis in matches:
                    self.analyses.append(analysis)
            self.productions = self.analyses
        if "needs" in self.meta:
            self.meta.pop("needs")

        self.pipeline = pipeline.lower()
        self.pipeline = known_pipelines[pipeline.lower()](self)

        if "needs" in self.meta:
            self._needs = self.meta.pop("needs")
        else:
            self._needs = []

        if "comment" in kwargs:
            self.comment = kwargs["comment"]
        else:
            self.comment = None

    def to_dict(self, event=True):
        """
        Return this production as a dictionary.

        Parameters
        ----------
        event : bool
           If set to True the output is designed to be included nested within an event.
           The event name is not included in the representation, and the production name is provided as a key.
        """
        dictionary = {}
        dictionary = update(dictionary, self.meta)

        if not event:
            dictionary["event"] = self.event.name
            dictionary["name"] = self.name

        dictionary["status"] = self.status
        if isinstance(self.pipeline, str):
            dictionary["pipeline"] = self.pipeline
        else:
            dictionary["pipeline"] = self.pipeline.name.lower()
        dictionary["comment"] = self.comment

        dictionary["analyses"] = self._analysis_spec

        if self.review:
            dictionary["review"] = self.review.to_dicts()

        dictionary["needs"] = deepcopy(self._needs)  # self.dependencies

        if "quality" in self.meta:
            dictionary["quality"] = self.meta["quality"]
        if "priors" in self.meta:
            dictionary["priors"] = self.meta["priors"]
        for key, value in self.meta.items():
            dictionary[key] = value
        if "repository" in self.meta:
            dictionary["repository"] = self.repository.url
        if "ledger" in dictionary:
            dictionary.pop("ledger")
        if "pipelines" in dictionary:
            dictionary.pop("pipelines")

        if not event:
            output = dictionary
        else:
            output = {self.name: dictionary}
        return output

    @classmethod
    def from_dict(cls, parameters, subject):
        parameters = deepcopy(parameters)
        # Check that pars is a dictionary
        if not {"pipeline", "name"} <= parameters.keys():
            raise ValueError(
                f"Some of the required parameters are missing."
                f"Found {parameters.keys()}"
            )
        if "status" not in parameters:
            parameters["status"] = "ready"
        if "event" in parameters:
            parameters.pop("event")
        pipeline = parameters.pop("pipeline")
        name = parameters.pop("name")
        if "comment" not in parameters:
            parameters["comment"] = None

        return cls(subject, name, pipeline, **parameters)


class ProjectAnalysis(Analysis):
    """
    A multi-subject analysis.
    """

    meta_defaults = {"scheduler": {}, "sampler": {}, "review": {}}

    def __init__(self, name, pipeline, ledger=None, **kwargs):
        """ """
        super().__init__()
        self.name = name
        self.logger = logger.getChild("project analyses").getChild(f"{self.name}")
        self.logger.setLevel(LOGGER_LEVEL)
        self.ledger = ledger
        self.category = "project_analyses"

        self._subjects = kwargs["subjects"]

        self._events = self._subjects
        if "analyses" in kwargs.keys():
            self._analysis_spec = kwargs["analyses"]
        else:
            self._analysis_spec = {}
        requirements = self._process_dependencies(self._analysis_spec)
        self.analyses = []

        # set up the working directory
        if "working_directory" in kwargs:
            self.work_dir = kwargs["working_directory"]
        else:
            subj_string = "_".join([f"{subject}" for subject in self._subjects])
            self.work_dir = os.path.join("working", "project-analyses", subj_string, f"{self.name}")

        if not os.path.exists(self.work_dir):
            os.makedirs(self.work_dir)

        self.repository = None

        self._subject_obs = []
        for subject in self.subjects:
            if self._analysis_spec:
                matches = set(subject.analyses)
                for attribute, match in requirements:
                    filtered_analyses = list(
                        filter(
                            lambda x: x.matches_filter(attribute, match),
                            subject.analyses,
                        )
                    )
                    matches = set.intersection(matches, set(filtered_analyses))
                for analysis in matches:
                    self.analyses.append(analysis)
        if "status" in kwargs:
            self.status_str = kwargs["status"].lower()
        else:
            self.status_str = "none"

        self.pipeline = pipeline  # .lower()
        if isinstance(pipeline, str):
            # try:
            self.pipeline = known_pipelines[str(pipeline).lower()](self)
            # except KeyError:
            self.logger.warning(f"The pipeline {pipeline} could not be found.")

        if "needs" in self.meta:
            self._needs = self.meta.pop("needs")
        else:
            self._needs = []

        if "comment" in kwargs:
            self.comment = kwargs["comment"]
        else:
            self.comment = None

        self.meta = deepcopy(self.meta_defaults)

        # Start by adding pipeline defaults
        if "pipelines" in self.ledger.data:
            if pipeline in self.ledger.data["pipelines"]:
                self.meta = update(
                    self.meta, deepcopy(self.ledger.data["pipelines"][pipeline])
                )

        self.meta = update(self.meta, deepcopy(kwargs))

    def __repr__(self):
        """
        A human-friendly representation of this project analysis.

        Parameters
        ----------
        None
        """
        return f"<Project analysis for {len(self.events)} events and {len(self.analyses)} analyses>"

    @property
    def subjects(self):
        """Return a list of subjects for this project analysis."""
        return [self.ledger.get_event(subject)[0] for subject in self._subjects]

    @property
    def events(self):
        return self.subjects()

    @classmethod
    def from_dict(cls, parameters, ledger=None):
        parameters = deepcopy(parameters)
        # Check that pars is a dictionary
        if not {"pipeline", "name"} <= parameters.keys():
            raise ValueError(
                f"Some of the required parameters are missing. "
                f"Found {parameters.keys()}"
            )
        if "status" not in parameters:
            parameters["status"] = "ready"
        if "event" in parameters:
            parameters.pop("event")
        pipeline = parameters.pop("pipeline")
        name = parameters.pop("name")
        if "comment" not in parameters:
            parameters["comment"] = None

        if "analyses" not in parameters:
            parameters["analyses"] = []

        return cls(name=name, pipeline=pipeline, ledger=ledger, **parameters)

    @property
    def dependencies(self):
        """Return a list of analyses which this analysis depends upon."""
        all_matches = []
        if len(self._needs) == 0:
            return []
        else:
            matches = set({})  # set(self.event.analyses)
            # matches.remove(self)
            requirements = self._process_dependencies(deepcopy(self._needs))
            analyses = []
            for subject in self.subjects:
                sub = self.ledger.get_event(subject)[0]
                self._subject_obs.append(sub)
                for analysis in sub.analyses:
                    analyses.append(analysis)
            for attribute, match in requirements:
                filtered_analyses = list(
                    filter(
                        lambda x: x.matches_filter(attribute, match),
                        analyses,
                    )
                )
                matches = set.union(matches, set(filtered_analyses))
            for analysis in matches:
                all_matches.append(analysis.name)

            return all_matches

    def to_dict(self):
        """
        Return this project production as a dictionary.

        Parameters
        ----------
        event : bool
           If set to True the output is designed to be included nested within an event.
           The event name is not included in the representation, and the production name is provided as a key.
        """
        dictionary = {}
        dictionary = update(dictionary, self.meta)

        dictionary["name"] = self.name
        dictionary["status"] = self.status
        if isinstance(self.pipeline, str):
            dictionary["pipeline"] = self.pipeline
        else:
            dictionary["pipeline"] = self.pipeline.name.lower()
        dictionary["comment"] = self.comment

        if self.review:
            dictionary["review"] = self.review.copy()  # .to_dicts()

        dictionary["needs"] = self.dependencies

        if "quality" in self.meta:
            dictionary["quality"] = self.meta["quality"]
        if "priors" in self.meta:
            dictionary["priors"] = self.meta["priors"]
        for key, value in self.meta.items():
            dictionary[key] = value
        if "repository" in self.meta:
            dictionary["repository"] = self.repository.url
        if "ledger" in dictionary:
            dictionary.pop("ledger")
        if "pipelines" in dictionary:
            dictionary.pop("pipelines")

        dictionary["subjects"] = self._subjects
        dictionary["analyses"] = self._analysis_spec

        output = dictionary

        return output

    @property
    def rundir(self):
        """
        Returns the rundir for this event
        """

        if "rundir" in self.meta:
            return self.meta["rundir"]
        elif self.work_dir:
            self.meta["rundir"] = self.work_dir
            return self.meta["rundir"]
        else:
            return None

    @rundir.setter
    def rundir(self, value):
        """
        Set the run directory.
        """
        if "rundir" not in self.meta:
            self.meta["rundir"] = value
        else:
            self.meta["rundir"] = value


class GravitationalWaveTransient(SimpleAnalysis):
    """
    A single subject, single pipeline analysis for a gravitational wave transient.
    """

    def __init__(self, subject, name, pipeline, **kwargs):
        """
        A specific analysis on a GW transient event.

        Parameters
        ----------
        subject : `asimov.event`
            The event this analysis is running on.
        name : str
            The name of this analysis.
        status : str
            The status of this analysis.
        pipeline : str
            This analysis's pipeline.
        comment : str
            A comment on this analysis.
        """

        self.category = config.get("general", "calibration_directory")
        super().__init__(subject, name, pipeline, **kwargs)
        self._checks()

        self.psds = self._collect_psds()
        self.xml_psds = self._collect_psds(format="xml")

        if "cip jobs" in self.meta:
            # TODO: Should probably raise a deprecation warning
            self.meta["sampler"]["cip jobs"] = self.meta["cip jobs"]

        if "scheduler" not in self.meta:
            self.meta["scheduler"] = {}

        if "likelihood" not in self.meta:
            self.meta["likelihood"] = {}
        if "marginalization" not in self.meta["likelihood"]:
            self.meta["likelihood"]["marginalization"] = {}

        if "data" not in self.meta:
            self.meta["data"] = {}
        if "data files" not in self.meta["data"]:
            self.meta["data"]["data files"] = {}

        if "lmax" in self.meta:
            # TODO: Should probably raise a deprecation warning
            self.meta["sampler"]["lmax"] = self.meta["lmax"]

        # Check that the upper frequency is included, otherwise calculate it
        if "quality" in self.meta:
            if ("maximum frequency" not in self.meta["quality"]) and (
                "sample rate" in self.meta["likelihood"]
            ):
                self.meta["quality"]["maximum frequency"] = {}
                # Account for the PSD roll-off with the 0.875 factor
                for ifo in self.meta["interferometers"]:
                    self.meta["quality"]["maximum frequency"][ifo] = int(
                        0.875 * self.meta["likelihood"]["sample rate"] / 2
                    )

        if ("quality" in self.meta) and ("event time" in self.meta):
            if ("segment start" not in self.meta["quality"]) and (
                "segment length" in self.meta["data"]
            ):
                self.meta["likelihood"]["segment start"] = (
                    self.meta["event time"] - self.meta["data"]["segment length"] + 2
                )
                # self.event.meta['likelihood']['segment start'] = self.meta['data']['segment start']

        # Update waveform data
        if "waveform" not in self.meta:
            self.logger.info("Didn't find waveform information in the metadata")
            self.meta["waveform"] = {}
        if "approximant" in self.meta:
            self.logger.warning(
                "Found deprecated approximant information, "
                "moving to waveform area of ledger"
            )
            approximant = self.meta.pop("approximant")
            self.meta["waveform"]["approximant"] = approximant
        if "reference frequency" in self.meta["likelihood"]:
            self.logger.warning(
                "Found deprecated ref freq information, "
                "moving to waveform area of ledger"
            )
            ref_freq = self.meta["likelihood"].pop("reference frequency")
            self.meta["waveform"]["reference frequency"] = ref_freq

        # Gather the PSDs for the job
        self.psds = self._collect_psds()

    def _checks(self):
        """
        Carry-out a number of data consistency checks on the information from the ledger.
        """
        # Check that the upper frequency is included, otherwise calculate it
        if self.quality:
            if ("high-frequency" not in self.quality) and (
                "sample-rate" in self.quality
            ):
                # Account for the PSD roll-off with the 0.875 factor
                self.meta["quality"]["high-frequency"] = int(
                    0.875 * self.meta["quality"]["sample-rate"] / 2
                )
            elif ("high-frequency" in self.quality) and ("sample-rate" in self.quality):
                if self.meta["quality"]["high-frequency"] != int(
                    0.875 * self.meta["quality"]["sample-rate"] / 2
                ):
                    self.logger.warn(
                        "The upper-cutoff frequency is not equal to 0.875 times the Nyquist frequency."
                    )

    @property
    def quality(self):
        if "quality" in self.meta:
            return self.meta["quality"]
        else:
            return None

    @property
    def reference_frame(self):
        """
        Calculate the appropriate reference frame.
        """
        ifos = self.meta["interferometers"]
        if len(ifos) == 1:
            return ifos[0]
        else:
            return "".join(ifos[:2])

    def get_timefile(self):
        """
        Find this event's time file.

        Returns
        -------
        str
           The location of the time file.
        """
        return self.event.repository.find_timefile(self.category)

    def get_coincfile(self):
        """
        Find this event's coinc.xml file.

        Returns
        -------
        str
           The location of the time file.
        """
        try:
            coinc = self.event.repository.find_coincfile(self.category)
            return coinc
        except FileNotFoundError:
            self.event.get_gracedb(
                "coinc.xml",
                os.path.join(
                    self.event.repository.directory, self.category, "coinc.xml"
                ),
            )
            coinc = self.event.repository.find_coincfile(self.category)
            return coinc

    def get_configuration(self):
        """
        Get the configuration file contents for this event.
        """
        if "ini" in self.meta:
            ini_loc = self.meta["ini"]
        else:
            # We'll need to search the repository for it.
            try:
                ini_loc = self.subject.repository.find_prods(self.name, self.category)[
                    0
                ]
                if not os.path.exists(ini_loc):
                    raise ValueError("Could not open the ini file.")
            except IndexError:
                raise ValueError("Could not open the ini file.")
        try:
            ini = RunConfiguration(ini_loc)
        except ValueError:
            raise ValueError("Could not open the ini file")
        except configparser.MissingSectionHeaderError:
            raise ValueError("This isn't a valid ini file")

        return ini

    def _collect_psds(self, format="ascii"):
        """
        Collect the required psds for this production.
        """
        psds = {}
        # If the PSDs are specifically provided in the ledger,
        # use those.

        if format == "ascii":
            keyword = "psds"
        elif format == "xml":
            keyword = "xml psds"
        else:
            raise ValueError(f"This PSD format ({format}) is not recognised.")

        if keyword in self.meta:
            # if self.meta["likelihood"]["sample rate"] in self.meta[keyword]:
            psds = self.meta[keyword]  # [self.meta["likelihood"]["sample rate"]]

        # First look through the list of the job's dependencies
        # to see if they're provided by a job there.
        elif self.dependencies:
            productions = {}
            for production in self.event.productions:
                productions[production.name] = production

            for previous_job in self.dependencies:
                try:
                    # Check if the job provides PSDs as an asset and were produced with compatible settings
                    if keyword in productions[previous_job].pipeline.collect_assets():
                        if self._check_compatible(productions[previous_job]):
                            psds = productions[previous_job].pipeline.collect_assets()[
                                keyword
                            ]
                            break
                        else:
                            self.logger.info(
                                f"The PSDs from {previous_job} are not compatible with this job."
                            )
                    else:
                        psds = {}
                except Exception:
                    psds = {}
        # Otherwise return no PSDs
        else:
            psds = {}

        for ifo, psd in psds.items():
            self.logger.debug(f"PSD-{ifo}: {psd}")

        return psds
