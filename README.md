# Label Generator :label:

---

- [Label Generator :label:](#label-generator-label)
  - [Usage](#usage)
  - [Development installation :cd:](#development-installation-cd)
  - [Build](#build)
    - [Python](#python)
    - [Docker](#docker)
  - [Execution](#execution)
    - [Python :snake:](#python-snake)
      - [Generate single label:](#generate-single-label)
    - [Docker :package:](#docker-package)
      - [Generating a single label:](#generating-a-single-label)
      - [Generating labels from a CSV file:](#generating-labels-from-a-csv-file)
  - [Notes :bookmark\_tabs:](#notes-bookmark_tabs)
  - [FAQ :raising\_hand\_woman::raising\_hand\_man:](#faq-raising_hand_womanraising_hand_man)
  - [Support :mechanic:](#support-mechanic)
  - [Contributing](#contributing)
  - [License](#license)

---

## Usage

```console
Options:
  -t, --text TEXT         Text to add on the label (Max. 86 characters). This
                          option is mutually exclusive with 'from_csv'.
  --from_csv PATH         Read labels to create from '.csv' file. This option
                          is mutually exclusive with 'text', 'qr_data'.
  -o, --output_path PATH  Full path where to create the image
  --font PATH             Font path to be use.
  --qr_data TEXT          Data to embed on the label as QR code. This option
                          is mutually exclusive with 'from_csv'.
  -ls, --label_size <FLOAT FLOAT>...
                                  Size in millimeters of the labels (Width,
                                  Height)
  -v, --verbose           Sets the debug noise level, specify multiple times
                          for more verbosity.  [0<=x<=3]
  -h, --help              Show this message and exit.
```

## Development installation :cd:

This step is not mandatory as we'll be heavily using docker for development and for executing the code on this repository.

- Clone this repository
  - `git clone https://github.com/yeyeto2788/LabelGenerator.git`
- Create the virtual environment and activate it
  - `poetry shell`
- Install dependencies
  - `poetry install --group dev`
- Instantiate the pre-commit plugin (Optional)
  - `poetry run pre-commit install`

---

## Build

### Python

For building the python package is as simple as executing the following command:

```console
poetry build
```

### Docker

In order to build the docker image you need to execute the following commands

```console
GENERATOR_VERSION=$(python -c "import pkg_resources;print(pkg_resources.get_distribution('label_generator').version)")
docker build --tag label_generator:$GENERATOR_VERSION .
```

---

## Execution

### Python :snake:

#### Generate single label:

```console
python ./label_generator/cli.py --text "TEXT FOR LABEL" --qr_data "https://myawesomecode.com" -ls 160 40
```

![Custom size label](docs/images/sample_execution_custom_size.png)

### Docker :package:

#### Generating a single label:

```console
docker run --rm  -v $PWD/output:/tmp label_generator:$GENERATOR_VERSION --text "TEXT FOR LABEL" --qr_data "https://myawesomecode.com" -o /tmp/label1.png
```

![Single label generated](docs/images/sample_execution.png)

#### Generating labels from a CSV file:

```console
docker run --rm  -v $PWD/output:/tmp label_generator:$GENERATOR_VERSION --from_csv /tmp/sample.csv -o /tmp/label.png
```

![Labels generated from csv file](./docs/images/sample_csv_execution.png)

---

## Notes :bookmark_tabs:

- Export the `setup.py` if changes are applied to the script
  ```console
  poetry build
  tar -xvf dist/*.tar.gz --wildcards --no-anchored '*/setup.py' --strip=1
  ```

---

<!-- Frequently asked questions -->

## FAQ :raising_hand_woman::raising_hand_man:

No frequently asked question yet. :neutral_face:

---

<!-- Support -->

## Support :mechanic:

Reach out to me at one of the following places!

- Website at [juanbiondi.com](https://www.juanbiondi.com) (Work In Progess)
- Create an [issue](https://github.com/yeyeto2788/LabelGenerator/issues/new/choose) on this repository. :pirate_flag:
- Send me an [email](mailto:jebp.freelance@gmail.com) :email:

---

<!-- Contributing -->

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/super_awesome_feature`)
3. Commit your Changes (`git commit -m 'Add some awesome feature'`)
4. Push to the Branch (`git push origin feature/super_awesome_feature`)
5. Open a Pull Request

---

<!-- License -->

## License

See [**`LICENSE`**](./LICENSE) for more information.
