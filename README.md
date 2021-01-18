# new-post-alert
Displays a list of recent new posts on r/buildapcsales.

Also, it checks for new posts every 30 seconds and updates the list if and only if a new post has been made.

To set it up yourself,

    1) Go to Reddit homepage on any browser of your choice.
    
    2) Login to your account and navigate to the preferences page.
    
    3) Go to the apps tab and click "create another app..."
    
    4) Name it anything and set it up as a "script" application.
    
    5) Grab your client_id (should be right under "personal use script") and client_secret credentials.
    
    6) Create a file named config.ini and copy in the format of
        "    [DEFAULT]
            client_id = 'your client_id'
            client_secret = 'your client_secret'"
    7) Run root.py for now
            
Todo:

    1) Add a settings page to control the interval between updates and possible different mode for links (opening the comments of the post instead of the direct link submitted by the user).
    
    2) Run the program in the background without having to display the window (when user clicks on a notification, display window right away).
    
    3) Display icon on system tray (research on how to as well).
    
