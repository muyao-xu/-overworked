import wxversion
wxversion.select('3.0')
import wx
import time
import wx.gizmos as gizmos
import datetime


s=0
sr= 0
input_work_time = -1
input_rest_time = -1

import httplib, urllib, base64
import json
import datetime
import time
import sched, os


############   Track working time of a day  ###############
#Global Variables used for # Track working time of a day #

total_seconds = 0
work_time_file_name = 'work_time.txt'
give_up = 0
flag = True
start_time = 0
boooo = 0;

scheduler = sched.scheduler(time.time, time.sleep)


def imagesnap(a='default'):
    os.system('imagesnap -w 1 snapshot.jpg')

def work(work_time):
    global flag, start_time

    if flag:
        start_time = time.time()
    flag = False

    t = 0
    no_face = 0
    start = round(time.time())
    length = 0
    for t in range(0, work_time):
        scheduler.enter(1, 1, imagesnap,('first',))
        scheduler.run()
        have_face = detect_face(str(round(time.time()*100)))
        if have_face:
            no_face = 0
        if not have_face:
            no_face += 1
        if no_face == 2:
            # TRUE for restart working
            return True

        length = round(time.time()) - start


        # if length >= work_time:
            # FALSE for need to take a rest
        if length >= work_time:
            add_work_time()
            return False


        

def detect_face(num):   
    from azure.storage.blob import BlockBlobService
    block_blob_service = BlockBlobService(account_name='snapshot2', account_key='wd6G16qs04fXYcO5qMZ6n1IrdVxvNwJ0wuC3ludTZ7AePUqe9XE+z1BS3b/fbiCm/vqrqnWqEAvyKeC6iYaEkQ==')

    # from azure.storage.blob import PublicAccess
    # block_blob_service.create_container('new', public_access=PublicAccess.Container)
    
    savename = 'myfile' + str(num)
    saveurl = 'https://snapshot2.blob.core.windows.net/pic/myfile' + str(num)


    from azure.storage.blob import ContentSettings
    block_blob_service.create_blob_from_path(
        'pic',
        savename,
        '/Users/Ivy/Desktop/snapshot.jpg',
        content_settings=ContentSettings(content_type='image/jpg'))           


    ################# Call Face - detect API ####################
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'f3cda7c8e0cd4a24a5a9746976e29c0c',
    }

    params = urllib.urlencode({
        # Request parameters
        'returnFaceId': 'false',
        'returnFaceLandmarks': 'true',
        'returnFaceAttributes': 'emotion',
    })

    url_face = saveurl
    #url_face2 = 'http://www.mychildmagazine.com.au/wp-content/uploads/2016/01/2-people-1-relationship-01.png'
    try:
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, "{\"url\":\""+url_face+"\"}", headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    #######################################
    #print(data)

    ########### Parse JSON #############
    for char in data:
        if char in "[]":
            data = data.replace(char,'')
    ####################################


    ########## Detect face, print bool ############
    x = 'faceAttributes'
    there_is_face = x in data
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    print there_is_face
    ###########################################################


    ############ Detect emotion ################
    emotion_comfort = 'Cheer up! This is not the worst day! <3'
    iamnegative = False;
    if there_is_face:
        j = json.loads(data)
        anger = j['faceAttributes']['emotion']['anger']
        sadness = j['faceAttributes']['emotion']['sadness']
        if anger > 0.2:
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            print emotion_comfort
            iamnegative = True
        elif sadness > 0.2:
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            print emotion_comfort
            iamnegative = True
    ############################################


    ############ Detect distance ################
    distance_remind = 'Your eyes maybe too close to the screen.'
    if there_is_face:
        j = json.loads(data)
        width = j['faceRectangle']['width']
        if width > 500:
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            print distance_remind
    #############################################

    
    if there_is_face:
        #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        record_detailed('detailed_data', iamnegative)
        return True
    else:
        add_work_time()
        return False


################## USE SECOND AS THE UNIT FOR DEMO ################
################# CALL THIS AFTER PRESSING START ####################
################## CALL THIS AGAIN IF ITSELF RETURNS TRUE ##################
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def start_to_work(work_time):
    return work(work_time)

############## CALL THIS FUNCTION IF START_TO_WORK RETURNS TRUE###############
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#check_rest = take_a_rest(rest_time)

################# IF RETURN FALSE ############################################
####### CALL START_TI_WORK #################

############## IF CHECK_REST RETURNS -1, continue the timer until times up. Call start_to_work as the following #################
######### IF CHECK_REST > 1, ######### POP UP A WINDOW ASK IF WANT TO GIVE UP ###########
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# if answer yes to give up:
#   update_give_up()
#   start_to_work(work___time)

######### IF NOT GIVE UP, CALL TAKE REST AGAIN WITH WHAT PREVIOUS CHECK_REST RETURNED ########################




