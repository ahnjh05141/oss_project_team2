import matplotlib
matplotlib.use("TkAgg")  # 백엔드 지정

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

class Commit:
    def __init__(self, commit_id, author, message, date):
        self.commit_id = commit_id
        self.author = author
        self.message = message
        self.date = date

class GitCommitHistoryGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Git Commit History")
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.commits = []
        self.selected_commit = None

    def add_commit(self, commit):
        self.commits.append(commit)

    def show_commit_history(self):
        commit_dates = []
        commit_ids = []
        for commit in self.commits:
            commit_dates.append(commit.date)
            commit_ids.append(commit.commit_id)
            #commit_counts.append(len(commit.changes))

        #self.ax.scatter(commit_dates, commit_ids, marker='o', s=100)

        self.ax.plot(commit_dates, commit_ids, marker='o')
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Commit Id')

        self.canvas.draw()

    def show_commit_details_dialog(self, commit):
        details = f"Commit ID: {commit.commit_id}\n"
        details += f"Author: {commit.author}\n"
        details += f"Message: {commit.message}\n"
        details += f"Date: {commit.date}\n"
        #details += "Changes:\n"
        # for change in commit.changes:
        #     details += f"- {change}\n"
        messagebox.showinfo("Commit Details", details)

    #그래프 위 각 점을 눌렀을 경우, 커밋 정보가 다이어로그로 출력된다.
    def on_click(self, event):
        if event.inaxes == self.ax:
            commit_index = round(event.ydata)
            if commit_index < len(self.commits):
                self.selected_commit = self.commits[commit_index]
                self.show_commit_details_dialog(self.selected_commit)