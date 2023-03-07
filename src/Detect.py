import cv2
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
import imutils
import scipy.optimize as optimization
import chess
import chess.svg
from slider_test import *
from scipy import ndimage



class ChessRecognizer():
    def __init__(self,get_img_str):
        # Function of i to get i'th frame of game
        self.get_img_str = get_img_str 

        # Calibrate with zeroth image
        self.img_num = 0
        self.cal_img = self.crop_resize_img(cv2.imread(get_img_str(self.img_num)))  
        
        self.y_h_min,self.y_h_max,self.y_s_min,self.y_s_max,self.y_v_min,self.y_v_max = 25,60,60,255,60,255
        self.b_h_min,self.b_h_max,self.b_s_min,self.b_s_max,self.b_v_min,self.b_v_max = 100,150,60,255,50,200

        # Save a history of coordinates of all pieces every frame
        self.y_piece_coord_hist = []
        self.b_piece_coord_hist = []

        self.turn = 'white'     

        # From Python chess library to validate moves and display the board
        self.board = chess.Board()

    def play(self):
        """
        Loop through the frames of the game and call parse on each one. 
        Prompt a recalibration if there is an error.
        """
        while True:
            img = cv2.imread(self.get_img_str(self.img_num))
            img = self.crop_resize_img(img)
            draw_img = img.copy()
            hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            y_centers,b_centers= self.get_piece_centers(img,hsv_img,draw_img)

            # Calculate the coordinates of all visible pieces
            y_piece_coords = set()
            b_piece_coords = set()
            for pt in y_centers:
                y_piece_coords.add(tuple(self.pixel_to_chess_coords(pt).astype(int)))
            for pt in b_centers:
                b_piece_coords.add(tuple(self.pixel_to_chess_coords(pt).astype(int)))

            move = self.parse_move(y_piece_coords,b_piece_coords)

            if move == 'error':
                backup = input('backup amount? >> ')
                self.img_num-=int(backup)
                img = cv2.imread(self.get_img_str(self.img_num))
                img = self.crop_resize_img(img)
                self.calibrate_colors(img)
                self.img_num-=1
            else:
                cv2.imshow("Game", ndimage.rotate(draw_img, 90))

                # Display each frame for 0.8 seconds
                k = cv2.waitKey(800) & 0xFF

                # The user may hit esc to recalibrate if something looks wrong
                if k == 27:
                    print('Undo')
                    self.y_piece_coord_hist.pop()
                    self.b_piece_coord_hist.pop()
                    self.calibrate_colors(img)
                    self.img_num-=1
                    if move == 'move':
                        self.board.pop()
            self.img_num+=1

    def nothing(self,_):
        pass

    def pick_color(self,img,name,h_min,h_max,s_min,s_max,v_min,v_max):
        """Calibrate colors for detecting each piece."""
        cv2.namedWindow(name)

        # Create a trackbar for each parameter
        cv2.createTrackbar('h_min',name,h_min,255,self.nothing)
        cv2.createTrackbar('h_max',name,h_max,255,self.nothing)
        cv2.createTrackbar('s_min',name,s_min,255,self.nothing)
        cv2.createTrackbar('s_max',name,s_max,255,self.nothing)
        cv2.createTrackbar('v_min',name,v_min,255,self.nothing)
        cv2.createTrackbar('v_max',name,v_max,255,self.nothing)

        img2 = img.copy()

        while(True):
            cv2.imshow(name,img2)
            k = cv2.waitKey(1) & 0xFF

            # Break on spacebar
            if k==32:
                break

            # Get current positions of four trackbars
            h_min = cv2.getTrackbarPos('h_min',name)
            h_max = cv2.getTrackbarPos('h_max',name)
            s_min = cv2.getTrackbarPos('s_min',name)
            s_max = cv2.getTrackbarPos('s_max',name)
            v_min = cv2.getTrackbarPos('v_min',name)
            v_max = cv2.getTrackbarPos('v_max',name)

            # Mask so only the parts of the image in this range are shown.
            hsv_img = cv.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = get_piece_mask(hsv_img,(h_min,s_min,v_min), (h_max,s_max,v_max))
            img2 = cv.bitwise_and(img,img,mask=mask)

        cv2.destroyAllWindows()
        return h_min,h_max,s_min,s_max,v_min,v_max
        

    def calibrate_colors(self,img):
        """Set the bounds for the color of both types of pieces"""
        self.y_h_min,self.y_h_max,self.y_s_min,self.y_s_max,self.y_v_min,self.y_v_max = self.pick_color(img,"Pick black Piece Color",self.y_h_min,self.y_h_max,self.y_s_min,self.y_s_max,self.y_v_min,self.y_v_max)
        self.b_h_min,self.b_h_max,self.b_s_min,self.b_s_max,self.b_v_min,self.b_v_max = self.pick_color(img,"Pick white Piece Color",self.b_h_min,self.b_h_max,self.b_s_min,self.b_s_max,self.b_v_min,self.b_v_max)

    def calibrate_grid(self):
        """
        Use the centers of each piece to create a grid for the board and 
        a coordinate transform from pixel to board coordinates
        """
        hsv_img = cv2.cvtColor(self.cal_img, cv2.COLOR_BGR2HSV)
        draw_img = self.cal_img.copy()

        # Find the average position of both sets of pieces. These positions should be in 
        y_centers, b_centers = self.get_piece_centers(self.cal_img, hsv_img,draw_img)
        avg_y = np.average(y_centers,axis=0)
        cv2.circle(draw_img, (int(avg_y[0]), int(avg_y[1])), 7, (0,0,0), -1)
        avg_b = np.average(b_centers,axis=0)
        cv2.circle(draw_img, (int(avg_b[0]), int(avg_b[1])), 7, (0,0,0), -1)

        self.center = (avg_y + avg_b) / 2
        cv2.circle(draw_img, (int(self.center[0]), int(self.center[1])), 7, (0,0,0), -1)

        across_vec = avg_y - avg_b
        self.u = across_vec/6.3
        p = np.polyfit(y_centers[:,1], y_centers[:,0],1)
        h = self.cal_img.shape[0]
        cv2.line(draw_img,(int(np.polyval(p,0)),0),(int(np.polyval(p,h)),h),1)
        p1 = np.polyfit(b_centers[:,1], b_centers[:,0],1)
        cv2.line(draw_img,(int(np.polyval(p1,0)),0),(int(np.polyval(p1,h)),h),1)
        v = [(p[0]+p1[0])/2,1]
        self.v = v/np.linalg.norm(v) * np.linalg.norm(self.u)

        # Draw points on what should be the tile corners        
        for i in range(9):
            for j in range(9):
                x = self.board_to_pixel_coord(np.array([i-4,j-4]))
                cv2.circle(draw_img, (int(x[0]), int(x[1])), 7, (0,0,0), -1)

        # Create a set of coordinates for each piece type for where all of those
        # pieces are on the board
        y_piece_coords = set()
        b_piece_coords = set()
        for pt in y_centers:  
            y_piece_coords.add(tuple(self.pixel_to_chess_coords(pt).astype(int)))
        for pt in b_centers:
            b_piece_coords.add(tuple(self.pixel_to_chess_coords(pt).astype(int)))
        self.y_piece_coord_hist.append( y_piece_coords )
        self.b_piece_coord_hist.append( b_piece_coords )


        cv2.imshow("Calibration", ndimage.rotate(draw_img, 90))
        k = cv2.waitKey(0) & 0xFF
        cv2.destroyAllWindows()
        if len(y_piece_coords) != 16 or len(b_piece_coords) != 16 or k == 27:
            print("Invalid Calibration")
            self.calibrate_colors(self.cal_img)
            self.calibrate_grid()

    def crop_resize_img(self,img):
        """ Crop and resize image to adjust the chessboard based on camera setup. """
        img = img[int(img.shape[0]/70):img.shape[0]-int(img.shape[0]/40),int(img.shape[1]/5):img.shape[1]-int(img.shape[1]/5)]
        scale_percent = 20 
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        img = cv2.resize(img,dim)
        return img

    def get_piece_contours(self,img,lower_bound_color,upper_bound_color):
        """ Find the contours of the colered parts of the pieces. """

        mask = cv2.inRange(img, lower_bound_color, upper_bound_color)


        kernel1 = np.array([[0,1,0,0,0],
                           [0,1,0,0,0],
                           [0,0,1,0,0],
                           [0,0,0,1,1],
                           [0,0,0,0,0]]).astype('uint8')
        mask1 = cv2.erode(mask,kernel1,iterations = 1)

        kernel2 = np.array([[0,0,0,0,0],
                           [1,1,0,0,0],
                           [0,0,1,0,0],
                           [0,0,0,1,0],
                           [0,0,0,1,0]]).astype('uint8')
        mask2 = cv2.erode(mask,kernel2,iterations = 1)

        kernel3 = np.array([[0,0,0,0,0],
                           [0,0,0,1,1],
                           [0,0,1,0,0],
                           [0,1,0,0,0],
                           [0,1,0,0,0]]).astype('uint8')
        mask3 = cv2.erode(mask,kernel3,iterations = 1)

        kernel4 = np.array([[0,0,0,1,0],
                            [0,0,0,1,0],
                            [0,0,1,0,0],
                            [1,1,0,0,0],
                            [0,0,0,0,0]]).astype('uint8')
        mask4 = cv2.erode(mask,kernel4,iterations = 1)

        kernel5 = np.array([[0,0,0,0,0],
                           [1,0,0,0,1],
                           [0,1,1,1,0],
                           [0,0,0,0,0],
                           [0,0,0,0,0]]).astype('uint8')
        mask5 = cv2.erode(mask,kernel5,iterations = 1)

        kernel6 = np.array([[0,0,0,0,0],
                           [0,0,0,0,0],
                           [0,1,1,1,0],
                           [1,0,0,0,1],
                           [0,0,0,0,0]]).astype('uint8')
        mask6 = cv2.erode(mask,kernel6,iterations = 1)

        kernel7 = np.array([[0,0,0,1,0],
                           [0,0,1,0,0],
                           [0,0,1,0,0],
                           [0,0,1,0,0],
                           [0,0,0,1,0]]).astype('uint8')
        mask7 = cv2.erode(mask,kernel7,iterations = 1)

        kernel8 = np.array([[0,1,0,0,0],
                            [0,0,1,0,0],
                            [0,0,1,0,0],
                            [0,0,1,0,0],
                            [0,1,0,0,0]]).astype('uint8')
        mask8 = cv2.erode(mask,kernel8,iterations = 1)
        
        # Being on an arc in any direction is fine
        mask10 = cv2.bitwise_or(cv2.bitwise_or(cv2.bitwise_or(cv2.bitwise_or(cv2.bitwise_or(cv2.bitwise_or(cv2.bitwise_or(mask1,mask2),mask3),mask4),mask5),mask6),mask7),mask8)

        # Erode the result again as a second iteration to get rid of more noise
        mask11 = cv2.erode(mask10,kernel1,iterations = 1)
        mask12 = cv2.erode(mask10,kernel2,iterations = 1)
        mask13 = cv2.erode(mask10,kernel3,iterations = 1)
        mask14 = cv2.erode(mask10,kernel4,iterations = 1)
        mask15 = cv2.erode(mask10,kernel5,iterations = 1)
        mask16 = cv2.erode(mask10,kernel6,iterations = 1)
        mask17 = cv2.erode(mask10,kernel7,iterations = 1)
        mask18 = cv2.erode(mask10,kernel8,iterations = 1)

        mask20 = cv2.bitwise_or(cv2.bitwise_or(cv2.bitwise_or(cv2.bitwise_or(cv2.bitwise_or(cv2.bitwise_or(cv2.bitwise_or(mask11,mask12),mask13),mask14),mask15),mask16),mask17),mask18)

        # Dilate to try to join any detected clumps on a piece into a single region for each piece
        kernel = np.ones((5,5),np.uint8)
        mask21 =  cv2.dilate(mask20, kernel, iterations = 3)


        # Find the contours from the mask
        contours = cv2.findContours(mask21, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        cnts = contours
        return cnts


    def draw_piece_centers(self,img,contours,color):
        """ Draw the center of each contour to the image. """
        centers = []
        for c in contours:
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(img, (cX, cY), 7, color, -1)
            centers.append([cX,cY])
        return np.array(centers)

    def get_piece_centers(self,img,hsv_img,draw_img):
        """ Get pixel coordinates of each piece center. """
        y_cnts = self.get_piece_contours(hsv_img,(self.y_h_min,self.y_s_min,self.y_v_min), (self.y_h_max,self.y_s_max,self.y_v_max))
        b_cnts = self.get_piece_contours(hsv_img,(self.b_h_min,self.b_s_min,self.b_v_min), (self.b_h_max,self.b_s_max,self.b_v_max))
        y_centers = self.draw_piece_centers(draw_img,y_cnts,(81,224, 221))
        b_centers = self.draw_piece_centers(draw_img,b_cnts,(161, 91, 54))
        return y_centers,b_centers
    
    def f(self,x,a,b):
        return a*x + b


    def board_to_pixel_coord(self,x):
        """ Use a transformation matrix to go from board to pixel coordinates. """
        A = np.array([[self.u[0],self.v[0]],
                    [self.u[1],self.v[1]]])
        return np.dot(A,x) + self.center

    def pixel_to_board_coord(self,x):
        """ Use the inverse transformation matrix to go from pixel to board coordinates. """
        A = np.array([[self.u[0],self.v[0]],
                    [self.u[1],self.v[1]]])
        B = np.linalg.inv(A)
        return np.dot(B,x-self.center)

    def board_to_corner_coords(self,x):
        """ Move origin from center of board to corner of board. """
        return x + np.array([4,4])

    def pixel_to_chess_coords(self,x):
        """ Move from pixel to chess coordinates row 1-8, column 1-8"""
        return np.ceil(self.board_to_corner_coords(self.pixel_to_board_coord(x)))

    def chess_to_proper_coords(self,x):
        """ Change coordinates to chess row file format. """
        x_to_row = ['1','2','3','4','5','6','7','8']
        y_to_file = ['a','b','c','d','e','f','g','h']
        return y_to_file[x[1]-1] + x_to_row[x[0]-1] 

    def parse_move(self,y_piece_coords,b_piece_coords):
        """ 
        Compare the latest board to the previous board state and determine 
        the move or error that occured
        """

        y_pieces_lost = self.y_piece_coord_hist[-1]-y_piece_coords

        y_extra_pieces = y_piece_coords-self.y_piece_coord_hist[-1]

        # We only care about stuff detected in the bounds of the board
        y_pieces_gained = set()
        for coord in y_extra_pieces:
            if coord[0] > 8 or coord[1] > 8 or coord[0] < 1 or coord[1] < 1:
                continue
            else:
                y_pieces_gained.add(coord)

        # Do the same stuff for the white pieces

        b_pieces_lost = self.b_piece_coord_hist[-1]-b_piece_coords
        b_extra_pieces = b_piece_coords-self.b_piece_coord_hist[-1]
        b_pieces_gained = set()
        for coord in b_extra_pieces:
            if coord[0] > 8 or coord[1] > 8 or coord[0] < 1 or coord[1] < 1:
                continue
            else:
                b_pieces_gained.add(coord)

        if self.turn == 'black':
            if len(b_pieces_gained) > 0:
                # We probably detected something that is not a white piece since it is not white's turn
                # or we missed an earlier move
                print("Error: white move on black turn")
                return 'error'
            elif len(y_pieces_lost) == 0 and len(y_pieces_gained) == 0:
                # Nothing happend
                self.y_piece_coord_hist.append(self.y_piece_coord_hist[-1])
                self.b_piece_coord_hist.append(self.b_piece_coord_hist[-1])
                return 'no move'
            elif len(y_pieces_lost) == 1 and len(y_pieces_gained) == 1:
                # We moved one piece
                move = self.chess_to_proper_coords(next(iter(y_pieces_lost))) + self.chess_to_proper_coords(next(iter(y_pieces_gained)))
                try:
                    # Check if we castled king but rook has not moved yet
                    if self.board.san(chess.Move.from_uci(move)) == 'O-O' or self.board.san(chess.Move.from_uci(move)) == 'O-O-O':
                        self.board.push_uci(move)
                        print(self.board)
                        print()
                        self.y_piece_coord_hist.append( (self.y_piece_coord_hist[-1] - y_pieces_lost) | y_pieces_gained)
                        self.b_piece_coord_hist.append(self.b_piece_coord_hist[-1])
                        self.turn = 'black_finish_castle'
                        return 'move'
                    self.board.push_uci(move)
                except:
                    return 'error'
                print(self.board)
                print()
                self.y_piece_coord_hist.append( (self.y_piece_coord_hist[-1] - y_pieces_lost) | y_pieces_gained)
                self.b_piece_coord_hist.append(self.b_piece_coord_hist[-1])
                self.turn = 'white'
                return 'move'
            elif len(y_pieces_lost) == 2 and len(y_pieces_gained) == 2:
                # A two piece move can only be a castle
                move = '0-0'
                try:
                    self.board.push_san(move)
                except:
                    try:
                        move = '0-0-0'
                        self.board.push_san(move)
                    except:
                        return 'error'
                print(self.board)
                print()  
                self.y_piece_coord_hist.append( (self.y_piece_coord_hist[-1] - y_pieces_lost) | y_pieces_gained)
                self.b_piece_coord_hist.append(self.b_piece_coord_hist[-1])
                self.turn = 'white'
                return 'move'
            elif len(b_pieces_lost) > 0 or len(y_pieces_lost) > 0:
                # Hidden pieces probably by a hand use memory
                self.b_piece_coord_hist.append(self.b_piece_coord_hist[-1])
                self.y_piece_coord_hist.append(self.y_piece_coord_hist[-1])
                return 'no move'
            else:
                print('Error')
                return 'error'
        elif self.turn == 'white':
            if len(y_pieces_gained) > 0:
                # We probably detected something that is not a black piece since it is not black's turn
                # or we missed an earlier move
                print("Error: black move on white turn")
                return 'error'
            elif len(b_pieces_lost) == 0 and len(b_pieces_gained) == 0:
                self.b_piece_coord_hist.append(self.b_piece_coord_hist[-1])
                self.y_piece_coord_hist.append(self.y_piece_coord_hist[-1])
                return 'no move'
            elif len(b_pieces_lost) == 1 and len(b_pieces_gained) == 1:
                move = self.chess_to_proper_coords(next(iter(b_pieces_lost))) + self.chess_to_proper_coords(next(iter(b_pieces_gained)))
                try:
                    if self.board.san(chess.Move.from_uci(move)) == 'O-O' or self.board.san(chess.Move.from_uci(move)) == 'O-O-O':
                        self.board.push_uci(move)
                        print(self.board)
                        print()
                        self.b_piece_coord_hist.append( (self.b_piece_coord_hist[-1] - b_pieces_lost) | b_pieces_gained)
                        self.y_piece_coord_hist.append(self.y_piece_coord_hist[-1])
                        self.turn = 'white_finish_castle'
                        return 'move'
                    self.board.push_uci(move)
                except:
                    return False
                print(self.board)
                print()
                self.b_piece_coord_hist.append( (self.b_piece_coord_hist[-1] - b_pieces_lost) | b_pieces_gained)
                self.y_piece_coord_hist.append(self.y_piece_coord_hist[-1])
                self.turn = 'black'
                return 'move'
            elif len(b_pieces_lost) == 2 and len(b_pieces_gained) == 2:
                # A two piece move can only be a castle
                move = '0-0'
                try:
                    self.board.push_san(move)
                except:
                    try:
                        move = '0-0-0'
                        self.board.push_san(move)
                    except:
                        return 'error'
                print(self.board)
                print()
                self.b_piece_coord_hist.append( (self.b_piece_coord_hist[-1] - b_pieces_lost) | b_pieces_gained)
                self.y_piece_coord_hist.append(self.y_piece_coord_hist[-1])
                self.turn = 'black'
                return 'move'
            elif len(b_pieces_lost) > 0 or len(y_pieces_lost) > 0:
                # Hidden pieces usually by a hand use memory
                self.b_piece_coord_hist.append(self.b_piece_coord_hist[-1])
                self.y_piece_coord_hist.append(self.y_piece_coord_hist[-1])
                return 'no move'
            else:
                print('Error')
                return 'error'
        elif self.turn == 'white_finish_castle':
            if len(y_pieces_gained) > 0:

                print("Error: black move on white finish castle")
                return 'error'
            elif len(b_pieces_lost) == 0 and len(b_pieces_gained) == 0:
                # Nothing Happenend
                self.b_piece_coord_hist.append(self.b_piece_coord_hist[-1])
                self.y_piece_coord_hist.append(self.y_piece_coord_hist[-1])
                return 'no move'
            elif len(b_pieces_lost) == 1 and len(b_pieces_gained) == 1:
                # Castled rook
                self.b_piece_coord_hist.append( (self.b_piece_coord_hist[-1] - b_pieces_lost) | b_pieces_gained)
                self.y_piece_coord_hist.append(self.y_piece_coord_hist[-1])
                self.turn = 'black'
                return 'no move'
            elif len(b_pieces_lost) > 0 or len(y_pieces_lost) > 0:
                # Hidden Pieces usually by a hand use memory
                self.b_piece_coord_hist.append(self.b_piece_coord_hist[-1])
                self.y_piece_coord_hist.append(self.y_piece_coord_hist[-1])
                return 'no move'
            else:
                print('Error')
                return 'error'
        elif self.turn == 'black_finish_castle':
            if len(b_pieces_gained) > 0:

                print("Error: white move on black finish castle")
                return 'error'
            elif len(y_pieces_lost) == 0 and len(y_pieces_gained) == 0:
                # Nothing happend
                self.y_piece_coord_hist.append(self.y_piece_coord_hist[-1])
                self.b_piece_coord_hist.append(self.b_piece_coord_hist[-1])
                return 'no move'
            elif len(y_pieces_lost) == 1 and len(y_pieces_gained) == 1:
                # Castled rook
                self.y_piece_coord_hist.append( (self.y_piece_coord_hist[-1] - y_pieces_lost) | y_pieces_gained)
                self.b_piece_coord_hist.append(self.b_piece_coord_hist[-1])
                self.turn = 'white'
                return 'no move'
            elif len(y_pieces_lost) > 0 or len(b_pieces_lost) > 0:
                # Hidden Pieces usually by a hand use memory
                self.y_piece_coord_hist.append(self.y_piece_coord_hist[-1])
                self.b_piece_coord_hist.append(self.b_piece_coord_hist[-1])
                return 'no move'
            else:
                print('Error')
                return 'error'


if __name__ == '__main__':

    # Pass the function for each game to use ChessRecognizer on it
    def get_img_str_game1(i):
        return 'game1\\ezgif-frame-'+str(i+1).rjust(3,'0')+'.jpg'
    def get_img_str_game2(i):
        return 'game2\\frame'+str(i)+'.jpg'
    def get_img_str_game3(i):
        return 'game3\\frame'+str(i)+'.jpg'
    def get_img_str_game4(i):
        return 'game4\\frame'+str(i)+'.jpg'
        

    chess_recognizer = ChessRecognizer(get_img_str_game3)
    chess_recognizer.calibrate_colors(chess_recognizer.cal_img)
    chess_recognizer.calibrate_grid()
    chess_recognizer.play()