################# Record detailed data ########################
#if there_is_face:
#CALL THIS FUNCTION WHEN THERE IS A FACE IN THE CAMERA
#SO THAT WORK TIME CAN BE RECORDED
def record_detailed(file_name, am_negative):
    dataFile = open(file_name, 'a')
    dt = datetime.datetime.now()

    #record the data when working
    dataFile.write(str(dt) + ' ')
    if am_negative:
        dataFile.write('negative\n')
    else:
        dataFile.write('positive\n\n')
    dataFile.close()
###############################################################


#CALL THIS FUNCTION WHEN THERE IS NO FACE IN THE CAMERA
#IN ORDER TO TRACK WORKING HOURS
def add_work_time():
    global total_seconds, start_time
    total_seconds += time.time() - start_time
    start_time = time.time()
###############################################################



#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
################## Call it a day ##############################
###### CALL THIS FUNCTION WHEN THE USER PUSH QUIT BUTTON ######
def call_it_a_day(work_time_file_name):
    global total_seconds, give_up
    file = open(work_time_file_name, 'a')
    dt = datetime.datetime.now()

    #record the data when working
    file.write('At ' + str(dt.month) + '/' + str(dt.day) + '/' + str(dt.year) + ' (' + str(datetime.datetime.today().weekday()+1) + ')' + ', ' + 'you worked ' + str(total_seconds) + ' seconds in total in front of the computer.' + '\n')
    file.write('You gave up ' + str(give_up) + ' chances to take a rest today. See you tomorrow!\n\n')
    file.close()
################################################################



#################### Update Give Up ############################
########## CALL WHEN THE USER CHOOSE TO GIVE UP REST############

    ############# BACK TO STRAT BUTTON MEMU ####################

################################################################


################## Take a rest function ########################
def take_a_rest(rest_time):
    t = 0
    no_face = 0
    start = round(time.time())
    length = 0
    for t in range(0, rest_time):
        scheduler.enter(0, 1, imagesnap, ('first',))
        scheduler.run()
        have_face = detect_face(str(round(time.time()*100)))
        if have_face:
            e = round(time.time())
            l = e - start
            return l

        length += time.time() - start
        if length > rest_time:
            return -1

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
################### CALL THIS FUNCTION WHEN USER ASKS FOR DATA CHART ##########################
def view_chart():
    os.system('open -a "Google Chrome" chart.html')



class win3(wx.Frame):
    def __init__(self, parent, id):

        wx.Frame.__init__(self, None, title="Time to Rest",size=(1080,720))
        panel = wx.Panel(self)
        self.txt = wx.StaticText(panel, label="Go")


        
    # def when_closed(self, event):
    #     if not s == input_rest_time:
    #         self.timer.Stop()
    #         pop_win = winWarn()
    #         pop_win.Show()

    # def OnTimer(self, event):
    #     # get current time from computer

    #     if sr == input_rest_time:
    #         self.txt.SetLabel("Rest Time Ends!")
    #         self.timer.Stop()
    #         sr = 0
    #         self.Destroy()

    # def ShowMessage(self, event):
    #     global sr
    #     dial = wx.MessageDialog(None, 'Are you sure to give up REST', 'Question', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
    #     result = dial.ShowModal()
    #     if result == wx.ID_YES:
    #         self.Destroy()
    #         sr = 0
        

class win2(wx.Frame):
    """
    create nice LED clock showing the current time
    """

    def __init__(self, parent, id):
        wx.Frame.__init__(self, None, title="Warning!!",size=(1080,720))
        panel = MainPanel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        
        vbox = wx.BoxSizer(wx.VERTICAL)
        st = wx.StaticText(panel, label='Do you want to give up REST ???',size=(1080,60))
        font1 = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font1.SetPointSize(45)
        st.SetFont(font1)
        vbox.Add(st, flag=wx.RIGHT, border=2)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        buttonYes = wx.Button(panel, label="Yes", size=(150,40))
        buttonNo = wx.Button(panel, label="No",size=(150,40))
        hbox3.Add(buttonYes)
        hbox3.Add(buttonNo)
        vbox.Add(hbox3, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)


        buttonYes.Bind(wx.EVT_BUTTON, self.update_give_up)
        buttonNo.Bind(wx.EVT_BUTTON, self.quit)

        panel.SetSizer(vbox)

    def update_give_up(self, event):
        global give_up
        give_up += 1
        win_ = Mainwin(self, -1)
        win_.Show()
        self.Destroy()

    def quit(self, event):
        self.Destroy()
        win_ = Mainwin(self, -1)
        win_.Show()

    #     pos = wx.DefaultPosition
    #     wx.Frame.__init__(self, parent, id, title='Your Progress...', pos=pos, size=(350, 100))
    #     size = wx.DefaultSize
    #     style = gizmos.LED_ALIGN_CENTER
    #     self.led = gizmos.LEDNumberCtrl(self, -1, pos, size, style)
    #     # default colours are green on black
    #     self.led.SetBackgroundColour("white")
    #     self.led.SetForegroundColour("black")
    #     self.OnTimer(None)
    #     self.timer = wx.Timer(self, -1)
    #     # update clock digits every second (1000ms)
    #     self.timer.Start(1000)
    #     self.Bind(wx.EVT_TIMER, self.OnTimer)
    #     #self.Centre()
    #     self.Bind(wx.EVT_CLOSE, self.ShowMessage)

    # def ShowMessage(self, event):
    #     global s
    #     dial = wx.MessageDialog(None, 'Are you sure to give up WORK', 'Question', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
    #     result = dial.ShowModal()
    #     if result == wx.ID_YES:
    #         self.Destroy()
    #         s = 0
        
    # def OnTimer(self, event):
    #     # get current time from computer
    #     global s

    #     s+=1



    #     if s == input_work_time:
    #         self.timer.Stop()
    #         s=0
    #         self.Hide()
    #         completewin = win3()
    #         completewin.Show()


    #     current = str(datetime.timedelta(seconds=s))
    #     self.led.SetValue(current)

    

