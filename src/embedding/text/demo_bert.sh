export BERT_BASE_DIR=/data/Cross_Cultural_Analysis/embedding/text/bert

python ./bert/extract_features.py \
  --input_file=./demo/zh.txt \
  --output_file=./demo/out_zh.jsonl \
  --vocab_file=$BERT_BASE_DIR/weights/multi_cased_L-12_H-768_A-12/vocab.txt \
  --bert_config_file=$BERT_BASE_DIR/weights/multi_cased_L-12_H-768_A-12/bert_config.json \
  --init_checkpoint=$BERT_BASE_DIR/weights/multi_cased_L-12_H-768_A-12/bert_model.ckpt \
  --layers=-1 \
  --max_seq_length=64 \
  --batch_size=4
