"""
==========================================================
 AI KDP AUTOPILOT V4
 Animal Poses Library
==========================================================

Version : 1.0
Purpose : Reusable body poses for Animal Engine

Rules:
- Kid-friendly
- Natural body positions
- Easy to illustrate
- Coloring book friendly
- Works with all animals

==========================================================
"""

POSES = {

    "standing": [
    "standing upright",
    "standing proudly",
    "standing with a smile",
    "standing with hands behind back",
    "standing with hands on hips",
    "standing with arms open",
    "standing and waving",
    "standing with one foot forward",
    "standing on a tree stump",
    "standing on a rock",

    "standing beside a flower",
    "standing under a tree",
    "standing near a river",
    "standing in tall grass",
    "standing on stepping stones",
    "standing beside a friend",
    "standing with a backpack",
    "standing with a basket",
    "standing with a balloon",
    "standing with a kite",

    "standing while looking up",
    "standing while looking around",
    "standing with curious posture",
    "standing confidently",
    "standing happily",
    "standing calmly",
    "standing in sunshine",
    "standing in a flower field",
    "standing in a forest clearing",
    "standing ready for adventure"

],

    "sitting": [
    "sitting upright",
    "sitting cross-legged",
    "sitting with legs stretched out",
    "sitting on a tree stump",
    "sitting on a rock",
    "sitting on a log",
    "sitting on a picnic blanket",
    "sitting on the grass",
    "sitting beside a river",
    "sitting beside a campfire",

    "sitting under a tree",
    "sitting in a flower field",
    "sitting on a wooden bench",
    "sitting on a swing",
    "sitting on stepping stones",
    "sitting with hands on knees",
    "sitting while waving",
    "sitting while reading",
    "sitting while drawing",
    "sitting while coloring",

    "sitting and smiling",
    "sitting with a backpack",
    "sitting with a picnic basket",
    "sitting with a balloon",
    "sitting with a teddy bear",
    "sitting comfortably",
    "sitting peacefully",
    "sitting curiously",
    "sitting happily",
    "relaxing in a seated pose"

],

    "walking": [
    "walking forward",
    "walking slowly",
    "walking confidently",
    "walking happily",
    "walking calmly",
    "walking carefully",
    "walking proudly",
    "walking with one foot raised",
    "walking with long strides",
    "walking with short steps",

    "walking on tiptoes",
    "walking through tall grass",
    "walking along a forest trail",
    "walking across stepping stones",
    "walking beside a river",
    "walking on a sandy beach",
    "walking through a flower meadow",
    "walking beneath tall trees",
    "walking across a wooden bridge",
    "walking up a gentle hill",

    "walking downhill",
    "walking around a tree",
    "walking toward a friend",
    "walking while waving",
    "walking with arms swinging",
    "walking with a relaxed posture",
    "walking with an energetic posture",
    "walking with a curious posture",
    "walking with a playful posture",
    "taking a cheerful stroll"

],

    "running": [
    "running forward",
    "running quickly",
    "running joyfully",
    "running with confidence",
    "running with excitement",
    "running with long strides",
    "running with short steps",
    "running on tiptoes",
    "running with arms swinging",
    "running with a playful posture",

    "running uphill",
    "running downhill",
    "running across a meadow",
    "running through a forest trail",
    "running beside a river",
    "running across stepping stones",
    "running on a sandy beach",
    "running through tall grass",
    "running beneath tall trees",
    "running through falling leaves",

    "running in light rain",
    "running through fresh snow",
    "running around a tree",
    "running toward a friend",
    "running in a zigzag path",
    "running with a bouncing step",
    "running with ears flopping",
    "running with tail raised",
    "running with energetic posture",
    "sprinting with determination"

],

    "jumping": [
    "jumping straight up",
    "jumping with joy",
    "jumping high",
    "jumping forward",
    "jumping with both feet",
    "jumping on one foot",
    "jumping over a log",
    "jumping over a puddle",
    "jumping across stepping stones",
    "jumping over a small rock",

    "jumping with arms raised",
    "jumping with arms spread",
    "jumping with a playful posture",
    "jumping with a happy posture",
    "jumping with a confident posture",
    "jumping with knees bent",
    "jumping with legs stretched out",
    "jumping with tail raised",
    "jumping with ears bouncing",
    "jumping lightly",

    "jumping through tall grass",
    "jumping in a flower meadow",
    "jumping on a forest trail",
    "jumping on a sandy beach",
    "jumping in fresh snow",
    "jumping in autumn leaves",
    "jumping in the sunshine",
    "jumping with perfect balance",
    "landing softly after a jump",
    "mid-air jumping pose"

],

    "climbing": [
    "climbing a tree",
    "climbing a tree trunk",
    "climbing a branch",
    "climbing a rock",
    "climbing a small hill",
    "climbing wooden steps",
    "climbing a ladder",
    "climbing a rope",
    "climbing a vine",
    "climbing a log",

    "climbing carefully",
    "climbing confidently",
    "climbing happily",
    "climbing with both hands",
    "climbing with one hand",
    "climbing with steady balance",
    "climbing upward",
    "climbing over rocks",
    "climbing across a fallen log",
    "climbing onto a platform",

    "climbing into a treehouse",
    "climbing over a fence",
    "climbing a gentle slope",
    "climbing with strong posture",
    "reaching the top",
    "pulling upward",
    "holding on tightly",
    "balanced while climbing",
    "carefully stepping upward",
    "mid-climb pose"

],

    "flying": [
    "flying high",
    "flying low",
    "gliding smoothly",
    "soaring gracefully",
    "hovering in place",
    "floating gently",
    "flapping wings",
    "wings fully spread",
    "wings partially spread",
    "taking off",

    "landing gently",
    "flying forward",
    "flying upward",
    "flying downward",
    "circling in the sky",
    "banking to one side",
    "gliding over a meadow",
    "gliding above a river",
    "flying through the clouds",
    "flying beneath a rainbow",

    "hovering over flowers",
    "flying between trees",
    "flying over the forest",
    "flying over mountains",
    "flying over the ocean",
    "floating with the breeze",
    "mid-flight pose",
    "balanced in the air",
    "light graceful flight",
    "peaceful flying pose"

],

    "swimming": [
    "swimming forward",
    "swimming gracefully",
    "swimming happily",
    "swimming calmly",
    "floating on the water",
    "gliding through the water",
    "paddling gently",
    "making gentle splashes",
    "floating with the current",
    "swimming underwater",

    "swimming near the surface",
    "diving into the water",
    "surfacing for air",
    "swimming in circles",
    "swimming through seaweed",
    "swimming over smooth rocks",
    "swimming beside coral",
    "swimming in a clear stream",
    "swimming across a lake",
    "swimming in the ocean",

    "playfully splashing water",
    "balanced in the water",
    "tail above the water",
    "creating tiny ripples",
    "swimming with steady strokes",
    "floating peacefully",
    "mid-swim pose",
    "gentle swimming posture",
    "relaxed swimming movement",
    "peaceful water pose"

],

    "dancing": [
    "standing dance pose",
    "spinning gracefully",
    "twirling happily",
    "one foot raised",
    "arms stretched outward",
    "arms raised joyfully",
    "hands clapping rhythmically",
    "feet tapping",
    "balanced dance pose",
    "playful dance pose",

    "happy dancing posture",
    "joyful movement",
    "gentle swaying",
    "side-to-side dance step",
    "small jumping dance",
    "celebration dance pose",
    "ballet pose",
    "tiptoe dance pose",
    "bowing after dancing",
    "performing a happy dance",

    "dancing with confidence",
    "light graceful movement",
    "energetic dance pose",
    "rhythmic body movement",
    "playful twirl",
    "raised knee dance pose",
    "balanced on one foot",
    "flowing dance movement",
    "cheerful performance pose",
    "cute dancing pose"

],

    "resting": [
    "resting comfortably",
    "standing at ease",
    "sitting at ease",
    "lying down comfortably",
    "curled up comfortably",
    "stretching gently",
    "leaning comfortably",
    "relaxed posture",
    "peaceful resting pose",
    "resting on one side",

    "resting on a tree stump",
    "resting on a rock",
    "resting on the grass",
    "resting beneath a tree",
    "resting with legs stretched out",
    "resting with paws together",
    "resting with arms folded",
    "resting with hands behind the head",
    "resting with eyes gently closed",
    "resting with a soft smile",

    "calm resting posture",
    "balanced resting pose",
    "relaxed seated posture",
    "comfortable standing posture",
    "quiet resting stance",
    "gentle body stretch",
    "relaxed full-body pose",
    "resting peacefully outdoors",
    "cozy resting position",
    "natural resting pose"

],

}