class Mainwin(wx.Frame):
    
    def __init__(self, parent, id):
        wx.Frame.__init__(self, None, title="Overworked",size=(1080,720))
            
        self.InitUI()
        self.Centre()
        self.Show()
        
    def InitUI(self):    

        panel = MainPanel(self)

        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(20)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        st = wx.StaticText(panel, label='Hello! Set your target: ',size=(1080,60))
        font1 = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font1.SetPointSize(45)
        st.SetFont(font1)
        hbox.Add(st, flag=wx.RIGHT, border=2)
        vbox.Add(hbox, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label='Work Time: ', size=(200,40))
        st1.SetFont(font)
        hbox1.Add(st1, flag=wx.RIGHT, border=2)
        tc1 = wx.TextCtrl(panel)
        tc1.Bind(wx.EVT_TEXT, self.update_work_time) 
        hbox1.Add(tc1, proportion=1)
        st2 = wx.StaticText(panel, label='sec',size=(500,40))
        st2.SetFont(font)
        hbox1.Add(st2, flag=wx.RIGHT, border=8)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st3 = wx.StaticText(panel, label='Rest Time: ',size=(200,40))
        st3.SetFont(font)
        hbox2.Add(st3, flag=wx.RIGHT, border=2)
        tc2 = wx.TextCtrl(panel)
        tc2.Bind(wx.EVT_TEXT, self.update_rest_time)
        hbox2.Add(tc2, proportion=1)
        st4 = wx.StaticText(panel, label='sec',size=(500,40))
        st4.SetFont(font)
        hbox2.Add(st4, flag=wx.RIGHT, border=8)
        vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        buttonStart = wx.Button(panel, label="Start", size=(300,50))
        buttonHistory = wx.Button(panel, label="View History",size=(300,50))
        hbox3.Add(buttonStart)
        hbox3.Add(buttonHistory)
        vbox.Add(hbox3, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        buttonQuit = wx.Button(panel, label="Call it a day", size=(600,30))
        hbox4.Add(buttonQuit)
        vbox.Add(hbox4, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        

        buttonQuit.Bind(wx.EVT_BUTTON, self.Close)
        buttonStart.Bind(wx.EVT_BUTTON, self.Start)
        buttonHistory.Bind(wx.EVT_BUTTON, self.viewchart)

        panel.SetSizer(vbox)
    
    def viewchart(self, event):
        view_chart()

    def Close(self, event):
        call_it_a_day(work_time_file_name)
    	self.Destroy()

    def Start(self, event):
        if not (input_work_time == -1 or input_rest_time == -1):
            # win = win2(self, -1)
            # win.Show()
            if start_to_work(input_work_time):
                self.Destroy()
            else:
                completewin = win3(self,-1)
                completewin.Show()
                self.Hide()
                
                if take_a_rest(input_rest_time) > 0:
                    win = win2(self, -1)
                    completewin.Destroy()
                    win.Show()
                if take_a_rest(input_rest_time) == -1:
                    # win_ = Mainwin(self, -1)
                    # win_.Show()
                    completewin.Destroy()
                    self.Show()






    def update_work_time(self, event):
    	global input_work_time
    	int_work_time = int(event.GetString())
    	input_work_time = int_work_time

    def update_rest_time(self, event):
    	global input_rest_time
    	int_rest_time = int(event.GetString())
    	input_rest_time = int_rest_time

    def ShowMessage(self):
        print 'oooo'
        global s
        dial = wx.MessageDialog(None, 'Are you sure to give up WORK', 'Question', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        result = dial.ShowModal()
        if result == wx.ID_YES:
            self.Destroy()
            s = 0
class MainPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
 
    #----------------------------------------------------------------------
    def OnEraseBackground(self, evt):
        """
        Add a picture to the background
        """
        # yanked from ColourDB.py
        dc = evt.GetDC()
 
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("back-min.jpg")
        dc.DrawBitmap(bmp, 0, 0)

class SecondPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
 
    #----------------------------------------------------------------------
    def OnEraseBackground(self, evt):
        """
        Add a picture to the background
        """
        # yanked from ColourDB.py
        dc = evt.GetDC()
 
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("rest.jpg")
        dc.DrawBitmap(bmp, 0, 0)

def main():
    app = wx.App()
    Mainwin(None, -1)
    app.MainLoop()   


if __name__ == '__main__':
    main()