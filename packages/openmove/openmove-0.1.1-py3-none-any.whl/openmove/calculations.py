import numpy as np
import pandas as pd
from scipy.signal import medfilt

def _get_time_intervals(df, frame_rate=30.0):
    if "timestamp" in df.columns:
        t = df["timestamp"].values
        dt = np.diff(t)
    else:
        dt = np.full(len(df)-1, 1.0/frame_rate)
    return dt

def _finite_difference(data, dt):
    ddata = np.diff(data)
    derivative = ddata / dt
    derivative = np.insert(derivative, 0, np.nan)
    return derivative

def estimate_2d_angle(df, landmark_name1, landmark_name2, landmark_name3):
    if f"{landmark_name1}_x" not in df.columns or f"{landmark_name2}_x" not in df.columns or f"{landmark_name3}_x" not in df.columns:
        return np.array([])
    x1, y1 = df[f"{landmark_name1}_x"].values, df[f"{landmark_name1}_y"].values
    x2, y2 = df[f"{landmark_name2}_x"].values, df[f"{landmark_name2}_y"].values
    x3, y3 = df[f"{landmark_name3}_x"].values, df[f"{landmark_name3}_y"].values

    v1x, v1y = x1 - x2, y1 - y2
    v2x, v2y = x3 - x2, y3 - y2

    dot = v1x*v2x + v1y*v2y
    mag_v1 = np.sqrt(v1x**2 + v1y**2)
    mag_v2 = np.sqrt(v2x**2 + v2y**2)
    cos_angle = np.where((mag_v1*mag_v2)!=0, dot/(mag_v1*mag_v2), np.nan)
    cos_angle = np.clip(cos_angle, -1, 1)
    angles = np.arccos(cos_angle)
    return np.degrees(angles)

def estimate_3d_angle(df, landmark_name1, landmark_name2, landmark_name3):
    for ln in [landmark_name1, landmark_name2, landmark_name3]:
        if f"{ln}_x" not in df.columns:
            return np.array([])
    x1, y1, z1 = df[f"{landmark_name1}_x"].values, df[f"{landmark_name1}_y"].values, df[f"{landmark_name1}_z"].values
    x2, y2, z2 = df[f"{landmark_name2}_x"].values, df[f"{landmark_name2}_y"].values, df[f"{landmark_name2}_z"].values
    x3, y3, z3 = df[f"{landmark_name3}_x"].values, df[f"{landmark_name3}_y"].values, df[f"{landmark_name3}_z"].values

    v1 = np.stack([x1 - x2, y1 - y2, z1 - z2], axis=1)
    v2 = np.stack([x3 - x2, y3 - y2, z3 - z2], axis=1)

    dot_prod = np.sum(v1 * v2, axis=1)
    mag_v1 = np.linalg.norm(v1, axis=1)
    mag_v2 = np.linalg.norm(v2, axis=1)

    cos_angle = np.where((mag_v1*mag_v2) != 0, dot_prod/(mag_v1*mag_v2), np.nan)
    cos_angle = np.clip(cos_angle, -1, 1)
    angles = np.arccos(cos_angle)
    return np.degrees(angles)

def estimate_linear_velocity(df, landmark_name, frame_rate=30.0):
    if f"{landmark_name}_x" not in df.columns:
        return np.array([])
    x = df[f"{landmark_name}_x"].values
    y = df.get(f"{landmark_name}_y", pd.Series(np.zeros(len(df)))).values
    z = df.get(f"{landmark_name}_z", pd.Series(np.zeros(len(df)))).values

    dt = _get_time_intervals(df, frame_rate=frame_rate)
    dx = np.diff(x)
    dy = np.diff(y)
    dz = np.diff(z)
    speeds = np.sqrt(dx*dx + dy*dy + dz*dz)/dt
    speeds = np.insert(speeds, 0, np.nan)
    return speeds

def estimate_angular_velocity(df, landmark_name1, landmark_name2, landmark_name3, frame_rate=30.0):
    angles = estimate_3d_angle(df, landmark_name1, landmark_name2, landmark_name3)
    if angles.size == 0:
        return np.array([])
    dt = _get_time_intervals(df, frame_rate=frame_rate)
    angular_vel = _finite_difference(angles, dt)
    return angular_vel

def estimate_linear_acceleration(df, landmark_name, frame_rate=30.0):
    vel = estimate_linear_velocity(df, landmark_name, frame_rate=frame_rate)
    if vel.size == 0:
        return np.array([])
    dt = _get_time_intervals(df, frame_rate=frame_rate)
    return _finite_difference(vel, dt)

def estimate_angular_acceleration(df, landmark_name1, landmark_name2, landmark_name3, frame_rate=30.0):
    ang_vel = estimate_angular_velocity(df, landmark_name1, landmark_name2, landmark_name3, frame_rate=frame_rate)
    if ang_vel.size == 0:
        return np.array([])
    dt = _get_time_intervals(df, frame_rate=frame_rate)
    return _finite_difference(ang_vel, dt)

def estimate_linear_jerk(df, landmark_name, frame_rate=30.0):
    acc = estimate_linear_acceleration(df, landmark_name, frame_rate=frame_rate)
    if acc.size == 0:
        return np.array([])
    dt = _get_time_intervals(df, frame_rate=frame_rate)
    return _finite_difference(acc, dt)

