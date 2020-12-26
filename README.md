# Last Price Sec Saver

Gets specified stock prices each second & saves it to a mysql database.

I can't find reliable data like this anywhere online...
Usually this data is available as "tick" data... Or if it is available as per "second" data, there's often times huge gaps missing every few minutes... Which just isn't sufficient for my needs.
Realistically, you can only query the API every ~1sec (I don't own a high frequency firm with microsecond latency to stock exchange servers, so going down to the 'tick' is unrealistic, and unnecessary)... Thus "tick" data isn't sufficient, thus the development of this application.
