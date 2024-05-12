#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import rospkg
import sys
import os
import copy
import numpy as np
import json
from std_msgs.msg import String
from math import cos,sin,sqrt,pow,atan2,pi
from geometry_msgs.msg import Point32,PoseStamped, PoseWithCovarianceStamped,Point
from nav_msgs.msg import Odometry,Path
from tf.transformations import euler_from_quaternion,quaternion_from_euler

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)

from lib.mgeo.class_defs import *



class dijkstra_path_pub :
    def __init__(self):
        rospy.init_node('dijkstra_path_pub', anonymous=True)

        # (1) Mgeo data 읽어온 후 데이터 확인
        load_path = os.path.normpath(os.path.join(current_path, 'lib/mgeo_data/R_KR_PG_K-City'))
        mgeo_planner_map = MGeo.create_instance_from_json(load_path)

        node_set = mgeo_planner_map.node_set
        link_set = mgeo_planner_map.link_set

        self.nodes=node_set.nodes
        self.links=link_set.lines
        self.global_planner=Dijkstra(self.nodes,self.links)

        self.is_odom = False
        self.is_init_pose = False
        self.current_position = Point()
        self.dijkstra_recieved = False

        self.dijkstra_path_pub = rospy.Publisher('/dijkstra_path',Path, queue_size = 1)
        print("Published!!")

        rospy.Subscriber("/odom", Odometry, self.odom_callback)
        rospy.Subscriber("Dijkstra_Flag", String, self.dijkstra_flag_callback)
        
        self.start_node = ""
        self.end_node = "A119BS010184"
        self.is_goal_pose = True
        while True:
            if self.is_goal_pose == True and self.is_init_pose == True:
                break
            elif self.is_goal_pose==False:
                rospy.loginfo('Waiting goal pose data')
            
            else:
                rospy.loginfo('Waiting init pose data')



        self.global_path_msg = Path()
        self.global_path_msg.header.frame_id = '/map'

        self.global_path_msg = self.calc_dijkstra_path_node(self.start_node, self.end_node)
 
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            if not self.dijkstra_recieved:
                print("Published!")
                self.dijkstra_path_pub.publish(self.global_path_msg)
            else:
                rospy.loginfo("Dijkstra Recieved, Stop Publishing ...")
                break
    
    
    # Dijkstra 성공적으로 전달했다면 Dijkstra Node 종료
    def dijkstra_flag_callback(self, msg):
        self.dijkstra_recieved = True

    def odom_callback(self,msg):
        self.is_odom=True
        odom_quaternion=(msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,msg.pose.pose.orientation.z,msg.pose.pose.orientation.w)
        _,_,self.vehicle_yaw=euler_from_quaternion(odom_quaternion)
        self.current_position.x=msg.pose.pose.position.x
        self.current_position.y=msg.pose.pose.position.y
        min_dist = float('inf')

        # 현재 위치와 가장 가까운 노드를 시작 노드로 설정
        start_node_idx = None
        for node in self.nodes.values():
            dist = sqrt(pow(self.current_position.x - node.point[0],2) + pow(self.current_position.y-node.point[1],2))
            if dist < min_dist:
                min_dist = dist
                start_node_idx = node.idx
        self.start_node = start_node_idx
        print(start_node_idx)
        self.is_init_pose = True

    def calc_dijkstra_path_node(self, start_node, end_node):

        result, path = self.global_planner.find_shortest_path(start_node, end_node)

        #(10) dijkstra 경로 데이터를 ROS Path 메세지 형식에 맞춰 정의
        out_path = Path()
        out_path.header.frame_id = '/map'
        
        point = Point32()

        for point in path['point_path']:
            pose = PoseStamped()
            pose.header.frame_id = '/map'
            pose.pose.position.x = point[0]
            pose.pose.position.y = point[1]
            pose.pose.position.z = point[2]
            out_path.poses.append(pose)

        self.global_path_msg = out_path
        

        return out_path

