# deepdonald

Tweeting like Donald Trump!

I used the fastai library to train an AWD_LSTM on Donald Trump's tweets from 2009 to 2018, retrieved from the 
[Trump Tweet Data Archive](https://github.com/bpb27/trump_tweet_data_archive).  All steps to create the model are included
in the Jupyter notebook.

The model is used to power a webapp (https://deepdonald.appspot.com) and a twitter bot (https://twitter.com/RNN_DonaldTrump).
On twitter, you can tweet a few words to @RNN_DonaldTrump, and the bot should respond in a few minutes.
