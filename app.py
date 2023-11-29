from flask import Flask, request, render_template
import numpy as np
import json,random

def read_json(file_path):
    with open(file_path,'r') as file:
        data = json.load(file)
    return data 

json_file_path = './data/data.json'
sudoku = read_json(json_file_path)


global score,key
key=random.randint(0, len(sudoku['sudoku_unsolved'])-1)
score=0

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    global score,key
    sudoku_solved=sudoku['sudoku_solved'][key]
    sudoku_unsolved=sudoku['sudoku_unsolved'][key]
    sudoku_board = sudoku_unsolved
    status={'status':'Start','score':str(score)}
    if request.method == 'POST':
        try:
            valid_move=False
            for i in range(9):
                for j in range(9):
                    key = f'cell-{i}-{j}'
                    val = (request.form[key])
                    if val=="" or int(val)==0:
                        continue
                    else:
                        val=int(val)
                        if sudoku_solved[i][j]==val and sudoku_board[i][j]==0:
                            sudoku_board[i][j]=val
                            valid_move=True
            if valid_move:
                move="VALID MOVE!"
                score+=5
                valid_move = False
            else:
                move='INVALID MOVE!'
                score-=3
            status={'status':move,'score':str(score)}                                            
        except Exception as e:
            print(e)
        finally:
            print(sudoku_board)
    return render_template('index.html', sudoku_board=sudoku_board,status=status)



@app.route("/newgame", methods=["POST"])
def newgame():
    global key,score
    key = random.randint(0,1)
    score = 0
    status={'status':'NEW GAME','score':score}
    sudoku_board=sudoku['sudoku_unsolved'][key]
    print(sudoku_board)  
    return render_template("index.html", sudoku_board=sudoku_board,status=status)


@app.route("/solve", methods=["POST"])
def solve():
    global key
    sudoku_solved=sudoku['sudoku_solved'][key]
    status={'status':'SOLVE','score':'0'}                                            
    return render_template("index.html",sudoku_board=sudoku_solved,status=status)
    

if __name__ == "__main__":
    app.run(use_reloader=True)

