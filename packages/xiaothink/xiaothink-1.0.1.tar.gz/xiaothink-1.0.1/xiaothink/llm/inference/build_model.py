import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
from tensorflow.keras.layers import Input, Embedding, GRU, Dense, Dropout  
from tensorflow.keras.models import Model  
from tensorflow.keras.layers import Multiply,Attention
from tensorflow.keras.layers import Bidirectional
from tensorflow.keras.layers import LayerNormalization
from tensorflow.keras.layers import Add,MultiHeadAttention
import gc
def ct():
    gc.collect()
tf.config.run_functions_eagerly(True)
dic={
40.231:[int(1024),{'rnn_units':int(2048),'embed_q':0.6,}, 512],#推理时需要500M内存
         }
from tensorflow.keras.layers import Embedding, GRU, Dropout, Dense, AdditiveAttention, LayerNormalization


class CustomMultiHeadAttentionGRUCell(tf.keras.layers.Layer):
    def __init__(self, units, attention_units, num_heads=16, activation='tanh', recurrent_activation='sigmoid', use_bias=True):
        super(CustomMultiHeadAttentionGRUCell, self).__init__()
        self.units = units
        self.attention_units = attention_units
        self.num_heads = num_heads
        assert attention_units % num_heads == 0, "Attention units must be divisible by the number of heads"
        self.depth = attention_units // num_heads
        self.activation = tf.keras.activations.get(activation)
        self.recurrent_activation = tf.keras.activations.get(recurrent_activation)
        self.use_bias = use_bias

        # GRU门控权重
        self.kernel_z = self.add_weight(shape=(units, units * 1), initializer='glorot_uniform', name='kernel_z')
        self.kernel_r = self.add_weight(shape=(units, units * 1), initializer='glorot_uniform', name='kernel_r')
        self.kernel_h = self.add_weight(shape=(units, units * 1), initializer='glorot_uniform', name='kernel_h')
        
        # 复查门权重
        self.kernel_rev = self.add_weight(shape=(units, units), initializer='glorot_uniform', name='kernel_rev')

        # 语法联系门
        self.kernel_scg = self.add_weight(shape=(units * 2 + attention_units, units), initializer='glorot_uniform', name='kernel_scg')


        # 多头注意力机制相关权重
        self.wq_att = self.add_weight(shape=(units, attention_units), initializer='glorot_uniform', name='wq_att')
        self.wk_att = self.add_weight(shape=(units, attention_units), initializer='glorot_uniform', name='wk_att')
        self.wv_att = self.add_weight(shape=(units, attention_units), initializer='glorot_uniform', name='wv_att')
        self.u_att = self.add_weight(shape=(attention_units, num_heads), initializer='glorot_uniform', name='u_att')

        if use_bias:
            self.bias_z = self.add_weight(shape=(units * 1,), initializer='zeros', name='bias_z')
            self.bias_r = self.add_weight(shape=(units * 1,), initializer='zeros', name='bias_r')
            self.bias_h = self.add_weight(shape=(units,), initializer='zeros', name='bias_h')
            self.bias_att = self.add_weight(shape=(num_heads,), initializer='zeros', name='bias_att')
            self.bias_rev = self.add_weight(shape=(units,), initializer='zeros', name='bias_rev')  # 新增复查门偏置
            self.bias_scg = self.add_weight(shape=(units,), initializer='zeros', name='bias_scg')


        self.layernorm_1 = tf.keras.layers.LayerNormalization()
        self.layernorm_2 = tf.keras.layers.LayerNormalization()

    def attention(self, h_tm1, h_all):
        # 多头注意力机制
        Q = tf.matmul(h_tm1, self.wq_att)
        K = tf.matmul(h_all, self.wk_att)
        V = tf.matmul(h_all, self.wv_att)

        # 形状调整以便进行多头注意力计算
        Q = tf.reshape(Q, [-1, self.num_heads, self.depth])
        K = tf.reshape(K, [-1, self.num_heads, self.depth])
        V = tf.reshape(V, [-1, self.num_heads, self.depth])

        # 计算注意力分数并应用softmax
        scores = tf.matmul(Q, K, transpose_b=True) / tf.math.sqrt(tf.cast(self.depth, tf.float32))
        att_weights = tf.nn.softmax(scores, axis=-1)

        # 上下文向量计算
        context_vector = tf.matmul(att_weights, V)
        context_vector = tf.reshape(context_vector, [-1, self.attention_units])

        return context_vector

    def call(self, inputs, states):
        h_tm1, h_all = states
        context_vector = self.attention(h_tm1, h_all)

        # 残差连接和层归一化
        h_tm1_res = self.layernorm_1(h_tm1 + context_vector)

        # 新增：复查门计算
        rev_gate = self.recurrent_activation(tf.matmul(inputs, self.kernel_rev) + tf.matmul(h_tm1_res, self.kernel_rev) + self.bias_rev)
        context_adjusted = rev_gate * context_vector

        # GRU更新，使用调整后的上下文向量
        z = self.recurrent_activation(tf.matmul(inputs, self.kernel_z) + tf.matmul(h_tm1_res, self.kernel_z) + self.bias_z)
        r = self.recurrent_activation(tf.matmul(inputs, self.kernel_r) + tf.matmul(h_tm1_res, self.kernel_r) + self.bias_r)
        rh_tm1 = r * h_tm1_res
        hh = self.activation(tf.matmul(inputs, self.kernel_h) + tf.matmul(rh_tm1, self.kernel_h) + self.bias_h)
        h = z * h_tm1_res + (1 - z) * hh

        # 融合复查门调整后的上下文信息
        h = h + context_adjusted
        
        '''
        # 最终层归一化
        h = self.layernorm_2(h)

        return h, [h, h_all]
        '''
        
        # 新增：计算语法联系门
        scg_input = tf.concat([inputs, h_tm1_res, context_vector], axis=-1)
        scg = self.recurrent_activation(tf.matmul(scg_input, self.kernel_scg) + self.bias_scg)

        # SCG调整最终隐藏状态，确保语法和内容连贯性
        h_adjusted = scg * h + (1 - scg) * h_tm1_res  # 调整输出以反映语法和连贯性的考量

        # 最终层归一化（调整后）
        h_final = self.layernorm_2(h_adjusted)

        return h_final, [h_final, h_all]

    def get_initial_state(self, inputs=None, batch_size=None, dtype=None):
        return [tf.zeros([batch_size, self.units], dtype=dtype),
                tf.zeros([batch_size, self.units], dtype=dtype)]

    @property
    def state_size(self):
        return [self.units, self.units]
    
class AGRU(tf.keras.layers.RNN):
    def __init__(self, units, attention_units, return_sequences=True, **kwargs):
        cell = CustomAttentionGRUCell(units, attention_units)
        super(AGRU, self).__init__(cell, return_sequences=return_sequences, **kwargs)

    @tf.function
    def call(self, inputs, states=None, training=None, mask=None):
        #tf.config.run_functions_eagerly(True)

        tf.compat.v1.enable_eager_execution()
        #print("AGRU Eager execution:", tf.executing_eagerly())
        if not tf.executing_eagerly():
            return inputs#tf.zeros(shape=(1, 6670))
        
        if states is None:
            print('None States')
            initial_states = [tf.zeros([tf.shape(inputs)[0], self.cell.units]),  # Initial hidden state
                              tf.zeros([tf.shape(inputs)[0], 1, self.cell.units])]  # Initial history placeholder
        else:
            initial_states = states
        tf.compat.v1.enable_eager_execution()
        care=super().call(inputs, training=training, mask=mask)
        try:outputs,states = care
        except:
            print('no states')
            outputs = care
        return outputs, states if self.return_sequences else outputs


    
