# Minimap analyser

![Pylint](https://github.com/Deuzwood/minimap-analyser/workflows/Pylint/badge.svg)

Minimap analyser for the game League of Legends. This repo is using some content from [TrainYourOwnYOLO](https://github.com/AntonMu/TrainYourOwnYOLO) (Mainly for "2_Training" and "3_Inference").

## Use

You can follow the Jupyter Notebook file with Google Colab. If you are using it on a personal machine a list of dependencies is given ( follow env section ).
If you plan to generate Confusion Matrix and mAP, we are using code from different repo. Any issues with these repo can be solve checking orignal repo.

## env

```
python3 -m venv env
source env/bin/activate
```

Then install module for your env with

`pip install -r requirements.txt`


## Code Used
- [TrainYourOwnYOLO](https://github.com/AntonMu/TrainYourOwnYOLO)
- [Confusion Matrix for Object Detection Models](https://github.com/Mr-TalhaIlyas/Confusion_Matrix_for_Objecti_Detection_Models)
- [mAP (mean Average Precision)](https://github.com/Cartucho/mAP)



## Authors

-   Nicolas **Wallet**
-   Pierre **Skibinski**
