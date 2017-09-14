
To test and modify the Optical Flow Algorithms in opencv_contrib
==============================================

To use this repository instead of original optflow,

```
$ cd opencv_contrib/modules
$ rm -rf optflow
$ https://github.com/yongduek/optflow_yndk.git optflow
```

Then do the same process to install opencv.
For example, in a ubuntu system
```
$ cmake -DCMAKE_BUILD_TYPE=Debug -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules/ ..
```
will build opencv package for debugging.

If you install debug-allowed version, then you may step into the opencv source code (e.g. in the Visual Studio debug run).
