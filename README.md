# Celebrity Identification Quest
Do you think you know celebrities well? You can identify every actor in a film?

This game is for you!

Celebrity Identification Quest is a daily game that tests your memory on faces of film celebrities

# Installation
## **To run Streamlit app locally:**
1. Install the packages in your environment:
    - Streamlit v.1.23.1
    - Pandas v.1.4.4
    - NumPy v.1.23.4
    - plotly v.5.9.0

2. Pull the repo

3. Execute the following line in your Linux terminal while at folder with the game:
```
streamlit run interface.py
```
## **For online version follow the link**:

https://celebrity-identification-quest.streamlit.app/

## **Requirements for notebooks**:

If you would like to play with our notebooks for data retrieval and processing you should have the following packages installed:

- Pandas v.1.4.4
- NumPy v.1.23.4
- plotly v.5.9.0
- Scikit-learn v.1.2.2
- DeepFace v.0.0.79
- opencv-python v.4.7.0.72
- SPARQLWrapper v.2.0.0
- cinemagoer v2023.5.1
- dlib v.19.24.2

# Rules of the Game:
## Objective:
The main objective of the game is to correctly identify the hidden celebrity by making educated guesses
based on the provided images.
## How it works:
To make a guess, you need to select from our list of celebrities the one that you believe
resemble the hidden personality. The game will analyze your choice and provide you with a score of similarity,
indicating how close your guess is to the correct answer. This score will help you refine your future guesses. CIQ isn't it?
## Visual progress:
You can track your progress not only in the table but also with our radar-like map. It's a polar plot where radius is the similarity of celebrity to a hidden celebrity and angle is shows how other celebrities are different from each other. Red points represent celebrities you have already tried and the blue points represent the rest of our celebrity database. The closer a point to the centre the higher the resemblence. It is normal that at some point there is a huge gap betweeen the hidden celebrity and other celebrities as not every person has a famous sibling or a doppelganger.
## Hint Button:
If you stack you can use our hints.
Every time you click hint button you get a piece of information about the hidden celebrity: first gender then occupation,
citizenship, and age.

# Further ideas:
Currently the celebrities databse is rather scanty and limited to only a small set of celebrities that is
mostly formed from Top-100 actors and actresses of all time. So later on we will add more celebrities to make it easier to play.

# Backend info
## Image retrieval and processing
Currently the images of celebrities are retrieved from IMDB and processing is performed via OpenCV to crop and align faces as these factors affect performance of the model immensly.

The hints are generated with the use of WikiData where we query the database and retrieve the info of our interest, namely: gender, occupations, citizenship, and age

## Model
We used pretrained VGG-Face model wrapped into DeepFace package to embed all the celebrities into one multidimensional space. To get similarity score we used cosine distances via sklearn.neighbors as they seem to be the best in terms of providing resonable scores (which is a relatively subjective matter)
## Polar plot
The angle values for the plot are 1D-tSNE values that are normalized to 0 to 360 to distribute within the whole circumference of the plot.
The values for radius are cosine similarities relative to a hidden celebrity. So the hidden celebrity is always at [0,0] and the closer you are to the centre the higher similarity score.

The plot is inspired by a great game callend Pimantle https://semantle.pimanrul.es/ and I thank Jacob Settlemyre for giving me insight on how it was done.

## **Good luck and have fun!**

---
**Author**: Stanislav Kondratev

**Development**: Stanislav Kondratev and Joaquim Albuquerque

**Test**: Carlota Armero and Hena Tabassum
