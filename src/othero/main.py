import tkinter as tk
from tkinter import messagebox

# 定数
BOARD_SIZE = 8
SQUARE_SIZE = 60
STONE_RADIUS = 25
WIDTH = SQUARE_SIZE * BOARD_SIZE
HEIGHT = SQUARE_SIZE * BOARD_SIZE
COLOR_BOARD = "#008800"  # 濃い緑色
COLOR_BLACK = "black"
COLOR_WHITE = "white"

class ReversiGame:
    def __init__(self, master):
        self.master = master
        master.title("リバーシ (Reversi)")

        # 盤面の状態 (0:空, 1:黒, 2:白)
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        # 初期配置
        self.board[3][3] = 2  # 白
        self.board[3][4] = 1  # 黒
        self.board[4][3] = 1  # 黒
        self.board[4][4] = 2  # 白

        # 現在の手番 (1:黒, 2:白)
        self.current_player = 1

        # GUI要素の設定
        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg=COLOR_BOARD)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click_handler)

        self.status_label = tk.Label(master, text="", font=("Arial", 14))
        self.status_label.pack(pady=10)

        self.draw_board()
        self.update_status()
        self.check_game_status()

# --------------------------------------------------
## 描画・更新処理
# --------------------------------------------------

    def draw_board(self):
        """盤面全体と石を描画します。"""
        self.canvas.delete("all")
        # マス目の線を描画
        for i in range(BOARD_SIZE + 1):
            # 縦線
            self.canvas.create_line(i * SQUARE_SIZE, 0, i * SQUARE_SIZE, HEIGHT, fill="black")
            # 横線
            self.canvas.create_line(0, i * SQUARE_SIZE, WIDTH, i * SQUARE_SIZE, fill="black")

        # 石を描画
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                stone = self.board[r][c]
                if stone != 0:
                    color = COLOR_BLACK if stone == 1 else COLOR_WHITE
                    # 石の中心座標
                    center_x = c * SQUARE_SIZE + SQUARE_SIZE // 2
                    center_y = r * SQUARE_SIZE + SQUARE_SIZE // 2
                    
                    self.canvas.create_oval(
                        center_x - STONE_RADIUS, center_y - STONE_RADIUS,
                        center_x + STONE_RADIUS, center_y + STONE_RADIUS,
                        fill=color, outline="gray"
                    )

        # 置ける場所（ヒント）を描画
        possible_moves = self.get_possible_moves(self.current_player)
        for r, c in possible_moves:
            center_x = c * SQUARE_SIZE + SQUARE_SIZE // 2
            center_y = r * SQUARE_SIZE + SQUARE_SIZE // 2
            # 小さな円を薄い色で表示
            self.canvas.create_oval(
                center_x - 5, center_y - 5,
                center_x + 5, center_y + 5,
                fill="red" if self.current_player == 1 else "blue",
                outline=""
            )

    def update_status(self):
        """現在の手番と石の数をステータスバーに表示します。"""
        black_count = sum(row.count(1) for row in self.board)
        white_count = sum(row.count(2) for row in self.board)
        player_color = "黒" if self.current_player == 1 else "白"
        
        status = f"手番: {player_color} | 黒: {black_count} vs 白: {white_count}"
        self.status_label.config(text=status)

# --------------------------------------------------
## ゲームロジック
# --------------------------------------------------

    def get_flips(self, r, c, player):
        """指定した位置に石を置いたときに裏返せる石のリストを返します。"""
        if self.board[r][c] != 0:
            return []

        flips = []
        opponent = 3 - player  # 相手の色 (1なら2, 2なら1)

        # 8方向をチェック (dy, dx)
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # 縦横
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # 斜め
        ]

        for dr, dc in directions:
            path = []
            for i in range(1, BOARD_SIZE):
                nr, nc = r + dr * i, c + dc * i

                if not (0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE):
                    break # 盤外
                
                cell = self.board[nr][nc]
                if cell == opponent:
                    path.append((nr, nc)) # 相手の石を発見
                elif cell == player:
                    # 自分の石に挟まれた！
                    flips.extend(path)
                    break
                elif cell == 0:
                    break # 空マスに当たった
            
        return flips

    def get_possible_moves(self, player):
        """現在のプレイヤーが石を置ける全てのマスを返します。"""
        moves = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.get_flips(r, c, player):
                    moves.append((r, c))
        return moves

    def make_move(self, r, c, player):
        """石を配置し、裏返す処理を実行します。"""
        flips = self.get_flips(r, c, player)
        if not flips:
            return False # 置けない場所

        # 石を置く
        self.board[r][c] = player
        # 石を裏返す
        for fr, fc in flips:
            self.board[fr][fc] = player
        
        return True

# --------------------------------------------------
## イベントハンドラ・ゲーム進行
# --------------------------------------------------

    def click_handler(self, event):
        """キャンバスがクリックされたときの処理です。"""
        # クリック座標からマス目(r, c)を計算
        c = event.x // SQUARE_SIZE
        r = event.y // SQUARE_SIZE

        if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
            return

        # 石を置いて裏返す
        if self.make_move(r, c, self.current_player):
            # 手番を交代
            self.current_player = 3 - self.current_player
            
            # ゲームの状態を更新
            self.draw_board()
            self.update_status()
            self.check_game_status()
        else:
            messagebox.showinfo("エラー", "そこには置けません！")


    def check_game_status(self):
        """ゲーム終了判定とパス処理を実行します。"""
        player = self.current_player
        opponent = 3 - player
        
        player_moves = self.get_possible_moves(player)
        opponent_moves = self.get_possible_moves(opponent)

        if not player_moves and not opponent_moves:
            # 両者とも打てない -> ゲーム終了
            self.end_game()
            return
        
        if not player_moves:
            # 現在の手番のプレイヤーが打てない -> パス
            messagebox.showinfo("パス", f"手番の{'黒' if player==1 else '白'}は打てないのでパスします。")
            self.current_player = opponent
            # パス後にもう一度チェック（相手が打てるか、そのまま終了か）
            self.draw_board()
            self.update_status()
            # パス後に相手が打てる場所がない場合もあるため再チェック
            if not opponent_moves:
                 self.end_game()

    def end_game(self):
        """ゲーム終了時の処理です。"""
        black_count = sum(row.count(1) for row in self.board)
        white_count = sum(row.count(2) for row in self.board)

        if black_count > white_count:
            winner = "黒"
        elif white_count > black_count:
            winner = "白"
        else:
            winner = "引き分け"

        final_message = (
            f"ゲーム終了！\n"
            f"黒: {black_count} vs 白: {white_count}\n"
            f"勝者: {winner}"
        )
        messagebox.showinfo("ゲーム終了", final_message)
        
        # キャンバスのクリックを無効化
        self.canvas.unbind("<Button-1>")


# メインウィンドウの作成と実行
root = tk.Tk()
game = ReversiGame(root)
root.mainloop()
