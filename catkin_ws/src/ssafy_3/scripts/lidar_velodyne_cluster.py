#!/usr/bin/env python
#-*- coding:utf-8 -*-

import rospy
import cv2
import numpy as np
from math import cos,sin,pi,sqrt,pow,atan2

from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
from geometry_msgs.msg import PoseArray,Pose
from sklearn.cluster import DBSCAN

# lidar_velodyne_cluster 는 LiDAR의 Point들을 물체 단위로 구분하는 Clustering 예제입니다.
# PointCloud Data를 입력받아 DBSCAN Algorithm을 활용하여 Clustering을 수행합니다.
# 교육생분들은 DBSCAN의 Parameter를 조절하여 적절한 Clustering 결과를 얻어내야 합니다.

# 노드 실행 순서
# 1. DBSCAN Parameter 입력
# 2. 각 Cluster를 대표하는 위치 값 계산
# 3. PointCloud Data로부터 Distance, Angle 값 계산

class SCANCluster:
    def __init__(self):

        self.scan_sub = rospy.Subscriber("/velodyne_points", PointCloud2, self.callback)

        self.cluster_pub = rospy.Publisher("clusters", PoseArray, queue_size=10)

        self.pc_np = None

        #TODO: (1) DBSCAN Parameter 입력
        
        # DBSCAN의 Parameter를 결정하는 영역입니다.
        # sklearn.cluster의 DBSCAN에 대해 조사하여 적절한 Parameter를 입력하기 바랍니다.

        self.dbscan = DBSCAN(eps=1.5, min_samples=50)
        
    
    def callback(self, msg):    
        self.pc_np = self.pointcloud2_to_xyz(msg)
        
        
        if len(self.pc_np) == 0:
            cluster_msg = PoseArray()

        else:
            cluster_msg = PoseArray()
            
            pc_xy = self.pc_np[:, :2] # x, y 좌표만 가져옴
            db = self.dbscan.fit_predict(pc_xy)
            n_cluster = np.max(db) + 1
            cluster_list = []
            # print(n_cluster)
            
            for cluster in range(0, n_cluster):
                #TODO: (2) 각 Cluster를 대표하는 위치 값 계산
                
                # DBSCAN으로 Clustering 된 각 Cluster의 위치 값을 계산하는 영역입니다.
                # Cluster에 해당하는 Point들을 활용하여 Cluster를 대표할 수 있는 위치 값을 계산합니다.
                # 계산된 위치 값을 ROS geometry_msgs/Pose type으로 입력합니다.
                # Input : cluster
                # Output : cluster position x,y

                cluster_points = pc_xy[db == cluster]
                cluster_center = np.mean(cluster_points, axis=0)

                tmp_pose = Pose()
                tmp_pose.position.x = cluster_center[0]
                tmp_pose.position.y = cluster_center[1]

                dis = sqrt(cluster_center[0] ** 2 + cluster_center[1] ** 2)

                if dis > 0.5:
                    # print(cluster, cluster_center[0], cluster_center[1])
                    cluster_msg.poses.append(tmp_pose)
            

        self.cluster_pub.publish(cluster_msg)
        

    def pointcloud2_to_xyz(self, cloud_msg):

        point_list = []
        # print(len(cloud_msg.poses))
        '''
        for point in cloud_msg.poses:
            dist = sqrt(pow(point.position.x,2) + pow(point.position.y,2))
            if dist < 20:
                point_list.append((point.position.x, point.position.y, point.position.z))
        '''
        

        for point in pc2.read_points(cloud_msg, skip_nans=True):
            # print(point)
            
            #TODO: (3) PointCloud Data로부터 Distance, Angle 값 계산
            
            # LiDAR의 PointCloud Data로부터 Distance와 Angle 값을 계산하는 영역입니다.
            # 각 Point의 XYZ 값을 활용하여 Distance와 Yaw Angle을 계산합니다.
            # Input : point (X, Y, Z, Intensity)
            
            dist = np.sqrt(point[0] ** 2 + point[1] ** 2)
            angle = np.arctan2(point[1], point[0])
            
            
            if point[0] > 0 and 1.50 > point[2] > -1.25 and dist < 50:
                point_list.append((point[0], point[1], point[2], point[3], dist, angle))
            

        point_np = np.array(point_list, np.float32)
        # print(cloud_msg.poses[0].orientation.w)
        return point_np
        
        
if __name__ == '__main__':

    rospy.init_node('velodyne_clustering', anonymous=True)

    scan_cluster = SCANCluster()

    rospy.spin() 
