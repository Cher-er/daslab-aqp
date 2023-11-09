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
     "input_file": "your_dataset_path/dataset.csv",
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
   > 该案例有两块GPU，且优先使用第二块GPU（第一块GPU显存不足），因此设置为 `"gpus": "[1,0]"`

   注意：数据集csv文件需要带表头，且属性名需加后缀 `_n` 或 `_c`，表示数值列（numerical columns）或分类列（categorical columns）。

   以下为一个合法数据集的前五行示例：

   ```csv
   year_data_c,unique_carrier_c,origin_c,origin_state_abr_c,dest_c,dest_state_abr_c,dep_delay_n,taxi_out_n,taxi_in_n,arr_delay_n,air_time_n,distance_n
   2001,AA,DFW,TX,MCI,MO,86.0,13.0,3.0,84.0,80.0,460.0
   2011,B6,JFK,NY,BTV,VT,-9.0,20.0,4.0,-16.0,44.0,267.0
   2013,US,PIT,PA,PHX,AZ,-11.0,13.0,5.0,-54.0,232.0,1814.0
   2012,DL,TPA,FL,ATL,GA,3.0,15.0,13.0,6.0,70.0,406.0
   ```

3. 运行 `do.py` 脚本

   ```sh
   python do.py
   ```

   执行成功后，在 your_out_path 目录下会生成 model.pt 文件，即 VAE 模型的参数

4. 修改 config/main.json

   ```json
   {
     "vae": {
       "train": false,
       "gen": true
     }
   }
   ```

   > 表示执行 VAE 的生成过程

5. 运行 do.py 脚本

   ```sh
   python do.py
   ```

   执行成功后，在 your_out_path 目录下会生成 samples_1000.csv 文件，后缀表示样本数量，由 config/vae.json 中的参数 num_samples 控制。



## 参数设置

- model_name：随便写
- input_file：数据集路径
- output_dir：输出文件路径
- data_output_dir：输出文件路径
- batch_size：神经网络训练过程中的批处理大小
- latent_dim：控制神经网络结构
- neuron_list：控制神经网络结构
- epochs：神经网络训练次数
- log_interval：本意应该是控制模型训练时的日志输出间隔，但目前代码没用到
- rejection
- num_samples：生成数据的样本数量
- seed：随机种子（设置numpy和torch模块的随机种子）
- gpus：配置GPU



## 输出文件
- output_dir/model_state: 保存模型训练过程中的中间状态（每10个epoch及最后一个epoch保存一次）
- output_dir/loss.pkl: 保存模型训练过程中的所有损失值（每10个epoch及最后一个epoch保存一次）
- output_dir/t-val.pkl: 保存t值（每10个epoch及最后一个epoch保存一次）
- output_dir/time_taken.pkl: 保存模型训练所用时间（每10个epoch及最后一个epoch保存一次）
- output_dir/loss.png: 保存损失值变化的折线图（每10个epoch及最后一个epoch保存一次）
- output_dir/model.pt: 保存模型训练过程中的损失值最低的模型参数
- output_dir/samples_xxx.csv: 保存模型生成的样本数据
- data_output_dir/data.pkl: 读取数据后，存储训练集、测试集
- data_output_dir/exp_info: 存储数据集的某些统计信息



## 问题

1. vae/train.py中，是否需要sample(1000000)?
2. vae/train.py中，没有使用测试集。
3. config/vae.json中，参数model_name的作用未知。
4. config/vae.json中，参数rejection的作用未知。