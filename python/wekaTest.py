from weka.core.converters import Loader
import weka.core.jvm as jvm

jvm.start()


data_dir = "./Gestures/"

loader = Loader(classname="weka.core.converters.ArffLoader")
data = loader.load_file(data_dir + "iris.arff")
data.class_is_last()

print(data)