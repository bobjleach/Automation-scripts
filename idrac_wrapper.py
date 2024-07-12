#import warnings
import requests
import json
#import re
#import time
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
 

class iDRAC_wrapper:
 	
 	# future use
	# protected data
	#_Read_Timeout = 10 # seconds
	#_Connection_timeout = 10 # seconds
	
	
	# initialize class
	def __init__(self):
	
		# Global variables
		self.Read_Timeout = 10.0        # Time allowed for client to establish
									   # connection to server (seconds).
		self.Connection_timeout = 10.0  # Time it will wait on responce once client
									   # has established connection (seconds).
		self.Max_Retries = 2           # Maximum retries 
		self.BackOff_factor = 1        # used to calculate timout (BackOff_factor)
									   # BackOff_factor * (2 ** ({number_retries} - 1))
	
	def Get_Global_Parms(self):
		
		''' return Global paramters defined below '''
		 
		Return_Results = {"Read_Timeout" : self.Read_Timeout,
		                  "Connection_timeout" : self.Connection_timeout,
		                  "Max_Retries" : self.Max_Retries,
		                  "BackOff_factor" : self.BackOff_factor}
		return Return_Results
	
	def Change_Global_Parms( self, Global_Parms=''):
		'''
		Return - dictionary:
		    ['VALUES_SET'] = True or False
		    ['ERROR_MSG'] = NONE or Error message.
		'''     
		
		Return_Results = {}
				 
		#--------------------------------		 
		# Check if dictionary passed in 
		if not(isinstance(Global_Parms,  dict)):
			# Not dictionary
			
			Return_Results['VALUES_SET'] = False
			Return_Results['ERROR_MSG'] = 'Must pass in a dictionary to set Global paramters. [Read_Timeout], [Connection_timeout], [Max_Retries], [BackOff_factor]'
			return Return_Results
		
		# set flags
		ERROR = False
		ERROR_MSG = "The following Items were not set:"
		
		if 'Read_Timeout' in Global_Parms:
			if isinstance(Global_Parms['Read_Timeout'], (float, int)):
				self.Read_Timeout = float(Global_Parms['Read_Timeout'])
				Read_Timeout_Set = True
			else:
				ERROR_MSG = ERROR_MSG + '\n' +'Dictionary item "Raed_Timeout" must be "int" or "float"'
				ERROR = True
				
		if 'Connection_timeout' in Global_Parms:
			if isinstance(Global_Parms['Connection_timeout'], (float, int)):
				self.Connection_timeout = float(Global_Parms['Connection_timeout'])
				Connectoin_Timeout_Set = True
			else:
				ERROR_MSG = ERROR_MSG + '\n' + 'Dictionary item "Connection_timeout" must be "int" or "float"'
				ERROR = True		
		
		if 'Max_Retries' in Global_Parms:
			if isinstance(Global_Parms['Max_Retries'], (int)):
				self.Max_Retries  = int(Global_Parms['Max_Retries'])
				Max_Retries_Set = True
			else:
				ERROR_MSG = ERROR_MSG + '\n' + 'Dictionary item "Max_Retries" must be "int"'
				ERROR = True	
				
		if 'BackOff_factor' in Global_Parms:
			if isinstance(Global_Parms['BackOff_factor'], (int)):
				self.BackOff_factor  = int(Global_Parms['BackOff_factor'])
				BackOff_factor_Set = True
			else:
				ERROR_MSG = ERROR_MSG + '\n' + 'Dictionary item "BackOff_factor" must be "int"'
				ERROR = True 
	
		if ERROR:
			# error setting some valur occured
			Return_Results['VALUES_SET'] = False
			Return_Results['ERROR_MSG'] = ERROR_MSG
			return Return_Results 
		else:
			Return_Results['VALUES_SET'] = True
			Return_Results['ERROR_MSG'] = "NONE"
			return Return_Results
	
	
	def Redfish_iDRAC( self, Redfish_Paramters="" ):
		""" POST_Password, 
		    Post Redfish/API using idrac user and password 
		    
		    Return - dictionary:
		    ['SUCCESS'] = True or False
		    ['SESSION_RESULTS'] = NONE or results from Post
		    ['ERROR_MSG'] = NONE or error message
		    """
		    
		Return_Results = {}
		
		#--------------------------------		 
		# Check if dictionary passed in 
		if not(isinstance(Redfish_Paramters,  dict)):
			# Not dictionary
			
			Return_Results['SUCCESS'] = False
			Return_Results['SESSION_RESULTS'] = "NONE"
			Return_Results['ERROR_MSG'] = 'Input paramter must be type "dict"'
			return Return_Results
		
		#----------------------------------  
		# Check a required inputs inputs
		
		#*****************	
		if 'iDRAC_IP' in Redfish_Paramters:
			if not(isinstance(Redfish_Paramters['iDRAC_IP'], str )):
				Return_Results['SUCCESS'] = False
				Return_Results['SESSION_RESULTS'] = "NONE"
				Return_Results['ERROR_MSG'] = 'Input dictionary item "iDRAC_IP" must be type "str"'
				return Return_Results
		else:
			Return_Results['SUCCESS'] = False
			Return_Results['SESSION_RESULTS'] = "NONE"
			Return_Results['ERROR_MSG'] = 'Input dictionary item "iDRAC_IP" is not defined'
			return Return_Results
		
		#*********************	
		if 'URL' in Redfish_Paramters:		 
			if not(isinstance(Redfish_Paramters['URL'], str )):
				Return_Results['SUCCESS'] = False
				Return_Results['SESSION_RESULTS'] = "NONE"
				Return_Results['ERROR_MSG'] = 'Input dictionary item "URL" must be type "str"'
				return Return_Results
		else:
			Return_Results['SUCCESS'] = False
			Return_Results['SESSION_RESULTS'] = "NONE"
			Return_Results['ERROR_MSG'] = 'Input dictionary item "URL" is not defined'
			return Return_Results
		
		#************************	
		if 'Valid_Return_Codes' in Redfish_Paramters:	
			if not(isinstance(Redfish_Paramters['Valid_Return_Codes'], list )):
				Return_Results['SUCCESS'] = False
				Return_Results['SESSION_RESULTS'] = "NONE"
				Return_Results['ERROR_MSG'] = 'Input dictionary item "Valid_Return_Codes" must be type "list"'
				return Return_Results
		else:
			Return_Results['SUCCESS'] = False
			Return_Results['SESSION_RESULTS'] = "NONE"
			Return_Results['ERROR_MSG'] = 'Input dictionary item "Valid_Return_Codes" is not defined'
			return Return_Results		
		
		#************************
		if 'Basic_Auth' in Redfish_Paramters:	
			if not(isinstance(Redfish_Paramters['Basic_Auth'], bool )):
				Return_Results['SUCCESS'] = False
				Return_Results['SESSION_RESULTS'] = "NONE"
				Return_Results['ERROR_MSG'] = 'Input dictionary item "Basic_Auth" must be type "bool"'
				return Return_Results
		else:
			Return_Results['SUCCESS'] = False
			Return_Results['SESSION_RESULTS'] = "NONE"
			Return_Results['ERROR_MSG'] = 'Input dictionary item "Basic_Auth" is not defined'
			return Return_Results
		
		  
		#***************************
		if 'Method'	in Redfish_Paramters:
			if (isinstance(Redfish_Paramters['Method'], str )):
				if not (Redfish_Paramters['Method'] == "GET" or	\
					    Redfish_Paramters['Method'] == "POST" or \
						Redfish_Paramters['Method'] == "PATCH" or \
						Redfish_Paramters['Method'] == "DELETE"):
					Return_Results['SUCCESS'] = False
					Return_Results['SESSION_RESULTS'] = "NONE"
					Return_Results['ERROR_MSG'] = 'Method must be "GET", "POST", "PATCH" or "DELETE"'
					return Return_Results		
								
			else:	
				Return_Results['SUCCESS'] = False
				Return_Results['SESSION_RESULTS'] = "NONE"
				Return_Results['ERROR_MSG'] = 'Input dictionary item "Method" must be type "string"'
				return Return_Results
		else:
			Return_Results['SUCCESS'] = False
			Return_Results['SESSION_RESULTS'] = "NONE"
			Return_Results['ERROR_MSG'] = 'Input dictionary item "Method" is not defined'
			return Return_Results


		#*****************************
		# Check for Body
		if Redfish_Paramters['Method'] != "GET":
			if not 'Body' in Redfish_Paramters:
				Return_Results['SUCCESS'] = False
				Return_Results['SESSION_RESULTS'] = "NONE"
				Return_Results['ERROR_MSG'] = 'Input Body must be defined"'
				return Return_Results


		
		Session_URL = 'https://%s%s' %(Redfish_Paramters['iDRAC_IP'], Redfish_Paramters['URL'])
			 
		
		# set up retry and backoff
		retry_strategy = Retry(
			total = self.Max_Retries, # Max number of retires
			backoff_factor = self.BackOff_factor,
			status_forcelist=[],  
	    )
		
		
		# Create an HTTP adapter with the retry strategy and mount it to session
		adapter = HTTPAdapter(max_retries=retry_strategy)
 
		# Create a new session object
		session = requests.Session()
		session.mount('https://', adapter)
		
				
		try:
			# Get with no Basic Auth
			if ( not Redfish_Paramters['Basic_Auth'] ) and Redfish_Paramters['Method'].upper() == "GET": 	   
				 	 
				Session_info = session.get( Session_URL,
											headers = Redfish_Paramters['Headers'],
											verify = False,
											timeout= (self.Connection_timeout, self.Read_Timeout ) )						
					 
			# Get with no Basic Auth	 
			elif Redfish_Paramters['Basic_Auth'] and Redfish_Paramters['Method'] == "GET":
				
				 
				Session_info = session.get( Session_URL,
											headers = Redfish_Paramters['Headers'],
											auth = ( Redfish_Paramters['User'], Redfish_Paramters['Password'] ),
											verify = False,
											timeout= (self.Connection_timeout, self.Read_Timeout ) )	 
					 
			# Post with no Basic Auth
			elif ( not Redfish_Paramters['Basic_Auth'] ) and Redfish_Paramters['Method'].upper() == "POST": 	   
				 	 
				Session_info = session.post( Session_URL,
											headers = Redfish_Paramters['Headers'],
											verify = False,
											data = json.dumps(Redfish_Paramters['Body']),
											timeout= (self.Connection_timeout, self.Read_Timeout ) )	    
			
			
			# Post with Basic Auth
			elif Redfish_Paramters['Basic_Auth']  and Redfish_Paramters['Method'].upper() == "POST": 	   
				 	 
				Session_info = session.post( Session_URL,
											headers = Redfish_Paramters['Headers'],
											auth = ( Redfish_Paramters['User'], Redfish_Paramters['Password'] ),
											verify = False,
											data = json.dumps(Redfish_Paramters['Body']),
											timeout= (self.Connection_timeout, self.Read_Timeout ) )
											
											
			# Delete no basic
			elif ( not Redfish_Paramters['Basic_Auth'] ) and Redfish_Paramters['Method'].upper() == "DELETE": 	   
				 	 
				Session_info = session.delete( Session_URL,
											headers = Redfish_Paramters['Headers'],
											verify = False,
											data = json.dumps(Redfish_Paramters['Body']),
											timeout= (self.Connection_timeout, self.Read_Timeout ) )
											
			# Delete with Bsaic
			elif Redfish_Paramters['Basic_Auth'] and Redfish_Paramters['Method'].upper() == "DELETE": 	   
				 	 
				Session_info = session.delete( Session_URL,
											headers = Redfish_Paramters['Headers'],
											auth = ( Redfish_Paramters['User'], Redfish_Paramters['Password'] ),
											verify = False,
											data = json.dumps(Redfish_Paramters['Body']),
											timeout= (self.Connection_timeout, self.Read_Timeout ) )
											
			# Patch no basic
			elif ( not Redfish_Paramters['Basic_Auth'] ) and Redfish_Paramters['Method'].upper() == "PATCH": 	   
				 	 
				Session_info = session.patch( Session_URL,
											headers = Redfish_Paramters['Headers'],
											verify = False,
											data = json.dumps(Redfish_Paramters['Body']),
											timeout= (self.Connection_timeout, self.Read_Timeout ) )	
											
			# Patch with basic
			elif Redfish_Paramters['Basic_Auth'] and Redfish_Paramters['Method'].upper() == "PATCH": 	   
				 	 
				Session_info = session.patch( Session_URL,
											headers = Redfish_Paramters['Headers'],
											auth = ( Redfish_Paramters['User'], Redfish_Paramters['Password'] ),
											verify = False,
											data = json.dumps(Redfish_Paramters['Body']),
											timeout= (self.Connection_timeout, self.Read_Timeout ) )															
			
			else:
				# Unkown error  
			
				Return_Results['SUCCESS'] = False
				Return_Results['SESSION_RESULTS'] = "NONE"
				Return_Results['ERROR_MSG'] = "Unknown method:" + Redfish_Paramters['Method'].upper()
				return Return_Results
			
			# for debug
			#raise requests.exceptions.RequestException
		except requests.exceptions.Timeout:
			#---------------------
			# requests timed out
			#---------------------
			 
			# Tried Max times and failed, return error
			  
			Return_Results['SUCCESS'] = False
			Return_Results['SESSION_RESULTS'] = "NONE"
			Return_Results['ERROR_MSG'] = "Requests Timeout Occured"
			return Return_Results
			
		except requests.exceptions.RequestException as e:
			#----------------------------------
			# an unkown requests error occured
			#----------------------------------
			  
			# Tried Max times and failed, return error
			Error_msg = "Connection Error: {0}".format(e) 
			Return_Results['SUCCESS'] = False
			Return_Results['SESSION_RESULTS'] = "NONE"
			Return_Results['ERROR_MSG'] = Error_msg
			return Return_Results
		
		except Exception as e:
			# runtime error
			 
			Error_msg = "Error: {0}".format(e) 
			Return_Results['SUCCESS'] = False
			Return_Results['SESSION_RESULTS'] = "NONE"
			Return_Results['ERROR_MSG'] = Error_msg
			return Return_Results
		
				 		
		if Session_info.status_code in Redfish_Paramters['Valid_Return_Codes']:
			#----------------------
			# Got Valid Return code
			#----------------------
			 	
			Return_Results['SUCCESS'] = True
			Return_Results['SESSION_RESULTS'] = Session_info
			Return_Results['ERROR_MSG'] = "NONE"
			return Return_Results	
				
				
		else:
			#--------------------- 
			# Invalid return code  
			#--------------------- 
			 
			# Tried Max times and failed, return error
			Error_msg = "Invalid return code = " + str(Session_info.status_code)
			Return_Results['SUCCESS'] = False
			Return_Results['SESSION_RESULTS'] = Session_info
			Return_Results['ERROR_MSG'] = Error_msg
			return Return_Results								 
			
				

	
	
