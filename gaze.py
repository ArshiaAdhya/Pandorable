import cv2 as cv
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import mediapipe as mp
import math
import threading
import time
from tkinter import simpledialog
from nav import TicTacToe, TodoList, SnakeGame, open_game, start_meditation, update_timer, helloCallBack



class ConfigDialog:
    def __init__(self, parent):
        self.parent = parent
        self.dialog = simpledialog.Dialog(parent, title="Configure Overlay")
        self.btn_tic_tac_toe = tk.Button(self.dialog, text="Tic Tac Toe", command=self.open_tic_tac_toe)
        self.btn_tic_tac_toe.pack()
        self.btn_snake_game = tk.Button(self.dialog, text="Snake Game", command=self.open_snake_game)
        self.btn_snake_game.pack()
        self.btn_todo_list = tk.Button(self.dialog, text="To-Do List", command=self.open_todo_list)
        self.btn_todo_list.pack()
        self.btn_meditation_timer = tk.Button(self.dialog, text="Break Timer", command=self.open_meditation_timer)
        self.btn_meditation_timer.pack()
        self.btn_play_pause_music = tk.Button(self.dialog, text="Play/Pause Music", command=self.play_pause_music)
        self.btn_play_pause_music.pack()

    def body(self, master):
        tk.Label(master, text="Background Image:").grid(row=0)
        self.bg_entry = tk.Entry(master)
        self.bg_entry.grid(row=0, column=1)
        return self.bg_entry  

    def apply(self):
        bg_image = self.bg_entry.get()
        self.parent.change_background(bg_image)
        
    

class OverlayApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('100x125')
        self.root.wm_attributes("-transparentcolor", "black")
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.offset_x, self.offset_y = None, None
        self.root.bind("<Button-1>", self.on_mouse_click)
        self.root.bind("<B1-Motion>", self.on_mouse_drag)
        self.root.bind("<ButtonRelease-1>", self.on_mouse_rel)
        self.change_allowed=True
        self.image_list = ['panda.jpg', 'pandanorm.jpg', 'pandasleep.jpg', 'pandathirst.jpg']
        self.current_image_index = 0
        self.iteration_delay = 5
        self.iteration_thread = None
        self.start_background_iteration()
        root.bind('<p>', self.on_key_press)

        # Set initial background image
        self.image = Image.open("pandanorm.jpg")
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.background_label = tk.Label(root, image=self.photo_image, bg="black")
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
    def start_background_iteration(self):
        if self.iteration_thread is None or not self.iteration_thread.is_alive():
            self.iteration_thread = threading.Thread(target=self.iterate_background)
            self.iteration_thread.daemon = True
            self.iteration_thread.start()

    
    def iterate_background(self):
        while True:
            time.sleep(self.iteration_delay)
            self.current_image_index = (self.current_image_index + 1) % len(self.image_list)
            if self.current_image_index == 0:
                break
            self.change_background(self.image_list[self.current_image_index])
    
    def on_key_press(self, event):
        if self.iteration_thread is not None and self.iteration_thread.is_alive():
            return
        self.start_background_iteration()

    def change_background(self, image_filename):
        new_image = Image.open(image_filename)
        new_photo_image = ImageTk.PhotoImage(new_image)
        self.background_label.config(image=new_photo_image)
        self.background_label.image = new_photo_image

    def on_mouse_click(self, event):
        self.offset_x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        self.offset_y = self.root.winfo_pointery() - self.root.winfo_rooty()

    def on_mouse_drag(self, event):
        if None not in (self.offset_x, self.offset_y):
            new_window_x = self.root.winfo_pointerx() - self.offset_x
            new_window_y = self.root.winfo_pointery() - self.offset_y
            self.root.geometry("+%d+%d" % (new_window_x, new_window_y))
    def configure_overlay(self):
        config_dialog = ConfigDialog(self.root)
        self.root.wait_window(config_dialog.dialog)
        
    def on_mouse_rel(self, event):
        self.offset_x, self.offset_y = None, None
        
    def start_timer(self, duration, image):
    # Start a new thread for the timer
        timer_thread = threading.Thread(target=self.timer, args=(duration, image))
        timer_thread.start()

    def timer(self, duration, image):
    # Wait for the specified duration
        time.sleep(duration)
    # After the duration, change the background image
        self.change_background(image)
        
    def flagchanger(self, flag):
        if (flag==True):
            flag = False
        else:
            flag = True
        
        
        

        


