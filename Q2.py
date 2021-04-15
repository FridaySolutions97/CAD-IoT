import textract
import re
import argparse
import pandas as pd


def extractToCsv(files, csv):
	# Extract text from pdf using textract
	text = textract.process(files).decode("utf-8")

	# adjustment
	text = '\x0c' + text
	text = re.sub(r'\r', '', text)
	text = re.sub(r'\x0c', '\n>>>\n', text) # indicate a different page
	text = re.sub(r':', '\n', text)
	lines = text.splitlines()
	while("" in lines) : 
		lines.remove("") 
	
	# Add the page number to the first item of each page
	idx_page = 0
	page = 0
	for idx, line in enumerate(lines):
		if line==">>>":
			try:
				for i in range(idx, 0, -1):
					if lines[i].isnumeric():
						lines[idx_page]+=lines[i]
						idx_page = idx
						page+=1
						break
			except:
				pass

	# Get the datas
	page_now = 0 
	datas = []
	searchCause = False
	data = {"Description":'', "Possible_Root_cause":[], "Page_number":''}
	for idx, line in enumerate(lines):
		if ">>>" in line:
			page_now = line[3:]
		elif line == "Description":
			data["Description"] = lines[idx+1]
		elif line == "Possible Root":
			searchCause=True
		elif line == "Troubleshooting":
			searchCause = False
			data["Page_number"] = page_now
			datas.append(data)
			data = {"Description":'', "Possible_Root_cause":[], "Page_number":''}
		elif searchCause and line != 'cause':
			data["Possible_Root_cause"].append(line)
	
	# Filtering unwanted text and tidy up the output
	for data in datas:
		new = []
		for i, each in enumerate(data["Possible_Root_cause"]):
			stripped = re.sub("([0-9]+.)", "", each).strip()
			if len(stripped)>0:
				try:
					if (stripped[0].isupper() or stripped[0].isdigit()) and new[-1][-1]=='.':
						new.append(stripped)
					else:
						new[-1] += ' ' + stripped
				except:
					new.append(stripped)
		data["Possible_Root_cause"] = new

	# Change to dataframe and convert it to csv file
	df = pd.DataFrame(datas)
	df.to_csv(csv, index=False)
	print("Done.")

if __name__ == "__main__":
	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--input", required=True,
		help="path to input pdf")
	ap.add_argument("-o", "--output", required=True,
		help="path to output csv")
	args = vars(ap.parse_args())

	extractToCsv(args['input'], args['output'])