class AGRU_ADD(tf.keras.layers.RNN):
    def __init__(self, units, attention_units, return_sequences=True, **kwargs):
        cell = CustomAttentionGRUCell(units, attention_units)
        super(AGRU_ADD, self).__init__(cell, return_sequences=return_sequences, **kwargs)
        self.gru = tf.keras.layers.GRU(units, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform')

    @tf.function
    def call(self, inputs, states=None, training=None, mask=None):
        # 获取GRU层的输出
        o1 = self.gru(inputs)
        if not tf.executing_eagerly():
            return inputs#tf.zeros(shape=(1, 6670))
        # 确保使用eager模式执行，尽管tf.function装饰器已经隐式地控制了执行模式
        # 注意：这里不再需要手动启用eager执行，因为tf.function会根据环境自动处理
        
        # 使用super()调用自定义RNN的call方法来获取CustomAttentionGRUCell的输出
        if states is None:
            initial_states = [
                tf.zeros([tf.shape(inputs)[0], self.cell.units]),
                tf.zeros([tf.shape(inputs)[0], 1, self.cell.units])
            ]
        else:
            initial_states = states
        tf.compat.v1.enable_eager_execution()
        care_output = super().call(inputs,  training=training, mask=mask)
        
        # 假设care_output是一个元组包含(output, state)，如果只有一个output则直接使用
        try:
            care_outputs, _ = care_output
        except ValueError:
            care_outputs = care_output  # 如果没有返回state，则直接取output
        
        # 确保两个输出形状一致，如果有必要调整形状
        # 这里假设o1和care_outputs已经是匹配的形状，特别是当units不同时需要调整

        # 权重融合
        alpha = 0.65
        beta = 0.35
        # 确保张量可以进行广播操作，如果维度不匹配可能需要调整
        fused_output = alpha * tf.cast(care_outputs, tf.float32) + beta * tf.cast(o1, tf.float32)
        
        return fused_output, states if self.return_sequences else fused_output
class DynamicWeightFusion(tf.keras.layers.Layer):
    def __init__(self, hidden_units=32, **kwargs):
        super(DynamicWeightFusion, self).__init__(**kwargs)
        self.hidden_layer = tf.keras.layers.Dense(hidden_units, activation='relu')
        self.hidden_layer2 = tf.keras.layers.Dense(hidden_units, activation='relu')

        self.alpha_layer = tf.keras.layers.Dense(1, activation='sigmoid', name='alpha')
        self.beta_layer = tf.keras.layers.Dense(1, activation='sigmoid', name='beta')

    @tf.function
    def call(self, inputs):
        hidden_rep = self.hidden_layer(inputs)
        hidden_rep = self.hidden_layer2(hidden_rep)
        alpha = self.alpha_layer(hidden_rep)
        beta = self.beta_layer(hidden_rep)
        # 确保α+β接近1，可以通过添加约束或直接在计算中使用softmax
        # 这里简单使用了sigmoid确保值域在0到1之间，实际应用中可能需要调整以满足具体需求
        alpha = tf.squeeze(alpha, axis=-1)
        beta = tf.squeeze(beta, axis=-1)
        print(alpha, beta)
        return alpha, beta
    
class CustomMultiHeadAttentionGRUCell(tf.keras.layers.Layer):
    def __init__(self, units, attention_units, num_heads=16, activation='tanh', recurrent_activation='sigmoid', use_bias=True):
        super(CustomMultiHeadAttentionGRUCell, self).__init__()
        self.units = units
        self.attention_units = attention_units
        self.num_heads = num_heads
        assert attention_units % num_heads == 0, "Attention units must be divisible by the number of heads"
        self.depth = attention_units // num_heads
        self.activation = tf.keras.activations.get(activation)
        self.recurrent_activation = tf.keras.activations.get(recurrent_activation)
        self.use_bias = use_bias

        # GRU门控权重
        self.kernel_z = self.add_weight(shape=(units, units * 1), initializer='glorot_uniform', name='kernel_z')
        self.kernel_r = self.add_weight(shape=(units, units * 1), initializer='glorot_uniform', name='kernel_r')
        self.kernel_h = self.add_weight(shape=(units, units * 1), initializer='glorot_uniform', name='kernel_h')
        
        # 复查门权重
        self.kernel_rev = self.add_weight(shape=(units, units), initializer='glorot_uniform', name='kernel_rev')

        # 语法联系门
        #self.kernel_scg = self.add_weight(shape=(units * 2 + attention_units, units), initializer='glorot_uniform', name='kernel_scg')
        self.kernel_scg1 = self.add_weight(shape=(units * 2 + attention_units, units), initializer='glorot_uniform', name='kernel_scg1')
        if use_bias:
            self.bias_scg1 = self.add_weight(shape=(units,), initializer='zeros', name='bias_scg1')
        
        # 第二层SCG权重和偏置
        self.kernel_scg2 = self.add_weight(shape=(units, units), initializer='glorot_uniform', name='kernel_scg2')
        if use_bias:
            self.bias_scg2 = self.add_weight(shape=(units,), initializer='zeros', name='bias_scg2')
     

        # 多头注意力机制相关权重
        self.wq_att = self.add_weight(shape=(units, attention_units), initializer='glorot_uniform', name='wq_att')
        self.wk_att = self.add_weight(shape=(units, attention_units), initializer='glorot_uniform', name='wk_att')
        self.wv_att = self.add_weight(shape=(units, attention_units), initializer='glorot_uniform', name='wv_att')
        self.u_att = self.add_weight(shape=(attention_units, num_heads), initializer='glorot_uniform', name='u_att')

        if use_bias:
            self.bias_z = self.add_weight(shape=(units * 1,), initializer='zeros', name='bias_z')
            self.bias_r = self.add_weight(shape=(units * 1,), initializer='zeros', name='bias_r')
            self.bias_h = self.add_weight(shape=(units,), initializer='zeros', name='bias_h')
            self.bias_att = self.add_weight(shape=(num_heads,), initializer='zeros', name='bias_att')
            self.bias_rev = self.add_weight(shape=(units,), initializer='zeros', name='bias_rev')  # 新增复查门偏置
            #self.bias_scg = self.add_weight(shape=(units,), initializer='zeros', name='bias_scg')


        self.layernorm_1 = tf.keras.layers.LayerNormalization()
        self.layernorm_2 = tf.keras.layers.LayerNormalization()

    def attention(self, h_tm1, h_all):
        # 多头注意力机制
        Q = tf.matmul(h_tm1, self.wq_att)
        K = tf.matmul(h_all, self.wk_att)
        V = tf.matmul(h_all, self.wv_att)

        # 形状调整以便进行多头注意力计算
        Q = tf.reshape(Q, [-1, self.num_heads, self.depth])
        K = tf.reshape(K, [-1, self.num_heads, self.depth])
        V = tf.reshape(V, [-1, self.num_heads, self.depth])

        # 计算注意力分数并应用softmax
        scores = tf.matmul(Q, K, transpose_b=True) / tf.math.sqrt(tf.cast(self.depth, tf.float32))
        att_weights = tf.nn.softmax(scores, axis=-1)

        # 上下文向量计算
        context_vector = tf.matmul(att_weights, V)
        context_vector = tf.reshape(context_vector, [-1, self.attention_units])

        return context_vector

    def call(self, inputs, states):
        h_tm1, h_all = states  # h_all 是累积的历史隐藏状态

        # 在每个时间步，将前一时间步的隐藏状态累积到历史隐藏状态中
        h_all = tf.concat([h_all, h_tm1[:, tf.newaxis, :]], axis=1)
        
        context_vector = self.attention(h_tm1, h_all)

        # 残差连接和层归一化
        h_tm1_res = self.layernorm_1(h_tm1 + context_vector)

        # 新增：复查门计算
        rev_gate = self.recurrent_activation(tf.matmul(inputs, self.kernel_rev) + tf.matmul(h_tm1_res, self.kernel_rev) + self.bias_rev)
        context_adjusted = rev_gate * context_vector

        # GRU更新，使用调整后的上下文向量
        z = self.recurrent_activation(tf.matmul(inputs, self.kernel_z) + tf.matmul(h_tm1_res, self.kernel_z) + self.bias_z)
        r = self.recurrent_activation(tf.matmul(inputs, self.kernel_r) + tf.matmul(h_tm1_res, self.kernel_r) + self.bias_r)
        rh_tm1 = r * h_tm1_res
        hh = self.activation(tf.matmul(inputs, self.kernel_h) + tf.matmul(rh_tm1, self.kernel_h) + self.bias_h)
        h = z * h_tm1_res + (1 - z) * hh

        # 融合复查门调整后的上下文信息
        h = h + context_adjusted*1.2
        
        '''
        # 最终层归一化
        h = self.layernorm_2(h)

        return h, [h, h_all]
        '''
        
        # 新增：计算语法联系门
        scg_input = tf.concat([inputs, h_tm1_res, context_vector], axis=-1)
        scg1 = self.recurrent_activation(tf.matmul(scg_input, self.kernel_scg1) + self.bias_scg1)

        # 第二层SCG进一步调整
        scg2_input = tf.concat([scg1, h_tm1_res], axis=-1)  # 可以根据需要调整输入
        scg2 = self.recurrent_activation(tf.matmul(scg2_input, self.kernel_scg2) + self.bias_scg2)

        # 强化调整最终隐藏状态
        h_adjusted = scg2 * h + (1 - scg2) * h_tm1_res  # 调整输出以反映语法和连贯性的考量

        # 最终层归一化（调整后）
        h_final = self.layernorm_2(h_adjusted)

        return h_final, [h_final, h_all]

    def get_initial_state(self, inputs=None, batch_size=None, dtype=None):
        # 初始化状态时，除了常规的隐藏状态，还需初始化一个用于累积历史隐藏状态的变量
        h_init = tf.zeros([batch_size, self.units], dtype=dtype)
        h_all_init = tf.zeros([batch_size, 1, self.units], dtype=dtype)  # 初始化为一个时间步的形状，方便后续拼接
        return [h_init, h_all_init]

    @property
    def state_size(self):
        return [self.units, self.units]

import tensorflow as tf
from tensorflow.keras import layers
class AGRU_v2(tf.keras.layers.RNN):
    def __init__(self, units, attention_units, return_sequences=True, num_heads=4, **kwargs):
        cell = CustomMultiHeadAttentionGRUCell(units, attention_units)
        super(AGRU_v2, self).__init__(cell, return_sequences=return_sequences, **kwargs)
        self.gru = tf.keras.layers.GRU(units, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform')
        #self.multi_head_attention = MultiHeadAttention(num_heads=num_heads, key_dim=512)
        self.dynamic_fusion = DynamicWeightFusion()
        
    @tf.function
    def call(self, inputs, states=None, training=None, mask=None):
        #print(1,1,1)
        #tf.config.run_functions_eagerly(True)

        inputs_att=inputs#self.multi_head_attention(inputs,inputs)       
        #tf.compat.v1.enable_eager_execution()
        # 获取GRU层的输出
        #alpha, beta = self.dynamic_fusion(inputs)  # 根据输入动态计算融合权重
        #print(alpha.numpy(), beta)
        if not tf.executing_eagerly():
            return inputs#tf.zeros(shape=(1, 6670))
        o1 = self.gru(inputs_att)
        # 确保使用eager模式执行，尽管tf.function装饰器已经隐式地控制了执行模式
        # 注意：这里不再需要手动启用eager执行，因为tf.function会根据环境自动处理
        
        # 使用super()调用自定义RNN的call方法来获取CustomAttentionGRUCell的输出
        if states is None:
            initial_states = [
                tf.zeros([tf.shape(inputs)[0], self.cell.units]),
                tf.zeros([tf.shape(inputs)[0], 1, self.cell.units])
            ]
        else:
            initial_states = states
        #tf.compat.v1.enable_eager_execution()
        care_output = super().call(inputs,  training=training, mask=mask)
        
        # 假设care_output是一个元组包含(output, state)，如果只有一个output则直接使用
        try:
            care_outputs, _ = care_output
        except ValueError:
            care_outputs = care_output  # 如果没有返回state，则直接取output
        
        # 确保两个输出形状一致，如果有必要调整形状
        # 这里假设o1和care_outputs已经是匹配的形状，特别是当units不同时需要调整
        '''
        # 权重融合
        alpha = 0.9#0.95#0.45#0.45
        beta = 0.1#0.05#0.55#0.55
        # 确保张量可以进行广播操作，如果维度不匹配可能需要调整
        fused_output = alpha * tf.cast(care_outputs, tf.float32) + beta * tf.cast(o1, tf.float32)
        
        return fused_output, states if self.return_sequences else fused_output
        '''
        # 添加动态权重融合层
        
        alpha, beta = self.dynamic_fusion(inputs)  # 根据输入动态计算融合权重
        #raise KeyError(str(alpha), str(beta))
        # 确保权重之和接近1，避免极端情况
        alpha, beta = alpha / (alpha + beta + 1e-7), beta / (alpha + beta + 1e-7)
        
        # 权重融合
        fused_output = alpha * tf.cast(care_outputs, tf.float32) + beta * tf.cast(o1, tf.float32)
        
        return fused_output, states if self.return_sequences else fused_output



class ResidualGRUBlock(tf.keras.layers.Layer):
    def __init__(self, units, dropout_rate):
        super(ResidualGRUBlock, self).__init__()
        self.gru = tf.keras.layers.GRU(units, return_sequences=True)
        self.norm = tf.keras.layers.LayerNormalization()
        self.dropout = tf.keras.layers.Dropout(dropout_rate)

    def call(self, inputs):
        output = self.gru(inputs)
        output = self.norm(output)
        output = self.dropout(output)
        return tf.keras.layers.Add()([inputs, output])


class TransformerEnhancedGRUCell(tf.keras.layers.Layer):
    def __init__(self, units, attention_units, num_heads=4, **kwargs):
        super(TransformerEnhancedGRUCell, self).__init__(**kwargs)
        self.units = units
        self.attention_units = attention_units
        self.num_heads = num_heads
        self.depth = attention_units // num_heads
        self.layernorm_1 = tf.keras.layers.LayerNormalization()
        self.layernorm_2 = tf.keras.layers.LayerNormalization()
        self.dense_proj = tf.keras.layers.Dense(units, activation='tanh')
        
        # Transformer相关组件
        maxlen=1024
        self.positional_encoding = PositionalEncoding(maximum_position_encoding=maxlen, d_model=attention_units)
        self.multi_head_self_attention = layers.MultiHeadAttention(num_heads=num_heads, key_dim=attention_units // num_heads)
        self.add_and_norm1 = tf.keras.layers.Add()  # 用于残差连接
        self.dropout1 = tf.keras.layers.Dropout(0.1)  # 注意力后的dropout
        
        # GRU门控权重
        self.kernel_z = self.add_weight(shape=(units, units), initializer='glorot_uniform', name='kernel_z')
        self.kernel_r = self.add_weight(shape=(units, units), initializer='glorot_uniform', name='kernel_r')
        self.kernel_h = self.add_weight(shape=(units, units), initializer='glorot_uniform', name='kernel_h')
        self.recurrent_activation = tf.keras.activations.sigmoid

    def build(self, input_shape):
        # 初始化累积历史状态的权重
        self.kernel_hist = self.add_weight(shape=(self.units, self.units), initializer='glorot_uniform', name='kernel_hist')
        self.bias_hist = self.add_weight(shape=(self.units,), initializer='zeros', name='bias_hist')
        super().build(input_shape)

    def call(self, inputs, states):
        # 解包状态：h_tm1为前一时间步隐藏状态，h_all为累积的历史隐藏状态
        h_tm1, h_all = states

        seq_len = tf.shape(inputs)[1]

        # 添加位置编码
        inputs_with_pos_encoding = inputs + self.positional_encoding(tf.range(seq_len))

        # Transformer的多头自注意力
        attn_output, _ = self.multi_head_self_attention(inputs_with_pos_encoding, inputs_with_pos_encoding, inputs_with_pos_encoding)
        attn_output = self.dropout1(attn_output)
        out1 = self.add_and_norm1([inputs_with_pos_encoding, attn_output])

        # 更新累积的历史隐藏状态
        h_all = self.recurrent_activation(tf.matmul(h_all, self.kernel_hist) + self.bias_hist + h_tm1)
        
        # 简化的GRU更新逻辑，融合Transformer输出
        z = self.recurrent_activation(tf.matmul(out1, self.kernel_z) + tf.matmul(h_all, self.kernel_z))
        r = self.recurrent_activation(tf.matmul(out1, self.kernel_r) + tf.matmul(h_all, self.kernel_r))
        rh_tm1 = r * h_tm1
        hh = tf.tanh(tf.matmul(out1, self.kernel_h) + tf.matmul(rh_tm1, self.kernel_h))
        h = z * h_tm1 + (1 - z) * hh

        # 应用Layer Normalization
        h = self.layernorm_2(h)

        return h, [h, h_all]  # 返回更新后的隐藏状态及累积的历史隐藏状态

    def get_initial_state(self, inputs=None, batch_size=None, dtype=None):
        return [tf.zeros(shape=(batch_size, self.units), dtype=dtype),
                tf.zeros(shape=(batch_size, 1, self.units), dtype=dtype)]
    @property
    def state_size(self):
        return [self.units, self.units]
    
# Positional Encoding 实现
class PositionalEncoding(layers.Layer):
    def __init__(self, maximum_position_encoding, d_model, **kwargs):
        super(PositionalEncoding, self).__init__(**kwargs)
        self.pos_encoding = self.positional_encoding(maximum_position_encoding, d_model)

    def get_angles(self, pos, i, d_model):
        angle_rates = 1 / tf.pow(10000., (2 * (i//2)) / tf.cast(d_model, tf.float32))
        return pos * angle_rates

    def positional_encoding(self, position, d_model):
        angle_rads = self.get_angles(
            tf.range(position, dtype=tf.float32)[:, tf.newaxis],
            tf.range(d_model, dtype=tf.float32)[tf.newaxis, :],
            d_model)
        
        # 将sin应用到偶数索引上，cos应用到奇数索引上
        sines = tf.sin(angle_rads[:, 0::2])
        cosines = tf.cos(angle_rads[:, 1::2])
        
        pos_encoding = tf.concat([sines, cosines], axis=-1)
        pos_encoding = pos_encoding[tf.newaxis, ...]
        return tf.cast(pos_encoding, tf.float32)

    def call(self, inputs):
        seq_len = tf.shape(inputs)[1]
        return tf.slice(self.pos_encoding, [0, 0], [1, seq_len])

class AGRU_v2_att(tf.keras.layers.RNN):
    def __init__(self, units, attention_units, return_sequences=True, num_heads=4, **kwargs):
        cell = TransformerEnhancedGRUCell(units, attention_units)
        super(AGRU_v2_att, self).__init__(cell, return_sequences=return_sequences, **kwargs)
        self.gru = tf.keras.layers.GRU(units, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform')
        #self.multi_head_attention = MultiHeadAttention(num_heads=num_heads, key_dim=512)
        self.dynamic_fusion = DynamicWeightFusion()
        
    @tf.function
    def call(self, inputs, states=None, training=None, mask=None):
        #tf.config.run_functions_eagerly(True)

        inputs_att=inputs#self.multi_head_attention(inputs,inputs)       
        #tf.compat.v1.enable_eager_execution()
        # 获取GRU层的输出
        
        if not tf.executing_eagerly():
            return inputs#tf.zeros(shape=(1, 6670))
        o1 = self.gru(inputs_att)
        # 确保使用eager模式执行，尽管tf.function装饰器已经隐式地控制了执行模式
        # 注意：这里不再需要手动启用eager执行，因为tf.function会根据环境自动处理
        
        # 使用super()调用自定义RNN的call方法来获取CustomAttentionGRUCell的输出
        if states is None:
            initial_states = [
                tf.zeros([tf.shape(inputs)[0], self.cell.units]),
                tf.zeros([tf.shape(inputs)[0], 1, self.cell.units])
            ]
        else:
            initial_states = states
        #tf.compat.v1.enable_eager_execution()
        care_output = super().call(inputs,  training=training, mask=mask)
        
        # 假设care_output是一个元组包含(output, state)，如果只有一个output则直接使用
        try:
            care_outputs, _ = care_output
        except ValueError:
            care_outputs = care_output  # 如果没有返回state，则直接取output
        
        # 确保两个输出形状一致，如果有必要调整形状
        # 这里假设o1和care_outputs已经是匹配的形状，特别是当units不同时需要调整
        '''
        # 权重融合
        alpha = 0.9#0.95#0.45#0.45
        beta = 0.1#0.05#0.55#0.55
        # 确保张量可以进行广播操作，如果维度不匹配可能需要调整
        fused_output = alpha * tf.cast(care_outputs, tf.float32) + beta * tf.cast(o1, tf.float32)
        
        return fused_output, states if self.return_sequences else fused_output
        '''
        # 添加动态权重融合层
        
        alpha, beta = self.dynamic_fusion(inputs)  # 根据输入动态计算融合权重
        
        # 确保权重之和接近1，避免极端情况
        alpha, beta = alpha / (alpha + beta + 1e-7), beta / (alpha + beta + 1e-7)
        
        # 权重融合
        fused_output = alpha * tf.cast(care_outputs, tf.float32) + beta * tf.cast(o1, tf.float32)
        
        return fused_output, states if self.return_sequences else fused_output



class TwoThinking(tf.keras.layers.Layer):
    def __init__(self, units, vocab):
        super(TwoThinking, self).__init__()
        self.dense_input = tf.keras.layers.Dense(vocab)
        self.think_1 = tf.keras.layers.GRU(units, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform')
        self.think_2 = tf.keras.layers.LSTM(units, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform')
        self.think_1_d = tf.keras.layers.Dense(vocab)
        self.think_2_d = tf.keras.layers.Dense(vocab)
        self.main_d = tf.keras.layers.Dense(vocab)
        self.main_think = tf.keras.layers.GRU(units, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform')
        self.dropout = tf.keras.layers.Dropout(0.2)

    def call(self, inputs):
        output = self.dense_input(inputs)
        output_1 = self.think_1(output)
        output_1 = self.think_1_d(output_1)
        

        
        output_2 = self.think_2(output)
        output_2 = self.think_2_d(output_2)
        

        
        # 假设我们想在进入main_think前合并output_1和output_2，且应用dropout
        combined_output = tf.keras.layers.concatenate([output_1, output_2,inputs])
        combined_output = self.dropout(combined_output)
        
        output = self.main_think(combined_output)#self.main_think(combined_output)  # 更新此处以匹配修改后的逻辑
        output = self.main_d(output)  # 移除了多余的重复调用
        #output = self.main_d(output)  # 移除了多余的重复调用
        #output = self.main_d(output)  # 移除了多余的重复调用
        
        # 注意：在实际使用中，根据需要在每个epoch后重置stateful层的状态
        
        return output#tf.keras.layers.Add()([inputs, output])

class TwoThinking_att_t0(tf.keras.layers.Layer):
    def __init__(self, units, vocab,__=1024):
        super(TwoThinking_att_t0, self).__init__()
        self.dense_input = tf.keras.layers.Dense(vocab)
        self.think_1 = tf.keras.layers.GRU(units*2, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform', )
        self.think_2 = tf.keras.layers.GRU(units, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform')
        #self.think_3 = tf.keras.layers.GRU(units, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform',unroll=True)
        self.think_1_d = tf.keras.layers.Dense(vocab)
        self.think_2_d = tf.keras.layers.Dense(vocab)
        #self.think_3_d = tf.keras.layers.Dense(vocab)
        self.main_d = tf.keras.layers.Dense(vocab)
        #self.main_think = tf.keras.layers.GRU(units, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform')
        self.dropout = tf.keras.layers.Dropout(0.15)
        self.attention = tf.keras.layers.MultiHeadAttention(num_heads=8, key_dim=__)
        #self.pe=PositionalEncoding(130,128)
        
        
    @tf.function
    def call(self, inputs):
        #inputs = self.dense_input(inputs)
        
        inputs = (self.attention(inputs, inputs))

        output = self.dense_input(inputs)
        output_1 = self.think_1(output)
        output_1 = self.think_1_d(output_1)
        output_1 = self.dropout(output_1)

        
        output_2 = self.think_2(output)
        output_2 = self.think_2_d(output_2)
        output_2 = self.dropout(output_2)
        #output_3 = self.think_3(output)
        #output_3 = self.think_3_d(output_3)
        

        
        # 假设我们想在进入main_think前合并output_1和output_2，且应用dropout
        #combined_output = inputs#tf.keras.layers.concatenate([output_1+output_2,inputs])
        #combined_output = self.dropout(combined_output)
        
        #outputm = self.main_think(combined_output)#self.main_think(combined_output)  # 更新此处以匹配修改后的逻辑
        #outputm = self.main_d(outputm)  # 移除了多余的重复调用
        #output = self.main_d(output)  # 移除了多余的重复调用
        #output = self.main_d(output)  # 移除了多余的重复调用
        
        # 注意：在实际使用中，根据需要在每个epoch后重置stateful层的状态
        
        return self.main_d(output_1+output_2)#self.main_d(output_1+output_2)#tf.keras.layers.Add()([inputs, output])
import tensorflow as tf
from tensorflow.keras.layers import Layer, Dense
from tensorflow.keras import initializers

class AttentionGRUCell(tf.keras.layers.Layer):
    def __init__(self, units, att_units, **kwargs):
        super(AttentionGRUCell, self).__init__(**kwargs)
        self.units = units
        self.att_units = att_units
        
        # 初始化GRU单元
        self.gru_cell = tf.keras.layers.GRUCell(units)
        
        # 注意力机制中的全连接层
        self.W1 = Dense(att_units, use_bias=False)
        self.W2 = Dense(att_units, use_bias=False)
        self.V = Dense(1, use_bias=False)

    def call(self, inputs, states, training=None):
        
        h_prev, seq_embed = states  # h_prev是前一时刻的隐藏状态，seq嵌入是整个序列的嵌入表示
        
        # GRU更新
        h_gru, _ = self.gru_cell(inputs, states=[h_prev])
        
        # 注意力机制计算
        time_steps = tf.shape(seq_embed)[1]
        h_gru_repeated = tf.repeat(tf.expand_dims(h_gru, 1), time_steps, axis=1)
        e = self.V(tf.nn.tanh(self.W1(seq_embed) + self.W2(h_gru_repeated)))
        alpha = tf.nn.softmax(e, axis=1)
        context = tf.reduce_sum(alpha * seq_embed, axis=1)
        
        # 结合GRU输出和注意力上下文
        output = tf.concat([h_gru, context], axis=-1)
        
        return output, [output, seq_embed]  # 输出新的隐藏状态及保持状态

class AttentionGRULayer(Layer):
    def __init__(self, units, att_units, **kwargs):
        super(AttentionGRULayer, self).__init__(**kwargs)
        self.cell = AttentionGRUCell(units, att_units)
        self.units=units
        self.att_units=att_units

    def get_initial_state(self, inputs):
        batch_size = tf.shape(inputs)[0]
        # 确保使用正确的units值
        initial_hidden = tf.zeros(shape=(batch_size, self.units))
        # 注意：对于seq_embed的处理，确保逻辑与你的模型设计相符
        return initial_hidden, inputs

    def call(self, inputs, states=None, training=None):
        if not tf.executing_eagerly():
            return inputs
        if states is None:
            states = self.get_initial_state(inputs)
        # 移除了return_sequences和return_states关键字参数
        outputs, new_states = tf.keras.backend.rnn(self.cell, inputs, states,
                                                  constants=None, unroll=False, time_major=False,
                                                  go_backwards=False, mask=None)
        
        # 根据需求处理输出
        final_output = outputs if isinstance(outputs, tf.Tensor) else outputs[-1]  # 如果是返回全序列则保持不变，否则取最后一个时间步
        return final_output, new_states
    
#——————————————————————————
class AttentionGRUCellWithGrammar(tf.keras.layers.Layer):
    def __init__(self, units, att_units, **kwargs):
        super(AttentionGRUCellWithGrammar, self).__init__(**kwargs)
        self.units = units
        self.att_units = att_units
        
        # 初始化GRU单元
        self.gru_cell = tf.keras.layers.GRUCell(units)
        
        # 注意力机制中的全连接层
        self.W1_att = Dense(att_units, use_bias=False)
        self.W2_att = Dense(att_units, use_bias=False)
        self.V_att = Dense(1, use_bias=False)
        
        # 语法纠正门的全连接层
        self.W1_gram = Dense(att_units, use_bias=False)
        self.W2_gram = Dense(att_units, use_bias=False)
        self.V_gram = Dense(1, activation='sigmoid', use_bias=False)  # 使用sigmoid激活函数作为门控
        
    def call(self, inputs, states, training=None):
        h_prev, seq_embed = states
        
        # GRU更新
        h_gru, _ = self.gru_cell(inputs, states=[h_prev])
        
        # 注意力机制计算
        time_steps = tf.shape(seq_embed)[1]
        h_gru_repeated = tf.repeat(tf.expand_dims(h_gru, 1), time_steps, axis=1)
        e_att = self.V_att(tf.nn.tanh(self.W1_att(seq_embed) + self.W2_att(h_gru_repeated)))
        alpha_att = tf.nn.softmax(e_att, axis=1)
        context = tf.reduce_sum(alpha_att * seq_embed, axis=1)
        
        # 语法纠正门计算
        e_gram = self.V_gram(tf.nn.tanh(self.W1_gram(seq_embed) + self.W2_gram(h_gru_repeated)))
        alpha_gram = tf.nn.sigmoid(e_gram)  # 使用sigmoid确保门值在0到1之间
        corrected_h_gru = alpha_gram * h_gru + (1 - alpha_gram) * context  # 语法纠正操作
        
        # 结合GRU输出（经语法纠正）和注意力上下文
        output = tf.concat([corrected_h_gru, context], axis=-1)
        
        return output, [output, seq_embed]

class AttentionGRULayerWithGrammar(Layer):
    def __init__(self, units, att_units, **kwargs):
        super(AttentionGRULayerWithGrammar, self).__init__(**kwargs)
        self.cell = AttentionGRUCellWithGrammar(units, att_units)
        self.units = units
        self.att_units = att_units

    def get_initial_state(self, inputs):
        batch_size = tf.shape(inputs)[0]
        initial_hidden = tf.zeros(shape=(batch_size, self.units))
        return initial_hidden, inputs

    def call(self, inputs, states=None, training=None):
        if not tf.executing_eagerly():
            return inputs
        if states is None:
            states = self.get_initial_state(inputs)
        outputs, new_states = tf.keras.backend.rnn(self.cell, inputs, states,
                                                  constants=None, unroll=False, time_major=False,
                                                  go_backwards=False, mask=None)
        final_output = outputs if isinstance(outputs, tf.Tensor) else outputs[-1]
        return final_output, new_states
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import tensorflow as tf
from tensorflow.keras import layers

class EnhancedAttentionMechanism(layers.Layer):
    def __init__(self, att_units, **kwargs):
        super(EnhancedAttentionMechanism, self).__init__(**kwargs)
        self.att_units = att_units
        self.Wq = layers.Dense(att_units, use_bias=True)
        self.Wk = layers.Dense(att_units, use_bias=True)
        self.Wv = layers.Dense(att_units, use_bias=True)
        
    def call(self, seq_embed):
        # Key, Query, Value计算
        Q = self.Wq(seq_embed)
        K = self.Wk(seq_embed)
        V = self.Wv(seq_embed)
        
        # 计算注意力权重
        attention_scores = tf.matmul(Q, K, transpose_b=True) / tf.math.sqrt(tf.cast(self.att_units, tf.float32))
        attention_weights = tf.nn.softmax(attention_scores, axis=-1)
        
        # 加权求和得到上下文向量
        context_vector = tf.matmul(attention_weights, V)
        return context_vector

class TemperaturePooling(layers.Layer):
    def __init__(self, temp_factor=1.0, **kwargs):
        super(TemperaturePooling, self).__init__(**kwargs)
        self.temp_factor = temp_factor
        
    def call(self, inputs):
        # 增加温度因子，动态调整注意力分布
        return inputs / self.temp_factor

class EnhancedAttentionGRUCell(AttentionGRUCell):
    def __init__(self, units, att_units, temp_factor=1.0, **kwargs):
        super().__init__(units, att_units, **kwargs)
        self.enhanced_attention = EnhancedAttentionMechanism(att_units)
        self.temp_pool = TemperaturePooling(temp_factor)
        
    def call(self, inputs, states, training=None):
        h_prev, seq_embed = states
        
        h_gru, _ = self.gru_cell(inputs, states=[h_prev])
        
        # 使用增强注意力机制
        attended_seq = self.enhanced_attention(seq_embed)
        
        # 引入温度池化
        temp_pooled_attended_seq = self.temp_pool(attended_seq)
        
        # 结合GRU输出和经过温度池化的注意力上下文
        output = tf.concat([h_gru, temp_pooled_attended_seq], axis=-1)
        
        return output, [output, seq_embed]
class AttentionGRULayerEn(Layer):
    def __init__(self, units, att_units, **kwargs):
        super(AttentionGRULayerEn, self).__init__(**kwargs)
        self.cell = EnhancedAttentionGRUCell(units, att_units)
        self.units = units
        self.att_units = att_units

    def get_initial_state(self, inputs):
        batch_size = tf.shape(inputs)[0]
        initial_hidden = tf.zeros(shape=(batch_size, self.units))
        return initial_hidden, inputs

    def call(self, inputs, states=None, training=None):
        if not tf.executing_eagerly():
            return inputs
        if states is None:
            states = self.get_initial_state(inputs)
        outputs, new_states = tf.keras.backend.rnn(self.cell, inputs, states,
                                                  constants=None, unroll=False, time_major=False,
                                                  go_backwards=False, mask=None)
        final_output = outputs if isinstance(outputs, tf.Tensor) else outputs[-1]
        return final_output, new_states
import tensorflow as tf
from tensorflow.keras import layers


class SimplifiedRotation(layers.Layer):
    """简化的旋转操作，用于模拟旋转知识"""
    def __init__(self, **kwargs):
        super(SimplifiedRotation, self).__init__(**kwargs)
    
    def call(self, x):
        x1, x2 = tf.split(x, num_or_size_splits=2, axis=-1)
        return tf.concat([-x2, x1], axis=-1)

class EnhancedAttentionMechanism_41(layers.Layer):
    def __init__(self, att_units,  max_seq_len=129, **kwargs):
        super(EnhancedAttentionMechanism_41, self).__init__(**kwargs)
        self.att_units = att_units
        self.max_seq_len = max_seq_len
        self.Wq = layers.Dense(att_units, use_bias=True)
        self.Wk = layers.Dense(att_units, use_bias=True)
        self.Wv = layers.Dense(att_units, use_bias=True)
        #self.positional_encoding = positional_encoding(max_seq_len, att_units // 2)
        self.rotation = SimplifiedRotation()
        
    def call(self, seq_embed):
        # 添加位置编码
        #seq_embed += tf.gather(self.positional_encoding, tf.range(tf.shape(seq_embed)[1]), batch_dims=1)
        
        Q = self.Wq(seq_embed)
        K = self.Wk(seq_embed)
        V = self.Wv(seq_embed)
        
        # 简化的“旋转”操作
        Q_rotated = self.rotation(Q)
        K_rotated = self.rotation(K)
        
        # 计算注意力权重
        attention_scores = tf.matmul(Q_rotated, K_rotated, transpose_b=True) / tf.math.sqrt(tf.cast(self.att_units // 2, tf.float32))
        attention_weights = tf.nn.softmax(attention_scores, axis=-1)
        
        # 加权求和得到上下文向量
        context_vector = tf.matmul(attention_weights, V)
        return context_vector
    
class EnhancedAttentionGRUCell_41(AttentionGRUCell):
    def __init__(self, units, att_units, temp_factor=1.0, **kwargs):
        super().__init__(units, att_units, **kwargs)
        self.enhanced_attention = EnhancedAttentionMechanism_41(att_units)
        self.temp_pool = TemperaturePooling(temp_factor)
        
    def call(self, inputs, states, training=None):
        h_prev, seq_embed = states
        
        h_gru, _ = self.gru_cell(inputs, states=[h_prev])
        
        # 使用增强注意力机制
        attended_seq = self.enhanced_attention(seq_embed)
        
        # 引入温度池化
        temp_pooled_attended_seq = self.temp_pool(attended_seq)
        
        # 结合GRU输出和经过温度池化的注意力上下文
        output = tf.concat([h_gru, temp_pooled_attended_seq], axis=-1)
        
        return output, [output, seq_embed]
class AttentionGRULayerEn_41(Layer):
    def __init__(self, units, att_units, **kwargs):
        super(AttentionGRULayerEn_41, self).__init__(**kwargs)
        self.cell = EnhancedAttentionGRUCell_41(units, att_units)
        self.units = units
        self.att_units = att_units

    def get_initial_state(self, inputs):
        batch_size = tf.shape(inputs)[0]
        initial_hidden = tf.zeros(shape=(batch_size, self.units))
        return initial_hidden, inputs

    def call(self, inputs, states=None, training=None):
        if not tf.executing_eagerly():
            return inputs
        if states is None:
            states = self.get_initial_state(inputs)
        outputs, new_sta
        tes = tf.keras.backend.rnn(self.cell, inputs, states,
                                                  constants=None, unroll=False, time_major=False,
                                                  go_backwards=False, mask=None)
        final_output = outputs if isinstance(outputs, tf.Tensor) else outputs[-1]
        return final_output, new_states
class CLModel(layers.Layer):
    def __init__(self, vocab_size, embedding_dim,
                 find_window, window, units, **kwargs):
        super(CLModel, self).__init__(**kwargs)
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.find_window = find_window
        self.window = window
        self.units = units
        
        # Layers
        self.embedding = layers.Embedding(vocab_size, embedding_dim)
        self.query_layer = layers.Dense(1)
        self.context_encoder = layers.GRU(units, return_sequences=True, return_state=True)
        self.next_token_predictor = layers.Dense(vocab_size)

    def call(self, inputs, training=None):
        # Embedding
        embedded_inputs = self.embedding(inputs)
        
        # Query Weighting
        query_weights = self.query_layer(embedded_inputs)
        query_weights = tf.squeeze(query_weights, axis=-1)
        top_indices = tf.argsort(query_weights, direction='DESCENDING')[:, :self.find_window]
        
        # History and Input Selection
        his = tf.gather(embedded_inputs, top_indices, batch_dims=1)
        inp = embedded_inputs[:, :self.window]
        
        # Remove duplicates from his if they appear in inp
        his_mask = tf.reduce_sum(tf.one_hot(top_indices, tf.shape(embedded_inputs)[1]), axis=1)
        his_mask = tf.cast(his_mask > 0, tf.float32)
        his_mask = tf.expand_dims(his_mask, -1) * tf.ones_like(embedded_inputs)
        his_mask = tf.slice(his_mask, [0, 0, 0], [-1, self.window, -1])
        inp = tf.where(his_mask > 0, tf.zeros_like(inp), inp)
        
        # Combine his and inp
        combined = tf.concat([his, inp], axis=1)
        
        # Sequence Encoding
        _, state = self.context_encoder(combined)
        
        # Next Token Prediction
        next_token_logits = self.next_token_predictor(state)
        
        return next_token_logits

    def get_config(self):
        config = super(CustomLanguageModel, self).get_config()
        config.update({
            "vocab_size": self.vocab_size,
            "embedding_dim": self.embedding_dim,
            "find_window": self.find_window,
            "window": self.window,
            "units": self.units
        })
        return config
import tensorflow as tf
from tensorflow.keras import layers
'''
class CLModel(layers.Layer):
    def __init__(self, vocab_size, embedding_dim, find_window, window, units, utf=True, **kwargs):
        super(CLModel, self).__init__(**kwargs)
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.find_window = find_window
        self.window = window
        self.units = units
        
        self.next_token_predictor = layers.Dense(vocab_size)
        self.utf=utf
        # Layers
        self.embedding = layers.Embedding(vocab_size, embedding_dim)
        self.query_layer = layers.Dense(1,name='query_layer')
        if type(units)==tuple:
            return
        self.context_encoder = layers.GRU(units, return_sequences=True, return_state=True,recurrent_initializer='glorot_uniform')

        
        
    def call(self, inputs, training=None, use_teacher_forcing=True, teacher_forcing_input=None):
        if not self.utf:
            use_teacher_forcing=False
        # Embedding
        embedded_inputs = self.embedding(inputs)
        
        # Query Weighting
        query_weights = self.query_layer(embedded_inputs)
        query_weights = tf.squeeze(query_weights, axis=-1)


        top_indices = tf.argsort(query_weights, direction='DESCENDING')[:, :self.find_window]
        
        # History and Input Selection
        his = tf.gather(embedded_inputs, top_indices, batch_dims=1)
        inp = embedded_inputs[:, :self.window]
        
        # Remove duplicates from his if they appear in inp
        his_mask = tf.reduce_sum(tf.one_hot(top_indices, tf.shape(embedded_inputs)[1]), axis=1)
        his_mask = tf.cast(his_mask > 0, tf.float32)
        his_mask = tf.expand_dims(his_mask, -1) * tf.ones_like(embedded_inputs)
        his_mask = tf.slice(his_mask, [0, 0, 0], [-1, self.window, -1])
        inp = tf.where(his_mask > 0, tf.zeros_like(inp), inp)
        
        # Combine his and inp
        combined = tf.concat([his, inp], axis=1)
        
        # Sequence Encoding
        encoded_sequences, _ = self.context_encoder(combined, initial_state=self.context_encoder.get_initial_state(combined))#/self.output_size

        if use_teacher_forcing:
            teacher_forcing_input=embedded_inputs
        # Teacher Forcing
        if use_teacher_forcing:# and teacher_forcing_input is not None:
            teacher_forcing_input = self.embedding(teacher_forcing_input)
            encoded_sequences = tf.concat([encoded_sequences, teacher_forcing_input], axis=1)
        
        # Next Token Prediction
        next_token_logits = self.next_token_predictor(encoded_sequences)
        
        return next_token_logits

    def get_config(self):
        config = super(CustomLanguageModel, self).get_config()
        config.update({
            "vocab_size": self.vocab_size,
            "embedding_dim": self.embedding_dim,
            "find_window": self.find_window,
            "window": self.window,
            "units": self.units
        })
        return config
'''
import tensorflow as tf
from tensorflow.keras import layers
class CharGRULayer(layers.Layer):
    def __init__(self, units, n_char, **kwargs):
        super(CharGRULayer, self).__init__(**kwargs)
        self.units = units
        self.n_char = n_char
        self.gru = layers.GRU(units,
                              return_sequences=True, return_state=True,
                              stateful=True,
                              trainable=False
                              )

    def call(self, inputs):
        # Extract the first n_char characters from the input sequence
        char_inputs = inputs[:, :self.n_char]
        
        # Pass through the GRU layer
        _, last_state = self.gru(char_inputs)
        
        return last_state

    def get_config(self):
        config = super(CharGRULayer, self).get_config()
        config.update({
            "units": self.units,
            "n_char": self.n_char
        })
        return config
    from tensorflow.keras.layers import Layer, GRU, Dense  
  
class CharGRULayer(Layer):  
    def __init__(self, units, n_char, dense_units, **kwargs):  
        super(CharGRULayer, self).__init__(**kwargs)  
        self.units = units  
        self.n_char = n_char  
        self.dense_units = dense_units  # 新增的Dense层单元数  
  
        # 创建GRU层  
        self.gru = GRU(units,  
                       return_sequences=True,  # 通常我们不需要序列输出，只关心最后一个状态  
                       return_state=True,  
                       stateful=True,  
                       trainable=True  # 通常我们希望GRU层是可训练的  
                       )  
  
        # 创建Dense层  
        self.dense = Dense(dense_units, activation='relu')  # 使用ReLU激活函数  
  
    def call(self, inputs):  
        # 提取输入序列的前n_char个字符  
        char_inputs = inputs[:, :self.n_char]  
          
        # 通过GRU层  
        _, last_state = self.gru(char_inputs)  
          
        # 通过Dense层变换特征表示  
        dense_output = self.dense(last_state)  
          
        return dense_output  
  
    def get_config(self):  
        config = super(CharGRULayer, self).get_config()  
        config.update({  
            "units": self.units,  
            "n_char": self.n_char,  
            "dense_units": self.dense_units  
        })  
        return config
from tensorflow.keras.layers import GRU, Dense
from tensorflow.keras.layers import Layer

class CharGRULayer(Layer):
    def __init__(self, units, n_char, dense_units, num_gru_layers=1, **kwargs):
        super(CharGRULayer, self).__init__(**kwargs)
        self.units = units
        self.n_char = n_char
        self.dense_units = dense_units
        self.num_gru_layers = num_gru_layers
        
        # 创建堆叠的GRU层
        self.grus = []
        for i in range(num_gru_layers):
            if 1:#i == num_gru_layers - 1:
                # 最后一层GRU不需要返回序列
                gru_layer = GRU(units,
                                return_sequences=False,
                                return_state=True,
                                stateful=True,
                                trainable=True)

            self.grus.append(gru_layer)

        # 创建Dense层
        self.dense = Dense(dense_units, activation='relu')
        self.dense2 = Dense(dense_units, activation='relu')

    def call(self, inputs):
        # 提取输入序列的前n_char个字符
        char_inputs = inputs[:, :self.n_char]
        
        # 通过堆叠的GRU层
        sequence_output = char_inputs
        for gru in self.grus[:-1]:
            _, last_state = gru(sequence_output)
            sequence_output = last_state
        
        _, last_state = self.grus[-1](sequence_output)
        
        # 通过Dense层变换特征表示
        dense_output = self.dense(last_state)
        dense_output=tf.keras.layers.Dropout(0.1)(dense_output)
        dense_output = self.dense2(dense_output)
        
        return dense_output

    def get_config(self):
        config = super(CharGRULayer, self).get_config()
        config.update({
            "units": self.units,
            "n_char": self.n_char,
            "dense_units": self.dense_units,
            "num_gru_layers": self.num_gru_layers
        })
        return config
import tensorflow as tf
from tensorflow.keras.layers import GRU, Dense, Dropout

class CharGRULayer(tf.keras.layers.Layer):
    def __init__(self, units, n_char,
                 dense_units, num_gru_layers=4, tra=False,
                 **kwargs):
        super(CharGRULayer, self).__init__(**kwargs)
        self.units = units
        self.n_char = n_char
        self.dense_units = dense_units
        self.num_gru_layers = num_gru_layers
        
        # 创建堆叠的GRU层
        self.grus = []
        for i in range(num_gru_layers):
            # 除了最后一层GRU，其他层都需要返回序列
            if i < num_gru_layers - 1:
                gru_layer = GRU(units,
                                return_sequences=True,
                                return_state=True,
                                stateful=False,
                                trainable=tra)
            else:
                # 最后一层GRU不需要返回序列
                gru_layer = GRU(units,
                                return_sequences=False,
                                return_state=True,
                                stateful=False,
                                trainable=tra)

            self.grus.append(gru_layer)

        # 创建Dense层
        self.dense = Dense(dense_units, activation='relu',trainable=tra)
        self.dense2 = Dense(dense_units, activation='relu',trainable=tra)
        self.dropout = Dropout(0.1)

    def call(self, inputs):
        # 提取输入序列的前n_char个字符
        char_inputs = inputs[:, :self.n_char, :]  # 确保这里提取的是三维数据
        
        # 通过堆叠的GRU层
        sequence_output = char_inputs
        for gru in self.grus[:-1]:
            last_state = gru(sequence_output)
            sequence_output = last_state#tf.expand_dims(char_inputs, 0, name=None)
        
        _, last_state = self.grus[-1](sequence_output)
        
        # 通过Dense层变换特征表示
        dense_output = self.dense(last_state)
        dense_output = self.dropout(dense_output)
        dense_output = self.dense2(dense_output)
        
        return dense_output

    def get_config(self):
        config = super(CharGRULayer, self).get_config()
        config.update({
            "units": self.units,
            "n_char": self.n_char,
            "dense_units": self.dense_units,
            "num_gru_layers": self.num_gru_layers
        })
        return config
import tensorflow as tf
from tensorflow.keras.layers import GRU, Dense, Dropout

class CharGRULayer(tf.keras.layers.Layer):
    def __init__(self, units, n_char,
                 dense_units, num_gru_layers=4, trainable=True,
                 **kwargs):
        super(CharGRULayer, self).__init__(**kwargs)
        self.units = units
        self.n_char = n_char
        self.dense_units = dense_units
        self.num_gru_layers = num_gru_layers
        self.trainable = trainable
        
        # 创建堆叠的GRU层
        self.grus = []
        for i in range(num_gru_layers):
            # 除了最后一层GRU，其他层都需要返回序列
            if i < num_gru_layers - 1:
                gru_layer = GRU(units,
                                return_sequences=True,
                                return_state=True,
                                stateful=False,
                                trainable=trainable)
            else:
                # 最后一层GRU不需要返回序列
                gru_layer = GRU(units,
                                return_sequences=True,
                                return_state=True,
                                stateful=False,
                                trainable=trainable)

            self.grus.append(gru_layer)

        # 创建Dense层
        #self.dense = Dense(dense_units, activation='tanh', trainable=trainable)
        #self.dense2 = Dense(dense_units, activation='tanh', trainable=trainable)
        #self.dropout = Dropout(0.1)

    def call(self, inputs, training=None):
        # 提取输入序列的前n_char个字符
        char_inputs = inputs[:, :self.n_char, :]  # 确保这里提取的是三维数据
        
        # 通过堆叠的GRU层
        sequence_output = char_inputs
        states = None
        for gru in self.grus:
            # 除了最后一层GRU外，其余层都需要返回序列和状态
            if gru is not self.grus[-1]:
                sequence_output, state = gru(sequence_output, initial_state=states)
                states = state
            else:
                sequence_output, state = gru(sequence_output, initial_state=states)
                states = state
        
        # 通过Dense层变换特征表示
        dense_output = states#self.dense(states)
        #dense_output = self.dropout(dense_output, training=training)
        #dense_output = self.dense2(dense_output)
        
        return dense_output

    def get_config(self):
        config = super(CharGRULayer, self).get_config()
        config.update({
            "units": self.units,
            "n_char": self.n_char,
            "dense_units": self.dense_units,
            "num_gru_layers": self.num_gru_layers,
            "trainable": self.trainable
        })
        return config
class CLModel(layers.Layer):
    def __init__(self, vocab_size, embedding_dim, #find_window,
                 window,
                 units,
                 batch_size=1,
                 n=1, utf=True,
                 his_q=0.75,
                 use_matt=True,
                 att_q=0.4,
                 att_units=None,
                 n_char=3,
                 wd_q=1.0,
                 nh=8,
                 train_deep_layer=False,
                 num_chargru_layer=8,
                 **kwargs):
        
        super(CLModel, self).__init__(**kwargs)
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        #self.find_window = find_window
        self.window = window
        self.units = units
        self.n = n  # Number of stacked GRU layers
        self.his_q=his_q
        if att_units is None:
            print('att_units is None')
            att_units=units
        self.wd_q=wd_q
        self.char_gru_layer = CharGRULayer(units//2,
                                           n_char=n_char,
                                           dense_units=units//2,
                                           trainable=train_deep_layer,
                                           num_gru_layers=num_chargru_layer)
        self.next_token_predictor = layers.Dense(vocab_size, trainable=bool(1-int(train_deep_layer)))
        self.next_token_predictor2 = layers.Dense(vocab_size, trainable=train_deep_layer)
        self.utf = utf
        self.att_q=att_q
        #self.query_layer = layers.Dense(1, name='query_layer')
        
        if isinstance(units, tuple):
            return
        
        # Stacked GRU layers
        self.context_encoders = [
            layers.GRU(units, return_sequences=True,
                       stateful=True,
                       recurrent_initializer='glorot_uniform',
                       name=f'gru__{i}', trainable=bool(1-int(train_deep_layer))) for i in range(n)
        ]
        
        self.dropout=tf.keras.layers.Dropout(0.1)
        self.att_units=att_units
        self.num_heads=nh

        #self.num_heads = find_window  # Number of attention heads
        
        # ...
        
        # Multi-Head Attention
        if use_matt and 0:
            self.multihead_attention = MultiHeadAttention(
                num_heads=nh , key_dim=embedding_dim,#embedding_dim // find_window ,
                            name='multihead_attention', trainable=True)
            self.multihead_attention0 = MultiHeadAttention(
                num_heads=nh , key_dim=embedding_dim,#embedding_dim // find_window ,
                            name='multihead_attention0', trainable=True)
        #attention_output = self.multihead_attention(sequence, sequence)
        self.use_matt=use_matt

        dff = 2 * att_units  # Typically, the inner-layer dimension is 2*att_units
        dropout_rate = 0.1

        # FFN layers
        self.ffn_layers = [
            layers.Dense(att_units, activation='relu'),  # Inner layer with ReLU activation
            layers.Dropout(dropout_rate),
            layers.Dense(att_units),  # Output layer same size as the attention layer
            layers.Dropout(dropout_rate)
        ]
        self.f_d=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh')
        self.f_d2=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh')
        #self.f_d3=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh')
        #self.f_d4=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh')
        

    def call(self, inputs, training=None, use_teacher_forcing=True,):
        if not self.utf:
            use_teacher_forcing = False
        if 1:#self.use_matt:
            #inputs_att = self.multihead_attention0(inputs, inputs)
            
            # Add the attention output to the sequence (Residual Connection)
            inputs_att = inputs#inputs*(1-self.att_q) + inputs_att*self.att_q
        # Embedding
        #embedded_inputs = inputs#self.embedding(inputs)
        input_shape = tf.shape(inputs)
        input_dim = input_shape[-1]
        #print('id',input_dim)
        
        # Create a Dense layer with units equal to the last dimension of the input
        
        # Apply the Dense layer to the inputs
        embedded_inputs = self.f_d(inputs)
        embedded_inputs = self.f_d2(embedded_inputs)
        #embedded_inputs = self.f_d3(embedded_inputs)
        #embedded_inputs = self.f_d4(embedded_inputs)
        
        # Query Weighting
        #query_weights = self.query_layer(embedded_inputs)
        #query_weights = tf.squeeze(query_weights, axis=-1)

        #top_indices = tf.argsort(query_weights, direction='DESCENDING')[:, :self.find_window]
        
        # Combine his and inp
        combined = embedded_inputs#tf.concat([his*self.his_q, inp], axis=1)

        char_level_representation = self.char_gru_layer(embedded_inputs)#(inputs_att)
        # Sequence Encoding with stacked GRUs
        sequence = combined
        #states = [layer.get_initial_state(sequence) for layer in self.context_encoders]

        for i, gru_layer in enumerate(self.context_encoders):
            #sequence, state = gru_layer(sequence)#, initial_state=states[i])
            tmp=gru_layer(sequence)#
            #sequence, state =tmp[0],tmp[1]

        #sequence=self.dropout(tmp)#, training=training)#(sequence)
        sequence_charout = tf.expand_dims(char_level_representation, 1)#sequence*(1-self.wd_q) + self.wd_q * tf.expand_dims(char_level_representation, 1)
        if 0:#self.use_matt:
            attention_output = self.multihead_attention(sequence, sequence)
            
            # Add the attention output to the sequence (Residual Connection)
            sequence = sequence*(1-self.att_q) + attention_output*self.att_q
        for layer in []:#self.ffn_layers:
            sequence = layer(sequence, training=training)
        # Next Token Prediction
        next_token_logits_main = self.next_token_predictor(sequence)
        next_token_logits_charout = self.next_token_predictor2(sequence_charout)
        next_token_logits=next_token_logits_main*(1-self.wd_q) + next_token_logits_charout*self.wd_q
        
        
        return next_token_logits


    def get_config(self):
        config = super(CLModel, self).get_config()
        config.update({
            "vocab_size": self.vocab_size,
            "embedding_dim": self.embedding_dim,
            "find_window": self.find_window,
            "window": self.window,
            "units": self.units,
            "n": self.n,
            "att_units": self.att_units,
            "his_q": self.his_q,
            "nh": self.nh,
            
        })
        return config
    
import tensorflow as tf
from tensorflow.keras import layers
class CLModel(layers.Layer):
    def __init__(self, vocab_size, embedding_dim, #find_window,
                 window,
                 units,
                 batch_size=1,
                 n=1, utf=True,
                 his_q=0.75,
                 use_matt=True,
                 att_q=0.4,
                 att_units=None,
                 n_char=3,
                 wd_q=1.0,
                 nh=8,
                 train_deep_layer=True,
                 train_main=True,
                 num_chargru_layer=8,
                 embed_q=0.5,
                 **kwargs):
        
        super(CLModel, self).__init__(**kwargs)
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        #self.find_window = find_window
        self.window = window
        self.units = units
        self.n = n  # Number of stacked GRU layers
        self.his_q=his_q
        self.next_token_predictor = layers.Dense(vocab_size, trainable=train_main)
        self.styler = layers.Dense(vocab_size, trainable=train_deep_layer)

        self.utf = utf
        self.dropout=tf.keras.layers.Dropout(0.1)
        self.embed_q=embed_q
        #self.train_main=train_main
        
        # Stacked GRU layers
        self.context_encoders = [
            layers.GRU(units, return_sequences=True,
                       stateful=True,
                       recurrent_initializer='glorot_uniform',
                       name=f'gru__{i}', trainable=train_main) for i in range(n)
        ]
        print('Train style',train_deep_layer)
        
        self.f_d=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=train_main)
        #self.f_d_0=tf.keras.layers.Dense(units=self.vocab_size,trainable=train_main)

        self.f_d2=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=train_main)
        #self.f_d2_0=tf.keras.layers.Dense(units=self.vocab_size,trainable=train_main)

        #self.f_d3=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=train_main)
        #self.f_d3_0=tf.keras.layers.Dense(units=self.vocab_size,trainable=train_main)

        #self.f_d4=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=bool(1-int(train_deep_layer)))
        #self.f_d5=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=bool(1-int(train_deep_layer)))
        #self.f_d6=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=bool(1-int(train_deep_layer)))

        
    def call(self, inputs, training=None, use_teacher_forcing=True):  
        # 如果不使用教师强制（Teacher Forcing），则忽略use_teacher_forcing参数  
        if not self.utf:  
            use_teacher_forcing = False  
      
        # Embedding层  
        input_shape = tf.shape(inputs)  
        input_dim = input_shape[-1]  
        embedded_inputs = self.f_d(inputs)
        #embedded_inputs = self.f_d_0(embedded_inputs) 
        embedded_inputs = self.f_d2(embedded_inputs)*self.embed_q+embedded_inputs*(1-self.embed_q)
        #embedded_inputs = self.f_d2_0(embedded_inputs)#*self.embed_q+embedded_inputs*(1-self.embed_q)

        #embedded_inputs = self.dropout(embedded_inputs)+embedded_inputs
        # embedded_inputs = self.f_d3(embedded_inputs)*self.embed_q+embedded_inputs*(1-self.embed_q)
        #embedded_inputs = self.f_d3_0(embedded_inputs)#*self.embed_q+embedded_inputs*(1-self.embed_q)

        #embedded_inputs = self.f_d4(embedded_inputs)*self.embed_q+embedded_inputs*(1-self.embed_q)
        #embedded_inputs = self.dropout(embedded_inputs)+embedded_inputs
        #embedded_inputs = self.f_d5(embedded_inputs)*self.embed_q+embedded_inputs*(1-self.embed_q)
        #embedded_inputs = self.f_d6(embedded_inputs)*self.embed_q+embedded_inputs*(1-self.embed_q)
        
        # 注释掉其他未使用的嵌入层  
      
        # 合并处理（这里没有实际合并，只是保留了embedded_inputs）  
        combined = embedded_inputs  
      
        # 使用GRU进行序列编码  
        sequence = combined  
        for gru_layer in self.context_encoders:  
            sequence = gru_layer(sequence)  
      
      
        # 下一个标记的预测  
        next_token_logits = self.next_token_predictor(sequence)
        next_token_logits = self.styler(next_token_logits)
        
      
        return next_token_logits


    def get_config(self):
        config = super(CLModel, self).get_config()
        config.update({
            "vocab_size": self.vocab_size,
            "embedding_dim": self.embedding_dim,
            "find_window": self.find_window,
            "window": self.window,
            "units": self.units,
            "n": self.n,
            "att_units": self.att_units,
            "his_q": self.his_q,
            "nh": self.nh,
            
        })
        return config

class DeepEncodingLayer(tf.keras.layers.Layer):
    def __init__(self, encoding_units, **kwargs):
        super(DeepEncodingLayer, self).__init__(**kwargs)
        self.encoding_units = encoding_units
        self.positional_encoding = None
        self.adaptive_filters = None
        self.feature_enhancer = None

    def build(self, input_shape):
        # 初始化位置编码
        self.positional_encoding = self.add_weight(shape=(input_shape[1], input_shape[2]),
                                                   initializer='uniform',
                                                   trainable=True,
                                                   name='positional_encoding')
        
        # 初始化自适应滤波器
        self.adaptive_filters = self.add_weight(shape=(input_shape[2], self.encoding_units),
                                                initializer='glorot_uniform',
                                                trainable=True,
                                                name='adaptive_filters')
        
        # 初始化特征增强层
        self.feature_enhancer = tf.keras.layers.Dense(input_shape[2],
                                                      activation='sigmoid',
                                                      name='feature_enhancer')

    def call(self, inputs):
        # 添加位置编码
        positional_inputs = inputs + self.positional_encoding
        
        # 自适应滤波
        filtered_inputs = tf.tensordot(positional_inputs, self.adaptive_filters, axes=1)
        
        # 特征增强
        enhanced_features = self.feature_enhancer(filtered_inputs)
        
        # 结合原始输入和增强特征
        outputs = enhanced_features * inputs + (1 - enhanced_features) * positional_inputs
        
        return outputs
import tensorflow as tf

class DeepEncodingLayer(tf.keras.layers.Layer):
    def __init__(self, encoding_units, max_sequence_length=512, **kwargs):
        super(DeepEncodingLayer, self).__init__(**kwargs)
        self.encoding_units = encoding_units
        self.max_sequence_length = max_sequence_length
        self.positional_encoding = None
        self.adaptive_filters = None
        self.feature_enhancer = None

    def build(self, input_shape):
        # 初始化位置编码
        self.positional_encoding = self.add_weight(
            shape=(self.max_sequence_length, input_shape[-1]),
            initializer='uniform',
            trainable=True,
            name='positional_encoding'
        )
        
        # 初始化自适应滤波器
        self.adaptive_filters = self.add_weight(
            shape=(input_shape[-1], self.encoding_units),
            initializer='glorot_uniform',
            trainable=True,
            name='adaptive_filters'
        )
        
        # 初始化特征增强层
        self.feature_enhancer = tf.keras.layers.Dense(
            input_shape[-1],
            activation='sigmoid',
            name='feature_enhancer'
        )

    def call(self, inputs):
        # 获取输入的实际序列长度
        sequence_length = tf.shape(inputs)[1]
        
        # 根据实际序列长度截取位置编码
        positional_encoding = self.positional_encoding[:sequence_length, :]
        positional_inputs = inputs + positional_encoding
        
        # 自适应滤波
        filtered_inputs = tf.tensordot(positional_inputs, self.adaptive_filters, axes=1)
        
        # 特征增强
        enhanced_features = self.feature_enhancer(filtered_inputs)
        
        # 结合原始输入和增强特征
        outputs = enhanced_features * inputs + (1 - enhanced_features) * positional_inputs
        
        return outputs

import tensorflow as tf
from tensorflow.keras import layers




class TokenAttentionLayer_test(layers.Layer):
    def __init__(self, n_heads, alpha=0.45, **kwargs):
        super(TokenAttentionLayer_test, self).__init__(**kwargs)
        self.n_heads = n_heads
        self.alpha = alpha
        self.dense=layers.Dense(self.n_heads)
        self.alpha_dense=layers.Dense(self.n_heads, activation='sigmoid')
    
    def build(self, input_shape):
        # Ensure the input shape is compatible with our operations.
        assert len(input_shape) >= 2, "Input must be at least 2D (batch_size, sequence_length, ...)"

    def call(self, inputs):
        # Assuming inputs shape is (batch_size, sequence_length, embedding_dim)
        # First, pass through a dense layer to get attentions for each token
        attentions = self.dense(inputs)
        
        # Softmax to get normalized weights between 0 and 1
        attentions = tf.nn.softmax(attentions, axis=-1)
        
        # Get top n_heads attentions and their indices
        top_attentions = tf.math.top_k(attentions, k=self.n_heads)
        q_values = top_attentions.values  # Shape (batch_size, sequence_length, n_heads)
        att_indices = top_attentions.indices  # Shape (batch_size, sequence_length, n_heads)

        # Gather the corresponding tokens based on the indices
        batch_range = tf.range(tf.shape(inputs)[0])
        batch_range = tf.expand_dims(batch_range, axis=1)
        batch_range = tf.expand_dims(batch_range, axis=2)
        batch_range = tf.tile(batch_range, [1, tf.shape(inputs)[1], self.n_heads])

        # Gather tokens using the indices and batch range
        token_atts = tf.gather_nd(inputs, tf.stack([batch_range, att_indices], axis=-1))
        
        # Predict dynamic alpha values for each token
        alpha_values = self.alpha_dense(inputs)  # sigmoid to keep alpha between 0 and 1
        
        # Compute new token values with the given formula
        new_tokens = []
        for i in range(self.n_heads):
            q_i = tf.expand_dims(q_values[:,:,i], axis=-1)
            token_att_i = token_atts[:,:,i,:]
            alpha_i = tf.expand_dims(alpha_values[:,:,i], axis=-1)  # Use predicted alpha
            
            # Calculate the new value for each token
            new_token = inputs * (alpha_i + (1 - q_i) * (1 - alpha_i)) + token_att_i * ((1 - alpha_i) * q_i)
            new_tokens.append(new_token)
        
        # Average the results across heads
        output = tf.reduce_mean(tf.stack(new_tokens, axis=0), axis=0)
        
        return output
    
    def compute_output_shape(self, input_shape):
        return input_shape

###########################
import tensorflow as tf
from tensorflow.keras.layers  import Layer, Dense, Embedding
import tensorflow as tf
from tensorflow.keras import layers

class TokenAttentionLayer(layers.Layer):
    def __init__(self, n_heads, alpha=0.45, **kwargs):
        super(TokenAttentionLayer, self).__init__(**kwargs)
        self.n_heads = n_heads
        self.alpha = alpha
        self.dense=layers.Dense(self.n_heads)
    
    def build(self, input_shape):
        # Ensure the input shape is compatible with our operations.
        assert len(input_shape) >= 2, "Input must be at least 2D (batch_size, sequence_length, ...)"

    def call(self, inputs):
        # Assuming inputs shape is (batch_size, sequence_length, embedding_dim)
        # First, pass through a dense layer to get attentions for each token
        attentions = self.dense(inputs)
        
        # Softmax to get normalized weights between 0 and 1
        attentions = tf.nn.softmax(attentions, axis=-1)
        
        # Get top n_heads attentions and their indices
        top_attentions = tf.math.top_k(attentions, k=self.n_heads)
        q_values = top_attentions.values  # Shape (batch_size, sequence_length, n_heads)
        att_indices = top_attentions.indices  # Shape (batch_size, sequence_length, n_heads)

        # Gather the corresponding tokens based on the indices
        batch_range = tf.range(tf.shape(inputs)[0])
        batch_range = tf.expand_dims(batch_range, axis=1)
        batch_range = tf.expand_dims(batch_range, axis=2)
        batch_range = tf.tile(batch_range, [1, tf.shape(inputs)[1], self.n_heads])

        # Gather tokens using the indices and batch range
        token_atts = tf.gather_nd(inputs, tf.stack([batch_range, att_indices], axis=-1))
        
        # Compute new token values with the given formula
        new_tokens = []
        for i in range(self.n_heads):
            q_i = tf.expand_dims(q_values[:,:,i], axis=-1)
            token_att_i = token_atts[:,:,i,:]
            
            # Calculate the new value for each token
            # 请你修改这里的代
            new_token = inputs * (self.alpha + (1 - q_i) * (1 - self.alpha)) + token_att_i * ((1 - self.alpha) * q_i)
            new_tokens.append(new_token)
        
        # Average the results across heads
        output = tf.reduce_mean(tf.stack(new_tokens, axis=0), axis=0)
        
        return output
    
    def compute_output_shape(self, input_shape):
        return input_shape
#######################################################
import tensorflow as tf
from tensorflow.keras import layers

class TokenAttentionLayer_att(layers.Layer):
    def __init__(self, n_heads, alpha=0.45, **kwargs):
        super(TokenAttentionLayer_att, self).__init__(**kwargs)
        self.n_heads = n_heads
        self.alpha = alpha
        
    def build(self, input_shape):
        self.embedding_dim = input_shape[-1]
        self.W_Q = layers.Dense(self.embedding_dim, use_bias=False)
        self.W_K = layers.Dense(self.embedding_dim, use_bias=False)
        self.W_V = layers.Dense(self.embedding_dim, use_bias=False)
        
        # Ensure the input shape is compatible with our operations.
        assert len(input_shape) >= 2, "Input must be at least 2D (batch_size, sequence_length, ...)"

    def call(self, inputs):
        # Assuming inputs shape is (batch_size, sequence_length, embedding_dim)
        Q = self.W_Q(inputs)  # Queries
        K = self.W_K(inputs)  # Keys
        V = self.W_V(inputs)  # Values

        # Scale dot product attention scores
        scores = tf.matmul(Q, K, transpose_b=True) / tf.math.sqrt(tf.cast(self.embedding_dim, tf.float32))

        # Apply softmax to get attention weights
        attentions = tf.nn.softmax(scores, axis=-1)
        
        # Get top n_heads attentions and their indices
        top_attentions = tf.math.top_k(attentions, k=self.n_heads)
        q_values = top_attentions.values  # Shape (batch_size, sequence_length, n_heads)
        att_indices = top_attentions.indices  # Shape (batch_size, sequence_length, n_heads)

        # Gather the corresponding tokens based on the indices
        batch_range = tf.range(tf.shape(inputs)[0])
        batch_range = tf.expand_dims(batch_range, axis=1)
        batch_range = tf.expand_dims(batch_range, axis=2)
        batch_range = tf.tile(batch_range, [1, tf.shape(inputs)[1], self.n_heads])

        # Gather tokens using the indices and batch range
        token_atts = tf.gather_nd(V, tf.stack([batch_range, att_indices], axis=-1))
        
        # Compute new token values with the given formula
        new_tokens = []
        for i in range(self.n_heads):
            q_i = tf.expand_dims(q_values[:,:,i], axis=-1)
            token_att_i = token_atts[:,:,i,:]
            
            # Calculate the new value for each token
            new_token = inputs * (self.alpha + (1 - q_i) * (1 - self.alpha)) + token_att_i * ((1 - self.alpha) * q_i)
            new_tokens.append(new_token)
        
        # Average the results across heads
        output = tf.reduce_mean(tf.stack(new_tokens, axis=0), axis=0)
        
        return output
    
    def compute_output_shape(self, input_shape):
        return input_shape

import tensorflow as tf
from tensorflow.keras import layers
class CLModel_3_1_1(layers.Layer):
    def __init__(self, vocab_size, embedding_dim, #find_window,
                 window,
                 units,
                 batch_size=1,
                 n=1, utf=True,
                 his_q=0.75,
                 use_matt=True,
                 att_q=0.4,
                 att_units=None,
                 n_char=3,
                 wd_q=1.0,
                 nh=8,
                 train_deep_layer=True,
                 train_main=True,
                 num_chargru_layer=8,
                 embed_q=0.5,
                 **kwargs):
        
        super(CLModel_3_1_1, self).__init__(**kwargs)
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        #self.find_window = find_window
        self.window = window
        self.units = units
        self.n = n  # Number of stacked GRU layers
        self.his_q=his_q
        self.next_token_predictor = layers.Dense(vocab_size, trainable=train_main)
        self.styler = layers.Dense(vocab_size, trainable=train_deep_layer)
        self.deep_encoding_layer=DeepEncodingLayer(encoding_units=embedding_dim)
        
        self.utf = utf
        self.dropout=tf.keras.layers.Dropout(0.1)
        self.embed_q=embed_q
        #self.train_main=train_main
        
        # Stacked GRU layers
        self.context_encoders = [
            layers.GRU(units, return_sequences=True,
                       stateful=True,
                       recurrent_initializer='glorot_uniform',
                       name=f'gru__{i}', trainable=train_main) for i in range(n)
        ]
        print('Train style',train_deep_layer)
        
        self.f_d=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=train_main)
        self.f_d_0=tf.keras.layers.Dense(units=self.vocab_size,trainable=train_main)

        self.f_d2=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=train_main)
        self.f_d2_0=tf.keras.layers.Dense(units=self.vocab_size,trainable=train_main)

        #self.f_d3=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=train_main)
        #self.f_d3_0=tf.keras.layers.Dense(units=self.vocab_size,trainable=train_main)

        #self.f_d4=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=bool(1-int(train_deep_layer)))
        #self.f_d5=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=bool(1-int(train_deep_layer)))
        #self.f_d6=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=bool(1-int(train_deep_layer)))
        #self.multihead_attention = MultiHeadAttention(
        #        num_heads=8 , key_dim=256,#embedding_dim // find_window ,
        #                    name='multihead_attention0', trainable=True)
        self.lnl=LayerNormalization(epsilon=1e-6)
        self.lnl0=LayerNormalization(epsilon=1e-6)
        self.lnl1=LayerNormalization(epsilon=1e-6)
        #self.TokenAttention_=TokenAttentionLayer()
        
        
        
    def call(self, inputs, training=None, use_teacher_forcing=True):  
        # 如果不使用教师强制（Teacher Forcing），则忽略use_teacher_forcing参数  
        if not self.utf:  
            use_teacher_forcing = False  

        #inputs = self.TokenAttention_(inputs)
        
        # Embedding层  
        input_shape = tf.shape(inputs)  
        input_dim = input_shape[-1]  
        embedded_inputs = self.f_d(inputs)
        embedded_inputs=self.lnl0(embedded_inputs)
        #embedded_inputs = self.f_d_0(embedded_inputs) 
        embedded_inputs = self.f_d2(embedded_inputs)*self.embed_q+embedded_inputs*(1-self.embed_q)
        #embedded_inputs = self.f_d2_0(embedded_inputs)
        #embedded_inputs = self.f_d3(embedded_inputs)*self.embed_q+embedded_inputs*(1-self.embed_q)
        #embedded_inputs = self.f_d3_0(embedded_inputs)#*self.embed_q+embedded_inputs*(1-self.embed_q)

        #embedded_inputs = self.f_d4(embedded_inputs)*self.embed_q+embedded_inputs*(1-self.embed_q)
        #embedded_inputs = self.dropout(embedded_inputs)+embedded_inputs
        #embedded_inputs = self.f_d5(embedded_inputs)*self.embed_q+embedded_inputs*(1-self.embed_q)
        #embedded_inputs = self.f_d6(embedded_inputs)*self.embed_q+embedded_inputs*(1-self.embed_q)
        embedded_inputs=self.lnl1(embedded_inputs)
        
        # 注释掉其他未使用的嵌入层  
      
        # 合并处理（这里没有实际合并，只是保留了embedded_inputs）  
        combined = embedded_inputs  
      
        # 使用GRU进行序列编码  
        sequence = combined
        #sequence = self.multihead_attention(sequence, sequence)
        for gru_layer in self.context_encoders:  
            sequence = gru_layer(sequence)
            sequence=self.lnl(sequence)
      
      
        # 下一个标记的预测  
        next_token_logits = self.next_token_predictor(sequence)
        
        next_token_logits = self.styler(next_token_logits)
        
      
        return next_token_logits


    def get_config(self):
        config = super(CLModel, self).get_config()
        config.update({
            "vocab_size": self.vocab_size,
            "embedding_dim": self.embedding_dim,
            "find_window": self.find_window,
            "window": self.window,
            "units": self.units,
            "n": self.n,
            "att_units": self.att_units,
            "his_q": self.his_q,
            "nh": self.nh,
            
        })
        return config
   
import tensorflow as tf
from tensorflow.keras import layers
class CLModel_3_1_1_tka(layers.Layer):
    def __init__(self, vocab_size, embedding_dim, #find_window,
                 window,
                 units,
                 batch_size=1,
                 n=1, utf=True,
                 his_q=0.75,
                 use_matt=True,
                 att_q=0.4,
                 att_units=None,
                 n_char=3,
                 wd_q=1.0,
                 nh=8,
                 train_deep_layer=True,
                 train_main=True,
                 num_chargru_layer=8,
                 embed_q=0.5,
                 pre_mode=False,
                 **kwargs):
        
        super(CLModel_3_1_1_tka, self).__init__(**kwargs)
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        #self.find_window = find_window
        self.window = window
        self.units = units
        self.n = n  # Number of stacked GRU layers
        self.his_q=his_q
        self.next_token_predictor = layers.Dense(vocab_size, trainable=train_main)
        self.styler = layers.Dense(vocab_size, trainable=train_deep_layer)
        self.deep_encoding_layer=DeepEncodingLayer(encoding_units=embedding_dim)
        
        self.utf = utf
        self.dropout=tf.keras.layers.Dropout(0.1)
        self.embed_q=embed_q
        #self.train_main=train_main
        
        # Stacked GRU layers
        self.context_encoders = [
            layers.GRU(units, return_sequences=True,
                       stateful=True,
                       recurrent_initializer='glorot_uniform',
                       name=f'gru__{i}', trainable=train_main) for i in range(n)
        ]
        print('Train style',train_deep_layer)
        
        self.f_d=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=train_main)
        self.f_d_0=tf.keras.layers.Dense(units=self.vocab_size,trainable=train_main)

        self.f_d2=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=train_main)
        self.f_d2_0=tf.keras.layers.Dense(units=self.vocab_size,trainable=train_main)

        #self.f_d3=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=train_main)
        #self.f_d3_0=tf.keras.layers.Dense(units=self.vocab_size,trainable=train_main)

        #self.f_d4=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=bool(1-int(train_deep_layer)))
        #self.f_d5=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=bool(1-int(train_deep_layer)))
        #self.f_d6=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=bool(1-int(train_deep_layer)))
        #self.multihead_attention = MultiHeadAttention(
        #        num_heads=8 , key_dim=256,#embedding_dim // find_window ,
        #                    name='multihead_attention0', trainable=True)
        self.lnl=LayerNormalization(epsilon=1e-6)
        #self.lnl0=LayerNormalization(epsilon=1e-6)
        #self.lnl1=LayerNormalization(epsilon=1e-6)
        self.TokenAttention_=TokenAttentionLayer(n_heads=8)
        self.pre_mode=pre_mode
        
        
        
    def call(self, inputs, training=None, use_teacher_forcing=True):  
        # 如果不使用教师强制（Teacher Forcing），则忽略use_teacher_forcing参数  
        if not self.utf:  
            use_teacher_forcing = False  

        #print(inputs.shape)
        if 1:#inputs.shape[1]!=None:
            inputs = self.TokenAttention_(inputs)
            #print('NoError')
        else:
            pass#print('Error')
        
        
        # Embedding层  
        input_shape = tf.shape(inputs)  
        input_dim = input_shape[-1]  
        embedded_inputs = self.f_d(inputs)
        #embedded_inputs=self.lnl0(embedded_inputs)
        #embedded_inputs = self.f_d_0(embedded_inputs) 
        embedded_inputs = self.f_d2(embedded_inputs)*self.embed_q+embedded_inputs*(1-self.embed_q)
        #embedded_inputs = self.f_d2_0(embedded_inputs)
        #embedded_inputs = self.f_d3(embedded_inputs)*self.embed_q+embedded_inputs*(1-self.embed_q)
        #embedded_inputs = self.f_d3_0(embedded_inputs)#*self.embed_q+embedded_inputs*(1-self.embed_q)

        #embedded_inputs = self.f_d4(embedded_inputs)*self.embed_q+embedded_inputs*(1-self.embed_q)
        #embedded_inputs = self.dropout(embedded_inputs)+embedded_inputs
        #embedded_inputs = self.f_d5(embedded_inputs)*self.embed_q+embedded_inputs*(1-self.embed_q)
        #embedded_inputs = self.f_d6(embedded_inputs)*self.embed_q+embedded_inputs*(1-self.embed_q)
        #embedded_inputs=self.lnl1(embedded_inputs)
        
        # 注释掉其他未使用的嵌入层  
      
        # 合并处理（这里没有实际合并，只是保留了embedded_inputs）  
        combined = embedded_inputs  
      
        # 使用GRU进行序列编码  
        sequence = combined
        #sequence = self.multihead_attention(sequence, sequence)
        for gru_layer in self.context_encoders:  
            sequence = gru_layer(sequence)
            sequence=self.lnl(sequence)
      
      
        # 下一个标记的预测  
        next_token_logits = self.next_token_predictor(sequence)
        
        next_token_logits = self.styler(next_token_logits)
        
      
        return next_token_logits


    def get_config(self):
        config = super(CLModel, self).get_config()
        config.update({
            "vocab_size": self.vocab_size,
            "embedding_dim": self.embedding_dim,
            "find_window": self.find_window,
            "window": self.window,
            "units": self.units,
            "n": self.n,
            "att_units": self.att_units,
            "his_q": self.his_q,
            "nh": self.nh,
            
        })
        return config
    


import tensorflow as tf
from tensorflow.keras import layers
class CLModel_3_2(layers.Layer):
    def __init__(self, vocab_size, embedding_dim, #find_window,
                 window,
                 units,
                 batch_size=1,
                 n=1, utf=True,
                 his_q=0.75,
                 use_matt=True,
                 att_q=0.4,
                 att_units=None,
                 n_char=3,
                 wd_q=1.0,
                 nh=8,
                 train_deep_layer=True,
                 train_main=True,
                 num_chargru_layer=8,
                 embed_q=0.5,
                 **kwargs):
        
        super(CLModel_3_2, self).__init__(**kwargs)
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        #self.find_window = find_window
        self.window = window
        self.units = units
        self.n = n  # Number of stacked GRU layers
        self.his_q=his_q
        self.next_token_predictor = layers.Dense(vocab_size, trainable=train_main)
        self.styler = layers.Dense(vocab_size, trainable=train_deep_layer)
        self.deep_encoding_layer=None#DeepEncodingLayer(encoding_units=embedding_dim)
        
        self.utf = utf
        self.dropout=tf.keras.layers.Dropout(0.1)
        self.embed_q=embed_q
        #self.train_main=train_main
        
        # Stacked GRU layers
        self.context_encoders = [
            layers.GRU(units, return_sequences=True,
                       stateful=True,
                       recurrent_initializer='glorot_uniform',
                       name=f'gru__{i}', trainable=train_main) for i in range(n)
        ]
        print('Train style',train_deep_layer)
        
        self.f_d=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=train_main)
        self.f_d_0=tf.keras.layers.Dense(units=self.vocab_size,trainable=train_main)

        self.f_d2=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=train_main)
        self.f_d2_0=tf.keras.layers.Dense(units=self.vocab_size,trainable=train_main)

        #self.f_d3=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=train_main)
        #self.f_d3_0=tf.keras.layers.Dense(units=self.vocab_size,trainable=train_main)

        #self.f_d4=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=bool(1-int(train_deep_layer)))
        #self.f_d5=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=bool(1-int(train_deep_layer)))
        #self.f_d6=tf.keras.layers.Dense(units=self.vocab_size, activation='tanh', trainable=bool(1-int(train_deep_layer)))
        #self.multihead_attention = MultiHeadAttention(
        #        num_heads=8 , key_dim=256,#embedding_dim // find_window ,
        #                    name='multihead_attention0', trainable=True)
        self.lnl=LayerNormalization(epsilon=1e-6)
        self.lnl0=LayerNormalization(epsilon=1e-6)
        self.lnl1=LayerNormalization(epsilon=1e-6)
        #self.TokenAttention_=TokenAttentionLayer()
        
        
        
    def call(self, inputs, training=None, use_teacher_forcing=True):  
        # 如果不使用教师强制（Teacher Forcing），则忽略use_teacher_forcing参数  
        if not self.utf:  
            use_teacher_forcing = False  

        #inputs = self.TokenAttention_(inputs)
        
        # Embedding层  
        input_shape = tf.shape(inputs)  
        input_dim = input_shape[-1]  
        embedded_inputs = self.f_d(inputs)
        embedded_inputs=self.lnl0(embedded_inputs)
        #embedded_inputs = self.f_d_0(embedded_inputs) 
        embedded_inputs = self.f_d2(embedded_inputs)*self.embed_q+embedded_inputs*(1-self.embed_q)
        #embedded_inputs = self.f_d2_0(embedded_inputs)
        #embedded_inputs = self.f_d3(embedded_inputs)*self.embed_q+embedded_inputs*(1-self.embed_q)
        #embedded_inputs = self.f_d3_0(embedded_inputs)#*self.embed_q+embedded_inputs*(1-self.embed_q)

        #embedded_inputs = self.f_d4(embedded_inputs)*self.embed_q+embedded_inputs*(1-self.embed_q)
        #embedded_inputs = self.dropout(embedded_inputs)+embedded_inputs
        #embedded_inputs = self.f_d5(embedded_inputs)*self.embed_q+embedded_inputs*(1-self.embed_q)
        #embedded_inputs = self.f_d6(embedded_inputs)*self.embed_q+embedded_inputs*(1-self.embed_q)
        embedded_inputs=self.lnl1(embedded_inputs)
        
        # 注释掉其他未使用的嵌入层  
      
        # 合并处理（这里没有实际合并，只是保留了embedded_inputs）  
        combined = embedded_inputs  
      
        # 使用GRU进行序列编码  
        sequence = combined
        #sequence = self.multihead_attention(sequence, sequence)
        for gru_layer in self.context_encoders:  
            sequence = gru_layer(sequence)
            sequence=self.lnl(sequence)
      
      
        # 下一个标记的预测  
        next_token_logits = self.next_token_predictor(sequence)
        
        next_token_logits = self.styler(next_token_logits)
        
      
        return next_token_logits


    def get_config(self):
        config = super(CLModel, self).get_config()
        config.update({
            "vocab_size": self.vocab_size,
            "embedding_dim": self.embedding_dim,
            "find_window": self.find_window,
            "window": self.window,
            "units": self.units,
            "n": self.n,
            "att_units": self.att_units,
            "his_q": self.his_q,
            "nh": self.nh,
            
        })
        return config

    import tensorflow as tf
from tensorflow.keras import layers

class CLModel_40_1(layers.Layer):
    def __init__(self, vocab_size, embedding_dim, window, units, n=1, his_q=0.75, use_matt=True, att_q=0.4, att_units=None, n_char=3, wd_q=1.0, nh=8, train_deep_layer=True, train_main=True, num_chargru_layer=8, embed_q=0.5, **kwargs):
        super(CLModel_40_1, self).__init__(**kwargs)
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.window = window
        self.units = units
        self.n = n  # Number of stacked GRU layers
        self.his_q = his_q
        self.use_matt = use_matt
        self.att_q = att_q
        self.att_units = att_units
        self.n_char = n_char
        self.wd_q = wd_q
        self.nh = nh
        self.train_deep_layer = train_deep_layer
        self.train_main = train_main
        self.num_chargru_layer = num_chargru_layer
        self.embed_q = embed_q

        self.next_token_predictor = layers.Dense(vocab_size, trainable=True)
        self.styler = layers.Dense(vocab_size, trainable=True)
        self.dropout = tf.keras.layers.Dropout(0.1)
        self.embedding = layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim)

        # Stacked GRU layers
        self.context_encoders = [
            layers.GRU(units, return_sequences=True, stateful=False, recurrent_initializer='glorot_uniform', name=f'gru_{i}', trainable=True) for i in range(n)
        ]

        self.lnl = layers.LayerNormalization(epsilon=1e-6)
        self.lnl0 = layers.LayerNormalization(epsilon=1e-6)
        self.lnl1 = layers.LayerNormalization(epsilon=1e-6)

    def call(self, inputs, training=None, use_teacher_forcing=True):
        # 嵌入层
        embedded_inputs = inputs#self.embedding(inputs)
        embedded_inputs = self.lnl0(embedded_inputs)
        embedded_inputs = self.dropout(embedded_inputs, training=training)

        # 使用GRU进行序列编码
        sequence = embedded_inputs
        for gru_layer in self.context_encoders:
            sequence = gru_layer(sequence, training=training)
            sequence = self.lnl(sequence)


        return sequence

    def get_config(self):
        config = super(CLModel_40_1, self).get_config()
        config.update({
            "vocab_size": self.vocab_size,
            "embedding_dim": self.embedding_dim,
            "window": self.window,
            "units": self.units,
            "n": self.n,
            "his_q": self.his_q,
            "use_matt": self.use_matt,
            "att_q": self.att_q,
            "att_units": self.att_units,
            "n_char": self.n_char,
            "wd_q": self.wd_q,
            "nh": self.nh,
            "train_deep_layer": self.train_deep_layer,
            "train_main": self.train_main,
            "num_chargru_layer": self.num_chargru_layer,
            "embed_q": self.embed_q
        })
        return config

class TransformerEncoderLayer(layers.Layer):
    def __init__(self, d_model, num_heads, dff, rate=0.1):
        super(TransformerEncoderLayer, self).__init__()
        self.mha = layers.MultiHeadAttention(key_dim=d_model,
                                             num_heads=num_heads)
        self.ffn = tf.keras.Sequential([
            layers.Dense(dff, activation='relu'),  # (Use 'gelu' for BERT-like models)
            layers.Dense(d_model)
        ])

        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)

        self.dropout1 = layers.Dropout(rate)
        self.dropout2 = layers.Dropout(rate)

    def call(self, x, training, mask=None):
        tmp=self.mha(x, x, x, attention_mask=mask)
        attn_output, _ = tmp[0], tmp[1]  # (batch_size, input_seq_len, d_model)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(x + attn_output)  # (batch_size, input_seq_len, d_model)

        ffn_output = self.ffn(out1)  # (batch_size, input_seq_len, d_model)
        ffn_output = self.dropout2(ffn_output, training=training)
        out2 = self.layernorm2(out1 + ffn_output)  # (batch_size, input_seq_len, d_model)

        return out2



import tensorflow as tf
from tensorflow.keras import layers, models

# 一个标准的Transformer模型
class TransformerBlock(layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.1):
        super(TransformerBlock, self).__init__()
        self.att = layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.ffn = models.Sequential([
            layers.Dense(ff_dim, activation="relu"),
            layers.Dense(embed_dim),
        ])
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(rate)
        self.dropout2 = layers.Dropout(rate)

    def call(self, inputs, training):
        attn_output = self.att(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)

# 一个简单的嵌入层
class TokenAndPositionEmbedding(layers.Layer):
    def __init__(self, maxlen, vocab_size, embed_dim):
        super(TokenAndPositionEmbedding, self).__init__()
        self.token_emb = layers.Embedding(input_dim=vocab_size, output_dim=embed_dim)
        self.pos_emb = layers.Embedding(input_dim=maxlen, output_dim=embed_dim)

    def call(self, x):
        maxlen = tf.shape(x)[-1]
        positions = tf.range(start=0, limit=maxlen, delta=1)
        positions = self.pos_emb(positions)
        x = self.token_emb(x)
        return x + positions

# 定义MoE模型
class MoEModel(tf.keras.Model):
    def __init__(self, experts, router, vocab_size, **kwargs):
        super(MoEModel, self).__init__(**kwargs)
        self.experts = experts
        #self.router = router
        self.router_outputs=None
        self.rout_dense=layers.Dense(2, activation='softmax')
        self.next_token_predictor = layers.Dense(vocab_size)
       
        
    def router(self,inputs,rout_dense):
        logits = rout_dense(inputs)
        return logits
        

    def call(self, inputs, training=None, mask=None):
        # 路由机制决定输入应该被分配给哪个专家
        self.router_outputs = self.router(inputs,self.rout_dense)
        print(self.router_outputs)
        # 将输入分配给不同的专家
        expert_outputs = []
        for i, expert in enumerate(self.experts):
            expert_input = inputs * tf.expand_dims(self.router_outputs[:, :, i], -1)
            expert_output = expert(expert_input, training=training)
            expert_outputs.append(expert_output)
        
        # 组合所有专家的输出
        combined_output = tf.reduce_sum(tf.stack(expert_outputs, axis=-1), axis=-1)
        next_token_logits = self.next_token_predictor(combined_output)
        return next_token_logits

# 定义路由机制
def create_router(num_experts):
    def router(inputs):
        logits = layers.Dense(num_experts, activation='softmax')(inputs)
        return logits
    return router

import tensorflow as tf
from tensorflow.keras.layers import Layer, Embedding, GRU

from tensorflow.keras.layers import Layer, Embedding, GRU

class EmbeddingGRULayer(Layer):
    def __init__(self, input_dim, output_dim, **kwargs):
        super(EmbeddingGRULayer, self).__init__(**kwargs)
        self.embedding  = Embedding(input_dim=input_dim, output_dim=output_dim)
        self.gru  = GRU(units=output_dim, return_sequences=True)

    def call(self, inputs):
        embedded_inputs = self.embedding(inputs) 
        gru_output = self.gru(embedded_inputs) 
        return gru_output

class TokenAndPositionEmbedding_40_2(layers.Layer):
    def __init__(self, maxlen, vocab_size, embed_dim):
        super(TokenAndPositionEmbedding_40_2, self).__init__()
        self.token_emb = EmbeddingGRULayer(input_dim=vocab_size, output_dim=embed_dim)
        self.pos_emb = layers.Embedding(input_dim=maxlen, output_dim=embed_dim)

    def call(self, x):
        maxlen = tf.shape(x)[-1]
        positions = tf.range(start=0, limit=maxlen, delta=1)
        positions = self.pos_emb(positions)
        x = self.token_emb(x)
        return x + positions

class TokenAndPositionEmbedding_40_231(layers.Layer):
    def __init__(self, maxlen, vocab_size, embed_dim):
        super(TokenAndPositionEmbedding_40_231, self).__init__()
        self.token_emb = EmbeddingGRULayer(input_dim=vocab_size, output_dim=embed_dim)
        #self.pos_emb = layers.Embedding(input_dim=maxlen, output_dim=embed_dim)

    def call(self, x):
        #maxlen = tf.shape(x)[-1]
        #positions = tf.range(start=0, limit=maxlen, delta=1)
        #positions = self.pos_emb(positions)
        x = self.token_emb(x)
        return x
# 定义MoE模型
class MoEModel_40_2(tf.keras.Model):
    def __init__(self, experts, vocab_size, **kwargs):
        super(MoEModel_40_2, self).__init__(**kwargs)
        self.experts = experts
        #self.router = router
        self.router_outputs=None
        self.rout_dense=layers.Dense(1, activation='softmax')
        self.next_token_predictor = layers.Dense(vocab_size)
       
        
    def router(self,inputs,rout_dense):
        logits = rout_dense(inputs)
        return logits
        

    def call(self, inputs, training=None, mask=None):
        # 路由机制决定输入应该被分配给哪个专家
        #self.router_outputs = self.router(inputs,self.rout_dense)
        #print(self.router_outputs)
        # 将输入分配给不同的专家
        expert_outputs = []
        for i, expert in enumerate(self.experts):
            expert_input = inputs #* tf.expand_dims(self.router_outputs[:, :, i], -1)
            expert_output = expert(expert_input, training=training)
            expert_outputs.append(expert_output)
        
        # 组合所有专家的输出
        combined_output = tf.reduce_sum(tf.stack(expert_outputs, axis=-1), axis=-1)
        next_token_logits = self.next_token_predictor(combined_output)
        return next_token_logits
    

import numpy as np
import os
import json
from datetime import datetime
import tensorflow as tf
from tensorflow.keras import backend as K 
import time
import pickle

import requests
tf.compat.v1.enable_eager_execution()

import numpy as np
import tensorflow as tf
import msgpack
import requests
import time
from tensorflow.python.ops.numpy_ops import np_config

class CLModel_41_1(layers.Layer):
    def __init__(self, vocab_size, embedding_dim, window, units, n=1, his_q=0.75, use_matt=True, att_q=0.4, att_units=None, n_char=3, wd_q=1.0, nh=8, train_deep_layer=True, train_main=True, num_chargru_layer=8, embed_q=0.5, **kwargs):
        super(CLModel_41_1, self).__init__(**kwargs)
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.window = window
        self.units = units
        self.n = n  # Number of stacked GRU layers
        self.his_q = his_q
        self.use_matt = use_matt
        self.att_q = att_q
        self.att_units = att_units
        self.n_char = n_char
        self.wd_q = wd_q
        self.nh = nh
        self.train_deep_layer = train_deep_layer
        self.train_main = train_main
        self.num_chargru_layer = num_chargru_layer
        self.embed_q = embed_q

        self.next_token_predictor = layers.Dense(vocab_size, trainable=True)
        self.styler = layers.Dense(vocab_size, trainable=True)
        self.dropout = tf.keras.layers.Dropout(0.1)
        self.embedding = layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim)

        # Stacked GRU layers
        self.context_encoders = [
            CustomGRU(units, return_sequences=True, stateful=False, recurrent_initializer='glorot_uniform', name=f'gru_{i}', trainable=True) for i in range(n)
        ]

        self.lnl = layers.LayerNormalization(epsilon=1e-6)
        self.lnl0 = layers.LayerNormalization(epsilon=1e-6)
        self.lnl1 = layers.LayerNormalization(epsilon=1e-6)

    def call(self, inputs, training=None, use_teacher_forcing=True):
        # 嵌入层
        embedded_inputs = inputs#self.embedding(inputs)
        embedded_inputs = self.lnl0(embedded_inputs)
        embedded_inputs = self.dropout(embedded_inputs, training=training)

        # 使用GRU进行序列编码
        sequence = embedded_inputs
        for gru_layer in self.context_encoders:
            sequence = gru_layer(sequence, training=training)
            sequence = self.lnl(sequence)


        return sequence

    def get_config(self):
        config = super(CLModel_40_1, self).get_config()
        config.update({
            "vocab_size": self.vocab_size,
            "embedding_dim": self.embedding_dim,
            "window": self.window,
            "units": self.units,
            "n": self.n,
            "his_q": self.his_q,
            "use_matt": self.use_matt,
            "att_q": self.att_q,
            "att_units": self.att_units,
            "n_char": self.n_char,
            "wd_q": self.wd_q,
            "nh": self.nh,
            "train_deep_layer": self.train_deep_layer,
            "train_main": self.train_main,
            "num_chargru_layer": self.num_chargru_layer,
            "embed_q": self.embed_q
        })
        return config

        

if 1:
    def build_model(vocab_size, embedding_dim, rnn_units,
                    batch_size,mt=2.2,window=128,
                    ):
      #global mt
      if mt==1 or mt==2 or mt==0.01 or mt==0.022:#旧模型
        model = tf.keras.Sequential([
            tf.keras.layers.Embedding(vocab_size, embedding_dim,
                                      batch_input_shape=[batch_size, None]),
            tf.keras.layers.GRU(rnn_units,
                                return_sequences=True,
                                stateful=True,
                                recurrent_initializer='glorot_uniform'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(vocab_size)
          ])
        return model
      elif  mt==40.231 or mt==40.232:
        # 参数设置
        maxlen = window
        #vocab_size = 20000
        embed_dim = embedding_dim

        num_experts = 1

        # 创建专家
        expert1 = CLModel_40_1(vocab_size=vocab_size,
                    embedding_dim=embedding_dim,
                    #find_window=rnn_units['find_window'],
                    window=window,
                    units=rnn_units['rnn_units'],
                    #utf=False,
                    batch_size=batch_size,
                    embed_q=rnn_units['embed_q'],
                    
                    )
        
        #TransformerBlock(embed_dim, num_heads, ff_dim)
        experts = [expert1]

        # 创建路由机制
        router = create_router(num_experts)

        # 创建MoE模型
        moe_model = MoEModel_40_2(experts, vocab_size)

        # 输入层
        input_layer = layers.Input(shape=(None,))
        x = TokenAndPositionEmbedding_40_231(maxlen, vocab_size, embed_dim)(input_layer)
        output = moe_model(x)

        # 构建完整模型
        model = tf.keras.Model(inputs=input_layer, outputs=output)
        return model

      else:
            raise Exception('MT Error!')