mp_face_mesh = mp.solutions.face_mesh

LEFT_EYE =[ 362, 382,381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398]  
RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ]  
RIGHT_IRIS = [474,475, 476, 477] 
LEFT_IRIS = [469, 470, 471, 472]
L_H_LEFT = [33]
L_H_RIGHT = [133]
R_H_LEFT = [362]
R_H_RIGHT = [263]
FOREHEAD_POINT = [101]
NOSE_TIP = [101]
CHIN = [152]

root = tk.Tk()
app = OverlayApp(root)

def euclidean_distance(point1, point2):
    x1, y1 = point1.ravel()
    x2, y2 = point2.ravel()
    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)  
    return distance

def iris_position(iris_center, right_point, left_point, scx, scy):
    center_to_right_dist = euclidean_distance(iris_center, right_point)
    total_distance = euclidean_distance(right_point, left_point)
    screen_center = np.array([scx, scy])
    center_to_screen_dist = euclidean_distance(iris_center, screen_center)
    ratio = center_to_right_dist/total_distance
    iris_position = ""
    if ratio <= 0.42:
        iris_position = "right"
    elif ratio > 0.42 and ratio <= 0.57:
        iris_position = "center"
    else:
        iris_position = "left"
    return iris_position, ratio, center_to_screen_dist



cap = cv.VideoCapture(0)

text_list = {}  # Empty list to store gaze direction text for each face
iris_pos_list = {}  # Empty list to store iris position for each face
change_counter = 0

