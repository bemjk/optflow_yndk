
CFLAGS = `pkg-config opencv --libs --cflags`
CXXFLAGS = `pkg-config opencv --libs --cflags`


EXECS = gpc_evaluate gpc_train dis_opticalflow motempl optical_flow_evaluation pcaflow_demo simpleflow_demo


all: $(EXECS)

gpc_train: gpc_train.cpp
	c++  $? -I /usr/local/include  -o $@ -L /usr/local/lib -lopencv_core -lopencv_optflow

gpc_evaluate: gpc_evaluate.cpp
	c++  $? -I /usr/local/include  -o $@ -L /usr/local/lib -lopencv_optflow -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_imgproc


$@: $@.cpp
	c++  $? -I /usr/local/include  -o $@ -L /usr/local/lib -lopencv_optflow -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_imgproc

clean:
	rm -f $(EXECS)