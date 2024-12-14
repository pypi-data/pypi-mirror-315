import pickle
import datetime

if __name__ == "__main__":
  bytes = pickle._dumps(datetime.datetime.now())
  time = pickle._loads(bytes)
  print(time)
