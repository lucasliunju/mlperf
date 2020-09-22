python train.py \
--batch_size=32 \
--weight_decay=5e-4 \
--step_per_epoch=312 \
--epoch_end=25 \
--epoch_size=20 \
--lr_mode=cos \
--frequency=312 \
--eval_batch_size=200 \
--eval_interval=4 \
--loss_scale=128 \
--damping_init=0.7 \
--lr_init=0.47 \
--damping_decay=0.3 \
--warmup_epoch=5