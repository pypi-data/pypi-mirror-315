import cv2
import numpy as np
import imageio
import mediapipe as mp
import pandas as pd  # Ensure pandas is imported

mp_pose = mp.solutions.pose
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands

def visualize(df_px, frames, output=None, output_path="output"):
    """
    Visualize tracking results:
    - Left: Original frame
    - Right: Black background with landmarks plotted in the same pixel coordinates.
    - A simple 3D-like grid floor is drawn beneath the person's feet to provide depth.
    
    All landmarks and connecting lines are colored white.
    
    Parameters
    ----------
    df_px : pd.DataFrame
        DataFrame with normalized landmark coordinates (values between 0 and 1).
        Must include a 'frame' column and landmark columns like 'nose_x', 'nose_y', etc.
    frames : list of np.ndarray
        Original video frames as NumPy arrays.
    output : str or None
        "gif", "video", or None. Determines if an output file is saved.
    output_path : str
        Path prefix for the output file (e.g., "tracking_results").
    
    Returns
    -------
    list of np.ndarray
        List of combined frames (original + processed side-by-side).
    """
    
    if "frame" not in df_px.columns:
        raise KeyError("DataFrame must contain a 'frame' column.")
    
    # Identify landmark groups
    body_landmarks = [l.name.lower() for l in mp_pose.PoseLandmark]
    face_landmarks = [f"face_{i}" for i in range(468)]
    left_hand_landmarks = [f"left__{hl.name.lower()}" for hl in mp_hands.HandLandmark]
    right_hand_landmarks = [f"right__{hl.name.lower()}" for hl in mp_hands.HandLandmark]
    
    # Connections
    body_connections = mp_pose.POSE_CONNECTIONS
    face_connections = mp_face_mesh.FACEMESH_CONTOURS
    hand_connections = mp_hands.HAND_CONNECTIONS
    
    # Initialize list to store combined frames
    output_frames = []
    num_frames = len(frames)
    
    for i in range(num_frames):
        row = df_px[df_px["frame"] == i]
        original = frames[i]
        h, w, _ = original.shape
        
        # Create black canvas for processed image
        processed_img = np.zeros((h, w, 3), dtype=np.uint8)
        
        if row.empty:
            # No landmarks for this frame, just combine original with blank
            combined = np.hstack((original, processed_img))
            output_frames.append(combined)
            continue
        
        row = row.iloc[0]  # Single row corresponding to frame i
        
        # Extract and scale coordinates for each landmark group
        body_2d = get_landmark_coords(row, body_landmarks, w, h)
        face_2d = get_landmark_coords(row, face_landmarks, w, h)
        lh_2d = get_landmark_coords(row, left_hand_landmarks, w, h)
        rh_2d = get_landmark_coords(row, right_hand_landmarks, w, h)
        
        # Determine floor_y based on hip landmarks
        # Use left_hip and right_hip to calculate floor_y
        hips = ['left_hip', 'right_hip']
        hip_ys = []
        for hip in hips:
            if hip in body_2d and body_2d[hip] is not None:
                hip_ys.append(body_2d[hip][1])
        if hip_ys:
            max_hip_y = max(hip_ys)
            floor_y = max_hip_y + 20  # Add offset to position grid slightly below hips
            floor_y = np.clip(floor_y, 0, h-1)  # Ensure floor_y is within image bounds
        else:
            # Default to bottom if hip landmarks are missing
            floor_y = h - 1
        
        # Draw floor line at floor_y
        #cv2.line(processed_img, (0, floor_y), (w, floor_y), (255, 255, 255), 2)  # White floor line
        
        # Add simple 3D-like grid floor beneath the person
        #add_simple_grid_floor(processed_img, floor_y, w, h, grid_spacing=50, color=(255, 255, 255), thickness=1)
        
        # Draw body connections and points
        draw_connections(processed_img, body_2d, body_connections, body_landmarks, color=(255, 255, 255))
        for pt in body_2d.values():
            if pt is not None:
                cv2.circle(processed_img, pt, 3, (255, 255, 255), -1)  # White landmarks
        
        # Draw face connections and points
        draw_connections(processed_img, face_2d, face_connections, face_landmarks, color=(255, 255, 255))
        for pt in face_2d.values():
            if pt is not None:
                cv2.circle(processed_img, pt, 2, (255, 255, 255), -1)  # White landmarks
        
        # Draw left hand connections and points
        draw_connections(processed_img, lh_2d, hand_connections, [hl.name.lower() for hl in mp_hands.HandLandmark], color=(255, 255, 255))
        for pt in lh_2d.values():
            if pt is not None:
                cv2.circle(processed_img, pt, 3, (255, 255, 255), -1)  # White landmarks
        
        # Draw right hand connections and points
        draw_connections(processed_img, rh_2d, hand_connections, [hl.name.lower() for hl in mp_hands.HandLandmark], color=(255, 255, 255))
        for pt in rh_2d.values():
            if pt is not None:
                cv2.circle(processed_img, pt, 3, (255, 255, 255), -1)  # White landmarks
        
        # Combine original and processed images side by side
        combined = np.hstack((original, processed_img))
        output_frames.append(combined)
    
    # Save output if requested
    if output == "gif":
        with imageio.get_writer(f"{output_path}.gif", mode='I', fps=10) as writer:
            for f in output_frames:
                writer.append_data(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))
    
    if output == "video":
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        h_combined, w_combined, _ = output_frames[0].shape
        out = cv2.VideoWriter(f"{output_path}.mp4", fourcc, 10, (w_combined, h_combined))
        for f in output_frames:
            out.write(f)
        out.release()
    
    return output_frames

