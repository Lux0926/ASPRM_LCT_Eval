# watch production of ckpts, convert to hf, and do evaluation
set -x
cd /data/oce/oce/eval

export MKL_THREADING_LAYER=GNU
export WEBHOOK_URL='' # sft bot

CONFIG_PATH=configs/sft.json # 配置文件
INTERVAL=60 # 监控文件夹是否有新ckpt产出的间隔
FEISHU_MSG=1 # 0为不发送飞书信息，1为发送飞书信息

source /home/liurb/anaconda3/bin/activate vllm
python run.py --config_path $CONFIG_PATH --interval $INTERVAL --feishu_msg $FEISHU_MSG