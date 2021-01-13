from tkinter import *
from tkinter import ttk
from tkinter.font import Font
import praw_feed as pf
import webbrowser as web
import time

# scraped_flag, list_of_posts = rss.reddit_new_rss("buildapcsales")

class Root(Tk):
	def __init__(self):
		super().__init__()

		self.title('New Post Alert')
		self.geometry('1200x700')
		self.prep_treeview()
		self.display_treeview()
		self.last_selected_item = None

	def prep_treeview(self):
		self.post_tree = ttk.Treeview(self)

		self.prep_list = pf.subreddit_post_fork('buildapcsales', 35)

		self.post_data = []
		self.post_url = {}

		for submission in self.prep_list:
			post = (submission.title, submission.link_flair_text, submission.created_utc)
			self.post_url[submission.title] = submission.url
			self.post_data.append(post)

		self.post_tree['columns'] = ('Post Title', 'Flair', 'Time Posted')

		self.post_tree.column('#0', width = 0, stretch = NO)
		self.post_tree.column('Post Title', anchor = W, width = 800, minwidth = 600)
		self.post_tree.column('Flair', anchor = CENTER, width = 100, minwidth = 100)
		self.post_tree.column('Time Posted', anchor = W, width = 80, minwidth = 80)

		self.post_tree.heading('Post Title', text = 'Post Title', anchor = W)
		self.post_tree.heading('Flair', text = 'Flair', anchor = CENTER)
		self.post_tree.heading('Time Posted', text = 'Time Posted', anchor = W)

		idx = 0

		for submission in self.post_data:
			self.post_tree.insert(parent = '', index = 'end', iid = idx, values = (submission[0], submission[1], submission[2]))
			idx+=1

		self.double_click_id = self.post_tree.bind("<Double-Button-1>", self.onClickPostEvent)

	def display_treeview(self):
		self.post_tree.pack(padx = 20, pady = 20, ipadx = 500, ipady = 500)

	def onClickPostEvent(self, event):
		item = self.post_tree.focus()
		post = self.post_tree.item(item, 'values')[0]
		post_link = self.post_url[post]

		if self.last_selected_item != post_link:
			print(self.last_selected_item)
			web.open_new_tab(post_link)
			self.last_selected_item = post_link
		else:
			self.last_selected_item = None

if __name__ == "__main__":
	root = Root()
	while True:
		root.update_idletasks()
		root.update()