def get_landmark_coords(row, landmark_names, frame_width, frame_height):
    """
    Extract and scale landmark coordinates from a DataFrame row.
    
    Parameters
    ----------
    row : pd.Series
        DataFrame row containing landmark coordinates.
    landmark_names : list of str
        List of landmark base names to extract.
    frame_width : int
        Width of the frame in pixels.
    frame_height : int
        Height of the frame in pixels.
    
    Returns
    -------
    dict
        Dictionary mapping landmark names to (x, y) tuples in pixel coordinates.
    """
    coords = {}
    for ln in landmark_names:
        x_col, y_col = f"{ln}_x", f"{ln}_y"
        if x_col in row and y_col in row:
            x_norm, y_norm = row[x_col], row[y_col]
            if pd.isna(x_norm) or pd.isna(y_norm):
                coords[ln] = None
            else:
                # Scale normalized coordinates to pixel coordinates
                x_pix = int(round(x_norm * frame_width))
                y_pix = int(round(y_norm * frame_height))
                coords[ln] = (x_pix, y_pix)
    return coords

def draw_connections(img, coords_2d, connections, landmark_list, color=(255,255,255)):
    """
    Draw lines between connected landmarks on the image.
    
    Parameters
    ----------
    img : np.ndarray
        Image to draw on.
    coords_2d : dict
        Dictionary of landmark coordinates.
    connections : list of tuples
        List of landmark index connections.
    landmark_list : list of str
        List of landmark names in order.
    color : tuple
        BGR color for the lines.
    """
    for connection in connections:
        start_idx, end_idx = connection
        if start_idx < len(landmark_list) and end_idx < len(landmark_list):
            start_name = landmark_list[start_idx]
            end_name = landmark_list[end_idx]
            if start_name in coords_2d and end_name in coords_2d:
                start_pt = coords_2d[start_name]
                end_pt = coords_2d[end_name]
                if start_pt is not None and end_pt is not None:
                    cv2.line(img, start_pt, end_pt, color, 1)

def add_simple_grid_floor(processed_img, floor_y, frame_width, frame_height, grid_spacing=50, color=(255, 255, 255), thickness=1):
    """
    Add a simple 3D-like grid floor beneath the person to simulate depth.
    
    The grid consists of horizontal and vertical lines extending downward from the floor line.
    
    Parameters
    ----------
    processed_img : np.ndarray
        The image to draw the grid on.
    floor_y : int
        The y-coordinate of the floor line.
    frame_width : int
        Width of the frame in pixels.
    frame_height : int
        Height of the frame in pixels.
    grid_spacing : int, optional
        Spacing between grid lines in pixels. Default is 50.
    color : tuple, optional
        BGR color of the grid lines. Default is white.
    thickness : int, optional
        Thickness of the grid lines. Default is 1.
    """
    # Draw horizontal grid lines extending downward from floor_y
    for y in range(floor_y + grid_spacing, frame_height, grid_spacing):
        cv2.line(processed_img, (0, y), (frame_width, y), color, thickness)
    
    # Draw vertical grid lines at regular intervals, starting from floor_y and extending downward
    for x in range(0, frame_width, grid_spacing):
        cv2.line(processed_img, (x, floor_y), (x, frame_height), color, thickness)
    
    # Optionally, add diagonal lines for a subtle 3D effect
    # Diagonal from left to right
    for i in range(0, frame_width, grid_spacing):
        end_y = floor_y + i
        end_y = min(end_y, frame_height - 1)
        cv2.line(processed_img, (i, floor_y), (frame_width, end_y), color, thickness)
    
    # Diagonal from right to left
    for i in range(0, frame_width, grid_spacing):
        end_y = floor_y + i
        end_y = min(end_y, frame_height - 1)
        cv2.line(processed_img, (frame_width - i, floor_y), (0, end_y), color, thickness)
