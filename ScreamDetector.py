import numpy as np
import librosa
import os
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt


# Define function to extract features from audio signal
def extract_features(file_path, max_pad_len=500):
    X, sample_rate = librosa.load(file_path)
    mfccs = librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40)
    spectrogram = librosa.amplitude_to_db(np.abs(librosa.stft(X)), ref=np.max)
    pad_width = max_pad_len - mfccs.shape[1]
    pad_width1 = max_pad_len - spectrogram.shape[1]
    if pad_width < 0:
        mfccs = mfccs[:, :max_pad_len]
        spectrogram = spectrogram[:, :max_pad_len]
    else:
        mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
        spectrogram = np.pad(spectrogram, pad_width=((0, 0), (0, pad_width)), mode='constant')
    combined_features = np.concatenate((mfccs.flatten(), spectrogram.flatten()))
    return combined_features

def callerFunction(tempfilepath):
    # Load positive and negative datasets
    positive_dir = "./positive"
    negative_dir = "./negative"

    positive_files = [os.path.join(positive_dir, f) for f in os.listdir(positive_dir) if f.endswith('.wav')]
    negative_files = [os.path.join(negative_dir, f) for f in os.listdir(negative_dir) if f.endswith('.wav')]

    X = []
    y = []
    for file_path in positive_files:
        X.append(extract_features(file_path))
        y.append(1)
    for file_path in negative_files:
        X.append(extract_features(file_path))
        y.append(0)

    # Split dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Train K-NN model
    clf = KNeighborsClassifier(n_neighbors=5)
    clf.fit(X_train, y_train)

    # Evaluate model on testing set
    accuracy = clf.score(X_test, y_test)
    print("Accuracy:", accuracy)

    # Use model to classify new audio signals
    new_file_path = tempfilepath
    features = extract_features(new_file_path)
    prediction = clf.predict(features.reshape(1, -1))
    if prediction == 1:
        print("Scream detected")
        return 1
    else:
        print("No scream detected")
        return 0



