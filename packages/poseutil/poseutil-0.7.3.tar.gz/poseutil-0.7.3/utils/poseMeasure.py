import math
from utils.const import *
from utils.pose_util import Coordinate

class PoseMeasure:
    def __init__(self, pose:list[Coordinate] = [Coordinate(0, 0, 0) for i in range(33)], model='mmpose'):
        match model:
            case 'mmpose':
                self.pose = pose
                self.head = pose[HEAD_MMPOSE]
                self.leftShoulder = pose[LEFT_SHOULDER_MMPOSE]
                self.rightShoulder = pose[RIGHT_SHOULDER_MMPOSE]
                self.leftElbow = pose[LEFT_ELBOW_MMPOSE]
                self.rightElbow = pose[RIGHT_ELBOW_MMPOSE]
                self.leftWrist = pose[LEFT_WRIST_MMPOSE]
                self.rightWrist = pose[RIGHT_WRIST_MMPOSE]
                self.leftHip = pose[LEFT_HIP_MMPOSE]
                self.rightHip = pose[RIGHT_HIP_MMPOSE]
                self.leftKnee = pose[LEFT_KNEE_MMPOSE]
                self.rightKnee = pose[RIGHT_KNEE_MMPOSE]
                self.leftAnkle = pose[LEFT_ANKLE_MMPOSE]
                self.rightAnkle = pose[RIGHT_ANKLE_MMPOSE]
                self.grip = pose[RIGHT_ANKLE_MMPOSE]
            case 'yolo':
                self.pose = pose
                self.leftNose = pose[NOSE_YOLOV11]
                self.rightNose = pose[NOSE_YOLOV11]
                self.leftEye = pose[LEFT_EYE_YOLOV11]
                self.rightEye = pose[RIGHT_EYE_YOLOV11]
                self.leftEar = pose[LEFT_EAR_YOLOV11]
                self.rightEar = pose[RIGHT_EAR_YOLOV11]
                self.leftShoulder = pose[LEFT_SHOULDER_YOLOV11]
                self.rightShoulder = pose[RIGHT_SHOULDER_YOLOV11]
                self.leftElbow = pose[LEFT_ELBOW_YOLOV11]
                self.rightElbow = pose[RIGHT_ELBOW_YOLOV11]
                self.leftWrist = pose[LEFT_WRIST_YOLOV11]
                self.rightWrist = pose[RIGHT_WRIST_YOLOV11]
                self.leftHip = pose[LEFT_HIP_YOLOV11]
                self.rightHip = pose[RIGHT_HIP_YOLOV11]
                self.leftKnee = pose[LEFT_KNEE_YOLOV11]
                self.rightKnee = pose[RIGHT_KNEE_YOLOV11]
                self.leftAnkle = pose[LEFT_ANKLE_YOLOV11]
                self.rightAnkle = pose[RIGHT_ANKLE_YOLOV11]
            case 'mediapipe':
                self.pose = pose
                self.leftNose = pose[NOSE]
                self.rightNose = pose[NOSE]
                self.leftEyeInner = pose[LEFT_EYE_INNER]
                self.leftEye = pose[LEFT_EYE]
                self.leftEyeOuter = pose[LEFT_EYE_OUTER]
                self.rightEyeInner = pose[RIGHT_EYE_INNER]
                self.rightEye = pose[RIGHT_EYE]
                self.rightEyeOuter = pose[RIGHT_EYE_OUTER]
                self.leftEar = pose[LEFT_EAR]
                self.rightEar = pose[RIGHT_EAR]
                self.leftMouth = pose[LEFT_MOUTH]
                self.rightMouth = pose[RIGHT_MOUTH]
                self.leftShoulder = pose[LEFT_SHOULDER]
                self.rightShoulder = pose[RIGHT_SHOULDER]
                self.leftElbow = pose[LEFT_ELBOW]
                self.rightElbow = pose[RIGHT_ELBOW]
                self.leftWrist = pose[LEFT_WRIST]
                self.rightWrist = pose[RIGHT_WRIST]
                self.leftPinky = pose[LEFT_PINKY]
                self.rightPinky = pose[RIGHT_PINKY]
                self.leftIndex = pose[LEFT_INDEX]
                self.rightIndex = pose[RIGHT_INDEX]
                self.leftThumb = pose[LEFT_THUMB]
                self.rightThumb = pose[RIGHT_THUMB]
                self.leftHip = pose[LEFT_HIP]
                self.rightHip = pose[RIGHT_HIP]
                self.leftKnee = pose[LEFT_KNEE]
                self.rightKnee = pose[RIGHT_KNEE]
                self.leftAnkle = pose[LEFT_ANKLE]
                self.rightAnkle = pose[RIGHT_ANKLE]
                self.leftHeel = pose[LEFT_HEEL]
                self.rightHeel = pose[RIGHT_HEEL]
                self.leftFootIndex = pose[LEFT_FOOT_INDEX]
                self.rightFootIndex = pose[RIGHT_FOOT_INDEX]

    # def __init__(self, pose = [Coordinate(0, 0, 0) for i in range(33)], hand = [Coordinate(0, 0, 0) for _ in range(42)]):
    #     self.pose = pose
    #     self.leftNose = pose[NOSE]
    #     self.rightNose = pose[NOSE]
    #     self.leftEyeInner = pose[LEFT_EYE_INNER]
    #     self.leftEye = pose[LEFT_EYE]
    #     self.leftEyeOuter = pose[LEFT_EYE_OUTER]
    #     self.rightEyeInner = pose[RIGHT_EYE_INNER]
    #     self.rightEye = pose[RIGHT_EYE]
    #     self.rightEyeOuter = pose[RIGHT_EYE_OUTER]
    #     self.leftEar = pose[LEFT_EAR]
    #     self.rightEar = pose[RIGHT_EAR]
    #     self.leftMouth = pose[LEFT_MOUTH]
    #     self.rightMouth = pose[RIGHT_MOUTH]
    #     self.leftShoulder = pose[LEFT_SHOULDER]
    #     self.rightShoulder = pose[RIGHT_SHOULDER]
    #     self.leftElbow = pose[LEFT_ELBOW]
    #     self.rightElbow = pose[RIGHT_ELBOW]
    #     self.leftWrist = pose[LEFT_WRIST]
    #     self.rightWrist = pose[RIGHT_WRIST]
    #     self.leftPinky = pose[LEFT_PINKY]
    #     self.rightPinky = pose[RIGHT_PINKY]
    #     self.leftIndex = pose[LEFT_INDEX]
    #     self.rightIndex = pose[RIGHT_INDEX]
    #     self.leftThumb = pose[LEFT_THUMB]
    #     self.rightThumb = pose[RIGHT_THUMB]
    #     self.leftHip = pose[LEFT_HIP]
    #     self.rightHip = pose[RIGHT_HIP]
    #     self.leftKnee = pose[LEFT_KNEE]
    #     self.rightKnee = pose[RIGHT_KNEE]
    #     self.leftAnkle = pose[LEFT_ANKLE]
    #     self.rightAnkle = pose[RIGHT_ANKLE]
    #     self.leftHeel = pose[LEFT_HEEL]
    #     self.rightHeel = pose[RIGHT_HEEL]
    #     self.leftFootIndex = pose[LEFT_FOOT_INDEX]
    #     self.rightFootIndex = pose[RIGHT_FOOT_INDEX]

    #     self.leftHandWrist = hand[LEFT_HAND_WRIST]
    #     self.rightHandWrist = hand[RIGHT_HAND_WRIST]
    #     self.leftHandThumbCmc = hand[LEFT_HAND_THUMB_CMC]
    #     self.rightHandThumbCmc = hand[RIGHT_HAND_THUMB_CMC]
    #     self.leftHandThumbMcp = hand[LEFT_HAND_THUMB_MCP]
    #     self.rightHandThumbMcp = hand[RIGHT_HAND_THUMB_MCP]
    #     self.leftHandThumbIp = hand[LEFT_HAND_THUMB_IP]
    #     self.rightHandThumbIp = hand[RIGHT_HAND_THUMB_IP]
    #     self.leftHandThumbTip = hand[LEFT_HAND_THUMB_TIP]
    #     self.rightHandThumbTip = hand[RIGHT_HAND_THUMB_TIP]
    #     self.leftHandIndexFingerMcp = hand[LEFT_HAND_INDEX_FINGER_MCP]
    #     self.rightHandIndexFingerMcp = hand[RIGHT_HAND_INDEX_FINGER_MCP]
    #     self.leftHandIndexFingerPip = hand[LEFT_HAND_INDEX_FINGER_PIP]
    #     self.rightHandIndexFingerPip = hand[RIGHT_HAND_INDEX_FINGER_PIP]
    #     self.leftHandIndexFingerDip = hand[LEFT_HAND_INDEX_FINGER_DIP]
    #     self.rightHandIndexFingerDip = hand[RIGHT_HAND_INDEX_FINGER_DIP]
    #     self.leftHandIndexFingerTip = hand[LEFT_HAND_INDEX_FINGER_TIP]
    #     self.rightHandIndexFingerTip = hand[RIGHT_HAND_INDEX_FINGER_TIP]
    #     self.leftHandMiddleFingerMcp = hand[LEFT_HAND_MIDDLE_FINGER_MCP]
    #     self.rightHandMiddleFingerMcp = hand[RIGHT_HAND_MIDDLE_FINGER_MCP]
    #     self.leftHandMiddleFingerPip = hand[LEFT_HAND_MIDDLE_FINGER_PIP]
    #     self.rightHandMiddleFingerPip = hand[RIGHT_HAND_MIDDLE_FINGER_PIP]
    #     self.leftHandMiddleFingerDip = hand[LEFT_HAND_MIDDLE_FINGER_DIP]
    #     self.righHandMiddleFingerDip = hand[RIGHT_HAND_MIDDLE_FINGER_DIP]
    #     self.leftHandMiddleFingerTip = hand[LEFT_HAND_MIDDLE_FINGER_TIP]
    #     self.rightHandMiddleFingerTip = hand[RIGHT_HAND_MIDDLE_FINGER_TIP]
    #     self.leftHandRingFingerMcp = hand[LEFT_HAND_RING_FINGER_MCP]
    #     self.rightHandRingFingerMcp = hand[RIGHT_HAND_RING_FINGER_MCP]
    #     self.leftHandRingFingerPip = hand[LEFT_HAND_RING_FINGER_PIP]
    #     self.rightHandRingFingerPip = hand[RIGHT_HAND_RING_FINGER_PIP]
    #     self.leftHandRingFingerDip = hand[LEFT_HAND_RING_FINGER_DIP]
    #     self.rightHandRingFingerDip = hand[RIGHT_HAND_RING_FINGER_DIP]
    #     self.leftHandRingFingerTip = hand[LEFT_HAND_RING_FINGER_TIP]
    #     self.rightHandRingFingerTip = hand[RIGHT_HAND_RING_FINGER_TIP]
    #     self.leftHandPinkyMcp = hand[LEFT_HAND_PINKY_MCP]
    #     self.rightHandPinkyMcp = hand[RIGHT_HAND_PINKY_MCP]
    #     self.leftHandPinkyPip = hand[LEFT_HAND_PINKY_PIP]
    #     self.rightHandPinkyPip = hand[RIGHT_HAND_PINKY_PIP]
    #     self.leftHandPinkyDip = hand[LEFT_HAND_PINKY_DIP]
    #     self.rightHandPinkyDip = hand[RIGHT_HAND_PINKY_DIP]
    #     self.leftHandPinkyTip = hand[LEFT_HAND_PINKY_TIP]
    #     self.righHandPinkyTip = hand[RIGHT_HAND_PINKY_TIP]

    # def getNoseAlnkeDistance(self, dimension=XYZ, direction=AVG):
    #     left = self.getDistance(self.leftNose, self.leftAnkle, dimension)
    #     right = self.getDistance(self.rightNose, self.rightAnkle, dimension)
    #     avg = (left + right) / 2
    #     if direction == LEFT:
    #         return left
    #     elif direction == RIGHT:
    #         return right
    #     elif direction == AVG:
    #         return avg
        
    # def onlyCableObliqueCrunch(self):
    #     left = self.getNoseAlnkeDistance(X, LEFT)
    #     right = self.getNoseAlnkeDistance(X, RIGHT)

    #     if left < right:
    #         return self.getShoulderElbowHipAngle(XY, LEFT)
    #     else:
    #         return self.getShoulderElbowHipAngle(XY, RIGHT)

    def getData(self, selector: str):
        func, *inputs = selector.split(",")
        dimension = inputs[0].strip().lower()
        direction = inputs[-1].strip()
        if inputs[-4].strip().isdigit():
            target = int(inputs[-4].strip())
        else:
            target = None
        if inputs[-3].strip().isdigit():
            second = int(inputs[-3].strip())
        else:
            second = None
        if inputs[-2].strip().isdigit():
            thrid = int(inputs[-2].strip())
        else:
            if inputs[-2].strip() == "DicisionFront":
                standardDicision = 0
            elif inputs[-2].strip() == "DicisionSide":
                standardDicision = 1
            thrid = None

        if func == "Point":
            return self.getCoordWithDirection(target, dimension, direction)
        elif func == "Distance":
            if second == None:
                return self.getDistanceEachWithDirection(target, dimension, direction, standardDicision)
            else:
                return self.getDistanceWithDirection(target, second, dimension, direction, standardDicision)
        elif func == "Angle":
            return self.getAngleWithDirection(target, second, thrid, dimension, direction)
        elif func == "Plane":
            if second == None:
                return self.getPlaneEachWithDirection(target, dimension, direction)
            else:
                return self.getPlaneWithDirection(target, second, dimension, direction)
        elif func == "Line":
            if second == None:
                return self.getLineEachWithDirection(target, dimension, direction, 'x')
            else:
                return self.getLineWithDirection(target, second, dimension, direction, 'x')
    
    def getCoordWithDirection(self, target, dimension, direction):
        left = self.getCoord(self.pose[target], dimension)
        right = self.getCoord(self.pose[target+1], dimension)
        if target == 0:
            return self.getCoord(self.pose[target], dimension)
        if direction == 'AVG':
            return (left + right)/2
        elif direction == 'LEFT':
            return left
        elif direction == 'RIGHT':
            return right
    
    def getDistanceEachWithDirection(self, target, dimension, direction, standardDicision):
        if self.getHipDistance(XY) == 0:
            dicision = 1
        else:
            if standardDicision == 0:
                dicision = self.getHipDistance(XY)
            elif standardDicision == 1:
                dicision = self.getShoulderDistance(XY)
        if dicision == 0:
            dicision = 1
        return self.getDistance(self.pose[target], self.pose[target+1], dimension) / dicision

    def getDistanceWithDirection(self, target, second, dimension, direction, standardDicision):
        if self.getHipDistance(XY) == 0:
            dicision = 1
        else:
            if standardDicision == 0:
                dicision = self.getHipDistance(XY)
            elif standardDicision == 1:
                dicision = self.getShoulderDistance(XY)
        if dicision == 0:
            dicision = 1
        if target == 0:
            left = self.getDistance(self.pose[target], self.pose[second], dimension) / dicision
            right = self.getDistance(self.pose[target], self.pose[second+1], dimension) / dicision
        elif second == 0:
            left = self.getDistance(self.pose[target], self.pose[second], dimension) / dicision
            right = self.getDistance(self.pose[target+1], self.pose[second], dimension) / dicision
        else:
            left = self.getDistance(self.pose[target], self.pose[second], dimension) / dicision
            right = self.getDistance(self.pose[target+1], self.pose[second+1], dimension) / dicision
        if direction == 'AVG':
            return (left + right)/2
        elif direction == 'LEFT':
            return left
        elif direction == 'RIGHT':
            return right
    
    def getAngleWithDirection(self, target, second, thrid, dimension, direction):
        if target == 0:
            left = self.getAngle(self.pose[target], self.pose[second], self.pose[thrid], dimension)
            right = self.getAngle(self.pose[target], self.pose[second+1], self.pose[thrid+1], dimension)
        elif second == 0:
            left = self.getAngle(self.pose[target], self.pose[second], self.pose[thrid], dimension)
            right = self.getAngle(self.pose[target+1], self.pose[second], self.pose[thrid+1], dimension)
        elif thrid == 0:
            left = self.getAngle(self.pose[target], self.pose[second], self.pose[thrid], dimension)
            right = self.getAngle(self.pose[target+1], self.pose[second+1], self.pose[thrid], dimension)
        else:
            left = self.getAngle(self.pose[target], self.pose[second], self.pose[thrid], dimension)
            right = self.getAngle(self.pose[target+1], self.pose[second+1], self.pose[thrid+1], dimension)
        if direction == 'AVG':
            return (left + right)/2
        elif direction == 'LEFT':
            return left
        elif direction == 'RIGHT':
            return right
    
    def getPlaneEachWithDirection(self, target, dimension, direction):
            return self.getPlane(self.pose[target], self.pose[target+1], dimension)
    
    def getPlaneWithDirection(self, target, second, dimension, direction):
        if target == 0:
            left = self.getPlane(self.pose[target], self.pose[second], dimension)
            right = self.getPlane(self.pose[target], self.pose[second+1], dimension)
        elif second == 0:
            left = self.getPlane(self.pose[target], self.pose[second], dimension)
            right = self.getPlane(self.pose[target+1], self.pose[second], dimension)
        else:
            left = self.getPlane(self.pose[target], self.pose[second], dimension)
            right = self.getPlane(self.pose[target+1], self.pose[second+1], dimension)
        if direction == 'AVG':
            return (left + right)/2
        elif direction == 'LEFT':
            return left
        elif direction == 'RIGHT':
            return right
        
    def getLineEachWithDirection(self, target, dimension, direction, line):
        return self.getLine(self.pose[target], self.pose[target+1], dimension, line)
        
    def getLineWithDirection(self, target, second, dimension, direction, line):
        if target == 0:
            left = self.getLine(self.pose[target], self.pose[second], dimension, line)
            right = self.getLine(self.pose[target], self.pose[second+1], dimension, line)
        elif second == 0:
            left = self.getLine(self.pose[target], self.pose[second], dimension, line)
            right = self.getLine(self.pose[target+1], self.pose[second], dimension, line)
        else:
            left = self.getLine(self.pose[target], self.pose[second], dimension, line)
            right = self.getLine(self.pose[target+1], self.pose[second+1], dimension, line)
        if direction == 'AVG':
            return (left + right)/2
        elif direction == 'LEFT':
            return left
        elif direction == 'RIGHT':
            return right

    def getAngleFromString(self, angleSelect: str):
        if "/" not in angleSelect:
            func, *inputs = angleSelect.split(",")
            angle = round(getattr(self, func)(*inputs), 2)
        else:
            numerator, denominator = angleSelect.split("/")
            func, *inputs = numerator.split(",")
            numeratorAngle = round(getattr(self, func)(*inputs), 2)
            func, *inputs = denominator.split(",")
            denominatorAngle = round(getattr(self, func)(*inputs), 2)
            if denominatorAngle == 0: 
                denominatorAngle = 1
            angle = numeratorAngle / denominatorAngle
        return angle

    def getCoord(self, a, dimension):
        if dimension == X:
            return a.x
        elif dimension == Y:
            return a.y
        elif dimension == Z:
            return a.z

    def getDiffer(self, a, b, dimension):
        if dimension == X:
            return a.x - b.x
        elif dimension == Y:
            return a.y - b.y
        elif dimension == Z:
            return a.z - b.z

    def getDistance(self, a, b, dimension):
        aX = abs(a.x - b.x)
        aY = abs(a.y - b.y)
        aZ = abs(a.z - b.z)
        distance = 0
        if dimension == X:
            distance = aX
        elif dimension == Y:
            distance = aY
        elif dimension == Z:
            distance = aZ
        elif dimension == XY:
            distance = math.sqrt(aX ** 2 + aY ** 2)
        elif dimension == YZ:
            distance = math.sqrt(aY ** 2 + aZ ** 2)
        elif dimension == XZ:
            distance = math.sqrt(aX ** 2 + aZ ** 2)
        else:
            distance = math.sqrt(aX ** 2 + aY ** 2 + aZ ** 2)
        return distance

    def calAngle(self, a, b, c):
        if b == 0 or c == 0:
            return 0
        cosineValue = (b ** 2 + c ** 2 - a ** 2) / (2 * b * c)
        cosineValue = max(-1, cosineValue)
        cosineValue = min(1, cosineValue)
        degree = math.acos(cosineValue)
        return math.degrees(degree)

    def getAngle(self, targetPoint, insidePoint, lastPoint, dimension):
        a = self.getDistance(insidePoint, lastPoint, dimension)
        b = self.getDistance(targetPoint, insidePoint, dimension)
        c = self.getDistance(targetPoint, lastPoint, dimension)
        return self.calAngle(a, b, c)
       
    def getPlane(self, a, b, dimension):
        if dimension == XY:
            distanceA = self.getDistance(a, b, Z)
        elif dimension == YZ:
            distanceA = self.getDistance(a, b, X)
        elif dimension == XZ:
            distanceA = self.getDistance(a, b, Y)
        
        distanceB = self.getDistance(a, b, XYZ)
        distanceC = self.getDistance(a, b, dimension)
        return self.calAngle(distanceA, distanceB, distanceC)
    
    def getLine(self, a, b, dimension, line):
        if line == X:
            if dimension == XY:
                distanceA = self.getDistance(a, b, Y)
            elif dimension == XZ:
                distanceA = self.getDistance(a, b, Z)        
        elif line == Y:
            if dimension == XY:
                distanceA = self.getDistance(a, b, X)
            elif dimension == YZ:
                distanceA = self.getDistance(a, b, Z)
        elif line == Z:
            if dimension == YZ:
                distanceA = self.getDistance(a, b, Y)
            elif dimension == XZ:
                distanceA = self.getDistance(a, b, X)
        distanceB = self.getDistance(a, b, dimension)
        distanceC = self.getDistance(a, b, line)
        return self.calAngle(distanceA, distanceB, distanceC)
        
    def getCenterPoint(self, firstPoint, secondPoint):
        x = (firstPoint.x + secondPoint.x) / 2
        y = (firstPoint.y + secondPoint.y) / 2
        z = (firstPoint.z + secondPoint.z) / 2
        return Coordinate(x, y, z)        


    def getEyePoint(self, dimension, direction):
        left = self.getCoord(self.leftEye, dimension)
        right = self.getCoord(self.rightEye, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg            


    def getEyeNosePlane(self, dimension=XZ, direction=AVG):
        left = self.getPlane(self.leftEye, self.leftNose, dimension)
        right = self.getPlane(self.rightEye, self.rightNose, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getEyeNoseMinusPlane(self, dimension=XZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getEyeNosePlane(dimension, LEFT)
        else:
            return self.getEyeNosePlane(dimension, RIGHT)        


    def getNosePoint(self, dimension, direction):
        left = self.getCoord(self.leftNose, dimension)
        right = self.getCoord(self.rightNose, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg            
            
            
    def getNoseAnkleCenterDistance(self, dimension=XYZ):
        return self.getDistance(self.leftNose, self.getCenterPoint(self.leftAnkle, self.rightAnkle), dimension)        


    def getNoseShoulderHipAngle(self, dimension=XYZ, direction=AVG):
        left = self.getAngle(self.leftNose, self.leftShoulder, self.leftHip, dimension)
        right = self.getAngle(self.rightNose, self.rightShoulder, self.rightHip, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getNoseShoulderHipMinusAngle(self, dimension=XZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getNoseShoulderHipAngle(dimension, LEFT)
        else:
            return self.getNoseShoulderHipAngle(dimension, RIGHT)    
    
    
    def getNoseShoulderCenterPlane(self, dimension=XZ):
        return self.getPlane(self.leftNose, self.getCenterPoint(self.leftShoulder, self.rightShoulder), dimension)            


    def getNoseHipLine(self, dimension, line, direction):
        left = self.getLine(self.leftNose, self.leftHip, dimension, line)
        right = self.getLine(self.rightNose, self.rightHip, dimension, line)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg            


    def getNoseShoulderLine(self, dimension, line, direction):
        left = self.getLine(self.leftNose, self.leftShoulder, dimension, line)
        right = self.getLine(self.rightNose, self.rightShoulder, dimension, line)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getNoseHipMinusLine(self, dimension, line, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getNoseHipLine(dimension, line, LEFT)
        else:
            return self.getNoseHipLine(dimension, line, RIGHT)        


    def getNoseShoulderMinusLine(self, dimension, line, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getNoseShoulderLine(dimension, line, LEFT)
        else:
            return self.getNoseShoulderLine(dimension, line, RIGHT)        


    def getNoseShoulderPlusLine(self, dimension, line, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) > self.getCoord(right, sDimension):
            return self.getNoseShoulderLine(dimension, line, LEFT)
        else:
            return self.getNoseShoulderLine(dimension, line, RIGHT)        


    def getEarPoint(self, dimension, direction):
        left = self.getCoord(self.leftEar, dimension)
        right = self.getCoord(self.rightEar, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getShoulderPoint(self, dimension, direction):
        left = self.getCoord(self.leftShoulder, dimension)
        right = self.getCoord(self.rightShoulder, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getShoulderPlusPoint(self, dimension, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) > self.getCoord(right, sDimension):
            return self.getShoulderPoint(dimension, LEFT)
        else:
            return self.getShoulderPoint(dimension, RIGHT)        


    def getShoulderMinusPoint(self, dimension, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getShoulderPoint(dimension, LEFT)
        else:
            return self.getShoulderPoint(dimension, RIGHT)    
    
    
    def getShoulderDistance(self, dimension=XYZ):
        return self.getDistance(self.leftShoulder, self.rightShoulder, dimension)        


    def getShoulderHipDistance(self, dimension=XYZ, direction=AVG):
        left = self.getDistance(self.leftShoulder, self.leftHip, dimension)
        right = self.getDistance(self.rightShoulder, self.rightHip, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        
        
    def getShoulderCenterHipCenterDistance(self, dimension=XYZ):
        shoulder_center = self.getCenterPoint(self.leftShoulder, self.rightShoulder)
        hip_center = self.getCenterPoint(self.leftHip, self.rightHip)
        result = self.getDistance(shoulder_center, hip_center, dimension)
        return result

    def getNoseShoulderDistance(self, dimension=XYZ, direction=AVG):
        left = self.getDistance(self.leftNose, self.leftShoulder, dimension)
        right = self.getDistance(self.rightNose, self.rightShoulder, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg
        
    def getNoseShoulderCenterDistance(self, dimension=XYZ):
        center = self.getCenterPoint(self.leftShoulder, self.rightShoulder)
        result = self.getDistance(self.leftNose, center, dimension)
        return result
        

    def getNoseShoulderPlusDistance(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) > self.getCoord(right, sDimension):
            return self.getNoseShoulderDistance(dimension, LEFT)
        else:
            return self.getNoseShoulderDistance(dimension, RIGHT)        


    def getNoseShoulderMinusDistance(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getNoseShoulderDistance(dimension, LEFT)
        else:
            return self.getNoseShoulderDistance(dimension, RIGHT)        


    def getShoulderKneeDistance(self, dimension=XYZ, direction=AVG):
        left = self.getDistance(self.leftShoulder, self.leftKnee, dimension)
        right = self.getDistance(self.rightShoulder, self.rightKnee, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getShoulderWristDistance(self, dimension=XYZ, direction=AVG):
        left = self.getDistance(self.leftShoulder, self.leftWrist, dimension)
        right = self.getDistance(self.rightShoulder, self.rightWrist, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getShoulderElbowDistance(self, dimension=XYZ, direction=AVG):
        left = self.getDistance(self.leftShoulder, self.leftElbow, dimension)
        right = self.getDistance(self.rightShoulder, self.rightElbow, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getShoulderHipPlusDistance(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) > self.getCoord(right, sDimension):
            return self.getShoulderHipDistance(dimension, LEFT)
        else:
            return self.getShoulderHipDistance(dimension, RIGHT)        


    def getShoulderHipMinusDistance(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getShoulderHipDistance(dimension, LEFT)
        else:
            return self.getShoulderHipDistance(dimension, RIGHT)        


    def getShoulderKneeMinusDistance(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getShoulderKneeDistance(dimension, LEFT)
        else:
            return self.getShoulderKneeDistance(dimension, RIGHT)        


    def getShoulderElbowMinusDistance(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getShoulderElbowDistance(dimension, LEFT)
        else:
            return self.getShoulderElbowDistance(dimension, RIGHT)        


    def getShoulderNoseHipAngle(self, dimension=XYZ, direction=AVG):
        left = self.getAngle(self.leftShoulder, self.leftNose, self.leftHip, dimension)
        right = self.getAngle(self.rightShoulder, self.rightNose, self.rightHip, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getShoulderElbowHipAngle(self, dimension=XYZ, direction=AVG):
        left = self.getAngle(self.leftShoulder, self.leftElbow, self.leftHip, dimension)
        right = self.getAngle(self.rightShoulder, self.rightElbow, self.rightHip, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getShoulderWristHipAngle(self, dimension=XYZ, direction=AVG):
        left = self.getAngle(self.leftShoulder, self.leftWrist, self.leftHip, dimension)
        right = self.getAngle(self.rightShoulder, self.rightWrist, self.rightHip, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getShoulderWristHipMinusAngle(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getShoulderWristHipAngle(dimension, LEFT)
        else:
            return self.getShoulderWristHipAngle(dimension, RIGHT)        


    def getShoulderNoseHipMinusAngle(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getShoulderNoseHipAngle(dimension, LEFT)
        else:
            return self.getShoulderNoseHipAngle(dimension, RIGHT)        


    def getShoulderElbowHipPlusAngle(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) > self.getCoord(right, sDimension):
            return self.getShoulderElbowHipAngle(dimension, LEFT)
        else:
            return self.getShoulderElbowHipAngle(dimension, RIGHT)
    
    
    def getShoulderWristShoulderAngle(self, dimension=XYZ, direction=AVG):
        left = self.getAngle(self.leftShoulder, self.leftWrist, self.rightShoulder, dimension)
        right = self.getAngle(self.rightShoulder, self.rightWrist, self.leftShoulder, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg    
    
    
    def getShoulderElbowShoulderAngle(self, dimension=XYZ, direction=AVG):
        left = self.getAngle(self.leftShoulder, self.leftElbow, self.rightShoulder, dimension)
        right = self.getAngle(self.rightShoulder, self.rightElbow, self.leftShoulder, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getShoulderElbowHipMinusAngle(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getShoulderElbowHipAngle(dimension, LEFT)
        else:
            return self.getShoulderElbowHipAngle(dimension, RIGHT)            


    def getShoulderPlane(self, dimension=XZ):
        return self.getPlane(self.leftShoulder, self.rightShoulder, dimension)            


    def getShoulderHipPlane(self, dimension=XZ, direction=AVG):
        left = self.getPlane(self.leftShoulder, self.leftHip, dimension)
        right = self.getPlane(self.rightShoulder, self.rightHip, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg            


    def getShoulderElbowPlane(self, dimension=XZ, direction=AVG):
        left = self.getPlane(self.leftShoulder, self.leftElbow, dimension)
        right = self.getPlane(self.rightShoulder, self.rightElbow, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getShoulderHipMinusPlane(self, dimension=XZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getShoulderHipPlane(dimension, LEFT)
        else:
            return self.getShoulderHipPlane(dimension, RIGHT)        


    def getShoulderElbowMinusPlane(self, dimension=XZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getShoulderElbowPlane(dimension, LEFT)
        else:
            return self.getShoulderElbowPlane(dimension, RIGHT)            


    def getShoulderLine(self, dimension, line):
        return self.getLine(self.leftShoulder, self.rightShoulder, dimension, line)            


    def getShoulderHipLine(self, dimension, line, direction):
        left = self.getLine(self.leftShoulder, self.leftHip, dimension, line)
        right = self.getLine(self.rightShoulder, self.rightHip, dimension, line)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg            


    def getShoulderElbowLine(self, dimension, line, direction):
        left = self.getLine(self.leftShoulder, self.leftElbow, dimension, line)
        right = self.getLine(self.rightShoulder, self.rightElbow, dimension, line)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getShoulderHipPlusLine(self, dimension, line, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) > self.getCoord(right, sDimension):
            return self.getShoulderHipLine(dimension, line, LEFT)
        else:
            return self.getShoulderHipLine(dimension, line, RIGHT)        


    def getShoulderHipMinusLine(self, dimension, line, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getShoulderHipLine(dimension, line, LEFT)
        else:
            return self.getShoulderHipLine(dimension, line, RIGHT)        


    def getShoulderElbowPlusLine(self, dimension, line, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) > self.getCoord(right, sDimension):
            return self.getShoulderElbowLine(dimension, line, LEFT)
        else:
            return self.getShoulderElbowLine(dimension, line, RIGHT)        


    def getShoulderElbowMinusLine(self, dimension, line, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getShoulderElbowLine(dimension, line, LEFT)
        else:
            return self.getShoulderElbowLine(dimension, line, RIGHT)    

    def getShoulderCenterHipCenterLine(self, dimension, line):
        shoulderCenter = self.getCenterPoint(self.leftShoulder, self.rightShoulder)
        hipCenter = self.getCenterPoint(self.leftHip, self.rightHip)
        return self.getLine(shoulderCenter, hipCenter, dimension, line)    

    def getShoulderPlusNumber(self, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.rightShoulder
        else:
            return self.leftShoulder    


    def getShoulderMinusNumber(self, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.leftShoulder
        else:
            return self.rightShoulder        


    def getElbowPoint(self, dimension, direction):
        left = self.getCoord(self.leftElbow, dimension)
        right = self.getCoord(self.rightElbow, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getElbowPlusPoint(self, dimension, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) > self.getCoord(right, sDimension):
            return self.getElbowPoint(dimension, LEFT)
        else:
            return self.getElbowPoint(dimension, RIGHT)        


    def getElbowMinusPoint(self, dimension, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getElbowPoint(dimension, LEFT)
        else:
            return self.getElbowPoint(dimension, RIGHT)    
    
    
    def getElbowDistance(self, dimension=XYZ):
        return self.getDistance(self.leftElbow, self.rightElbow, dimension)        


    def getElbowWristDistance(self, dimension=XYZ, direction=AVG):
        left = self.getDistance(self.leftElbow, self.leftWrist, dimension)
        right = self.getDistance(self.rightElbow, self.rightWrist, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getElbowShoulderDistance(self, dimension=XYZ, direction=AVG):
        left = self.getDistance(self.leftElbow, self.leftShoulder, dimension)
        right = self.getDistance(self.rightElbow, self.rightShoulder, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        
        
    
    def getElbowShoulderMinusDistance(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getElbowShoulderDistance(dimension, LEFT)
        else:
            return self.getElbowShoulderDistance(dimension, RIGHT)


    def getElbowWristShoulderAngle(self, dimension=XYZ, direction=AVG):
        left = self.getAngle(self.leftElbow, self.leftWrist, self.leftShoulder, dimension)
        right = self.getAngle(self.rightElbow, self.rightWrist, self.rightShoulder, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getElbowWristShoulderPlusAngle(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) > self.getCoord(right, sDimension):
            return self.getElbowWristShoulderAngle(dimension, LEFT)
        else:
            return self.getElbowWristShoulderAngle(dimension, RIGHT)        


    def getElbowWristShoulderMinusAngle(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getElbowWristShoulderAngle(dimension, LEFT)
        else:
            return self.getElbowWristShoulderAngle(dimension, RIGHT)            


    def getElbowWristPlane(self, dimension=XZ, direction=AVG):
        left = self.getPlane(self.leftElbow, self.leftWrist, dimension)
        right = self.getPlane(self.rightElbow, self.rightWrist, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getElbowWristMinusPlane(self, dimension=XZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getElbowWristPlane(dimension, LEFT)
        else:
            return self.getElbowWristPlane(dimension, RIGHT)            


    def getElbowWristLine(self, dimension, line, direction):
        left = self.getLine(self.leftElbow, self.leftWrist, dimension, line)
        right = self.getLine(self.rightElbow, self.rightWrist, dimension, line)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getElbowWristMinusLine(self, dimension, line, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getElbowWristLine(dimension, line, LEFT)
        else:
            return self.getElbowWristLine(dimension, line, RIGHT)    


    def getElbowPlusNumber(self, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.rightElbow
        else:
            return self.leftElbow    


    def getElbowMinusNumber(self, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.leftElbow
        else:
            return self.rightElbow        


    def getHipPoint(self, dimension, direction):
        left = self.getCoord(self.leftHip, dimension)
        right = self.getCoord(self.rightHip, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        

    def getHipCenterPoint(self):
        hipCenter = self.getCenterPoint(self.leftHip, self.rightHip)
        return hipCenter


    def getHipMinusPoint(self, dimension, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getHipPoint(dimension, LEFT)
        else:
            return self.getHipPoint(dimension, RIGHT)    
    
    
    def getHipDistance(self, dimension=XYZ):
        return self.getDistance(self.leftHip, self.rightHip, dimension)        


    def getHipKneeDistance(self, dimension=XYZ, direction=AVG):
        left = self.getDistance(self.leftHip, self.leftKnee, dimension)
        right = self.getDistance(self.rightHip, self.rightKnee, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getHipWristDistance(self, dimension=XYZ, direction=AVG):
        left = self.getDistance(self.leftHip, self.leftWrist, dimension)
        right = self.getDistance(self.rightHip, self.rightWrist, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getHipAnkleDistance(self, dimension=XYZ, direction=AVG):
        left = self.getDistance(self.leftHip, self.leftAnkle, dimension)
        right = self.getDistance(self.rightHip, self.rightAnkle, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getHipKneePlusDistance(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) > self.getCoord(right, sDimension):
            return self.getHipKneeDistance(dimension, LEFT)
        else:
            return self.getHipKneeDistance(dimension, RIGHT)        


    def getHipKneeMinusDistance(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getHipKneeDistance(dimension, LEFT)
        else:
            return self.getHipKneeDistance(dimension, RIGHT)        


    def getHipAnkleMinusDistance(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getHipAnkleDistance(dimension, LEFT)
        else:
            return self.getHipAnkleDistance(dimension, RIGHT)    
    
    
    def getHipKneeHipAngle(self, dimension=XYZ, direction=AVG):
        left = self.getAngle(self.leftHip, self.leftKnee, self.rightHip, dimension)
        right = self.getAngle(self.rightHip, self.rightKnee, self.leftHip, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg    
    
    def getHipShoulderHipAngle(self, dimension=XYZ, direction=AVG):
        left = self.getAngle(self.leftHip, self.leftShoulder, self.rightHip, dimension)
        right = self.getAngle(self.rightHip, self.rightShoulder, self.leftHip, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg    
        
    def getHipKneeKneeAngle(self, dimension=XYZ, direction=AVG):
        left = self.getAngle(self.leftHip, self.leftKnee, self.rightKnee, dimension)
        right = self.getAngle(self.rightHip, self.rightKnee, self.leftKnee, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getHipKneeShoulderAngle(self, dimension=XYZ, direction=AVG):
        left = self.getAngle(self.leftHip, self.leftKnee, self.leftShoulder, dimension)
        right = self.getAngle(self.rightHip, self.rightKnee, self.rightShoulder, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        

    def getHipShoulderHipMinusAngle(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getHipShoulderHipAngle(dimension, LEFT)
        else:
            return self.getHipShoulderHipAngle(dimension, RIGHT)      
        
    def getHipShoulderHipPlusAngle(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getHipShoulderHipAngle(dimension, RIGHT)
        else:
            return self.getHipShoulderHipAngle(dimension, LEFT)   
        
    def getHipKneeHipMinusAngle(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getHipKneeHipAngle(dimension, LEFT)
        else:
            return self.getHipKneeHipAngle(dimension, RIGHT)        


    def getHipKneeKneeMinusAngle(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getHipKneeKneeAngle(dimension, LEFT)
        else:
            return self.getHipKneeKneeAngle(dimension, RIGHT)        


    def getHipAnkleShoulderAngle(self, dimension=XYZ, direction=AVG):
        left = self.getAngle(self.leftHip, self.leftAnkle, self.leftShoulder, dimension)
        right = self.getAngle(self.rightHip, self.rightAnkle, self.rightShoulder, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getHipKneeShoulderPlusAngle(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) > self.getCoord(right, sDimension):
            return self.getHipKneeShoulderAngle(dimension, LEFT)
        else:
            return self.getHipKneeShoulderAngle(dimension, RIGHT)        


    def getHipKneeShoulderMinusAngle(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getHipKneeShoulderAngle(dimension, LEFT)
        else:
            return self.getHipKneeShoulderAngle(dimension, RIGHT)        


    def getHipAnkleShoulderMinusAngle(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getHipAnkleShoulderAngle(dimension, LEFT)
        else:
            return self.getHipAnkleShoulderAngle(dimension, RIGHT)            


    def getHipPlane(self, dimension=XZ):
        return self.getPlane(self.leftHip, self.rightHip, dimension)            


    def getHipKneePlane(self, dimension=XZ, direction=AVG):
        left = self.getPlane(self.leftHip, self.leftKnee, dimension)
        right = self.getPlane(self.rightHip, self.rightKnee, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getHipKneeMinusPlane(self, dimension=XZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getHipKneePlane(dimension, LEFT)
        else:
            return self.getHipKneePlane(dimension, RIGHT)            


    def getHipLine(self, dimension, line):
        return self.getLine(self.leftHip, self.rightHip, dimension, line)            


    def getHipKneeLine(self, dimension, line, direction):
        left = self.getLine(self.leftHip, self.leftKnee, dimension, line)
        right = self.getLine(self.rightHip, self.rightKnee, dimension, line)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg            


    def getHipAnkleLine(self, dimension, line, direction):
        left = self.getLine(self.leftHip, self.leftAnkle, dimension, line)
        right = self.getLine(self.rightHip, self.rightAnkle, dimension, line)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getHipKneePlusLine(self, dimension, line, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) > self.getCoord(right, sDimension):
            return self.getHipKneeLine(dimension, line, LEFT)
        else:
            return self.getHipKneeLine(dimension, line, RIGHT)        


    def getHipKneeMinusLine(self, dimension, line, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getHipKneeLine(dimension, line, LEFT)
        else:
            return self.getHipKneeLine(dimension, line, RIGHT)        


    def getHipAnklePlusLine(self, dimension, line, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) > self.getCoord(right, sDimension):
            return self.getHipAnkleLine(dimension, line, LEFT)
        else:
            return self.getHipAnkleLine(dimension, line, RIGHT)        


    def getHipAnkleMinusLine(self, dimension, line, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getHipAnkleLine(dimension, line, LEFT)
        else:
            return self.getHipAnkleLine(dimension, line, RIGHT)    


    def getHipMinusNumber(self, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.leftHip
        else:
            return self.rightHip        


    def getWristPoint(self, dimension, direction):
        left = self.getCoord(self.leftWrist, dimension)
        right = self.getCoord(self.rightWrist, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getWristMinusPoint(self, dimension, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getWristPoint(dimension, LEFT)
        else:
            return self.getWristPoint(dimension, RIGHT)    
    
    
    def getWristDistance(self, dimension=XYZ):
        return self.getDistance(self.leftWrist, self.rightWrist, dimension)        


    def getWristHipDistance(self, dimension=XYZ, direction=AVG):
        left = self.getDistance(self.leftWrist, self.leftHip, dimension)
        right = self.getDistance(self.rightWrist, self.rightHip, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getWristKneeDistance(self, dimension=XYZ, direction=AVG):
        left = self.getDistance(self.leftWrist, self.leftKnee, dimension)
        right = self.getDistance(self.rightWrist, self.rightKnee, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getWristIndexDistance(self, dimension=XYZ, direction=AVG):
        left = self.getDistance(self.leftWrist, self.leftIndex, dimension)
        right = self.getDistance(self.rightWrist, self.rightIndex, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getWristShoulderDistance(self, dimension=XYZ, direction=AVG):
        left = self.getDistance(self.leftWrist, self.leftShoulder, dimension)
        right = self.getDistance(self.rightWrist, self.rightShoulder, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getWristHipMinusDistance(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getWristHipDistance(dimension, LEFT)
        else:
            return self.getWristHipDistance(dimension, RIGHT)        


    def getWristKneePlusDistance(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) > self.getCoord(right, sDimension):
            return self.getWristKneeDistance(dimension, LEFT)
        else:
            return self.getWristKneeDistance(dimension, RIGHT)        


    def getWristKneeMinusDistance(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getWristKneeDistance(dimension, LEFT)
        else:
            return self.getWristKneeDistance(dimension, RIGHT)        


    def getWristShoulderMinusDistance(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getWristShoulderDistance(dimension, LEFT)
        else:
            return self.getWristShoulderDistance(dimension, RIGHT)        


    def getWristElbowIndexAngle(self, dimension=XYZ, direction=AVG):
        left = self.getAngle(self.leftWrist, self.leftElbow, self.leftIndex, dimension)
        right = self.getAngle(self.rightWrist, self.rightElbow, self.rightIndex, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getWristElbowPinkyAngle(self, dimension=XYZ, direction=AVG):
        left = self.getAngle(self.leftWrist, self.leftElbow, self.leftPinky, dimension)
        right = self.getAngle(self.rightWrist, self.rightElbow, self.rightPinky, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getWristElbowIndexPlusAngle(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) > self.getCoord(right, sDimension):
            return self.getWristElbowIndexAngle(dimension, LEFT)
        else:
            return self.getWristElbowIndexAngle(dimension, RIGHT)        


    def getWristElbowPinkyMinusAngle(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getWristElbowPinkyAngle(dimension, LEFT)
        else:
            return self.getWristElbowPinkyAngle(dimension, RIGHT)        


    def getWristElbowIndexMinusAngle(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getWristElbowIndexAngle(dimension, LEFT)
        else:
            return self.getWristElbowIndexAngle(dimension, RIGHT)            


    def getWristThumbPlane(self, dimension=XZ, direction=AVG):
        left = self.getPlane(self.leftWrist, self.leftThumb, dimension)
        right = self.getPlane(self.rightWrist, self.rightThumb, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg            


    def getWristPinkyPlane(self, dimension=XZ, direction=AVG):
        left = self.getPlane(self.leftWrist, self.leftPinky, dimension)
        right = self.getPlane(self.rightWrist, self.rightPinky, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getWristPinkyMinusPlane(self, dimension=XZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getWristPinkyPlane(dimension, LEFT)
        else:
            return self.getWristPinkyPlane(dimension, RIGHT)        


    def getWristThumbMinusPlane(self, dimension=XZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getWristThumbPlane(dimension, LEFT)
        else:
            return self.getWristThumbPlane(dimension, RIGHT)    


    def getWristPlusNumber(self, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.rightWrist
        else:
            return self.leftWrist    


    def getWristMinusNumber(self, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.leftWrist
        else:
            return self.rightWrist    


    def getPinkyMinusNumber(self, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.leftPinky
        else:
            return self.rightPinky        


    def getKneePoint(self, dimension, direction):
        left = self.getCoord(self.leftKnee, dimension)
        right = self.getCoord(self.rightKnee, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getKneeMinusPoint(self, dimension, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getKneePoint(dimension, LEFT)
        else:
            return self.getKneePoint(dimension, RIGHT)    
    
    
    def getKneeDistance(self, dimension=XYZ):
        return self.getDistance(self.leftKnee, self.rightKnee, dimension)        


    def getKneeAnkleDistance(self, dimension=XYZ, direction=AVG):
        left = self.getDistance(self.leftKnee, self.leftAnkle, dimension)
        right = self.getDistance(self.rightKnee, self.rightAnkle, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getKneeAnkleMinusDistance(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getKneeAnkleDistance(dimension, LEFT)
        else:
            return self.getKneeAnkleDistance(dimension, RIGHT)        


    def getKneeHipAnkleAngle(self, dimension=XYZ, direction=AVG):
        left = self.getAngle(self.leftKnee, self.leftHip, self.leftAnkle, dimension)
        right = self.getAngle(self.rightKnee, self.rightHip, self.rightAnkle, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getKneeHipAnklePlusAngle(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) > self.getCoord(right, sDimension):
            return self.getKneeHipAnkleAngle(dimension, LEFT)
        else:
            return self.getKneeHipAnkleAngle(dimension, RIGHT)        


    def getKneeHipAnkleMinusAngle(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getKneeHipAnkleAngle(dimension, LEFT)
        else:
            return self.getKneeHipAnkleAngle(dimension, RIGHT)            


    def getKneeAnklePlane(self, dimension=XZ, direction=AVG):
        left = self.getPlane(self.leftKnee, self.leftAnkle, dimension)
        right = self.getPlane(self.rightKnee, self.rightAnkle, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getKneeAnkleMinusPlane(self, dimension=XZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getKneeAnklePlane(dimension, LEFT)
        else:
            return self.getKneeAnklePlane(dimension, RIGHT)            


    def getKneeAnkleLine(self, dimension, line, direction):
        left = self.getLine(self.leftKnee, self.leftAnkle, dimension, line)
        right = self.getLine(self.rightKnee, self.rightAnkle, dimension, line)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getKneeAnklePlusLine(self, dimension, line, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) > self.getCoord(right, sDimension):
            return self.getKneeAnkleLine(dimension, line, LEFT)
        else:
            return self.getKneeAnkleLine(dimension, line, RIGHT)        


    def getKneeAnkleMinusLine(self, dimension, line, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getKneeAnkleLine(dimension, line, LEFT)
        else:
            return self.getKneeAnkleLine(dimension, line, RIGHT)    


    def getKneeMinusNumber(self, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.leftKnee
        else:
            return self.rightKnee        


    def getAnklePoint(self, dimension, direction):
        left = self.getCoord(self.leftAnkle, dimension)
        right = self.getCoord(self.rightAnkle, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getAnkleMinusPoint(self, dimension, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getAnklePoint(dimension, LEFT)
        else:
            return self.getAnklePoint(dimension, RIGHT)        


    def getAnklePlusPoint(self, dimension, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) > self.getCoord(right, sDimension):
            return self.getAnklePoint(dimension, LEFT)
        else:
            return self.getAnklePoint(dimension, RIGHT)    
    
    
    def getAnkleDistance(self, dimension=XYZ):
        return self.getDistance(self.leftAnkle, self.rightAnkle, dimension)        

    def getAnkleFootDistance(self, dimension=XYZ, direction=AVG):
        left_foot = self.getCenterPoint(self.leftFootIndex, self.leftHeel)
        right_foot = self.getCenterPoint(self.rightFootIndex, self.rightHeel)
        left = self.getDistance(left_foot, self.leftAnkle, dimension)
        right = self.getDistance(right_foot, self.rightAnkle, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        

    def getAnkleKneeFootIndexAngle(self, dimension=XYZ, direction=AVG):
        left = self.getAngle(self.leftAnkle, self.leftKnee, self.leftFootIndex, dimension)
        right = self.getAngle(self.rightAnkle, self.rightKnee, self.rightFootIndex, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg    
    
    
    def getAnkleFootIndexAnkleAngle(self, dimension=XYZ, direction=AVG):
        left = self.getAngle(self.leftAnkle, self.leftFootIndex, self.rightAnkle, dimension)
        right = self.getAngle(self.rightAnkle, self.rightFootIndex, self.leftAnkle, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getAnkleKneeFootIndexMinusAngle(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getAnkleKneeFootIndexAngle(dimension, LEFT)
        else:
            return self.getAnkleKneeFootIndexAngle(dimension, RIGHT)        


    def getAnkleFootIndexHeelAngle(self, dimension=XYZ, direction=AVG):
        left = self.getAngle(self.leftAnkle, self.leftFootIndex, self.leftHeel, dimension)
        right = self.getAngle(self.rightAnkle, self.rightFootIndex, self.rightHeel, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getAnkleFootIndexHeelMinusAngle(self, dimension=XYZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getAnkleFootIndexHeelAngle(dimension, LEFT)
        else:
            return self.getAnkleFootIndexHeelAngle(dimension, RIGHT)            


    def getAnklePlane(self, dimension=XZ):
        return self.getPlane(self.leftAnkle, self.rightAnkle, dimension)            


    def getAnkleFootIndexPlane(self, dimension=XZ, direction=AVG):
        left = self.getPlane(self.leftAnkle, self.leftFootIndex, dimension)
        right = self.getPlane(self.rightAnkle, self.rightFootIndex, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getAnkleFootIndexMinusPlane(self, dimension=XZ, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getAnkleFootIndexPlane(dimension, LEFT)
        else:
            return self.getAnkleFootIndexPlane(dimension, RIGHT)            


    def getAnkleLine(self, dimension):
        return self.getLine(self.leftAnkle, self.rightAnkle, dimension)            


    def getAnkleFootIndexLine(self, dimension, line, direction):
        left = self.getLine(self.leftAnkle, self.leftFootIndex, dimension, line)
        right = self.getLine(self.rightAnkle, self.rightFootIndex, dimension, line)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getAnkleFootIndexMinusLine(self, dimension, line, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getAnkleFootIndexLine(dimension, line, LEFT)
        else:
            return self.getAnkleFootIndexLine(dimension, line, RIGHT)        


    def getAnkleFootIndexPlusLine(self, dimension, line, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) > self.getCoord(right, sDimension):
            return self.getAnkleFootIndexLine(dimension, line, LEFT)
        else:
            return self.getAnkleFootIndexLine(dimension, line, RIGHT)    


    def getAnklePlusNumber(self, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.rightAnkle
        else:
            return self.leftAnkle    


    def getAnkleMinusNumber(self, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.leftAnkle
        else:
            return self.rightAnkle            

    def getHeelPorint(self, dimension, direction):
        left = self.getCoord(self.leftHeel, dimension)
        right = self.getCoord(self.rightHeel, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        

    def getFootindexPoint(self, dimension, direction):
        left = self.getCoord(self.leftFootIndex, dimension)
        right = self.getCoord(self.rightFootIndex, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        

    def getFootIndexDistance(self, dimension=XYZ):
        return self.getDistance(self.leftFootIndex, self.rightFootIndex, dimension)

    def getFootIndexHeelDistance(self, dimension=XYZ, direction=AVG):
        left = self.getDistance(self.leftFootIndex, self.leftHeel, dimension)
        right = self.getDistance(self.rightFootIndex, self.rightHeel, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        
        
    def getFootIndexHeelLine(self, dimension, line, direction):
        left = self.getLine(self.leftFootIndex, self.leftHeel, dimension, line)
        right = self.getLine(self.rightFootIndex, self.rightHeel, dimension, line)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        


    def getFootIndexHeelMinusLine(self, dimension, line, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) < self.getCoord(right, sDimension):
            return self.getFootIndexHeelLine(dimension, line, LEFT)
        else:
            return self.getFootIndexHeelLine(dimension, line, RIGHT)        


    def getFootIndexHeelPlusLine(self, dimension, line, sDimension=Z, standard=LEFT_SHOULDER):
        standard = int(standard)
        left = self.pose[standard-1] if standard % 2 == 0 else self.pose[standard]
        right = self.pose[standard] if standard % 2 == 0 else self.pose[standard+1]

        if self.getCoord(left, sDimension) > self.getCoord(right, sDimension):
            return self.getFootIndexHeelLine(dimension, line, LEFT)
        else:
            return self.getFootIndexHeelLine(dimension, line, RIGHT)
        
    def getWristPinkyMcpDistance(self, dimension=XYZ, direction=AVG):
        left = self.getDistance(self.leftHandWrist, self.leftHandPinkyMcp, dimension)
        right = self.getDistance(self.rightHandWrist, self.rightHandPinkyMcp, dimension)
        avg = (left + right) / 2
        if direction == LEFT:
            return left
        elif direction == RIGHT:
            return right
        elif direction == AVG:
            return avg        
        
    def getHipCenterScreenDistance(self, x, y, dimension=XYZ):
        x, y = int(x), int(y)
        hipcenter = self.getHipCenterPoint()
        print(f"JINWOO: {self.getDistance(hipcenter, Coordinate(x, y/2, hipcenter.z), dimension)}")
        return self.getDistance(hipcenter, Coordinate(x, y/2, hipcenter.z), dimension)


    # SwingEZ
    def isUserInFrame(self):
        return self.leftWrist.visibility > 0.8 and self.rightWrist.visibility > 0.8 and self.leftAnkle.visibility > 0.8 and self.rightAnkle.visibility > 0.8
    
    def isUserInFront(self):
        hipPlane = self.getHipPlane(XY)
        return int(hipPlane) in range(0, 45)
    
    def getIsFrontAddress(self):
        checkXBodyPairList = [
            (self.leftShoulder.x, self.rightShoulder.x),
            (self.leftHip.x, self.rightHip.x),
            (self.leftKnee.x, self.rightKnee.x),
            (self.leftAnkle.x, self.rightAnkle.x),
            (self.leftKnee.x, self.leftWrist.x),
            (self.rightWrist.x, self.rightKnee.x),
            (self.leftAnkle.x, self.leftNose.x),
            (self.leftNose.x, self.rightAnkle.x)
            ]
        checkYBodyPairList = [
            (self.getCenterPoint(self.leftElbow, self.rightElbow).y, self.getCenterPoint(self.leftShoulder, self.rightShoulder).y),
            (self.getCenterPoint(self.leftHip, self.rightHip).y, self.getCenterPoint(self.leftElbow, self.rightElbow).y)
            ]
        
        return all(pair[0] > pair[1] for pair in checkXBodyPairList) and all(pair[0] > pair[1] for pair in checkYBodyPairList)

    def getCheckTakeBackPosture(self):
        leftAramAngle = self.getAngle(self.leftShoulder, self.leftWrist, 
                                      Coordinate(self.leftShoulder.x, self.leftHip.y, self.leftHip.z), XY)
        centerWrist = self.getCenterPoint(self.leftWrist, self.rightWrist)
        checkPairList = [
            (leftAramAngle, 40.0),
            (self.leftWrist.x, self.rightWrist.x),
            (self.rightAnkle.x, centerWrist.x)
        ]
        return all(pair[0] > pair[1] for pair in checkPairList)
    
    def getCheckBackSwingPosture(self):
        checkPairList1 = [
            (self.leftWrist.x, self.rightWrist.x),
            ((self.leftHip.y + self.leftShoulder.y)/2, self.leftWrist.y)
        ]
        checkPairList2 = [
            (self.leftWrist.x, self.rightWrist.x),
            ((self.rightHip.y + self.rightShoulder.y)/2, self.rightWrist.y)
        ]
        return all(pair[0] > pair[1] for pair in checkPairList1) or all(pair[0] > pair[1] for pair in checkPairList2)

    def getCheckDownSwingPosture(self):
        bodyCenter = self.getCenterPoint(self.leftShoulder, self.rightHip)
        wristCenter = self.getCenterPoint(self.leftWrist, self.rightWrist)
        checkPairList = [
            (wristCenter.y, bodyCenter.y)
        ]
        return all(pair[0] > pair[1] for pair in checkPairList)
    
    def getCheckFollowSwingPosture(self):
        bodyCenter = self.getCenterPoint(self.leftShoulder, self.rightHip)
        wristCenter = self.getCenterPoint(self.leftWrist, self.rightWrist)
        hipCenter = self.getCenterPoint(self.leftHip, self.rightHip)
        checkPairList = [
            (bodyCenter.y, wristCenter.y),
            (wristCenter.x, hipCenter.x),
        ]
        return all(pair[0] > pair[1] for pair in checkPairList)
