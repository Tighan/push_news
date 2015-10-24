import time
def printtime():
	ISOTIMEFORMAT="%Y-%m-%d %X"
	time_now=time.strftime( ISOTIMEFORMAT, time.localtime() )
	print(time_now)
printtime()