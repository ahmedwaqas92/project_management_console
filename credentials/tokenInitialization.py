import os

module_dir = os.path.dirname(os.path.abspath(__file__))
textfile_path = os.path.join(module_dir, 'token.txt')

class tokenInitialization:													#Building the necessary Token Class
	def __init__(self, startline, endline):									#Initializing the Function
		f = open(textfile_path, 'r')										#Reading the Text Token File for Client ID
		self.value = f.readlines()[startline:endline]						#Reading Lines and Adding to List
		self.value = str(self.value[0])										#Making the Required List as a String
		self.value = self.value[self.value.find(': "'):]					#Removing every string before ': "' character
		self.value = self.value[self.value.find('"'):]						#Removing every string before '"' character
		self.value = self.value.strip()										#Stripping Leading and Trailing White Spacing
		self.value = self.value[1:-1]										#Removing the Leading and Trailing quotation marks by slicing string using Leading and Trailing Index
		f.close()															#Closing the Token File


clientId = tokenInitialization(1,2)
clientSecret = tokenInitialization(2,3)
token = tokenInitialization(3,4)



# print(clientId.value)
# print(clientSecret.value)
# print(token.value)
