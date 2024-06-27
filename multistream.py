import streamer

s=streamer.Streamer()

s.channel("NTPC.NS")
s.start_stream()
while(1):
	data=s.get_data()
	if(data):
		print(data)
		data=None
