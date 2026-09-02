song_id : The in-game song ID
Difficulty: Apparently PST,PRS,FTR,BYD,ETR,INS map to 0:5 (not sure about the 5)
modifier: idk what the hell does that mean, randomly 0 and 2.
rating: the play rating (Cool!)
score: duh
perfec count: pure
near cound: far
miss count: lost
clear type: I don't really know what this maps to. But we know that it's the clear types
title: Title with localization
artist: uk
time played: the unix timestamp for the play
bg: probably an md5 code for the in game oggs or something

---

What we can use:
The song_id will be used to tie things together accross tables
we should map difficulties using a bin
note count by merging the 3 counts
we can also cmerge the cc. though probably not needed in the b50

actually. I shouldn't try scraping the b50 at all. The chart data should be enough
