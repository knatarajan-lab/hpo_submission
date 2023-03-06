## Run submission pipeline

### Get Started

#### Install dependencies
```
pip install -r requirements.txt
```

#### Create folder for holding final submission files
```
mkdir submission_folder
```
#### Fill in the config file with your database credentials in `a_dm_aou.ini` file
```
[DEFAULT]
server =
database =
schema =
user =
password =
```

#### Run pipeline
```
sh run_pipeline.sh
```

### aou-ehr-file-check

This is a submodule included to check the format of submission files. It is initialized and updated 
from [aou-ehr-file-check](https://github.com/all-of-us/aou-ehr-file-check) repo.

In order to initialize and update the submodule, run the following commands:

#### Initialize submodule
```
git submodule update --init
```

#### Update submodule contents
```
git submodule sync
git submodule update --remote --merge
```

### Submit to the All of Us Research Program
You will find the submission files in folder `submission_folder`.

Please follow the steps described in [Transferring Data to the DRC](https://aou-ehr-ops.zendesk.com/hc/en-us/articles/1500012461721-Transferring-Data-to-the-DRC) to submit your data to the All of Us Research Program.