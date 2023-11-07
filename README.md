# VAE
## 使用示例
1. 修改 config/main.json

   ```json
   {
     "vae": {
       "train": true,
       "gen": false
     }
   }
   ```

   > 表示执行 VAE 的训练过程

2. 修改 config/vae.json

   ```json
   {
     "model_name": "flights",
     "input_file": "your_dataset_path/flights.csv",
     "output_dir": "your_out_path",
     "data_output_dir": "your_data_out_path",
     "batch_size": 64,
     "latent_dim": 64,
     "neuron_list": 200,
     "epochs": 10,
     "log_interval": 25,
     "rejection": 0,
     "num_samples": 1000,
     "seed": 42,
     "gpus": "[1,0]"
   }
   ```

   > 若主机只有一块GPU，则设置为 `"gpus": "0"`；
   >
   > 该案例有两块GPU，且优先使用第二块GPU，因此设置为 `"gpus": "[1,0]"`

3. 运行 `do.py` 脚本

   ```sh
   python do.py
   ```

4. 



## 输出文件
- output_dir/model_state: 保存模型训练过程中的中间状态（每10个epoch及最后一个epoch保存一次）
- output_dir/loss.pkl: 保存模型训练过程中的所有损失值（每10个epoch及最后一个epoch保存一次）
- output_dir/t-val.pkl: 保存t值（每10个epoch及最后一个epoch保存一次）
- output_dir/time_taken.pkl: 保存模型训练所用时间（每10个epoch及最后一个epoch保存一次）
- output_dir/loss.png: 保存损失值变化的折线图（每10个epoch及最后一个epoch保存一次）
- output_dir/model.pt: 保存模型训练过程中的损失值最低的模型参数
- data_output_dir/data.pkl: 读取数据后，存储训练集、测试集
- data_output_dir/exp_info: 存储数据集的某些统计信息





# 问题
1. vae/train.py中，是否需要sample(1000000)?
2. vae/train.py中，没有使用测试集。