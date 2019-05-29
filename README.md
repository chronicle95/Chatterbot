# Chatterbot

This is a simple chatterbot program.
It is clever enough to recognize short phrases, but way too stupid to keep the meaningful conversation up.

The bot uses vector distance algorithm. It converts the words into numbers and makes vectors out of them. By fuzzily comparing question vectors it finds the best answers and then randomly chooses one so that each conversation is somehow different.

It has no personality from the start. You should manually teach it, or try loading some chat logs. 

_Why Kurisu? - I originally intended to make the bot just to imitate Makise Kurisu from Steins;Gate, but in the process of writing and debugging code, it came clear that the program is more universal than I originally thought. So the naming is there for historical reasons and I won't change it._