class Dijkstra:
    def __init__(self, nodes, links):
        self.nodes = nodes
        self.links = links
        self.weight = self.get_weight_matrix()
        self.lane_change_link_idx = []

    def get_weight_matrix(self):
        # (3) weight 값 계산
        
        # weight 값 계산은 각 Node 에서 인접 한 다른 Node 까지의 비용을 계산합니다.
        # 계산된 weight 값 은 각 노드간 이동시 발생하는 비용(거리)을 가지고 있기 때문에
        # Dijkstra 탐색에서 중요하게 사용 됩니다.
        # weight 값은 딕셔너리 형태로 사용 합니다.
        # 이중 중첩된 딕셔너리 형태로 사용하며 
        # Key 값으로 Node의 Idx Value 값으로 다른 노드 까지의 비용을 가지도록 합니다.
        # 아래 코드 중 self.find_shortest_link_leading_to_node 를 완성하여 
        # Dijkstra 알고리즘 계산을 위한 Node와 Node 사이의 최단 거리를 계산합니다.

        
        # 초기 설정
        weight = dict() 
        for from_node_id, from_node in self.nodes.items():
            # 현재 노드에서 다른 노드로 진행하는 모든 weight
            weight_from_this_node = dict()
            for to_node_id, to_node in self.nodes.items():
                weight_from_this_node[to_node_id] = float('inf')
            # 전체 weight matrix에 추가
            weight[from_node_id] = weight_from_this_node

        for from_node_id, from_node in self.nodes.items():
            # 현재 노드에서 현재 노드로는 cost = 0
            weight[from_node_id][from_node_id] = 0

            for to_node in from_node.get_to_nodes():
                # 현재 노드에서 to_node로 연결되어 있는 링크를 찾고, 그 중에서 가장 빠른 링크를 찾아준다
                shortest_link, min_cost = self.find_shortest_link_leading_to_node(from_node,to_node)
                weight[from_node_id][to_node.idx] = min_cost           

        return weight

    def find_shortest_link_leading_to_node(self, from_node,to_node):
        """현재 노드에서 to_node로 연결되어 있는 링크를 찾고, 그 중에서 가장 빠른 링크를 찾아준다"""
        # (3) weight 값 계산
        
        # 최단거리 Link 인 shortest_link 변수와
        # shortest_link 의 min_cost 를 계산 합니다.
        # print("From Node : ")
        # print(from_node.idx)
        # print("To Node : ")
        # print(to_node.idx)
        # print("\n")
        shortest_link = None
        min_cost = float('inf')
        for link_id in from_node.to_links:
            link = link_id
            if link.to_node.idx == to_node.idx:
                if link.cost < min_cost:
                    shortest_link = link
                    min_cost = link.cost
        
        return shortest_link, min_cost
        
    def find_nearest_node_idx(self, distance, s):        
        idx_list = self.nodes.keys()
        min_value = float('inf')
        min_idx = idx_list[-1]

        for idx in idx_list:
            if distance[idx] < min_value and s[idx] == False :
                min_value = distance[idx]
                min_idx = idx
        return min_idx

    def find_shortest_path(self, start_node_idx, end_node_idx): 
        # (4) Dijkstra Path 초기화 로직
        # s 초기화         >> s = [False] * len(self.nodes)
        # from_node 초기화 >> from_node = [start_node_idx] * len(self.nodes)
        
        # Dijkstra 경로 탐색을 위한 초기화 로직 입니다.
        # 변수 s와 from_node 는 딕셔너리 형태로 크기를 MGeo의 Node 의 개수로 설정합니다. 
        # Dijkstra 알고리즘으로 탐색 한 Node 는 변수 s 에 True 로 탐색하지 않은 변수는 False 로 합니다.
        # from_node 의 Key 값은 Node 의 Idx로
        # from_node 의 Value 값은 Key 값의 Node Idx 에서 가장 비용이 작은(가장 가까운) Node Idx로 합니다.
        # from_node 통해 각 Node 에서 가장 가까운 Node 찾고
        # 이를 연결해 시작 노드부터 도착 노드 까지의 최단 경로를 탐색합니다. 

        
        s = dict()
        from_node = dict() 
        for node_id in self.nodes.keys():
            s[node_id] = False
            from_node[node_id] = start_node_idx

        s[start_node_idx] = True
        distance =copy.deepcopy(self.weight[start_node_idx])

        #: (5) Dijkstra 핵심 코드
        for i in range(len(self.nodes.keys()) - 1):
            selected_node_idx = self.find_nearest_node_idx(distance, s)
            s[selected_node_idx] = True            
            for j, to_node_idx in enumerate(self.nodes.keys()):
                if s[to_node_idx] == False:
                    distance_candidate = distance[selected_node_idx] + self.weight[selected_node_idx][to_node_idx]
                    if distance_candidate < distance[to_node_idx]:
                        distance[to_node_idx] = distance_candidate
                        from_node[to_node_idx] = selected_node_idx
        print(from_node)
        #: (6) node path 생성
        tracking_idx = end_node_idx
        node_path = [end_node_idx]
        while start_node_idx != tracking_idx:
            tracking_idx = from_node[tracking_idx]
            node_path.append(tracking_idx)     

        node_path.reverse()
        print(node_path)
        #: (7) link path 생성
        link_path = []
        # print(len(node_path))
        for i in range(len(node_path) - 1):
            from_node_idx = node_path[i]
            to_node_idx = node_path[i + 1]

            from_node = self.nodes[from_node_idx]
            to_node = self.nodes[to_node_idx]
            #print(from_node)
            #print(to_node)

            shortest_link, min_cost = self.find_shortest_link_leading_to_node(from_node,to_node)
            #만약에 경로가 없어서 shortest_link가 None이라면 에러!
            link_path.append(shortest_link.idx)

        #: (8) Result 판별
        if len(link_path) == 0:
            return False, {'node_path': node_path, 'link_path':link_path, 'point_path':[]}

        #: (9) point path 생성
        point_path = []        
        for link_id in link_path:
            link = self.links[link_id]
            for point in link.points:
                point_path.append([point[0], point[1], 0])

        return True, {'node_path': node_path, 'link_path':link_path, 'point_path':point_path}

if __name__ == '__main__':
    
    dijkstra_path_pub = dijkstra_path_pub()