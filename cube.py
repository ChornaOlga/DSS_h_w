import pylab
import random
import matplotlib.pyplot as plt
import numpy as np


def OLAP_cube(features_normalized, score):
    """
        Generate a 3D bar plot representing an OLAP cube.

        This function uses matplotlib to create a 3D bar plot where the x-axis
        represents alternatives, the y-axis represents features, and the z-axis
        represents the normalized values of the features.

        Parameters:
        - features_normalized (numpy.ndarray): A 2D array containing the normalized
                                               features for each alternative.
        - score (pandas.DataFrame): A DataFrame containing the scores for each alternative.

        Returns:
        - None
    """
    # --------------------- OLAP_cube ----------------------

    xg = np.arange(len(features_normalized[1]))

    fig = pylab.figure()
    ax = fig.add_subplot(projection='3d')
    for index, line in enumerate(features_normalized):
        ax.bar(xg, line, index + 1, zdir='y', color=np.random.rand(3, ))
    ax.set_xlabel('Alternatives')
    ax.set_ylabel('Features')
    ax.set_zlabel('Normalized value')
    pylab.show()

    return


def OLAP_3D(features_normalized, score_df):
    """
        Generate a 3D bar plot representing an OLAP cube.

        This function uses matplotlib to create a 3D bar plot where the x-axis
        represents features, the y-axis represents alternatives, and the z-axis
        represents the normalized values of the features.

        Parameters:
        - features_normalized (numpy.ndarray): A 2D array containing the normalized
                                               features for each alternative.
        - score_df (pandas.DataFrame): A DataFrame containing the scores for each alternative.

        Returns:
        - None
    """
    feat = features_normalized
    xpos = np.arange(feat.shape[0])
    ypos = np.arange(feat.shape[1])
    yposM, xposM = np.meshgrid(ypos + 0.5, xpos + 0.5)
    zpos = np.zeros(feat.shape).flatten()

    dx = 0.5 * np.ones_like(zpos)
    dy = 0.4 * np.ones_like(zpos)
    dz = feat.ravel()

    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')

    clr = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in range(feat.shape[1])]
    colors = clr * feat.shape[0]

    ax.bar3d(xposM.ravel(), yposM.ravel(), zpos, dx, dy, dz, color=colors)

    ticks_y = np.arange(feat.shape[1])
    ax.set_yticks(ticks_y)

    ax.set_xlabel('Features')
    ax.set_ylabel('Alternatives')
    ax.set_zlabel('Normalized value')
    plt.yticks(ticks_y, score_df['currency'].to_list())

    plt.show()

    return
