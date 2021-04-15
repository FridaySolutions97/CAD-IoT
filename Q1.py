from jcopml.utils import save_model, load_model
import json
import argparse
import pandas as pd

pump_faulty_predictor = load_model("model/pump_faulty.pkl")

def predict_pump_faulty(sensor_data):
	X_pred = pd.DataFrame([sensor_data], columns=['CP1T1', 'CP1T2', 'CP2T1', 'CP2T2', 'CP1V1', 'CP1V2', 'CP2V1', 'CP2V2'])
	faulty = pump_faulty_predictor.predict(X_pred)[0]
	print("PUMP FAULTY!") if faulty else print("Pump is fine")
	return faulty

if __name__ == "__main__":
	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--input", required=True,
		help="path to input json file")
	args = vars(ap.parse_args())

	f = open(args['input'])
	data = json.load(f)
	faulty = predict_pump_faulty(data)
	print(">>> Pump status:", faulty)