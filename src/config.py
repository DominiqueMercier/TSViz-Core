from enum import Enum


class Dataset_Splits(Enum):
    # Indices
    TRAIN = 0
    TEST = 1

class Dataset_Types(Enum):
    # Dataset types
    CLASSIFICATION = 0
    REGRESSION = 1

class Datasets(Enum):
    # Dataset names
    INTERNET_TRAFFIC = 0
    ANOMALY_DETECTION = 1
    CHARACTER_TRAJECTORIES = 2


class Clustering(Enum):
    # Clustering types
    K_MEANS = 0
    ADAPTIVE_K_MEANS = 1
    GMM = 2
    MEAN_SHIFT = 3
    HIERARCHICAL = 4

class Distances(Enum):
    # Distance metrics
    DTW = 0
    EUCLIDEAN = 1

class Selection(Enum):
    # Automatic number of cluster selection methods
    ASANKA = 0
    SILHOUETTE = 1


# Dataset settings
DATASET = Datasets.ANOMALY_DETECTION
DATASET_TYPE = Dataset_Types.REGRESSION if DATASET == Datasets.INTERNET_TRAFFIC else Dataset_Types.CLASSIFICATION
CLASS_NAMES = [""] if DATASET == Datasets.INTERNET_TRAFFIC else ["No Anomaly", "Anomaly"] if DATASET == Datasets.ANOMALY_DETECTION else ['a', 'b', 'c', 'd', 'e', 'g', 'h', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 'u', 'v', 'w', 'y', 'z'] if DATASET == Datasets.CHARACTER_TRAJECTORIES else [""]
BATCH_NORM = False  # Takes more time - new layers
INPUT_FEATURE_NAMES = ["Internet Traffic", "1D Derivative"] if DATASET == Datasets.INTERNET_TRAFFIC else ["Pressure", "Temperature", "Torque"] if DATASET == Datasets.ANOMALY_DETECTION else ["X", "Y", "Pressure"] if DATASET == Datasets.CHARACTER_TRAJECTORIES else ["Signal"]

CLUSTERING_METHOD = Clustering.HIERARCHICAL
DISTANCE_METRIC = Distances.DTW if CLUSTERING_METHOD == Clustering.HIERARCHICAL else Distances.EUCLIDEAN
SELECTION_TYPE = Selection.SILHOUETTE
MEAN_SHIFT_BANDWIDTH = 0.5

SCALE_X_AXIS = True
SCALE_X_AXIS = False if DISTANCE_METRIC == Distances.DTW else SCALE_X_AXIS  # X-axis scaling should be turned off with DTW
RANDOM_STATE = 313  # or None
