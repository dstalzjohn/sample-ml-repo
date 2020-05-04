# sample-ml-repo

## Overview

This is a repo to get you started right away with your ML project!

Advantages:

- With the use of kedro you are production ready
- Reproducibility with storing the commit-hash for each experiment
- Using streamlit instead of notebooks to visualize your results right away

## Installation

- Install [python-poetry](https://python-poetry.org/docs/) on your computer 
- Clone the following repos:
  - [ccmlutils](git@github.com:JohnDenis/ccmlutils.git)
  - [sample-ml-project](git@github.com:JohnDenis/sample-ml-repo.git)
- To create a python environment do ```poetry install``` in your working directory.
- ```WORKING_DIR``` directory of the sample-ml-repo
- Set your project dependency such that it includes ```ccmlutils``` in the ```PYTHONPATH``` (either in your IDE or the CL)
- Rename ```samplemlproject``` to your desired name at following occurrences:
  - folder in the main project (do a refactoring)
  - ```parameters.yml```
  - ```pre-commit-hook.sh```
  - ```.kedro.yml```
  - ```run.py```
- Change the origin location in ```.git/config```


## Run the sample code

- Download the dataset [Fruits360](https://www.kaggle.com/moltean/fruits)
- After extraction change parameter in ```catalog.yml```
- Use ```kedro run``` in the working dir to run the default pipeline
- Attention to your dependency and set python environment (```poetry shell``` gives you the correct one)
- For visualization: ```PYTHONPATH=".:../ccmlutils" streamlit run samplemlproject/visualization/train_visu.py```
- The experiment results are stored at ```experiment_outputs``` (each experiment has its own folder)


## Points of entry

- You can define your own pipeline in ```pipeline.py```


## Technologies

- [Poetry](https://python-poetry.org)
- [Kedro](https://kedro.readthedocs.io)
- [Streamlit](https://www.streamlit.io)
- [Altair](https://altair-viz.github.io)
- [DVC](https://dvc.org)
- [Keras](https://keras.io)

