
import numpy as np

parameters = {
    "10": {
        "exploration": 10.0,
        "learning_rate": 1175.0,
    },
    "20": {
        "exploration": 20.0,
        "learning_rate": 1662.0,
    },
    "30": {
        "exploration": 30.0,
        "learning_rate": 2035.0,
    },
    "ttt_2_level": {
        "exploration": 100.0,
        "learning_rate": 1000.0,
    },
    "ttt_dyn_level": {
        "exploration": 1000.0,
        "learning_rate": 10.0,
    }
}

means_10_10 = np.array([
    [0.75, 0.0 , 0.78, 0.22, 0.48, 0.06, 0.01, 0.32, 0.29, 0.1 ],
    [0.36, 0.43, 0.47, 0.4 , 0.95, 0.23, 0.76, 0.16, 0.98, 0.41],
    [0.48, 0.59, 0.5 , 0.34, 0.33, 0.28, 0.95, 0.47, 0.57, 1.0 ],
    [0.17, 0.49, 0.58, 0.53, 0.94, 0.9 , 0.73, 0.02, 0.07, 0.6 ],
    [0.86, 0.54, 0.8 , 0.65, 0.96, 0.57, 0.74, 0.53, 0.48, 0.97],
    [0.85, 0.49, 0.06, 0.65, 0.53, 0.66, 0.4 , 0.75, 0.33, 0.43],
    [0.04, 0.13, 0.09, 0.87, 0.17, 0.43, 0.0 , 0.13, 0.48, 0.83],
    [0.78, 0.3 , 0.53, 0.81, 0.02, 0.27, 0.35, 0.41, 0.02, 0.38],
    [0.31, 0.29, 0.69, 0.68, 0.06, 0.72, 0.82, 0.71, 0.67, 0.53],
    [0.82, 0.62, 0.47, 0.1 , 0.52, 0.35, 0.96, 0.62, 0.28, 0.56]
])

means_20_20 = np.array([
    [0.42, 0.71, 0.16, 0.32, 0.83, 0.71, 0.04, 0.47, 0.78, 0.27, 0.71, 0.07,
        0.1 , 0.33, 0.86, 0.15, 0.41, 0.28, 0.65, 0.  ],
    [0.2 , 0.46, 0.59, 0.89, 0.27, 0.03, 0.84, 0.52, 0.69, 0.51, 0.02, 0.29,
        0.35, 0.11, 0.4 , 0.7 , 0.77, 0.17, 0.69, 0.82],
    [0.34, 0.19, 0.01, 0.12, 0.74, 0.41, 0.85, 0.95, 0.68, 0.85, 0.35, 0.06,
        0.06, 0.83, 0.76, 0.53, 0.53, 0.95, 0.68, 0.21],
    [0.46, 0.41, 0.15, 0.51, 0.17, 0.07, 0.07, 0.69, 0.6 , 0.2 , 0.01, 0.68,
        0.99, 0.89, 0.67, 0.17, 0.46, 0.44, 0.55, 0.24],
    [0.43, 0.64, 0.29, 0.41, 0.8 , 0.7 , 0.45, 0.09, 0.74, 0.2 , 0.99, 0.83,
        0.04, 0.03, 0.2 , 0.98, 0.47, 0.67, 0.11, 0.16],
    [0.52, 0.56, 0.82, 0.89, 0.58, 0.82, 0.76, 0.59, 0.69, 0.69, 0.92, 0.96,
        0.66, 0.52, 0.3 , 0.79, 0.59, 0.54, 0.34, 0.21],
    [0.22, 0.37, 0.16, 0.59, 0.48, 0.07, 0.05, 0.35, 0.93, 0.04, 0.67, 0.51,
        0.5 , 0.52, 0.86, 0.75, 0.37, 0.49, 0.43, 0.24],
    [0.6 , 0.79, 0.63, 0.25, 0.51, 0.86, 0.37, 0.3 , 0.73, 0.51, 0.12, 0.44,
        0.63, 0.7 , 0.06, 0.57, 0.09, 0.54, 0.47, 0.05],
    [0.63, 0.46, 0.25, 0.81, 0.65, 0.51, 0.14, 0.73, 0.47, 0.22, 0.87, 0.26,
        0.39, 0.72, 0.31, 0.04, 0.22, 0.33, 0.62, 0.14],
    [0.26, 0.03, 0.58, 0.48, 0.35, 0.33, 0.96, 0.01, 0.4 , 0.21, 0.31, 0.02,
        0.76, 0.76, 0.47, 0.58, 0.59, 0.31, 0.75, 0.29],
    [0.68, 0.3 , 0.61, 0.69, 0.87, 0.26, 0.95, 0.89, 0.22, 0.22, 0.39, 0.83,
        0.43, 0.2 , 0.22, 0.68, 0.84, 0.88, 0.02, 0.73],
    [0.33, 0.65, 0.31, 0.41, 0.5 , 0.33, 0.32, 0.54, 0.41, 0.44, 0.38, 0.76,
        0.79, 0.87, 0.5 , 0.19, 0.32, 0.93, 0.  , 0.8 ],
    [0.27, 0.01, 0.23, 0.98, 0.34, 0.49, 0.78, 0.76, 0.58, 0.95, 0.07, 0.64,
        .45, 0.67, 0.76, 0.2 , 0.31, 0.27, 0.35, 0.47],
    [0.09, 0.32, 0.21, 0.02, 0.56, 0.58, 0.87, 0.76, 0.93, 0.34, 0.69, 0.77,
        0.09, 0.68, 0.08, 0.55, 0.66, 0.3 , 0.15, 0.35],
    [0.61, 0.98, 0.63, 0.07, 0.94, 0.52, 0.62, 0.87, 0.99, 0.95, 0.89, 0.7 ,
        0.58, 0.01, 0.72, 0.51, 0.09, 0.95, 0.05, 0.7 ],
    [0.93, 0.9 , 0.68, 0.23, 0.94, 0.27, 0.55, 0.  , 0.59, 0.41, 0.11, 0.54,
        0.14, 0.18, 0.29, 0.39, 0.49, 0.24, 0.1 , 0.07],
    [0.77, 0.15, 0.22, 0.32, 0.25, 0.99, 0.84, 0.41, 0.77, 0.06, 0.25, 0.32,
        0.92, 0.13, 0.98, 0.28, 0.49, 0.77, 0.72, 0.13],
    [0.98, 0.54, 0.53, 0.87, 0.76, 0.2 , 0.51, 0.99, 0.72, 0.65, 0.64, 0.52,
        0.11, 0.79, 0.08, 0.76, 0.66, 0.09, 0.94, 0.02],
    [0.13, 0.13, 0.78, 0.17, 0.35, 0.6 , 0.68, 0.89, 0.6 , 0.9 , 0.13, 0.6 ,
        0.51, 0.45, 0.54, 0.45, 0.08, 0.32, 0.96, 0.67],
    [0.02, 0.4 , 0.98, 0.59, 0.73, 0.96, 0.31, 0.19, 0.56, 0.38, 0.6 , 0.03,
        0.41, 0.32, 0.25, 0.9 , 0.13, 0.94, 0.42, 0.03]
])

