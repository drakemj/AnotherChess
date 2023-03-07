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