def estimate_angular_jerk(df, landmark_name1, landmark_name2, landmark_name3, frame_rate=30.0):
    ang_acc = estimate_angular_acceleration(df, landmark_name1, landmark_name2, landmark_name3, frame_rate=frame_rate)
    if ang_acc.size == 0:
        return np.array([])
    dt = _get_time_intervals(df, frame_rate=frame_rate)
    return _finite_difference(ang_acc, dt)

def estimate_center_of_mass(df, landmark_names=None):
    if landmark_names is None:
        landmark_names = ["left_shoulder", "right_shoulder", "left_hip", "right_hip"]
    valid_cols = []
    for ln in landmark_names:
        if f"{ln}_x" in df.columns and f"{ln}_y" in df.columns and f"{ln}_z" in df.columns:
            valid_cols.append(ln)
    if not valid_cols:
        return None
    x_cols = [f"{ln}_x" for ln in valid_cols]
    y_cols = [f"{ln}_y" for ln in valid_cols]
    z_cols = [f"{ln}_z" for ln in valid_cols]

    com_x = df[x_cols].mean(axis=1).values
    com_y = df[y_cols].mean(axis=1).values
    com_z = df[z_cols].mean(axis=1).values
    return com_x, com_y, com_z

def estimate_postural_sway(df, frame_rate=30.0, landmark_names=None):
    com_xyz = estimate_center_of_mass(df, landmark_names)
    if com_xyz is None:
        return {}
    com_x, com_y, com_z = com_xyz
    dt = _get_time_intervals(df, frame_rate=frame_rate)

    ml_velocity = _finite_difference(com_x, dt)
    ml_acc = _finite_difference(ml_velocity[1:], dt[1:])
    ml_acc = np.insert(ml_acc, 0, np.nan)
    ml_acc = np.insert(ml_acc, 0, np.nan)

    ap_velocity = _finite_difference(com_y, dt)
    ap_acc = _finite_difference(ap_velocity[1:], dt[1:])
    ap_acc = np.insert(ap_acc, 0, np.nan)
    ap_acc = np.insert(ap_acc, 0, np.nan)

    sway_metrics = {
        "com_x": com_x,
        "com_y": com_y,
        "com_z": com_z,
        "ml_velocity": ml_velocity,
        "ap_velocity": ap_velocity,
        "ml_acceleration": ml_acc,
        "ap_acceleration": ap_acc
    }
    return sway_metrics

def add_virtual_landmarks(df):
    req = [
        "left_shoulder_x","left_shoulder_y","left_shoulder_z",
        "right_shoulder_x","right_shoulder_y","right_shoulder_z",
        "left_hip_x","left_hip_y","left_hip_z",
        "right_hip_x","right_hip_y","right_hip_z"
    ]
    for c in req:
        if c not in df.columns:
            return df
    df = df.copy()
    df["mid_shoulder_x"] = (df["left_shoulder_x"] + df["right_shoulder_x"]) / 2.0
    df["mid_shoulder_y"] = (df["left_shoulder_y"] + df["right_shoulder_y"]) / 2.0
    df["mid_shoulder_z"] = (df["left_shoulder_z"] + df["right_shoulder_z"]) / 2.0

    df["mid_hip_x"] = (df["left_hip_x"] + df["right_hip_x"]) / 2.0
    df["mid_hip_y"] = (df["left_hip_y"] + df["right_hip_y"]) / 2.0
    df["mid_hip_z"] = (df["left_hip_z"] + df["right_hip_z"]) / 2.0

    df["mid_torso_x"] = (df["mid_shoulder_x"] + df["mid_hip_x"]) / 2.0
    df["mid_torso_y"] = (df["mid_shoulder_y"] + df["mid_hip_y"]) / 2.0
    df["mid_torso_z"] = (df["mid_shoulder_z"] + df["mid_hip_z"]) / 2.0
    return df

def scale_landmarks_from_known_length(df, landmark_name1, landmark_name2, known_distance, use_average=True):
    if (f"{landmark_name1}_x" not in df.columns) or (f"{landmark_name2}_x" not in df.columns):
        return df
    x1, y1, z1 = df[f"{landmark_name1}_x"].values, df[f"{landmark_name1}_y"].values, df.get(f"{landmark_name1}_z", np.zeros(len(df))).values
    x2, y2, z2 = df[f"{landmark_name2}_x"].values, df[f"{landmark_name2}_y"].values, df.get(f"{landmark_name2}_z", np.zeros(len(df))).values

    dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    if use_average:
        mean_dist = np.nanmean(dist)
    else:
        valid_idx = np.where(~np.isnan(dist))[0]
        if len(valid_idx) == 0:
            return df
        mean_dist = dist[valid_idx[0]]

    if mean_dist == 0 or np.isnan(mean_dist):
        return df

    scale_factor = known_distance / mean_dist
    df = df.copy()
    for c in df.columns:
        if c.endswith("_x") or c.endswith("_y") or c.endswith("_z"):
            df[c] = df[c] * scale_factor
    return df

def median_filter(df, landmark_names=None, kernel_size=5):
    df = df.copy()
    if landmark_names is None:
        landmark_names = sorted(set([c[:-2] for c in df.columns if c.endswith("_x")]))

    for ln in landmark_names:
        for dim in ["x","y","z"]:
            col = f"{ln}_{dim}"
            if col in df.columns:
                data = df[col].values
                data_series = pd.Series(data).interpolate().fillna(method='bfill').fillna(method='ffill')
                filtered = medfilt(data_series.values, kernel_size=kernel_size)
                df[col] = filtered
    return df