def cv_processing():
    with mp_face_mesh.FaceMesh(
        max_num_faces=5,
        refine_landmarks=True,
        min_detection_confidence = 0.7,
        min_tracking_confidence=0.8
    ) as face_mesh: 
        
        face_data = {}
        

        while True:
            
            ret, frame = cap.read()
            if not ret:
                continue
            frame = cv.flip(frame,1)
            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            img_h, img_w, img_c = frame.shape
            face_2d_list = []
            face_3d_list = []
            
            
            screen_center_x = int(img_w / 2)
            screen_center_y = int(img_h / 2)
            results = face_mesh.process(rgb_frame)
            if results.multi_face_landmarks is not None:
                num_faces = len(results.multi_face_landmarks)
            if num_faces == 1:
                single_face_id = str(0)
                if single_face_id in iris_pos_list and single_face_id in text_list:
                    if iris_pos_list[single_face_id] == 'center' and text_list[single_face_id] == 'Forward':
                        app.start_background_iteration()
            if results.multi_face_landmarks:
                for face_id in range(len(results.multi_face_landmarks)):
                    faceLms = results.multi_face_landmarks[face_id]
                    face_2d = []
                    face_3d = []
                    for idx, lm in enumerate(faceLms.landmark):
                        if idx == 33 or idx == 263 or idx ==1 or idx == 61 or idx == 291 or idx==199:
                            if idx == 1:
                                nose_2d = (lm.x * img_w,lm.y * img_h)
                                nose_3d = (lm.x * img_w,lm.y * img_h,lm.z * 3000)
                            x,y = int(lm.x * img_w),int(lm.y * img_h)

                            face_2d.append([x,y])
                            face_3d.append(([x,y,lm.z]))
                            
                    face_2d_list.append(face_2d)
                    face_3d_list.append(face_3d)
                            
                    #Get 2d Coord
                    face_2d = np.array(face_2d,dtype=np.float64)

                    face_3d = np.array(face_3d,dtype=np.float64)

                    focal_length = 1 * img_w

                    cam_matrix = np.array([[focal_length,0,img_h/2],
                                        [0,focal_length,img_w/2],
                                        [0,0,1]])
                    distortion_matrix = np.zeros((4,1),dtype=np.float64)

                    success,rotation_vec,translation_vec = cv.solvePnP(face_3d,face_2d,cam_matrix,distortion_matrix)


                    #getting rotational of face
                    rmat,jac = cv.Rodrigues(rotation_vec)

                    angles,mtxR,mtxQ,Qx,Qy,Qz = cv.RQDecomp3x3(rmat)

                    x = angles[0] * 360
                    y = angles[1] * 360
                    z = angles[2] * 360

                    #here based on axis rot angle is calculated
                    if y < -5:
                        text="Looking Left"
                    elif y > 5:
                        text="Looking Right"
                    elif x < -20:
                        text="Looking Down"
                    elif x > 20:
                        text="Looking Up"
                    else:
                        text="Forward"

                    nose_3d_projection,jacobian = cv.projectPoints(nose_3d,rotation_vec,translation_vec,cam_matrix,distortion_matrix)

                    p1 = (int(nose_2d[0]),int(nose_2d[1]))
                    p2 = (int(nose_2d[0] + y*10), int(nose_2d[1] -x *10))

                    cv.line(frame,p1,p2,(255,0,0),3)
                    # cv.putText(frame,"x: " + str(np.round(x,2)),(500,50),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                    # cv.putText(frame,"y: "+ str(np.round(y,2)),(500,100),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                    # cv.putText(frame,"z: "+ str(np.round(z, 2)), (500, 150), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                    # print(results.multi_face_landmarks[0].landmark)
                    mesh_points = np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in faceLms.landmark])
                    # print(mesh_points.shape)
                    # cv.polylines(frame, [mesh_points[LEFT_IRIS]], True, (0,0,255), 1, cv.LINE_AA)
                    # cv.polylines(frame, [mesh_points[RIGHT_IRIS]], True, (0,0,255), 1, cv.LINE_AA)
                    (l_cx, l_cy), l_radius = cv.minEnclosingCircle(mesh_points[LEFT_IRIS])
                    (r_cx, r_cy), r_radius = cv.minEnclosingCircle(mesh_points[RIGHT_IRIS])
                    center_left = np.array([l_cx, l_cy], dtype = np.int32)
                    center_right = np.array([r_cx, r_cy], dtype = np.int32)
                    cv.circle(frame, center_left, int(l_radius), (0,0,255), 1, cv.LINE_AA)
                    cv.circle(frame, center_right, int(r_radius), (0,0,255), 1, cv.LINE_AA)
                    iris_pos, ratio, csdist = iris_position(
                        center_right, 
                        mesh_points[R_H_RIGHT], 
                        mesh_points[R_H_LEFT],
                        screen_center_x,
                        screen_center_y
                    )
                    
                    text_list[str(face_id)] = text
                    iris_pos_list[str(face_id)] = iris_pos
                    
                    if(len(results.multi_face_landmarks)>1):
                        for i in range (1, len(results.multi_face_landmarks)):
                            if str(i) in iris_pos_list and str(i) in text_list:
                                if (((iris_pos_list[str(i)] == 'center' and text_list[str(i)] == 'Forward') or (iris_pos_list[str(i)] == 'right' and text_list[str(i)] == 'Looking Left') or (iris_pos_list[str(i)] == 'left' and text_list[str(i)] == 'Looking Right'))):
                                    app.change_background("pandaspook.jpg")
                                else:
                                    app.change_background("pandanorm.jpg")
                                # print(iris_pos_list[str(i)])
                                # cv.putText(frame,text_list[str(i)],(20,50),cv.FONT_HERSHEY_SIMPLEX,2,(0,255,0),2)
                                # cv.putText(
                                #     frame, 
                                #     f"Iris pos: {iris_pos} {ratio:.2f}", 
                                #     (30,30), 
                                #     cv.FONT_HERSHEY_DUPLEX, 
                                #     1.2, 
                                #     (255,255,0), 
                                #     1, 
                                #     cv.LINE_AA
                                # )
                                # change_counter = 0
                            # change_counter+=1
                            # print(change_counter)
                                # time.sleep(10)
                    
                    
            cv.imshow("frame", frame)
            key = cv.waitKey(1)
            if key == ord('q'):
                break

    cap.release()
    cv.destroyAllWindows()

def start_tkinter():
    
    root.mainloop()


threading.Thread(target=cv_processing).start()
start_tkinter()