means_30_30 = np.array([
    [0.68, 0.11, 0.86, 0.8 , 0.28, 0.51, 0.41, 0.63, 0.5 , 0.19, 0.87, 0.53,
    0.59, 0.51, 0.07, 0.43, 0.65, 0.36, 0.46, 0.87, 0.08, 0.17, 0.98, 0.46,
    0.33, 0.49, 0.36, 0.88, 0.64, 0.17],
    [0.29, 0.02, 0.67, 0.65, 0.66, 0.38, 0.46, 0.6 , 0.57, 0.38, 0.81, 0.4 ,
    0.25, 0.33, 0.44, 0.91, 0.29, 0.37, 0.65, 0.39, 0.44, 0.07, 0.4 , 0.52,
    0.94, 0.27, 0.16, 0.52, 0.62, 0.6 ],
    [0.42, 0.06, 0.4 , 0.23, 0.87, 0.83, 0.59, 0.05, 0.45, 0.92, 0.01, 0.05,
    0.62, 0.37, 0.76, 0.58, 0.74, 0.12, 0.79, 0.1 , 0.34, 0.27, 0.59, 0.24,
    0.26, 0.44, 0.71, 0.71, 0.61, 0.94],
    [0.56, 0.26, 0.35, 0.95, 0.35, 0.88, 0.26, 0.85, 0.42, 0.03, 0.77, 0.46,
    0.6 , 0.98, 0.54, 0.47, 0.53, 0.31, 0.11, 0.4 , 0.18, 0.89, 0.6 , 0.84,
    0.2 , 0.33, 0.09, 0.59, 0.15, 0.5 ],
    [0.41, 0.33, 0.04, 0.44, 0.94, 0.14, 0.36, 0.15, 0.15, 0.36, 0.2 , 0.34,
    0.52, 0.11, 0.28, 0.96, 0.3 , 0.19, 0.33, 0.5 , 0.1 , 0.13, 0.77, 0.67,
    0.45, 0.51, 0.72, 0.21, 0.7 , 0.96],
    [0.59, 0.44, 0.43, 0.25, 0.57, 0.48, 0.21, 0.86, 0.76, 0.81, 0.57, 0.92,
    0.2 , 0.86, 0.12, 0.68, 0.11, 0.21, 0.87, 0.65, 0.33, 0.52, 0.73, 0.79,
    0.48, 0.3 , 0.47, 0.21, 0.93, 0.15],
    [0.68, 0.43, 0.13, 0.68, 0.07, 0.66, 0.83, 0.88, 0.24, 0.54, 0.67, 0.87,
    0.88, 0.79, 0.84, 0.22, 0.97, 0.66, 0.35, 0.05, 0.89, 0.75, 0.28, 0.36,
    0.75, 0.51, 0.78, 0.38, 0.51, 0.73],
    [0.43, 0.36, 0.32, 0.08, 0.16, 0.71, 0.7 , 0.44, 0.08, 0.08, 0.69, 0.67,
    0.97, 0.59, 0.68, 0.9 , 0.75, 0.38, 0.51, 0.22, 0.88, 0.25, 0.58, 0.07,
    0.35, 0.03, 0.91, 0.1 , 0.38, 0.37],
    [0.3 , 0.34, 0.36, 0.67, 0.81, 0.35, 0.66, 0.92, 0.52, 0.11, 0.05, 0.85,
    0.03, 0.39, 0.27, 0.08, 0.12, 0.2 , 0.3 , 0.11, 0.57, 0.23, 0.94, 0.27,
    0.82, 0.6 , 0.1 , 0.97, 0.51, 0.93],
    [0.8 , 0.23, 0.11, 0.91, 0.68, 0.84, 0.05, 0.77, 0.7 , 0.89, 0.71, 0.69,
    0.07, 0.55, 0.64, 0.36, 0.6 , 0.19, 0.41, 0.44, 0.63, 0.37, 0.06, 0.96,
    0.14, 0.21, 0.63, 0.68, 0.92, 0.42],
    [0.88, 0.42, 0.66, 0.92, 0.8 , 0.08, 0.9 , 0.64, 0.92, 0.9 , 0.88, 0.7 ,
    0.4 , 0.8 , 0.33, 0.47, 0.55, 0.03, 0.5 , 0.82, 0.9 , 0.51, 0.26, 0.83,
    0.16, 0.04, 0.82, 0.67, 0.3 , 0.35],
    [0.68, 0.13, 0.01, 0.54, 0.44, 0.14, 0.42, 0.95, 0.58, 0.81, 0.18, 0.05,
    0.31, 0.24, 0.51, 0.41, 0.4 , 0.6 , 0.04, 0.66, 0.81, 0.31, 0.82, 0.03,
    0.77, 0.18, 0.64, 0.4 , 0.13, 0.28],
    [0.66, 0.04, 0.44, 0.51, 0.26, 0.65, 0.75, 0.81, 0.13, 0.7 , 0.21, 0.23,
    0.02, 0.6 , 0.21, 0.64, 0.38, 0.04, 0.44, 0.61, 0.21, 0.98, 0.49, 0.95,
    0.83, 0.04, 0.82, 0.55, 0.2 , 0.76],
    [0.4 , 0.46, 0.97, 0.55, 0.67, 0.92, 0.46, 0.44, 0.57, 0.66, 0.61, 0.62,
    0.51, 0.51, 0.17, 0.8 , 0.22, 0.3 , 0.38, 0.77, 0.15, 0.54, 0.91, 0.97,
    0.5 , 0.11, 0.57, 0.11, 0.84, 0.61],
    [0.31, 0.58, 0.56, 0.94, 0.83, 0.8 , 0.87, 0.52, 0.64, 0.85, 0.28, 0.06,
    0.33, 0.05, 0.63, 0.4 , 0.7 , 0.97, 0.75, 0.39, 0.51, 0.11, 0.69, 0.69,
    0.99, 0.55, 0.13, 0.46, 0.19, 0.82],
    [0.17, 0.26, 0.58, 0.72, 0.84, 0.87, 0.17, 0.41, 0.73, 0.08, 0.93, 0.24,
    0.98, 0.46, 0.57, 0.1 , 0.39, 0.95, 0.67, 0.81, 0.84, 0.79, 0.92, 0.38,
    0.73, 0.26, 0.02, 0.4 , 0.04, 0.59],
    [0.4 , 0.27, 0.32, 0.68, 0.72, 0.65, 0.6 , 0.77, 0.07, 1.  , 0.49, 0.17,
    0.26, 0.63, 0.44, 0.53, 0.89, 0.02, 0.12, 0.01, 0.51, 0.32, 0.08, 0.52,
    0.23, 0.69, 0.45, 0.34, 0.09, 0.7 ],
    [0.2 , 0.01, 0.36, 0.19, 0.99, 0.9 , 0.96, 0.49, 0.71, 0.08, 0.37, 0.38,
    0.98, 0.48, 0.12, 0.95, 0.31, 0.8 , 0.52, 0.95, 0.04, 0.14, 0.02, 0.34,
    0.37, 0.8 , 0.86, 0.55, 0.84, 0.98],
    [0.1 , 0.79, 0.44, 0.35, 0.25, 0.83, 0.08, 0.49, 0.22, 0.99, 0.35, 0.27,
    0.54, 0.67, 0.87, 0.6 , 0.2 , 0.92, 0.01, 0.34, 0.86, 0.06, 0.76, 0.13,
    0.74, 0.38, 0.86, 0.  , 0.88, 0.84],
    [0.54, 0.83, 0.97, 0.7 , 0.38, 0.05, 0.09, 0.54, 0.32, 0.35, 0.76, 0.97,
    0.86, 0.99, 0.37, 0.22, 0.62, 0.98, 0.24, 0.12, 0.36, 0.69, 0.04, 0.04,
    0.  , 0.66, 0.12, 0.73, 0.74, 0.89],
    [0.23, 0.73, 0.08, 0.67, 0.34, 0.54, 0.61, 0.56, 0.42, 0.33, 0.18, 0.01,
    0.73, 0.27, 0.11, 0.85, 0.7 , 0.95, 0.74, 0.01, 0.53, 0.83, 0.57, 0.14,
    0.49, 0.61, 0.22, 0.86, 0.45, 0.22],
    [0.16, 0.46, 0.51, 1.  , 0.18, 0.8 , 0.79, 0.07, 0.66, 0.29, 0.77, 0.97,
    0.49, 0.75, 0.35, 0.89, 0.08, 0.61, 0.15, 0.21, 0.19, 0.23, 0.19, 0.66,
    0.91, 0.64, 0.2 , 0.37, 0.18, 0.74],
    [0.22, 0.08, 0.8 , 0.21, 0.62, 0.79, 0.77, 0.29, 0.08, 0.82, 0.72, 0.86,
    0.26, 0.11, 0.33, 0.61, 0.36, 0.17, 0.82, 0.67, 0.04, 0.15, 0.21, 0.98,
    0.83, 0.98, 0.59, 0.91, 0.76, 0.69],
    [0.8 , 0.77, 0.9 , 0.5 , 0.8 , 0.37, 0.55, 0.73, 0.86, 0.04, 0.59, 0.05,
    0.05, 0.83, 0.22, 0.34, 0.36, 0.05, 0.27, 0.39, 0.35, 0.21, 0.23, 0.66,
    0.06, 0.49, 0.44, 0.27, 0.31, 0.83],
    [0.62, 0.8 , 0.21, 0.42, 0.01, 0.88, 0.62, 0.73, 0.51, 0.81, 0.64, 0.53,
    0.17, 0.82, 0.83, 0.56, 0.83, 0.27, 0.73, 0.28, 0.27, 0.22, 0.35, 0.47,
    0.92, 0.35, 0.89, 0.46, 0.22, 0.27],
    [0.03, 0.64, 0.57, 0.43, 0.22, 0.55, 0.74, 0.83, 0.74, 0.81, 0.44, 0.42,
    0.3 , 0.23, 0.23, 0.91, 0.38, 0.84, 0.05, 0.24, 0.93, 0.79, 0.34, 0.14,
    0.39, 0.5 , 0.2 , 0.02, 0.27, 0.37],
    [0.07, 0.31, 0.24, 0.63, 0.12, 0.76, 0.78, 0.22, 0.79, 0.48, 0.21, 0.57,
    0.26, 0.89, 0.82, 0.55, 0.42, 0.94, 0.11, 0.65, 0.7 , 0.06, 0.78, 0.91,
    0.03, 0.1 , 0.46, 0.03, 0.05, 0.91],
    [0.55, 0.46, 0.26, 0.88, 0.35, 0.78, 0.47, 0.3 , 0.3 , 0.09, 0.47, 0.71,
    0.26, 0.91, 0.75, 0.59, 0.82, 0.9 , 0.3 , 0.61, 0.68, 0.03, 0.03, 0.13,
    0.08, 0.56, 0.1 , 0.63, 0.49, 0.11],
    [0.18, 0.08, 0.37, 0.55, 0.65, 0.61, 0.9 , 0.95, 0.76, 0.05, 0.45, 0.92,
    0.22, 0.66, 0.19, 0.12, 0.21, 0.37, 0.95, 0.01, 0.84, 0.72, 0.7 , 0.86,
    0.15, 0.78, 0.46, 0.37, 0.79, 0.81],
    [0.84, 0.07, 0.39, 0.9 , 0.56, 0.05, 0.62, 0.63, 0.77, 0.05, 0.82, 0.01,
    0.23, 0.74, 0.99, 0.31, 0.84, 0.86, 0.83, 0.96, 0.22, 0.7 , 0.71, 0.37,
    0.16, 0.92, 0.13, 0.13, 0.66, 0.96]
])
