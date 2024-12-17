import doctest
import os
import shutil
import subprocess
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd

from psychopy_bids import bids


class TestBIDSHandler(unittest.TestCase):

    def setUp(self):
        self.example_dataset = "example_dataset"
        if os.path.exists(self.example_dataset):
            shutil.rmtree(self.example_dataset)

    # -------------------------------------------------------------------------------------------- #

    def tearDown(self):
        if os.path.exists(self.example_dataset):
            shutil.rmtree(self.example_dataset)

    # -------------------------------------------------------------------------------------------- #

    def test_init(self):
        with self.assertRaises(TypeError):
            bids.BIDSHandler()
            bids.BIDSHandler(dataset=self.example_dataset)
            bids.BIDSHandler(subject="A")
            bids.BIDSHandler(task="A")
            bids.BIDSHandler(dataset=self.example_dataset, subject="A")
            bids.BIDSHandler(dataset=self.example_dataset, task="A")
            bids.BIDSHandler(subject="A", task="A")

    # -------------------------------------------------------------------------------------------- #

    def test_addChanges(self):
        subject = {"participant_id": "01", "sex": "male", "age": 20}

        handler = bids.BIDSHandler(
            dataset=self.example_dataset,
            subject=subject["participant_id"],
            task="task1",
        )
        handler.createDataset()
        handler.addChanges(["Init dataset"], version="MAJOR")
        handler.addChanges(["Added subject"], version="MINOR")
        handler.addChanges(["Added session"], version="PATCH")

    # -------------------------------------------------------------------------------------------- #

    def test_addDatasetDescription(self):
        subject = {"participant_id": "01", "sex": "male", "age": 20}

        handler = bids.BIDSHandler(
            dataset=self.example_dataset,
            subject=subject["participant_id"],
            task="task1",
        )
        handler.createDataset()
        handler.addDatasetDescription()
        handler.addDatasetDescription(force=True)

    # -------------------------------------------------------------------------------------------- #

    def test_addLicense(self):
        subject = {"participant_id": "01", "sex": "male", "age": 20}

        handler = bids.BIDSHandler(
            dataset=self.example_dataset,
            subject=subject["participant_id"],
            task="task1",
        )
        handler.createDataset(lic=False, force=True)

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            handler.addLicense(identifier="ABC")
        expected = "License 'ABC' not found or could not be downloaded.\n"
        actual = mock_stderr.getvalue()
        self.assertEqual(expected, actual)

        handler.addLicense(identifier="CC0-1.0")
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            handler.addLicense(identifier="CC0-1.0")
        expected = "File 'LICENSE' already exists, use force for overwriting it!\n"
        actual = mock_stderr.getvalue()
        self.assertEqual(expected, actual)
        handler.addLicense(identifier="CC0-1.0", force=True)

    # -------------------------------------------------------------------------------------------- #

    def test_addReadme(self):
        subject = {"participant_id": "01", "sex": "male", "age": 20}

        handler = bids.BIDSHandler(
            dataset=self.example_dataset,
            subject=subject["participant_id"],
            task="task1",
        )
        handler.createDataset(force=True)
        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            handler.addReadme()
        expected = "File 'README' already exists, use force for overwriting it!\n"
        actual = mock_stderr.getvalue()
        self.assertEqual(expected, actual)

    # -------------------------------------------------------------------------------------------- #

    def test_addStimuliFolder(self):
        subject = {"participant_id": "01", "sex": "male", "age": 20}

        handler = bids.BIDSHandler(
            dataset=self.example_dataset,
            subject=subject["participant_id"],
            task="task1",
        )
        handler.createDataset(force=True)

        image = bids.BIDSTaskEvent(
            onset=0,
            duration=0,
            trial_type="start",
            stim_file="images/orig_BIDS.png",
        )
        handler.addEvent(image)

        error = bids.BIDSTaskEvent(
            onset=0, duration=0, trial_type="start", stim_file="orig_BIDS.png"
        )
        handler.addEvent(error)

        tsv_file = handler.writeTaskEvents(participant_info=subject)

        handler.addStimuliFolder(tsv_file, "tests")

        self.assertIn("stimuli", os.listdir(self.example_dataset))
        self.assertEqual(
            os.listdir(f"{self.example_dataset}{os.sep}stimuli{os.sep}images"),
            ["orig_BIDS.png"],
        )

        with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
            handler.addStimuliFolder(tsv_file, "tests")
            expected_path = os.path.join("tests", "orig_BIDS.png")
            expected = f"File '{expected_path}' does not exist!\n"
            actual = mock_stderr.getvalue()
            self.assertEqual(expected, actual)

    # -------------------------------------------------------------------------------------------- #

    def test_addTaskCode(self):
        subject = {"participant_id": "01", "sex": "male", "age": 20}

        handler = bids.BIDSHandler(
            dataset=self.example_dataset,
            subject=subject["participant_id"],
            task="task1",
        )
        handler.createDataset(force=True)

        handler.addTaskCode(path="tests/bids_validator/experiment_lastrun.py")

        code_dir = Path(self.example_dataset) / "code"
        expected_file = code_dir / "experiment_lastrun.py"

        self.assertTrue(
            expected_file.exists(), f"File {expected_file} was not found in /code."
        )

    # -------------------------------------------------------------------------------------------- #

    def test_addEnvironment(self):
        subject = {"participant_id": "01", "sex": "male", "age": 20}

        handler = bids.BIDSHandler(
            dataset=self.example_dataset,
            subject=subject["participant_id"],
            task="task1",
        )
        handler.createDataset(force=True)
        handler.addEnvironment()

        # Verify `requirements.txt` was created
        requirements_path = os.path.join(self.example_dataset, "requirements.txt")
        assert os.path.exists(
            requirements_path
        ), "requirements.txt file was not created."

        # Verify `requirements.txt` content
        with open(requirements_path, "r") as f:
            content = f.read().strip()
        assert content, "requirements.txt is empty."
        assert (
            "# Python version:" in content
        ), "Python version is missing in requirements.txt."

        # Dynamically check for any package from `pip freeze` output
        pip_freeze_output = subprocess.run(
            ["pip", "freeze"], stdout=subprocess.PIPE, text=True, check=True
        ).stdout.strip()
        installed_packages = [
            line.split("==")[0] for line in pip_freeze_output.splitlines()
        ]
        requirements_packages = [
            line.split("==")[0] for line in content.splitlines() if "==" in line
        ]

        # Assert that at least one package from the current environment is present in `requirements.txt`
        assert any(
            pkg in requirements_packages for pkg in installed_packages
        ), "No common packages found between pip freeze and requirements.txt"

        # Verify `.bidsignore` was updated
        bidsignore_path = os.path.join(self.example_dataset, ".bidsignore")
        assert os.path.exists(bidsignore_path), ".bidsignore file was not created."
        with open(bidsignore_path, "r") as f:
            bidsignore_content = f.read()
        assert (
            "requirements.txt" in bidsignore_content
        ), "requirements.txt not added to .bidsignore."

    # -------------------------------------------------------------------------------------------- #

    def test_addTaskCode(self):
        subject = {"participant_id": "01", "sex": "male", "age": 20}

        handler = bids.BIDSHandler(
            dataset=self.example_dataset,
            subject=subject["participant_id"],
            task="task1",
        )
        handler.createDataset(force=True)

        handler.addTaskCode(path="tests/bids_validator/experiment_lastrun.py")
        code_dir = Path(self.example_dataset) / "code"
        expected_file = code_dir / "experiment_lastrun.py"

        self.assertTrue(
            expected_file.exists(), f"File {expected_file} was not found in /code."
        )

    # -------------------------------------------------------------------------------------------- #
    def test_checkDSwithAcq(self):
        subject = {"participant_id": "01", "sex": "male", "age": 20}

        start = bids.BIDSTaskEvent(onset=0, duration=0, trial_type="start")
        presentation = bids.BIDSTaskEvent(
            onset=0.5, duration=5, trial_type="presentation"
        )
        stop = bids.BIDSTaskEvent(onset=10, duration=0, trial_type="stop")

        events = [start, presentation, stop]

        handler = bids.BIDSHandler(
            dataset=self.example_dataset,
            subject=subject["participant_id"],
            acq="highres",
            task="task1",
        )
        handler.createDataset()

        for event in events:
            handler.addEvent(event)

        tsv_file = handler.writeTaskEvents(participant_info=subject)
        handler.addJSONSidecar(tsv_file)
        self.assertEqual(
            set(os.listdir(self.example_dataset)),
            set(
                [
                    "CHANGES",
                    "dataset_description.json",
                    "LICENSE",
                    "participants.json",
                    "participants.tsv",
                    "README",
                    "sub-01",
                ]
            ),
        )
        self.assertEqual(os.listdir(f"{self.example_dataset}{os.sep}sub-01"), ["beh"])
        self.assertEqual(
            set(os.listdir(f"{self.example_dataset}{os.sep}sub-01{os.sep}beh")),
            set(
                [
                    "sub-01_task-task1_acq-highres_run-1_events.json",
                    "sub-01_task-task1_acq-highres_run-1_events.tsv",
                ]
            ),
        )

    # -------------------------------------------------------------------------------------------- #

    def test_checkDSMultipleSessions(self):
        subject = {"participant_id": "01", "sex": "male", "age": 20}

        start = bids.BIDSTaskEvent(onset=0, duration=0, trial_type="start")
        presentation = bids.BIDSTaskEvent(
            onset=0.5, duration=5, trial_type="presentation"
        )
        stop = bids.BIDSTaskEvent(onset=10, duration=0, trial_type="stop")

        events = [start, presentation, stop]

        handler1 = bids.BIDSHandler(
            dataset=self.example_dataset,
            subject=subject["participant_id"],
            session="1",
            task="task1",
        )
        handler1.createDataset()
        for event in events:
            handler1.addEvent(event)
        tsv_file1 = handler1.writeTaskEvents(participant_info=subject)
        handler1.addJSONSidecar(tsv_file1)
        handler2 = bids.BIDSHandler(
            dataset=self.example_dataset,
            subject=subject["participant_id"],
            session="2",
            task="task1",
        )
        handler2.createDataset(chg=False, readme=False, lic=False, force=False)
        for event in events:
            handler2.addEvent(event)
        tsv_file2 = handler2.writeTaskEvents(participant_info=subject)
        handler2.addJSONSidecar(tsv_file2)
        self.assertEqual(
            set(os.listdir(self.example_dataset)),
            set(
                [
                    "CHANGES",
                    "dataset_description.json",
                    "LICENSE",
                    "participants.json",
                    "participants.tsv",
                    "README",
                    "sub-01",
                ]
            ),
        )
        self.assertEqual(
            sorted(os.listdir(f"{self.example_dataset}{os.sep}sub-01")),
            sorted(["ses-1", "ses-2"]),
        )
        self.assertEqual(
            set(
                os.listdir(f"{self.example_dataset}{os.sep}sub-01{os.sep}ses-1{os.sep}beh")
            ),
            set(
                [
                    "sub-01_ses-1_task-task1_run-1_events.json",
                    "sub-01_ses-1_task-task1_run-1_events.tsv",
                ]
            ),
        )
        self.assertEqual(
            set(
                os.listdir(f"{self.example_dataset}{os.sep}sub-01{os.sep}ses-2{os.sep}beh")
            ),
            set(
                [
                    "sub-01_ses-2_task-task1_run-1_events.json",
                    "sub-01_ses-2_task-task1_run-1_events.tsv",
                ]
            ),
        )

    # -------------------------------------------------------------------------------------------- #

    def test_checkDSMultipleSubjects(self):
        subject1 = {"participant_id": "01", "sex": "male", "age": 20}
        subject2 = {"participant_id": "02", "sex": "female", "age": 22}

        start = bids.BIDSBehEvent(onset=0, duration=0, trial_type="start")
        presentation = bids.BIDSBehEvent(
            onset=0.5, duration=5, trial_type="presentation"
        )
        stop = bids.BIDSBehEvent(onset=10, duration=0, trial_type="stop")

        events = [start, presentation, stop]

        handler1 = bids.BIDSHandler(
            dataset=self.example_dataset,
            subject=subject1["participant_id"],
            task="task1",
            runs=False,
        )
        handler1.createDataset()

        for event in events:
            handler1.addEvent(event)

        tsv_file1 = handler1.writeBehEvents(participant_info=subject1)
        handler1.addJSONSidecar(tsv_file1)

        handler2 = bids.BIDSHandler(
            dataset=self.example_dataset,
            subject=subject2["participant_id"],
            task="task1",
            runs=False,
        )
        handler2.createDataset()

        for event in events:
            handler2.addEvent(event)

        tsv_file2 = handler2.writeBehEvents(participant_info=subject2)
        handler2.addJSONSidecar(tsv_file2)

        self.assertEqual(
            set(os.listdir(self.example_dataset)),
            set(
                [
                    "CHANGES",
                    "dataset_description.json",
                    "LICENSE",
                    "participants.json",
                    "participants.tsv",
                    "README",
                    "sub-01",
                    "sub-02",
                ]
            ),
        )
        self.assertEqual(os.listdir(f"{self.example_dataset}{os.sep}sub-01"), ["beh"])
        self.assertEqual(
            set(os.listdir(f"{self.example_dataset}{os.sep}sub-01{os.sep}beh")),
            set(
                [
                    "sub-01_task-task1_beh.json",
                    "sub-01_task-task1_beh.tsv",
                ]
            ),
        )
        self.assertEqual(os.listdir(f"{self.example_dataset}{os.sep}sub-02"), ["beh"])
        self.assertEqual(
            set(os.listdir(f"{self.example_dataset}{os.sep}sub-02{os.sep}beh")),
            set(
                [
                    "sub-02_task-task1_beh.json",
                    "sub-02_task-task1_beh.tsv",
                ]
            ),
        )

    # -------------------------------------------------------------------------------------------- #

    def test_parseLog(self):
        handler = bids.BIDSHandler(
            dataset=self.example_dataset,
            subject="01",
            task="task1",
        )

        # Define the log file paths
        script_dir = Path(__file__).parent
        simple1_log = f"{script_dir}{os.sep}simple1.log"
        simple2_log = f"{script_dir}{os.sep}simple2.log"
        simple3_log = f"{script_dir}{os.sep}simple3.log"

        # Test with simple1.log
        events = handler.parseLog(simple1_log)
        self.assertEqual(len(events), 3)

        # Test with simple2.log and a regex
        regex = r"duration-(?P<duration>\d{1})_trial-(?P<trial>\d{1})"
        events = handler.parseLog(simple2_log, regex=regex)
        self.assertEqual(len(events), 3)

        # Test with simple3.log expecting a warning
        with self.assertWarns(UserWarning):
            events = handler.parseLog(simple3_log)

    # -------------------------------------------------------------------------------------------- #

    def test_subject(self):
        handler = bids.BIDSHandler(
            dataset=self.example_dataset, subject="sub-01", task="A"
        )
        self.assertEqual(handler.subject, "sub-01")
        handler = bids.BIDSHandler(dataset=self.example_dataset, subject="01", task="A")
        self.assertEqual(handler.subject, "sub-01")

    # -------------------------------------------------------------------------------------------- #

    def test_task(self):
        handler = bids.BIDSHandler(
            dataset=self.example_dataset, subject="01", task="task-A"
        )
        self.assertEqual(handler.task, "task-A")
        handler = bids.BIDSHandler(dataset=self.example_dataset, subject="01", task="A")
        self.assertEqual(handler.task, "task-A")

    # -------------------------------------------------------------------------------------------- #

    def test_session(self):
        handler = bids.BIDSHandler(
            dataset=self.example_dataset, subject="01", task="A", session="ses-1"
        )
        self.assertEqual(handler.session, "ses-1")
        handler = bids.BIDSHandler(
            dataset=self.example_dataset, subject="01", task="A", session="1"
        )
        self.assertEqual(handler.session, "ses-1")

    # -------------------------------------------------------------------------------------------- #

    def test_data_type(self):
        handler = bids.BIDSHandler(
            dataset=self.example_dataset,
            subject="01",
            task="A",
            session="1",
            data_type="beh",
        )
        dt = [
            "anat",
            "beh",
            "dwi",
            "eeg",
            "fmap",
            "func",
            "ieeg",
            "meg",
            "micr",
            "perf",
            "pet",
        ]
        self.assertTrue(handler.data_type in dt)
        with self.assertRaises(SystemExit):
            bids.BIDSHandler(
                dataset=self.example_dataset,
                subject="01",
                task="A",
                session="1",
                data_type="abc",
            )

    # -------------------------------------------------------------------------------------------- #

    def test_acq(self):
        handler = bids.BIDSHandler(
            dataset=self.example_dataset, subject="01", task="A", acq="acq-1"
        )
        self.assertEqual(handler.acq, "acq-1")
        handler = bids.BIDSHandler(
            dataset=self.example_dataset, subject="01", task="A", acq="1"
        )
        self.assertEqual(handler.acq, "acq-1")

    # -------------------------------------------------------------------------------------------- #

    def test_doc_strings(self):
        """
        Test docstrings using doctest and pytest.
        We are also mocking file paths and a dataframe for successful tests.
        """
        mock_df = pd.DataFrame(
            {"participant_id": [1, 2, 3], "other_column": ["a", "b", "c"]}
        )

        with patch("pandas.read_csv", MagicMock(return_value=mock_df)):
            results = doctest.testmod(
                bids.bidshandler,
                globs={
                    "bids": bids,
                    "BIDSHandler": bids.BIDSHandler,
                    "BIDSBehEvent": bids.BIDSBehEvent,
                    "BIDSTaskEvent": bids.BIDSTaskEvent,
                },
            )

        self.assertEqual(
            results.failed,
            0,
            f"{results.failed} doctests failed out of {results.attempted}.",
        )


# ----------------------------------------------------------------------------------------------- #


if __name__ == "__main__":
    unittest.main()
