Running the REVISION renderer requires [blenderproc](https://github.com/DLR-RM/BlenderProc)

Some sample object and background assets are already available.

The floor assets are avaiable [here](https://www.dropbox.com/scl/fo/qqhwmtz2g4jj215czq4f4/AAyRyCy-zp4-NsfZ4Axb-0I?rlkey=7miycqs6jz5t0gd4ubsowcrx7&dl=0). Once downloaded please put the floor asset files into floor/ .

Run ``sh launch_sample.sh`` to obtain some sample synthetic REVISION reference images in hdf5 format. You may visualize them with ``
blenderproc vis hdf5 output/0.hdf5``.