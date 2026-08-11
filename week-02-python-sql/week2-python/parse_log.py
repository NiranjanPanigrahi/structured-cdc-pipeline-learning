with open("sample.log") as f:
	for line in f:
		line = line.strip()
		parts = line.split(" ")
		print(parts)
		break


