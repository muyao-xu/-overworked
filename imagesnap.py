import httplib, urllib, base64
import json
import datetime
import time
import sched, os


############   Track working time of a day  ###############
#Global Variables used for # Track working time of a day #
global start_time
global total_seconds 
global work_time_file_name
global give_up
global flag

total_seconds = 0
#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
work_time_file_name = 'file_name'
give_up = 0
flag = True

scheduler = sched.scheduler(time.time, time.sleep)


def imagesnap(a='default'):
	os.system('imagesnap -w 1 snapshot.jpg')

def work(work_time):
	if falg:
		start_time = time.time()
	flag = False

	t = 0
	no_face = 0
	start = round(time.time())
	length = 0
	for t in range(0, work_time):
		scheduler.enter(0, 1, imagesnap,('first',))
		scheduler.run()
		have_face = detect_face(str(round(time.time()*100)))
		if have_face:
			no_face = 0
		if not have_face:
			no_face += 1
		if no_face == 2:
		##################### DISPLAY START MEMU #####################
		#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
			# TRUE for restart working
			return True

		length += time.time() - start
		if length >= work_time:
			# FALSE for need to take a rest
			return False


		

def detect_face(num):	
	from azure.storage.blob import BlockBlobService
	block_blob_service = BlockBlobService(account_name='snapshot2', account_key='wd6G16qs04fXYcO5qMZ6n1IrdVxvNwJ0wuC3ludTZ7AePUqe9XE+z1BS3b/fbiCm/vqrqnWqEAvyKeC6iYaEkQ==')

	# from azure.storage.blob import PublicAccess
	# block_blob_service.create_container('new', public_access=PublicAccess.Container)
	
	savename = 'myfile' + str(num)
	saveurl = 'https://snapshot2.blob.core.windows.net/new/myfile' + str(num)


	from azure.storage.blob import ContentSettings
	block_blob_service.create_blob_from_path(
		'new',
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
	if there_is_face
		j = json.loads(data)
		width = j['faceRectangle']['width']
		if width > 500:
			#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
			print distance_remind
	#############################################

	
	if there_is_face:
		#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
		record_detailed('put_file_name_here', iamnegative)
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
check_rest = take_a_rest(rest_time)
################# IF RETURN FALSE ############################################
####### CALL START_TI_WORK #################

############## IF CHECK_REST RETURNS -1, continue the timer until times up. Call start_to_work as the following #################
######### IF CHECK_REST > 1, ######### POP UP A WINDOW ASK IF WANT TO GIVE UP ###########
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
if answer yes to give up:
	update_give_up()
	start_to_work(work___time)

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
	total_seconds += time.time() - start_time
	start_time = time.time()
###############################################################



#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
################## Call it a day ##############################
###### CALL THIS FUNCTION WHEN THE USER PUSH QUIT BUTTON ######
def call_it_a_day(work_time_file_name):
	file = open(work_time_file_name, 'a')
	dt = datetime.datetime.now()

	#record the data when working
	file.write('At ' + str(dt.month) + '/' + str(dt.day) + '/' + str(dt.year) + ' (' + str(datetime.datetime.today().weekday()+1) + ')' + ', ' + 'you worked ' + str(total_seconds) + ' seconds in total in front of the computer.' + '/n')
	file.write('You gave up ' + give_up + ' chances to take a rest today. See you tomorrow!\n\n')
	file.close()
################################################################



#################### Update Give Up ############################
########## CALL WHEN THE USER CHOOSE TO GIVE UP REST############
def update_give_up():
	give_up += 1
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
			l = e - a
			return l

		length += time.time() - start
		if length > rest_time:
			return -1

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
################### CALL THIS FUNCTION WHEN USER ASKS FOR DATA CHART ##########################
def view_chart():
	os.system('open -a "Google Chrome" chart.html')

