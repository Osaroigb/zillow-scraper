from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

from scrapy.utils import project
from scrapy import spiderloader
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import threading


def get_spiders():

    project_settings = project.get_project_settings()
    spider_loader = spiderloader.SpiderLoader.from_settings(project_settings)
    return spider_loader.list()


def get_selected_spider(value):

    global selected_spider
    selected_spider = value
    return selected_spider


def get_selected_feed(value):

    global selected_feed
    selected_feed = value
    return selected_feed


def browse_button():

    global folder_path
    folder_path = filedialog.askdirectory()
    folder_path_entry.delete(0, END)
    folder_path_entry.insert(index=0, string=folder_path)
    return folder_path


def execute_spider():

    if dataset_entry.get() == "" or folder_path_entry.get() == "":
        messagebox.showerror(title="Error", message="All fields are required!")
    else:

        try:
            feed_uri = f"file:///{folder_path}/{dataset_entry.get()}.{selected_feed}"
        except NameError:
            messagebox.showerror(title="Error", message="Select a feed type!")
        else:

            project_settings = project.get_project_settings()
            project_settings.set(name="FEED_URI", value=feed_uri)
            project_settings.set(name="FEED_TYPE", value=selected_feed)

            configure_logging()
            runner = CrawlerRunner(settings=project_settings)

            try:
                runner.crawl(crawler_or_spidercls=selected_spider)
                reactor.run()
            except NameError:
                messagebox.showerror(title="Error", message="Select a spider!")


def start_thread(event):

    global execute_thread
    execute_thread = threading.Thread(target=execute_spider, daemon=True)
    execute_thread.start()
    app.after(ms=10, func=check_thread)


def check_thread():

    if execute_thread.is_alive():
        app.after(ms=10, func=check_thread)


app = Tk()

# Spiders
spider_label = Label(app, text="Choose a Spider")
spider_label.grid(row=0, column=0, sticky=W, pady=10, padx=10)

spider_text = StringVar(app)
spider_text.set(value="Choose a Spider")
spiders = [spider for spider in get_spiders()]

spiders_dropdown = OptionMenu(app, spider_text, *spiders, command=get_selected_spider)
spiders_dropdown.grid(row=0, column=1, sticky=E, columnspan=2)

# Feeds
feed_label = Label(app, text="Choose a Feed")
feed_label.grid(row=1, column=0, sticky=W, pady=10, padx=10)

feed_text = StringVar(app)
feed_text.set(value="Choose a Feed Type")
feeds = ["json", "csv", "xml"]

feeds_dropdown = OptionMenu(app, feed_text, *feeds, command=get_selected_feed)
feeds_dropdown.grid(row=1, column=1, sticky=E, columnspan=2)

# Path Entry
folder_path_text = StringVar(app)
folder_path_entry = Entry(app, textvariable=folder_path_text)
folder_path_entry.grid(row=2, column=0, pady=10, padx=10)

# Dataset Entry
dataset_text = StringVar(app)
dataset_entry = Entry(app, textvariable=dataset_text, width=10)
dataset_entry.grid(row=2, column=1, pady=10, padx=10)

# Browse Button
browse_btn = Button(app, text="Browse", command=browse_button)
browse_btn.grid(row=2, column=2, sticky=E)

# Scrape Button
scrape_btn = Button(app, text="Scrape", width=10, command=lambda: start_thread(event=None))
scrape_btn.grid(row=3, column=0, columnspan=3)

# App
app.title(string="Web Scraper")
app.geometry("305x160")

app.resizable(width=False, height=False)
app.mainloop()
