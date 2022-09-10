# Spotify Music Recommender - Kyle Ness

Imagine you are an avid music listener, but having already explored so many genres and artists, you have no idea where to look next for hot new tracks. In other words, you are facing a plight of overabundance. Do you look deeper into genres you're already accustomed to? Or do you try to find your way by artists? No matter the route taken, finding enjoyable new music is much a task. If only there existed an easy way to search for new songs based on the characteristics of the tracks you already love.

Enter my track recommender!

By taking in a list of songs (or even just one), finding the means of their audio features in aggregate, and subsequently finding the 10 tracks closest in cosine distance to that mean vector, this track recommender is able to provide suggestions based on track content. This means that instead of a user needing to search aimlessly by track metadata or genre for new music, they can simply be served tracks that they are inclined to like on demand. This efficiency introduced to the user is not only good for them, but also helps the streaming company (in this case, Spotify) retain their customers better because they are wasting less time searching and more time enjoying or purchasing products.

Beyond finding new songs, this content-based recommender can also be used for fun in finding hidden relationships between songs. Two songs from two different genres may, in fact, sound exactly the same! There are many possibilities. 

This recommender was created with already scraped Spotify data from Kaggle, Spotipy API pulls, and the use of KMeans and distance modules.

### Dictionary
Note: Data was not uploaded to GitHub due to file size limits. However, they can easily be reproduced by following all steps.
These features are shared betweeen all the datasets used / created (some others exist that are either dropped or are of no importance).

|Feature             |Type  |Description                                                                           |
|--------------------|------|--------------------------------------------------------------------------------------|
|name                |string|The name / title of the track                                                         |
|artists             |string|Artists who are listed as creators on the track                                       |
|year                |int   |Year that the track was released=                                                     |
|genre               |string|Genre of the track                                                                    |
|explicit            |int   |Binary variable describing whether track contains explicit lyrics. 0 = no, 1 = yes    |
|popularity          |int   |Popularity on a scale of 0 - 100. Deteriorates over time -> newer songs biased        |
|danceability        |float |Describes how suitable track is for dancing. 0.0 = least, 1.0 = most                  |
|energy              |float |Perceptual measure of activity and intensity. 0.0 = least, 1.0 = most                 |
|key                 |float |The key the song is in. Integers 1-11 mapping to A-G (including flats, sharps)        |
|loudness            |float |Loudness of the track in decibels (dB)                                                |
|mode                |int   |Modality of track, 0 = minor, 1 = major                                               |
|speechiness         |float |Detects presence of speech in track. >0.66 = mostly words, <0.33 mostly music.        |
|acousticness        |float |Confidence measure of whether the track is acoustic, ranging 0 to 1                   |
|instrumentalness    |float |Predicts whether track contains no vocals, ex: 1 = highly likely there are no vocals  |
|liveness            |float |Detects presence of audience in the recording, above 0.8 = highly likely              |
|valence             |float |Musical positiveness conveyed by a track, ranging 0 to 1                              |
|tempo               |float |Estimated tempo of track in beats per minute (BPM)                                    |
|duration_ms         |int   |Duration of track in milliseconds (ms)                                                |
|time_signature      |int   |Time signature of track, ranging from 3 to 7                                          |


For further information, check Spotify's Web API documentation: https://developer.spotify.com/documentation/web-api/reference/#/

### Build - Summary
Track and artist data was downloaded from Kaggle. These datasets were cleaned of nulls and bad entries, and data types were fixed. Tracks with unknown artists (not contained in artists.csv) were dropped. Post-cleaning, ~489,000 tracks remained for use (a reduction of close to 100,000 tracks from download). This track data was transformed with sklearn's StandardScaler so that distances between track vectors could be more accurately computed. For recommendations, the system first looks to this scaled data to see if the track exists there already (i.e., is it downloaded?). If not, the track and its features are pulled from the Spotify Web API with Spotipy. For a list of songs, this is repeated until all songs' vectors (only the numerical features, scaled) are possessed. A mean vector is produced from this list. Cosine distances are calculated from this vector to every vector in the cleaned, scaled data. The 10 tracks closest to the mean vector are returned. In theory, these closest tracks are very similar in composition, and the user should find them familiar / enjoyable.

Finally, by deploying this system in Streamlit, a user can quickly and easily find new songs.

### Conclusion
Building a new song recommender with Spotify data is both possible and rewarding. Providing good recommendations is great for the company, and receiving good recommendations is great for the users. 

Although some results of this recommender are surprisingly (given the relatively small amount of data) accurate, others may be a bit off. If time allowed, perhaps coming around to a more sophisticated algorithm rather than one that just relies on the mean vector would yield more consistently accurate results. Further, some assumptions made in creating this recommender like that of only considering the first API search result (by popularity) may explain shortcomings. If several songs were to share the same name and release year (like in the case of remixes), recommender may grab the wrong one, for example. Another shortcoming is that recommendations are only sourced from the downloaded data. Searching through all of Spotify's available songs for extremely identical songs would be intensive.

All in all, this system works well enough as an MVP, and goes to show how fun and even lucrative an amazing recommender system can be. Through personalization, the accessibility of music is so much broader. 

### Datasets Sources:
-Obtained 'tracks' and 'artists' datasets from Kaggle: https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks?select=artists.csv
-Song data not contained within the Kaggle sets were gathered via Spotipy: https://spotipy.readthedocs.io/en/master/

### References:
Much inspiration and help came from these various blog posts / links:
-https://www.popsci.com/technology/spotify-audio-recommendation-research/
-https://towardsdatascience.com/how-to-build-an-amazing-music-recommendation-system-4cce2719a572#:~:text=Compute%20the%20average%20vector%20of,the%20songs%20corresponding%20to%20them
-https://www.kaggle.com/code/minc33/visualizing-high-dimensional-clusters/notebook
