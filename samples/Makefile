
CXX = c++ -Ofast
CFLAGS = `pkg-config opencv --libs --cflags`
CXXFLAGS = -I /usr/local/include 
LDLIBS =  -L /usr/local/lib -lopencv_optflow -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_imgproc -lopencv_videoio -lopencv_video


EXECS = gpc_evaluate gpc_train dis_opticalflow motempl optical_flow_evaluation pcaflow_demo simpleflow_demo

PYFILES = gpc_train_middlebury.py gpc_evaluate_sintel.py gpc_train_sintel.py motempl.py optical_flow_benchmark.py

all: $(EXECS) $(PYFILES)
	cp -f $(EXECS) $(PYFILES) $(HOME)/bin

gpc_train: gpc_train.cpp 
	$(CXX)  $@.cpp -I /usr/local/include  -o $@ -L /usr/local/lib -lopencv_core -lopencv_optflow

gpc_evaluate: gpc_evaluate.cpp
	$(CXX)  $? -I /usr/local/include  -o $@ -L /usr/local/lib -lopencv_optflow -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_imgproc

clean:
	rm -f $(EXECS)

depend:
	makedepend $(CXXFLAGS) *.cpp
