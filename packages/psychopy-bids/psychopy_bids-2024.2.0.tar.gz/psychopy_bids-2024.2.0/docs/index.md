# Home

A [PsychoPy](https://www.psychopy.org/) plugin to work with the [Brain Imaging Data Structure (BIDS)](https://bids-specification.readthedocs.io/)

* **Website:** [https://psygraz.gitlab.io/psychopy-bids](https://psygraz.gitlab.io/psychopy-bids)
* **Documentation:** [https://psychopy-bids.readthedocs.io](https://psychopy-bids.readthedocs.io)
* **Source code:** [https://gitlab.com/psygraz/psychopy-bids](https://gitlab.com/psygraz/psychopy-bids)
* **Bug reports:** [https://gitlab.com/psygraz/psychopy-bids/issues](https://gitlab.com/psygraz/psychopy-bids/issues)

## Installation

```console
pip install psychopy-bids
```

For more detailed installation instructions, including guidance on setting up a virtual environment and additional configuration options, visit the [Installation Guide](./installation.md) in the documentation.

## Usage

The psychopy bids plugin can be used to create valid BIDS valid datasets by creating [behavioral](https://bids-specification.readthedocs.io/en/stable/modality-specific-files/behavioral-experiments.html#example-_behtsv) or [task events](https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/05-task-events.html) in Psychopy. This can be done directly in python code or using the psychopy builder.

In code, the *BIDSHandler* can create or extend an existing BIDS dataset, including directory structure and necessary metadata files. Individual BIDS events can be added during the experiment and are passed to the *BIDSHandler* to write event `.tsv` files and accompanying `.json` files.

```py
from psychopy_bids import bids

handler = bids.BIDSHandler(dataset="example_dataset", subject="01", task="A")
handler.createDataset()

events = [
    bids.BIDSTaskEvent(onset=1.0, duration=0.5, event_type="stimulus", response="correct"),
    bids.BIDSTaskEvent(onset=1.0, duration=0, trial_type="trigger")
]

for event in events:
    handler.addEvent(event)

participant_info = {"participant_id": handler.subject, "age": 18}

handler.writeTaskEvents(participant_info=participant_info)

handler.addStimuliFolder(event_file="example_dataset/sub-01/beh/sub-01_task-A_run-1_events.tsv")
handler.addEnvironment()
handler.addTaskCode()
```

In the builder, you can now use the newly added **BIDS components** to add events to a BIDS dataset. The previously used components—**BIDS Task Event** and **BIDS Beh Event**—are deprecated and retained only for backward compatibility.

![BIDS components](./image/index/home-fig01.png)

You can now select the **BIDS Event Type** directly in the **BIDS Event Properties**, streamlining the process.

![BIDS Event Component](./image/index/home-fig02.png)


Using features such as custom columns it is possible to create detailed event tables for BIDS data.

| onset   | duration | event_role  | word             | color | pressed_key | trial_type  | response_time | trial_number | response_accuracy |
| :------ | :------- | :---------- | :--------------- | :---- | :---------- | :---------- | :------------ | :----------- | :---------------- |
| 15.2876 | 1.2295   | instruction | instruction_text | black | space       | n/a         | 1.2295        | n/a          | n/a               |
| 16.5171 | n/a      | response    | n/a              | n/a   | space       | n/a         | 1.2295        | n/a          | n/a               |
| 16.538  | 0.5      | fixation    | +                | black | n/a         | n/a         | n/a           | n/a          | n/a               |
| 17.0593 | 0.8105   | stimulus    | Red              | green | left        | incongruent | 0.8105        | 1.0          | correct           |
| 17.8698 | n/a      | response    | Red              | green | left        | incongruent | 0.8105        | 1.0          | correct           |
| 17.8972 | 1.0      | feedback    | Correct!         | green | n/a         | incongruent | n/a           | 1.0          | n/a               |
| 18.9272 | 0.5      | fixation    | +                | black | n/a         | n/a         | n/a           | n/a          | n/a               |

Please see individual tutorials for using psychopy bids in [code](./coder.md) or the [psychopy builder](./builder.md).

## Contributing

Interested in contributing? Check out the [contributing guidelines](./contributing.md). Please note that this project is released with a [Code of Conduct](./conduct.md). By contributing to this project, you agree to abide by its terms.

## License

`psychopy-bids` was created by Christoph Anzengruber & Florian Schöngaßner. It is licensed under the terms of the GNU General Public License v3.0 license.

## Credits

`psychopy-bids` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
