mpirun -np 64 -bind-to none -map-by slot -H ...
resnet50_op_auto 
	-blueprint full_model_v1.5.txt 
	-configBase ./b512_nhwc_1.5 
	-isFp16 1 
	-nhwc 1 
	-loops 3510 
	-reportInterval 39 
	-saveInterval 39 
	-reserveMemMB 5120 
	-dataDir /data/imagenet 
	-distribute 1 
	-cycleLength 1 
	-useLars 1 
	-warmupEpochs 15 
	-learningRate 0.1953125 
	-cosLR "3510,0.0" 
	-labelSmoothing 0.1 
	-weightDecay 0.00016 
	-evalSchedule "1:156,3276:39" 
	-stopThreshold 0.759 
	-mlperf 1 
