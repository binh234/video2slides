import imagehash

# -------------- Initializations ---------------------

DOWNLOAD_DIR = "downloads"

FRAME_BUFFER_HISTORY = 15  # Length of the frame buffer history to model background.
DEC_THRESH = (
    0.75  # Threshold value, above which it is marked foreground, else background.
)
DIST_THRESH = 100  # Threshold on the squared distance between the pixel and the sample to decide whether a pixel is close to that sample.

MIN_PERCENT = (
    0.15  # %age threshold to check if there is motion across subsequent frames
)
MAX_PERCENT = (
    0.01  # %age threshold to determine if the motion across frames has stopped.
)

# Post processing

SIM_THRESHOLD = (
    96  # Minimum similarity threshold (in percent) to consider 2 images to be similar
)

HASH_SIZE = 12  # Hash size to use for image hashing

HASH_FUNC = "dhash"  # Hash function to use for image hashing

HASH_BUFFER_HISTORY = 5  # Number of history images used to find out duplicate image

HASH_FUNC_DICT = {
    "dhash": imagehash.dhash,
    "phash": imagehash.phash,
    "ahash": imagehash.average_hash,
    "difference hashing": imagehash.dhash,
    "perceptual hashing": imagehash.phash,
    "average hashing": imagehash.average_hash,
}

# ----------------------------------------------------
