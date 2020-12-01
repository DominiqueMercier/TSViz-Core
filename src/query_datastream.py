import pickle

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import zscore
from tqdm import tqdm

def sampleTimeSeriesStream(strides, length, numTimeSteps, numChannels, numAnomalies, minDist, plotData=False):
    x = smoothSampling(strides * length + numTimeSteps, numChannels)
    # sc = StandardScaler()
    # x = sc.fit_transform(x)
    # print ("X:", x.shape)

    # introduce anomalies
    anomaly_list = []
    
    possible_anomalies = np.arange(x.shape[0])
    for i in range(numAnomalies):
        # Anomaly - can be both positive or negative
        scalingFactor = (np.sign(np.random.normal()) *
                        np.random.normal(loc=3.0, scale=0.75))
        
        anomalyIdx = np.random.permutation(possible_anomalies)[0]

        # Never introduce anomalies in the first channel
        anomalyChannel = np.random.randint(1, numChannels)
        
        fails = 0
        while x[anomalyIdx, anomalyChannel] < 1.0:  # Only take significant values
            pa = set(possible_anomalies)
            pa.remove(anomalyIdx)
            possible_anomalies = np.array(list(pa))
            anomalyIdx = np.random.permutation(possible_anomalies)[0]
            fails += 1
            if fails > 10:
                break
        
        if fails <= 10:
            pa = set(possible_anomalies)
            pa.difference_update(set(np.arange(anomalyIdx - minDist, anomalyIdx + minDist)))
            possible_anomalies = np.array(list(pa))
            x[anomalyIdx, anomalyChannel] *= scalingFactor
            anomaly_list.append(anomalyIdx)
        
    x_data, y_data = [], []
    for i in range(length):
        offset = strides * i
        x_tmp = x[offset:offset+numTimeSteps]

        window = np.arange(offset, offset+numTimeSteps)
        y = 0  # Normal
        true_a = -1
        for a in anomaly_list:
            if a in window:
                y = 1
                true_a = int(np.argwhere(window==a))
                break
        
        x_data.append(x_tmp)
        y_data.append(y)

        if plotData:
            plot_sample(x_tmp, y, true_a)
    return np.array(x_data), np.array(y_data)

def plot_sample(x, y, a):
    fig, ax = plt.subplots()
    if y == 1:
        ax.set_title('Label: ' + str(y) + ' | Anomly: ' + str(a))
    else:
        ax.set_title('Label: ' + str(y))
    plt.plot(x)
    plt.show()

def smoothSampling(numVals, numChannels, mean=0.0, std=0.05):
    finalSeries = []
    for channel in range(numChannels):
        stdDev = np.max([np.finfo(float).eps, 0.05 + np.random.normal(scale=std)])  # [0, 1)
        result = []
        y = np.random.normal(loc=mean, scale=stdDev)
        for _ in range(numVals):
            result.append(y)
            y += np.random.normal(loc=mean, scale=stdDev)
        result = np.array(result)

        # Normalize
        result = zscore(result)  # @UndefinedVariable

        finalSeries.append(result)

    return np.stack(finalSeries, axis=1)


def create_dataset(dataPath, strides, length, numTimeSteps, numChannels, numAnomalies, minDist, plotData=False):
    trainX, trainY = sampleTimeSeriesStream(strides, length, numTimeSteps, numChannels, numAnomalies, minDist, plotData)
    testX, testY = sampleTimeSeriesStream(strides, length, numTimeSteps, numChannels, numAnomalies, minDist, plotData)
    
    # Normalize the data
    # sc = StandardScaler()
    # trainX = sc.fit_transform(trainX)
    # testX = sc.transform(testX)

    # Dump data to pickle file
    print("Saving data to file: %s" % (dataPath))
    with open(dataPath, "wb") as pickleFile:
        pickle.dump([trainX, trainY, testX, testY], pickleFile,
                    protocol=pickle.HIGHEST_PROTOCOL)
    print("Data saved successfully!")

if __name__ == "__main__":
    np.random.seed(1)
    sampleTimeSeriesStream(strides=1, length=10, numTimeSteps=50, numChannels=3, numAnomalies=3, minDist=10, plotData=True)