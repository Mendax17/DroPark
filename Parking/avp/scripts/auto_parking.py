#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import threading
import time
import os
import math
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')  # 또는 'Qt4Agg'
import matplotlib.pyplot as plt
from morai_msgs.msg import CtrlCmd, EgoVehicleStatus, EventInfo
from morai_msgs.srv import MoraiEventCmdSrv
from geometry_msgs.msg import Vector3
from nav_msgs.msg import Odometry
from enum import Enum

class Gear(Enum):
    P = 1
    R = 2
    N = 3
    D = 4

class a_parking():
    
    def __init__(self):
        rospy.init_node('auto_parking', anonymous=True)
        
        self.cmd_pub = rospy.Publisher('/ctrl_cmd', CtrlCmd, queue_size=1)
        
        rospy.Subscriber('/Ego_topic', EgoVehicleStatus, self.ego_callback)

        rospy.wait_for_service('/Service_MoraiEventCmd')
        self.event_cmd_srv = rospy.ServiceProxy('Service_MoraiEventCmd', MoraiEventCmdSrv)
        
        # 초기화
        self.is_loc=False
        self.is_plot=True
        
        def calculate_angle(coord1, coord2):
            delta_x = coord2.x - coord1.x
            delta_y = coord2.y - coord1.y
            slope = delta_y / delta_x if delta_x != 0 else float('inf')  # 기울기 계산 (0으로 나누는 경우를 처리)
            angle_rad = math.atan(slope)  # 아크탄젠트를 이용하여 각도 계산
            angle_deg = math.degrees(angle_rad)  # 라디안에서 도로 변환
            if(angle_deg > 0):
                return angle_deg
            else:
                return 180 + angle_deg
            
        def calculate_line_equation(coord1, slope):
            # Calculate the y-intercept
            y_intercept = coord1.y - slope * coord1.x
            
            return y_intercept
                    
        def update_plot():
            while self.is_plot:
                plt.clf()  # 이전 그래프를 지우고 새로운 그래프를 그리기 위해 clear
                # Extract x and y coordinates
                x_values = [target_position.x, target_1.x, target_2.x, self.ego_status.position.x]
                y_values = [target_position.y, target_1.y, target_2.y, self.ego_status.position.y]

                # Plot the points
                plt.scatter(x_values, y_values, color=['r', 'g', 'g', 'b'])
                
                # Calculate the slope of the line passing through now_position and with angle cal_target_angle
                slope = math.tan(math.radians(cal_target_angle))

                # Calculate the y-intercept
                y_intercept = calculate_line_equation(now_position, slope)

                # Generate x values for the line
                x_line = np.linspace(min(x_values), max(x_values), 100)

                # Calculate corresponding y values for the line
                y_line = slope * x_line + y_intercept

                # Plot the line
                plt.plot(x_line, y_line, color='r', linestyle='--')

                # Calculate the slope of the line passing through now_position and with angle now_angle
                slope_now = math.tan(math.radians(now_angle))

                # Calculate the y-intercept for the line passing through now_position with angle now_angle
                y_intercept_now = calculate_line_equation(now_position, slope_now)

                # Calculate corresponding y values for the line passing through now_position with angle now_angle
                y_line_now = slope_now * x_line + y_intercept_now

                # Plot the line passing through now_position with angle now_angle
                plt.plot(x_line, y_line_now, color='b', linestyle='--')

                # Set labels and title
                plt.xlabel('X')
                plt.ylabel('Y')
                plt.title('Vector3 Points Visualization')

                # Add legend
                plt.legend()

                # Show plot
                plt.pause(0.01)  # 업데이트된 그래프가 표시되는 시간 (초 단위)

                time.sleep(0.01)  # 갱신 주기 설정
            # 코드 실행이 끝나면 Matplotlib 창을 닫음
            plt.close()
        
        self.ego_status = EgoVehicleStatus()
        wheelbase = 2.544462773659777
        # wheelbase = 2.414462773659777
        
        target_position = Vector3(0, 0, 0) # 주차선 앞 기준
        target_line_dot1 = Vector3(2.18, 1020.99, 0) # 후진 도착 위치1
        target_line_dot2 = Vector3(4.43279695511, 1019.83178711, -0.875219464302) # 후진 도착 위치2
        target_angle = 59.79750583426879 #61.4259338379
        target_1 = Vector3(3.27, 1025.04, -1.15)
        target_2 = Vector3(5.18, 1023.99, -1.15)
        target_3 = Vector3(2.69, 1019.72, -1.22) # 사용 안함
        target_4 = Vector3(0.79, 1020.78, -1.14) # 사용 안함
        target_position.x = (target_1.x + target_2.x)/2
        target_position.y = (target_1.y + target_2.y)/2
        
        #self.target_position = Vector3(-4.85, 1050.03, 0)
        #target_1 = Vector3(-1.00, 1049.20, -0.80)
        #target_2 = Vector3(-2.11, 1047.22, -0.82)
        #target_3 = Vector3(-6.27, 1049.52, -0.77)
        #target_4 = Vector3(-5.14, 1051.50, -0.74)
    
        start_position = Vector3(0, 0, 0)
        start_angle = None
        std1, std2 = None, None
        steering_value = None
        circle_angle = None
        point_angle = None
        distance = None
        line_a = (target_line_dot2.y - target_line_dot1.y)/(target_line_dot2.x - target_line_dot1.x)
        line_b = -1
        line_c = target_line_dot1.x*(target_line_dot1.y - target_line_dot2.y)/(target_line_dot2.x - target_line_dot1.x) + target_line_dot1.y
        
        # 메시지 발행 속도 설정
        self.rate = rospy.Rate(10)
        
        start_time = time.time()
        while (time.time() - start_time) < 1:
            print("test")
            
        #############################
        now_angle = self.ego_status.heading # 최초 : 151.518554688 # 가변 # 0
        now_position = self.ego_status.position # (2.13018512726, 1044.87438965) # 가변
        point_angle = calculate_angle(now_position, target_position) # 사이각 반환 # 95.8350343266
        theta_angle = 2*abs(target_angle - point_angle) # 2*|-36.0356924511|
        if(target_angle - point_angle < 0): # 왼쪽일때
            cal_target_angle = target_angle + theta_angle # 131.96425082 # 목표 각도
        else: # 오른쪽일때
            cal_target_angle = target_angle - theta_angle
        std1 = cal_target_angle - now_angle # -19.5480172464

        if(std1 >= 0):
            steering_value = -1
        else:
            steering_value = 1
            
        ###############################
        # 대화형 모드로 설정하여 그래프가 동적으로 업데이트될 수 있도록 함
        plt.ion()

        # 스레드 생성 및 실행
        update_thread = threading.Thread(target=update_plot)
        update_thread.start()

        # 그래프가 닫힐 때까지 대기
        plt.ioff()
        plt.show()
        ###############################
        
        self.send_gear_cmd(Gear.R.value)
        
        while(abs(std1) > 0.3): # Default : 2
            os.system('clear')
            now_angle = self.ego_status.heading
            now_position = self.ego_status.position # 계속 바뀌는 위치
            point_angle = calculate_angle(now_position, target_position) # 사이각 반환
            theta_angle = 2*abs(target_angle - point_angle)
            if(target_angle - point_angle < 0): # 왼쪽일때
                print("left")
                cal_target_angle = target_angle + theta_angle # 131.96425082 # 목표 각도
            else: # 오른쪽일때
                print("right")
                cal_target_angle = target_angle - theta_angle
            std1 = cal_target_angle - now_angle
            
            print(abs(std1))
            if(abs(self.ego_status.velocity.x*3.6) > 1.0): # Default : 1.5
                self.send_ctrl_cmd2(0.05, steering_value)
            else:
                self.send_ctrl_cmd(steering_value, 1) # Default : 1
            self.rate.sleep()
            
        self.send_ctrl_cmd(0, 10)
        self.rate.sleep()
        
        self.send_gear_cmd(Gear.P.value)
        
        self.is_plot=False
        
        #############################

        start_angle = self.ego_status.heading
        start_position = self.ego_status.position
        
        distance = math.sqrt((start_position.x - target_position.x)**2 + (start_position.y - target_position.y)**2)
        
        std1 = target_angle - start_angle
        std2 = 360 - abs(target_angle - start_angle)
        if(std1 >= 0):
            std2*=(-1)
            
        if(abs(std1) < abs(std2)):
            if(std1 >= 0):
                steering_value = -1
            else:
                steering_value = 1
            circle_angle = math.radians(abs(std1)/2)
        else:
            if(std2 >= 0):
                steering_value = -1
            else:
                steering_value = 1
            circle_angle = math.radians(abs(std2)/2)
            
        steering_value *= math.pi*36.25/180
        steering_value *= math.degrees(math.asin(2*wheelbase*math.sin(circle_angle)/distance))/36.25

        self.send_gear_cmd(Gear.R.value)
        
        for _ in range(5):
            self.send_ctrl_cmd(steering_value, 1)
            self.rate.sleep()
        
        while(abs(self.ego_status.heading - target_angle) > 5): # Default : 2
            os.system('clear')
            print("steering_value : ", steering_value)
            print(abs(self.ego_status.heading - target_angle))
            
            if(abs(self.ego_status.velocity.x*3.6) > 7): # Default : 1.5
                self.send_ctrl_cmd2(0.05, steering_value)
            else:
                self.send_ctrl_cmd(steering_value, 20) # Default : 1
            self.rate.sleep()
        
        while(1):
            dis = abs(self.ego_status.position.x*line_a + self.ego_status.position.y*line_b + line_c)/math.sqrt(line_a**2 + line_b**2)
            os.system('clear')
            print(dis)
            if(dis < 0.7): # Default : 0.2
                break
            
            self.send_ctrl_cmd(0, 10)
            self.rate.sleep()
        
        self.send_gear_cmd(Gear.P.value)

    def ego_callback(self, data):
        self.ego_status = data
        self.is_loc=True

    def send_gear_cmd(self, gear_mode):
        while(abs(self.ego_status.velocity.x) > 0.1):
            self.send_ctrl_cmd(0, 0)
            self.rate.sleep()
        
        gear_cmd = EventInfo()
        gear_cmd.option = 3
        gear_cmd.ctrl_mode = 3
        gear_cmd.gear = gear_mode
        gear_cmd_resp = self.event_cmd_srv(gear_cmd)
        rospy.loginfo(gear_cmd)

    def send_ctrl_cmd(self, steering, velocity):
        cmd = CtrlCmd()
        if(velocity > 0):
            cmd.longlCmdType = 2
            cmd.velocity = velocity
            cmd.steering = steering
        else:
            cmd.longlCmdType = 1
            cmd.brake = 1
            cmd.steering = 0
        self.cmd_pub.publish(cmd)
    
    def send_ctrl_cmd2(self, brake, steering):
        cmd = CtrlCmd()
        cmd.longlCmdType = 1
        cmd.brake = brake
        cmd.steering = steering
        self.cmd_pub.publish(cmd)

if __name__ == '__main__':
    try:
        a_d = a_parking()
    except rospy.ROSInterruptException:
        pass