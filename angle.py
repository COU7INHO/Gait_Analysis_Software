import numpy as np

def angle_calculation(file):
    global distance

    alpha = np.arctan((file['GT_H'] - file['LE_H']) / (file['GT_V'] - file['LE_V']))
    y = int(distance) * np.cos(alpha) + file['GT_V']
    x = int(distance) * np.sin(alpha) + file['GT_H']

    trunk_angle = np.degrees(np.arctan(((x - file['A_H']) / (y - file['A_V']))))
    thigh_angle = np.degrees(np.arctan((file['LE_V'] - file['GT_V']) / (file['LE_H'] - file['GT_H'])))
    shank_angle = np.degrees(np.arctan((file['LM_V'] - file['LE_V']) / (file['LM_H'] - file['LE_H'])))
    foot_angle = np.degrees(np.arctan((file['VM_V'] - file['LM_V']) / (file['VM_H'] - file['LM_H'])))

    thigh_angle[thigh_angle <= 0] = thigh_angle[thigh_angle <= 0] + 180
    shank_angle[shank_angle <= 0] = shank_angle[shank_angle <= 0] + 180
    foot_angle[foot_angle >= 0] = 90 - foot_angle[foot_angle >= 0]
    foot_angle[foot_angle <= 0] = foot_angle[foot_angle <= 0] + 90

    hip_ang = thigh_angle - trunk_angle - 90
    knee_ang = thigh_angle - shank_angle
    ankle_ang = foot_angle - shank_angle + 90
    ankle_ang = ankle_ang - ankle_ang[0]

    return hip_ang, knee_ang, ankle_ang
