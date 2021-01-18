from tkinter import *
from tkinter import ttk
from tkinter.font import Font
import copy
import praw_feed as pf
import webbrowser as web
import time
from win10toast import ToastNotifier

class Root(Tk):
	def __init__(self):
		super().__init__()
		self.title('New Post Alert')
		self.geometry('1200x700')
		self.create_menu()
		self.prep_treeview()
		self.notifier = ToastNotifier()
		self.last_selected_item = None
	
	# Create the menu bar for quitting the program for now.
	def create_menu(self):
		menu_bar = Menu(self)
		self.config(menu = menu_bar)

		file_menu = Menu(menu_bar)
		file_menu.add_command(label = 'Exit', command = self.quit)
		menu_bar.add_cascade(label = 'File', menu = file_menu)

	# Initialize the treeview with proper headings before filling up the data with posts
	def prep_treeview(self):
		self.post_tree = ttk.Treeview(self)

		fetched_list = pf.subreddit_post_fork('buildapcsales', 35)

		self.make_post_list(fetched_list)

		self.post_tree['columns'] = ('Post Title', 'Flair', 'Time Posted')

		self.post_tree.column('#0', width = 0, stretch = NO)
		self.post_tree.column('Post Title', anchor = W, width = 800, minwidth = 600)
		self.post_tree.column('Flair', anchor = CENTER, width = 100, minwidth = 100)
		self.post_tree.column('Time Posted', anchor = W, width = 80, minwidth = 80)

		self.post_tree.heading('Post Title', text = 'Post Title', anchor = W)
		self.post_tree.heading('Flair', text = 'Flair', anchor = CENTER)
		self.post_tree.heading('Time Posted', text = 'Time Posted', anchor = W)

		self.double_click_id = self.post_tree.bind("<Double-Button-1>", self.onClickPostEvent)

		self.idx = 0
		self.populate_treeview()

		self.post_tree.pack(padx = 20, pady = 20, ipadx = 500, ipady = 500)
	
	# Using the data from PRAW, make a usable list and dictionary
	def make_post_list(self, fetched_list):
		self.post_data = []
		self.post_url = {}

		for submission in fetched_list:
			post = (submission.title, submission.link_flair_text, submission.created_utc)
			self.post_url[submission.title] = submission.url
			self.post_data.append(post)
	
	# Fill the treeview with information taken from PRAW
	def populate_treeview(self):
		for submission in self.post_data:
			self.post_tree.insert(parent = '', index = 'end', iid = self.idx, values = (submission[0], submission[1], submission[2]))
			self.idx+=1

	# Event handler for double clicking an item in the treeview
	def onClickPostEvent(self, event):
		item = self.post_tree.focus()
		post = self.post_tree.item(item, 'values')[0]
		post_link = self.post_url[post]

		if self.last_selected_item != post_link:
			web.open_new_tab(post_link)
			self.last_selected_item = post_link
		else:
			self.last_selected_item = None
	
	# Simple notification for Windows
	def pushNotification(self, post_title):
		self.notifier.show_toast('New Post Alert', post_title, duration = 5, threaded = True)
	
	# Check if a new post has been submitted to the subreddit every X amount of seconds
	def check_new_post(self):
		new_fetched_list = pf.subreddit_post_fork('buildapcsales', 35)
		copy_list = copy.deepcopy(new_fetched_list)
		update_new_post = False
		
		for post in new_fetched_list:
			if post.title not in self.post_url:
				update_new_post = True
				post_title = post.title
				break

		if update_new_post:
			self.pushNotification(post_title)
			self.update_treeview(copy_list)

		self.after(30000, self.check_new_post)

	# Clear the treeview and populate with newly fetched information
	def update_treeview(self, to_replace_with_list):
		for child in self.post_tree.get_children():
			self.post_tree.delete(child)
		self.make_post_list(to_replace_with_list)
		self.populate_treeview()


if __name__ == "__main__":
	root = Root()
	root.after(30000, root.check_new_post)
	root.mainloop()