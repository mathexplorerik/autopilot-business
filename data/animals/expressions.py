"""
==========================================================
 AI KDP AUTOPILOT V4
 Animal Expressions Library
==========================================================

Version : 1.0
Purpose : Reusable facial expressions and emotions

Rules:
- Kid-friendly
- Easy to recognize
- Easy for AI to illustrate
- Coloring book friendly
- No negative or scary expressions

==========================================================
"""

EXPRESSIONS = {


    "happy": [
    "big smile",
    "gentle smile",
    "cheerful grin",
    "joyful smile",
    "bright smile",
    "warm smile",
    "sweet smile",
    "happy eyes",
    "sparkling eyes",
    "laughing eyes",

    "smiling with closed eyes",
    "smiling with open mouth",
    "toothy grin",
    "friendly smile",
    "delighted expression",
    "content smile",
    "gleeful smile",
    "beaming face",
    "radiant smile",
    "playful grin",

    "laughing happily",
    "giggling",
    "soft laugh",
    "joyful laughter",
    "happy face",
    "cheerful face",
    "smiling proudly",
    "excited smile",
    "adorable smile",
    "cute happy expression"

],

    "excited": [
    "wide excited smile",
    "eyes wide with excitement",
    "sparkling excited eyes",
    "raised eyebrows",
    "open mouth smile",
    "jumping with excitement",
    "cheering happily",
    "clapping excitedly",
    "waving excitedly",
    "bouncing with joy",

    "hands raised happily",
    "tail wagging excitedly",
    "ears perked up",
    "big joyful grin",
    "gleeful expression",
    "thrilled smile",
    "happy surprise",
    "celebration pose",
    "bursting with excitement",
    "joyful laughter",

    "excited giggle",
    "cheering with friends",
    "celebrating happily",
    "playful excitement",
    "energetic smile",
    "enthusiastic expression",
    "bright sparkling face",
    "can't wait expression",
    "full of joy",
    "super excited face"

],

    "curious": [
    "curious smile",
    "head tilted with curiosity",
    "raised eyebrows",
    "wide curious eyes",
    "sparkling curious eyes",
    "looking closely",
    "carefully observing",
    "peeking around a tree",
    "peeking from behind a rock",
    "looking through binoculars",

    "looking through a magnifying glass",
    "studying a butterfly",
    "watching a tiny bug",
    "examining a flower",
    "following tiny footprints",
    "looking at a treasure map",
    "discovering something new",
    "wonder-filled expression",
    "thoughtful curious face",
    "exploring with interest",

    "listening carefully",
    "ears perked up",
    "tail raised with curiosity",
    "nose sniffing the air",
    "looking up in wonder",
    "watching the stars",
    "finding a hidden surprise",
    "investigating happily",
    "playfully exploring",
    "adorable curious expression"

],

    "playful": [
    "curious smile",
    "head tilted with curiosity",
    "raised eyebrows",
    "wide curious eyes",
    "sparkling curious eyes",
    "looking closely",
    "carefully observing",
    "peeking around a tree",
    "peeking from behind a rock",
    "looking through binoculars",

    "looking through a magnifying glass",
    "studying a butterfly",
    "watching a tiny bug",
    "examining a flower",
    "following tiny footprints",
    "looking at a treasure map",
    "discovering something new",
    "wonder-filled expression",
    "thoughtful curious face",
    "exploring with interest",

    "listening carefully",
    "ears perked up",
    "tail raised with curiosity",
    "nose sniffing the air",
    "looking up in wonder",
    "watching the stars",
    "finding a hidden surprise",
    "investigating happily",
    "playfully exploring",
    "adorable curious expression"

],

    "calm": [
    "gentle smile",
    "peaceful smile",
    "relaxed expression",
    "calm eyes",
    "soft gaze",
    "content expression",
    "serene smile",
    "quiet happiness",
    "resting peacefully",
    "sitting peacefully",

    "enjoying the sunshine",
    "watching the clouds",
    "watching butterflies quietly",
    "listening to birds singing",
    "breathing fresh air",
    "relaxing under a tree",
    "enjoying a gentle breeze",
    "watching the sunset",
    "watching the sunrise",
    "stargazing peacefully",

    "meditating quietly",
    "reading peacefully",
    "walking calmly",
    "smiling softly",
    "feeling comfortable",
    "resting happily",
    "peaceful closed-eye smile",
    "calm and content",
    "gentle joyful expression",
    "completely relaxed"

],

    "proud": [
    "proud smile",
    "confident smile",
    "standing proudly",
    "head held high",
    "bright confident eyes",
    "beaming with pride",
    "happy after success",
    "celebrating an achievement",
    "holding a trophy proudly",
    "wearing a winner medal",

    "showing a certificate",
    "graduating happily",
    "raising a victory hand",
    "cheering after winning",
    "finishing a challenge",
    "showing artwork proudly",
    "displaying a finished project",
    "sharing a success with friends",
    "receiving applause",
    "accepting a prize",

    "posing confidently",
    "smiling with confidence",
    "looking accomplished",
    "feeling successful",
    "standing like a champion",
    "celebrating a personal best",
    "giving a thumbs up",
    "happy with hard work",
    "glowing with confidence",
    "cute proud expression"

],

    "surprised": [
    "wide surprised eyes",
    "raised eyebrows",
    "open mouth in surprise",
    "gasping happily",
    "pleasantly surprised smile",
    "amazed expression",
    "looking in wonder",
    "eyes sparkling with surprise",
    "jaw dropped playfully",
    "delighted surprise",

    "discovering something amazing",
    "finding hidden treasure",
    "seeing a rainbow",
    "watching fireworks",
    "meeting a new friend",
    "spotting a butterfly",
    "finding a shiny crystal",
    "opening a surprise gift",
    "seeing shooting stars",
    "finding a secret path",

    "astonished happy face",
    "excited surprise",
    "curious surprise",
    "looking up in amazement",
    "bright surprised smile",
    "happy shocked expression",
    "wonder-filled eyes",
    "looking around in surprise",
    "magical surprise expression",
    "cute surprised face"

],

    "sleepy": [
    "sleepy smile",
    "half-closed eyes",
    "heavy eyelids",
    "gentle yawn",
    "big yawn",
    "rubbing sleepy eyes",
    "cozy sleepy expression",
    "peaceful sleepy face",
    "soft sleepy smile",
    "ready for bedtime",

    "snuggling into a blanket",
    "holding a favorite teddy bear",
    "hugging a soft pillow",
    "wearing cozy pajamas",
    "curled up comfortably",
    "dreamy expression",
    "sleeping peacefully",
    "taking a gentle nap",
    "resting quietly",
    "relaxing before bedtime",

    "eyes gently closing",
    "calm bedtime expression",
    "peaceful dreaming face",
    "soft relaxed smile",
    "sleeping under the stars",
    "sleeping on a fluffy cloud",
    "snuggled up happily",
    "sleepy but smiling",
    "cozy nighttime expression",
    "cute sleepy face"

],

    "thoughtful": [
    "thoughtful smile",
    "gentle thinking expression",
    "deep in thought",
    "looking at the sky thoughtfully",
    "looking at the stars",
    "looking at the clouds",
    "wondering happily",
    "dreaming about adventures",
    "imagining something fun",
    "planning the next adventure",

    "studying a map carefully",
    "reading thoughtfully",
    "looking at a flower closely",
    "watching butterflies quietly",
    "observing tiny insects",
    "thinking while drawing",
    "thinking while coloring",
    "thinking with a smile",
    "head slightly tilted",
    "chin resting on one hand",

    "looking into the distance",
    "thinking creatively",
    "discovering new ideas",
    "carefully solving a puzzle",
    "planning something exciting",
    "peacefully reflecting",
    "quiet moment of thinking",
    "bright thoughtful eyes",
    "calm thoughtful face",
    "cute thoughtful expression"

],

    "silly": [
    "silly grin",
    "goofy smile",
    "funny face",
    "crossed eyes playfully",
    "tongue sticking out playfully",
    "puffed cheeks",
    "puffy smile",
    "cheeky expression",
    "mischievous smile",
    "playful wink",

    "laughing out loud",
    "giggling happily",
    "trying not to laugh",
    "rolling with laughter",
    "snorting with laughter",
    "big goofy grin",
    "making a silly pose",
    "pretending to roar",
    "pretending to fly",
    "pretending to be invisible",

    "wearing an upside-down hat",
    "balancing something on the nose",
    "making funny animal sounds",
    "dancing in a funny way",
    "posing like a superhero",
    "acting like a pirate",
    "pulling a funny face",
    "laughing with friends",
    "full of silly energy",
    "adorable goofy expression"

],

}