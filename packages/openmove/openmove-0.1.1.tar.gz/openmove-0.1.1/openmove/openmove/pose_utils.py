import pandas as pd
import numpy as np
import mediapipe as mp

mp_holistic = mp.solutions.holistic

# Landmark naming:
# Pose: mp_holistic.PoseLandmark
POSE_LANDMARKS = {l.value: l.name.lower().replace("pose_landmark_", "") for l in mp_holistic.PoseLandmark}
# Face: 468 landmarks, face_{i}
FACE_LANDMARKS = {i: f"face_{i}" for i in range(468)}
# Hands: mp_holistic.HandLandmark
HAND_LANDMARKS = {l.value: l.name.lower() for l in mp_holistic.HandLandmark}

def estimate_human_pose(frames):
    """
    Extract pose, face, and hand landmarks using MediaPipe Holistic.
    Returns a wide-format DataFrame with columns:
    frame, <landmark>_x, <landmark>_y, <landmark>_z, [<landmark>_visibility for pose]
    Landmarks: pose, face, left hand, right hand
    """
    data_pose = []
    data_face = []
    data_left_hand = []
    data_right_hand = []

    with mp_holistic.Holistic(static_image_mode=True, 
                              model_complexity=2, 
                              min_detection_confidence=0.5) as holistic:
        for i, frame in enumerate(frames):
            results = holistic.process(frame[:,:,::-1])
            
            # Pose Landmarks
            if results.pose_landmarks:
                for idx, lm in enumerate(results.pose_landmarks.landmark):
                    data_pose.append([i, POSE_LANDMARKS[idx], lm.x, lm.y, lm.z, lm.visibility])
            
            # Face Landmarks
            if results.face_landmarks:
                for idx, lm in enumerate(results.face_landmarks.landmark):
                    data_face.append([i, FACE_LANDMARKS[idx], lm.x, lm.y, lm.z])
            
            # Left Hand
            if results.left_hand_landmarks:
                for idx, lm in enumerate(results.left_hand_landmarks.landmark):
                    data_left_hand.append([i, "left__" + HAND_LANDMARKS[idx], lm.x, lm.y, lm.z])
            
            # Right Hand
            if results.right_hand_landmarks:
                for idx, lm in enumerate(results.right_hand_landmarks.landmark):
                    data_right_hand.append([i, "right__" + HAND_LANDMARKS[idx], lm.x, lm.y, lm.z])

    # Combine all data
    # Pose
    pose_df = pd.DataFrame(data_pose, columns=["frame","landmark_name","x","y","z","visibility"])
    # Face
    face_df = pd.DataFrame(data_face, columns=["frame","landmark_name","x","y","z"])
    # Hands
    lh_df = pd.DataFrame(data_left_hand, columns=["frame","landmark_name","x","y","z"])
    rh_df = pd.DataFrame(data_right_hand, columns=["frame","landmark_name","x","y","z"])
    
    # Merge all into one DataFrame
    df_list = []
    if not pose_df.empty:
        df_list.append(_long_to_wide(pose_df, include_visibility=True))
    if not face_df.empty:
        df_list.append(_long_to_wide(face_df, include_visibility=False))
    if not lh_df.empty:
        df_list.append(_long_to_wide(lh_df, include_visibility=False))
    if not rh_df.empty:
        df_list.append(_long_to_wide(rh_df, include_visibility=False))

    if not df_list:
        return pd.DataFrame(columns=["frame"])
    
    # Merge on frame
    # Start with the first, merge others
    merged_df = df_list[0]
    for d in df_list[1:]:
        merged_df = pd.merge(merged_df, d, on="frame", how="outer")

    merged_df = merged_df.sort_values("frame").reset_index(drop=True)
    return merged_df

def _long_to_wide(df, include_visibility=False):
    df = df.copy()
    # We have columns: frame, landmark_name, x, y, z[, visibility]
    columns_to_keep = ["frame","landmark_name","x","y"]
    if "z" in df.columns:
        columns_to_keep.append("z")
    if include_visibility and "visibility" in df.columns:
        columns_to_keep.append("visibility")
    
    df = df[columns_to_keep]
    df_long = df.melt(id_vars=["frame","landmark_name"], var_name="dim", value_name="val", ignore_index=False)
    df_wide = df_long.pivot_table(index="frame", columns=["landmark_name","dim"], values="val")
    df_wide.columns = [f"{ln}_{dim}" for ln,dim in df_wide.columns]
    df_wide = df_wide.reset_index()
    return df_wide
