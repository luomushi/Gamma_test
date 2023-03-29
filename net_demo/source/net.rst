3.Net调试
=============
**3.1参数配置**:
    参数的配置与 第2页Pid调试2.1. 参数配置 相同，这里就不做赘述。
    :doc:`如有需要点此查看详情<../pid>`

**3.2网络模型库**:
    .. code-block:: python
        :emphasize-lines: 3-14
        :linenos:

        srcData_668nits = [

            771,665,841,441.500807,465.493631,559.137249,
            771,665,911,473.867607,464.221478,814.854431,
            771,665,981,510.717535,463.069248,1105.271816,
            771,725,841,480.752277,625.001764,555.071449,
            771,725,911,512.772274,621.381092,808.318138,
            771,725,981,548.329830,616.283417,1094.490414,
            771,785,841,523.064184,797.157526,550.392056,
            ..................
            #由于数据太多这里就不全部展开
            71,60,83,0.004032,0.002454,0.000049,
            71,60,167,0.009334,0.006371,-0.000043,
            71,60,237,0.040985,0.039362,0.009906,

        ]

.. attention:: 

    将pid调试后跑出来的模型替换掉上面的模型库（黄色部分），其他不变。


**3.3 Net调试**::

     - 函数说明: 

        def Gamma2_2_Net(gaDe,srcData,startReg=None,GAMMA_LEVEL=None,NumMax=50,setReg=None):
        
        参数：
            gaDe : 默认配置参数
            srcData  :  网络模型库名称，（从网络模型库中获取对应的数据）
            startReg :  设置初始RGB的值,可设可不设
            GAMMA_LEVEL :  绑点
            NumMax  :  每阶调试的次数，（默认50）
            setReg  :  写入寄存器的函数接口
        返回 :
            -1 : 调试失败
            outData : 调试成功则返回RGB的值           
        
    - 使用实例:
       outdates = Gamma2_2_Net(gaDe,srcData_668nits,GAMMA_LEVEL=GAMMA_LEVEL,NumMax=120,setReg = set_255_668nits)

.. hint:: 

    该函数已经封装到run_net的函数，在调试Gamam的过程中不需要外部调用。


**3.4 跑 Net**::

    - 函数说明: 

        def run_net():
        
        参数：无
        返回 :无

    - 使用实例:

       run_net()
.. note:: 

    调用函数前需要将以下部分配置全部好


    .. code-block:: python
        :emphasize-lines: 0-28
        :linenos:

        #默认的参数配置：
        gaDe = GammaDesc()
        gaDe.maxLv = 668 #目标亮度
        # gaDe.zeroLv = zeroxyz[0][2] #暗态亮度值(需要的客户赋值,不需要的设置为None)
        gaDe.zeroLv = None  # 不需要的设置为None)

        gaDe.gamma = 2.2 #目标gamma
        gaDe.x = 0.300  #目标x
        gaDe.y = 0.320  #目标y

        gaDe.register_max = 1023 #寄存器最大值
        gaDe.register_min =0     #寄存器最小值

        gaDe.pass_positive_dGamma = 0.03 #客户+gamma
        gaDe.pass_minus_dGamma = 0.03 #客户-gamma
        gaDe.calculate_positive_dGamma = 0.028 #my+gamma
        gaDe.calculate_minus_dGamma = 0.028 #my-gamma

        gaDe.pass_positive_dxy = 0.00135 #客户+xy
        gaDe.pass_minus_dxy = 0.00135    #客户-xy
        gaDe.calculate_positive_dxy =0.0013 #my+xy
        gaDe.calculate_minus_dxy =0.0013    #my-xy

        gaDe.dEMax = 0.5 #DE

        gaDe.gamma_err = 0.3  #上下两阶gamma限制(255不要用)
        #gaDe.special_value = 255 #有特殊要求的相邻两阶的值寄存器的值不超过多少的可以卡控一下


        GAMMA_LEVEL = [255, 223, 191, 159, 127, 111, 95, 79, 71, 63, 55, 47, 39, 35, 31, 27, 23, 19, 15, 11, 7, 5, 3, 1] #绑点对应灰阶值

        #每阶独立的参数配置，如255阶：
                                 #是否要调, 基础卡亮度   加强卡亮度  基础gamma卡控    加强gamma卡控  是否要和上阶gamma值进行约束    基础卡色坐标        加强卡色坐标       de卡控  设置的值,每次都会GRB减这个值
        gaDe.ld[255] = GammaLevelDesc(1,   3.34, 3.34,   3,   3,   None, None,      None, None,              None,          0.00135, 0.00135,  0.00130, 0.00130,    0.5,      None)
    
        gaDe.ld[127] = GammaLevelDesc(1, None,None,None,None, 0.03,0.03,0.01,0.01,  None,  0.00135,0.00135,0.00130, 0.00130,0.65,None)
        gaDe.ld[111] = GammaLevelDesc(1, None,None,None,None, 0.03,0.03,0.01,0.01,  None,  0.00135,0.00135,0.00130, 0.00130,0.8,None)
        gaDe.ld[95]  = GammaLevelDesc(1, None,None,None,None, 0.03,0.03,0.01,0.01,  None,  0.00135,0.00135,0.00130, 0.00130,0.8,None)
        # gaDe.ld[47]  = GammaLevelDesc(1, None,None,None,None, 0.03,0.03,0.01,0.01,  None,  0.00135,0.00135,0.00130, 0.00130,0.8,None)

        gaDe.ld[23] = GammaLevelDesc(1,None,None,None,None,0.03,0.03,0.01,0.01,None,0.0015,0.0015,0.0012,0.0012,0.5,None)
        gaDe.ld[19] = GammaLevelDesc(1,None,None,None,None,0.03,0.03,0.01,0.01,None,0.0015,0.0015,0.0012,0.0012,0.5,None)


        gaDe.ld[15] = GammaLevelDesc(1,None,None,None,None,0.03,0.03,0.01,0.01,None,0.0018,0.0018,0.0012,0.0012,0.7,None)
        gaDe.ld[11] = GammaLevelDesc(1,None,None,None,None,0.03,0.03,0.01,0.01,None,0.0018,0.0018,0.0011,0.0011,0.7,None)

        gaDe.ld[7] = GammaLevelDesc(1,None,None,None,None,0.03,0.03,0.02,0.01, None, 0.008,0.008,0.006,0.006,None,None)
        gaDe.ld[5] = GammaLevelDesc(1,None,None,None,None,0.09,0.09,0.08,0.09, None, None,None,None,None,None,None)
        gaDe.ld[3] = GammaLevelDesc(1,None,None,None,None,0.09,0.09,0.08,0.09, None, None,None,None,None,None,None)
        gaDe.ld[1] = GammaLevelDesc(1,None,None,None,None,0.09,0.09,0.08,0.09, None, None,None,None,None,None, 3)

        #函数配置示例：         
        outdates = Gamma2_2_Net(gaDe,srcData_668nits,GAMMA_LEVEL=GAMMA_LEVEL,NumMax=120,setReg = set_255_668nits)

**3.5. 使用示例** ::

    # 初始化镜头
    CA410_Init(1)
    # 跑Net
    run_net()
