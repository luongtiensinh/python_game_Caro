import tkinter as tk
from tkinter import messagebox, Frame, Label
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Co Caro 5x5: Nguoi vs May")
        self.root.configure(bg="#F0F0F0")
        
        # Tăng kích thước bàn cờ lên 5x5
        self.size = 5
        self.board = [["" for _ in range(self.size)] for _ in range(self.size)]
        self.buttons = [[None for _ in range(self.size)] for _ in range(self.size)]
        
        # Theo dõi điểm số
        self.player_score = 0
        self.computer_score = 0
        self.draws = 0
        
        # Màu sắc và thiết kế
        self.bg_color = "#F0F0F0"       # Màu nền
        self.board_color = "#E0E0E0"    # Màu bàn cờ
        self.player_color = "#4285F4"   # Màu người chơi (X) - Xanh Google
        self.computer_color = "#EA4335" # Màu máy tính (O) - Đỏ Google
        self.font = ("Roboto", 28, "bold")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame chính
        main_frame = Frame(self.root, bg=self.bg_color, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Tiêu đề
        title_frame = Frame(main_frame, bg=self.bg_color)
        title_frame.pack(pady=(0, 15))
        
        title_label = Label(title_frame, text="CO CARO 5x5", 
                           font=("Roboto", 22, "bold"), 
                           bg=self.bg_color, fg="#202124")
        title_label.pack()
        
        subtitle_label = Label(title_frame, text="Nguoi vs May (AI Minimax)", 
                             font=("Roboto", 14), 
                             bg=self.bg_color, fg="#5F6368")
        subtitle_label.pack()
        
        # Frame bảng điểm
        score_frame = Frame(main_frame, bg=self.bg_color)
        score_frame.pack(pady=(0, 15))
        
        self.score_label = Label(score_frame, 
                                text=f"Nguoi: {self.player_score}  |  Hoa: {self.draws}  |  May: {self.computer_score}", 
                                font=("Roboto", 12, "bold"), 
                                bg=self.bg_color, fg="#202124")
        self.score_label.pack()
        
        # Frame bàn cờ
        board_frame = Frame(main_frame, bg=self.board_color, bd=2, relief="ridge")
        board_frame.pack(padx=10, pady=10)
        
        for r in range(self.size):
            for c in range(self.size):
                btn = tk.Button(board_frame, text="", font=self.font, width=2, height=1,
                               bg="white", activebackground="#F8F9FA",
                               command=lambda row=r, col=c: self.player_move(row, col))
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[r][c] = btn
        
        # Frame điều khiển
        control_frame = Frame(main_frame, bg=self.bg_color)
        control_frame.pack(pady=15)
        
        reset_btn = tk.Button(control_frame, text="Choi lai", font=("Roboto", 12, "bold"),
                             bg="#FBBC05", fg="white", activebackground="#F9A602",
                             relief="flat", padx=15, pady=5,
                             command=self.reset_board)
        reset_btn.pack(side="left", padx=5)
        
        quit_btn = tk.Button(control_frame, text="Thoat", font=("Roboto", 12, "bold"),
                            bg="#EA4335", fg="white", activebackground="#D33426",
                            relief="flat", padx=15, pady=5,
                            command=self.root.quit)
        quit_btn.pack(side="left", padx=5)
        
        # Trạng thái
        self.status_label = Label(main_frame, text="Luot cua ban", 
                                 font=("Roboto", 12), 
                                 bg=self.bg_color, fg="#202124")
        self.status_label.pack(pady=(10, 0))
    
    def player_move(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = "X"
            self.buttons[row][col]["text"] = "X"
            self.buttons[row][col]["fg"] = self.player_color
            self.buttons[row][col]["disabledforeground"] = self.player_color
            self.buttons[row][col]["state"] = "disabled"
            
            self.status_label.config(text="Dang suy nghi...")
            
            winner = self.check_winner()
            if winner:
                self.end_game(winner)
            elif self.is_draw():
                self.end_game("draw")
            else:
                # Sử dụng after để tạo delay và cập nhật giao diện trước khi máy đi
                self.root.after(500, self.computer_move)
    
    def computer_move(self):
        # Sử dụng thuật toán Minimax để tìm nước đi tốt nhất
        depth = 3  # Chiều sâu tìm kiếm - có thể điều chỉnh
        best_score = float('-inf')
        best_move = None
        
        # Giới hạn thời gian tính toán trên bàn 5x5 bằng cách heuristic đơn giản:
        # Nếu có nước đi thắng ngay, chọn nước đó
        # Nếu có nước chặn thắng của người chơi, chọn nước đó
        
        # Kiểm tra nếu máy có thể thắng ngay
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == "":
                    self.board[r][c] = "O"
                    if self.check_winner() == "O":
                        self.board[r][c] = ""
                        best_move = (r, c)
                        break
                    self.board[r][c] = ""
            if best_move:
                break
                
        # Nếu không thể thắng ngay, kiểm tra nếu phải chặn người chơi
        if not best_move:
            for r in range(self.size):
                for c in range(self.size):
                    if self.board[r][c] == "":
                        self.board[r][c] = "X"
                        if self.check_winner() == "X":
                            self.board[r][c] = ""
                            best_move = (r, c)
                            break
                        self.board[r][c] = ""
                if best_move:
                    break
        
        # Nếu không có nước nguy hiểm, sử dụng minimax (với giới hạn để tăng tốc độ)
        if not best_move:
            # Ưu tiên ô giữa nếu trống
            center = self.size // 2
            if self.board[center][center] == "":
                best_move = (center, center)
            else:
                # Sử dụng Minimax cho các nước đi còn lại nhưng giới hạn số ô trống để xem xét
                empty_cells = [(r, c) for r in range(self.size) for c in range(self.size) if self.board[r][c] == ""]
                
                # Giới hạn số lượng nước đi xem xét để tránh quá lâu
                candidates = empty_cells[:min(len(empty_cells), 9)]  # Chỉ xem xét tối đa 9 nước đi
                
                for r, c in candidates:
                    self.board[r][c] = "O"
                    score = self.minimax(depth - 1, False, float('-inf'), float('inf'))
                    self.board[r][c] = ""
                    
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)
        
        # Nếu không tìm được nước đi tốt, chọn ngẫu nhiên
        if not best_move:
            empty_cells = [(r, c) for r in range(self.size) for c in range(self.size) if self.board[r][c] == ""]
            if empty_cells:
                best_move = random.choice(empty_cells)
        
        # Thực hiện nước đi
        if best_move:
            r, c = best_move
            self.board[r][c] = "O"
            self.buttons[r][c]["text"] = "O"
            self.buttons[r][c]["fg"] = self.computer_color
            self.buttons[r][c]["disabledforeground"] = self.computer_color
            self.buttons[r][c]["state"] = "disabled"
            
            winner = self.check_winner()
            if winner:
                self.end_game(winner)
            elif self.is_draw():
                self.end_game("draw")
            else:
                self.status_label.config(text="Luot cua ban")
    
    def minimax(self, depth, is_maximizing, alpha, beta):
        winner = self.check_winner()
        if winner == "O":
            return 10
        if winner == "X":
            return -10
        if self.is_draw() or depth == 0:
            return 0
        
        if is_maximizing:
            best_score = float('-inf')
            for r in range(self.size):
                for c in range(self.size):
                    if self.board[r][c] == "":
                        self.board[r][c] = "O"
                        score = self.minimax(depth - 1, False, alpha, beta)
                        self.board[r][c] = ""
                        best_score = max(score, best_score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
            return best_score
        else:
            best_score = float('inf')
            for r in range(self.size):
                for c in range(self.size):
                    if self.board[r][c] == "":
                        self.board[r][c] = "X"
                        score = self.minimax(depth - 1, True, alpha, beta)
                        self.board[r][c] = ""
                        best_score = min(score, best_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
            return best_score
    
    def check_winner(self):
        # Số ký tự cần xếp hàng để thắng (3 cho bàn cờ 5x5 để dễ chơi hơn)
        win_length = 4
        
        # Kiểm tra các hàng
        for r in range(self.size):
            for c in range(self.size - win_length + 1):
                if self.board[r][c] != "" and all(self.board[r][c] == self.board[r][c + i] for i in range(win_length)):
                    return self.board[r][c]
        
        # Kiểm tra các cột
        for c in range(self.size):
            for r in range(self.size - win_length + 1):
                if self.board[r][c] != "" and all(self.board[r][c] == self.board[r + i][c] for i in range(win_length)):
                    return self.board[r][c]
        
        # Kiểm tra đường chéo xuống
        for r in range(self.size - win_length + 1):
            for c in range(self.size - win_length + 1):
                if self.board[r][c] != "" and all(self.board[r][c] == self.board[r + i][c + i] for i in range(win_length)):
                    return self.board[r][c]
        
        # Kiểm tra đường chéo lên
        for r in range(win_length - 1, self.size):
            for c in range(self.size - win_length + 1):
                if self.board[r][c] != "" and all(self.board[r][c] == self.board[r - i][c + i] for i in range(win_length)):
                    return self.board[r][c]
        
        return None
    
    def is_draw(self):
        return all(self.board[r][c] != "" for r in range(self.size) for c in range(self.size))
    
    def highlight_winning_line(self, player):
        win_length = 4
        winning_cells = []
        
        # Kiểm tra các hàng
        for r in range(self.size):
            for c in range(self.size - win_length + 1):
                if all(self.board[r][c + i] == player for i in range(win_length)):
                    winning_cells = [(r, c + i) for i in range(win_length)]
                    break
            if winning_cells:
                break
                
        # Kiểm tra các cột
        if not winning_cells:
            for c in range(self.size):
                for r in range(self.size - win_length + 1):
                    if all(self.board[r + i][c] == player for i in range(win_length)):
                        winning_cells = [(r + i, c) for i in range(win_length)]
                        break
                if winning_cells:
                    break
        
        # Kiểm tra đường chéo xuống
        if not winning_cells:
            for r in range(self.size - win_length + 1):
                for c in range(self.size - win_length + 1):
                    if all(self.board[r + i][c + i] == player for i in range(win_length)):
                        winning_cells = [(r + i, c + i) for i in range(win_length)]
                        break
                if winning_cells:
                    break
        
        # Kiểm tra đường chéo lên
        if not winning_cells:
            for r in range(win_length - 1, self.size):
                for c in range(self.size - win_length + 1):
                    if all(self.board[r - i][c + i] == player for i in range(win_length)):
                        winning_cells = [(r - i, c + i) for i in range(win_length)]
                        break
                if winning_cells:
                    break
        
        # Tô sáng các ô thắng
        highlight_color = "#FBBC05"  # Màu vàng Google
        for r, c in winning_cells:
            self.buttons[r][c].config(bg=highlight_color)
    
    def end_game(self, result):
        if result == "X":
            self.player_score += 1
            self.highlight_winning_line("X")
            message = "Ban da thang!"
            self.status_label.config(text="Ban thang!")
        elif result == "O":
            self.computer_score += 1
            self.highlight_winning_line("O")
            message = "May da thang!"
            self.status_label.config(text="May thang!")
        else:  # Hòa
            self.draws += 1
            message = "Hoa!"
            self.status_label.config(text="Hoa!")
        
        # Cập nhật bảng điểm
        self.score_label.config(text=f"Nguoi: {self.player_score}  |  Hoa: {self.draws}  |  May: {self.computer_score}")
        
        # Hiển thị thông báo
        messagebox.showinfo("Ket qua", message)
        
        # Vô hiệu hóa các nút sau khi game kết thúc
        for r in range(self.size):
            for c in range(self.size):
                self.buttons[r][c]["state"] = "disabled"
    
    def reset_board(self):
        self.board = [["" for _ in range(self.size)] for _ in range(self.size)]
        for r in range(self.size):
            for c in range(self.size):
                self.buttons[r][c]["text"] = ""
                self.buttons[r][c]["state"] = "normal"
                self.buttons[r][c]["bg"] = "white"
                self.buttons[r][c]["fg"] = "black"
        
        self.status_label.config(text="Luot cua ban")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()