"""
    PsychoPy routine to support the creation of valid bids-datasets.
"""

from pathlib import Path
from sys import path as sys_path

from psychopy.experiment import Param
from psychopy.experiment.routines._base import BaseStandaloneRoutine
from psychopy.localization import _translate

plugin_dir = Path(__file__).parent
if str(plugin_dir) not in sys_path:
    sys_path.insert(0, str(plugin_dir))

_localized = {
    "path": _translate("Path"),
    "runs": _translate("Add runs to event file name"),
    "event_json": _translate("event JSON"),
    "dataset_description": _translate("Dataset Description"),
}


class BidsExportRoutine(BaseStandaloneRoutine):
    """
    This class provides methods for creating and managing BIDS datasets and their modality agnostic
    files plus modality specific files.
    """

    categories = ["BIDS"]
    targets = ["PsychoPy"]
    iconFile = Path(__file__).parent / "BIDS.png"
    tooltip = _translate(
        "BIDS export: creates BIDS structure, writes tsv file and update"
        " further files"
    )
    plugin = "psychopy-bids"

    def __init__(self, exp, name="bidsExport"):
        BaseStandaloneRoutine.__init__(self, exp, name=name)

        self.exp.requireImport(
            importName="BIDSHandler", importFrom="psychopy_bids.bids"
        )

        self.type = "BIDSexport"

        self.params["name"].hint = _translate("Name of the Routine.")
        self.params["name"].label = _translate("Routine Name")

        hnt = _translate(
            "Name of the experiment (parent folder), if this (task) is part of"
            " a larger one."
        )
        self.params["dataset_name"] = Param(
            "bids",
            valType="str",
            inputType="single",
            categ="Basic",
            allowedTypes=[],
            canBePath=False,
            hint=hnt,
            label=_translate("Dataset Name"),
        )

        hnt = _translate("BIDS defined data type")
        self.params["data_type"] = Param(
            "beh",
            valType="str",
            inputType="choice",
            categ="Basic",
            allowedVals=[
                "func",
                "dwi",
                "fmap",
                "anat",
                "perf",
                "meg",
                "eeg",
                "ieeg",
                "beh",
                "pet",
                "micr",
            ],
            hint=hnt,
            label=_translate("data type"),
        )

        hnt = _translate(
            "Custom label to distinguish different conditions present during"
            " multiple runs of the same task"
        )
        self.params["acq"] = Param(
            "",
            valType="str",
            inputType="single",
            categ="Basic",
            allowedVals=[],
            canBePath=False,
            hint=hnt,
            label=_translate("acquisition mode"),
        )

        hnt = _translate(
            "Name of the default event JSON file. Will be copied into each"
            " subject folder."
        )
        self.params["event_json"] = Param(
            "",
            valType="str",
            inputType="file",
            allowedTypes=[],
            categ="Basic",
            updates="constant",
            allowedUpdates=["constant"],
            hint=hnt,
            label=_localized["event_json"],
        )

        # Params for dataset description
        hnt = _translate(
            "Path to the dataset_description.json. If not"
            " provided and no existing file is found, a default template"
            " will be used. Specifying a file will overwrite any existing"
            " dataset_description.json on every run."
        )
        self.params["dataset_description"] = Param(
            "",
            valType="str",
            inputType="file",
            allowedTypes=[],
            categ="Basic",
            updates="constant",
            allowedUpdates=["constant"],
            hint=hnt,
            label=_translate("dataset description"),
        )

        # license
        hnt = _translate("License of the dataset")
        self.params["bids_license"] = Param(
            "",
            valType="str",
            inputType="choice",
            categ="Basic",
            allowedVals=[
                "",
                "CC0-1.0",
                "CC-BY-4.0",
                "CC-BY-SA-4.0",
                "CC-BY-ND-4.0",
                "CC-BY-NC-4.0",
                "CC-BY-NC-SA-4.0",
                "CC-BY-NC-ND-4.0",
                "ODC-By-1.0",
                "ODbL-1.0",
                "PDDL-1.0",
            ],
            hint=hnt,
            label=_translate("license"),
        )

        hnt = _translate("Include lastrun and .psyexp in BIDS dataset /code directory.")
        self.params["add_code"] = Param(
            True,
            valType="bool",
            inputType="bool",
            categ="Basic",
            hint=hnt,
            label=_translate("Add lastrun.py/psyexp to dataset"),
        )

        hnt = _translate(
            "Include requirements.txt with all pip versions and the python version in BIDS dataset."
        )
        self.params["add_environment"] = Param(
            True,
            valType="bool",
            inputType="bool",
            categ="Basic",
            hint=hnt,
            label=_translate("Add requirements.txt to dataset"),
        )

        # runs params
        hnt = _translate("Should runs be added to event file name?")
        self.params["runs"] = Param(
            True,
            valType="bool",
            inputType="bool",
            categ="Basic",
            hint=hnt,
            label=_translate("Add runs to event filename"),
        )

        # these inherited params are harmless but might as well trim:
        for parameter in (
            "startType",
            "startVal",
            "startEstim",
            "stopVal",
            "stopType",
            "durationEstim",
            "saveStartStop",
            "syncScreenRefresh",
        ):
            if parameter in self.params:
                del self.params[parameter]

    def writeStartCode(self, buff):
        """Write code at the beginning of the experiment."""
        original_indent_level = buff.indentLevel

        # Create the initial folder structure
        code = "if expInfo['session']:\n"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(1, relative=True)
        code = (
            "bids_handler = BIDSHandler(dataset=%(dataset_name)s,\n"
            " subject=expInfo['participant'], task=expInfo['expName'],\n"
            " session=expInfo['session'], data_type=%(data_type)s, acq=%(acq)s,\n"
            " runs=%(runs)s)\n"
        )
        buff.writeIndentedLines(code % self.params)
        buff.setIndentLevel(-1, relative=True)

        # Handle case where session is not provided
        code = "else:\n"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(1, relative=True)
        code = (
            "bids_handler = BIDSHandler(dataset=%(dataset_name)s,\n"
            " subject=expInfo['participant'], task=expInfo['expName'],\n"
            " data_type=%(data_type)s, acq=%(acq)s, runs=%(runs)s)\n"
        )
        buff.writeIndentedLines(code % self.params)
        buff.setIndentLevel(-1, relative=True)

        # Initialize dataset and add license
        code = "bids_handler.createDataset()\n"
        if self.params["bids_license"] not in ["", None]:
            code += "bids_handler.addLicense(%(bids_license)s, force=True)\n"
        buff.writeIndentedLines(code % self.params)

        # Add task code if enabled
        if self.params["add_code"]:
            code = "bids_handler.addTaskCode(force=True)\n"
            buff.writeIndentedLines(code % self.params)

        # Add environment if enabled
        if self.params["add_environment"]:
            code = "bids_handler.addEnvironment()\n"
            buff.writeIndentedLines(code % self.params)

        # Add dataset description if provided
        if self.params["dataset_description"].val not in ["", None]:
            code = "bids_handler.addDatasetDescription(%(dataset_description)s, force=True)\n"
            buff.writeIndentedLines(code % self.params)
        buff.setIndentLevel(original_indent_level)

    def writeExperimentEndCode(self, buff):
        """Write code at the end of the routine."""
        original_indent_level = buff.indentLevel

        code = "ignore_list = [\n"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(1, relative=True)
        code = (
            "'participant',\n"
            "'session',\n"
            "'date',\n"
            "'expName',\n"
            "'psychopyVersion',\n"
            "'OS',\n"
            "'frameRate'\n"
        )
        buff.writeIndentedLines(code)
        buff.setIndentLevel(-1, relative=True)
        code = "]\nparticipant_info = {\n"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(1, relative=True)
        code = (
            "key: thisExp.extraInfo[key]\n"
            "for key in thisExp.extraInfo\n"
            "if key not in ignore_list\n"
        )
        buff.writeIndentedLines(code)
        buff.setIndentLevel(-1, relative=True)
        code = "}\n# write tsv file and update\ntry:\n"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(1, relative=True)
        code = (
            "if any(isinstance(item, BIDSBehEvent) for item in bids_handler.events):\n"
        )
        buff.writeIndentedLines(code)
        buff.setIndentLevel(1, relative=True)
        code = "event_file = bids_handler.writeBehEvents(participant_info)\n"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(-1, relative=True)
        code = "else:\n"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(1, relative=True)
        code = "event_file = bids_handler.writeTaskEvents(participant_info)\n"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(-1, relative=True)
        code = "bids_handler.addJSONSidecar(\n"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(1, relative=True)
        code = "event_file,\n%(event_json)s,\nthisExp.extraInfo['psychopyVersion']\n"
        buff.writeIndentedLines(code % self.params)
        buff.setIndentLevel(-1, relative=True)
        code = ")\nbids_handler.addStimuliFolder(event_file)\n"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(-1, relative=True)
        code = "except KeyError:\n"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(1, relative=True)
        code = "pass\n"
        buff.writeIndentedLines(code)
        buff.setIndentLevel(original_indent_level)
