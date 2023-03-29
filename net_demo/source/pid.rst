2.Pid调试
=============
**2.1. 参数配置：** 
    .. code-block:: python
        :emphasize-lines: 0-33
        :linenos:

        class GammaDesc:
            maxLv = None
            zeroLv = None
            gamma = None
            
            x = None
            y = None
            dEMax = None                #DE 的卡控制

            count_flag = 1              #某一阶是否要调 ,默认全调 =1此阶要调 , = 0 此阶不调,跳过此阶
            
            register_max = None    #寄存器设置的最大值
            register_min = None    #寄存器设置的最小值

            special_value = None   #对于只卡gamma2.2的, 不对色坐标有要求的,调不过时 可以设置这个,设置的值,每次都会GRB减这个值
            gamma_err = None #是否要和上阶gamma值进行约束,如果需要请设置值,约束值,是上阶的gamma2.2值与此阶gamma2.2的差值
            register_difference = 255 #类似云英谷之类的相邻两个绑点差值不能超过255

            pass_positive_dlv = None #+dlv   +0.2
            pass_minus_dlv = None    #-dlv    -0.2
            calculate_positive_dlv = None #+dlv  0.1
            calculate_minus_dlv = None    #-dlv   0.1  

            pass_positive_dGamma = None #+gamma 值越大,亮度越小 能够通过的卡控
            pass_minus_dGamma = None    #-gamma 值越小,亮度越大 能够通过的卡控
            calculate_positive_dGamma = None #+gamma 值越大,亮度越小 自己设置的比较严的卡控
            calculate_minus_dGamma = None    #-gamma 值越小,亮度越大 自己设置的比较严的卡控

            pass_positive_dxy = None #+dxy
            pass_minus_dxy = None    #-dxy 
            calculate_positive_dxy = None #+dxy
            calculate_minus_dxy = None    #-dxy   
            ld = {}  

        class GammaLevelDesc(
            count_flag: int = 1,           #某一阶是否要调 ,默认全调 =1此阶要调 , = 0 此阶不调,跳过此阶

            pass_positive_dlv: Any | None = None, #+dlv   +0.2  基础的卡亮度
            pass_minus_dlv: Any | None = None,    #-dlv    -0.2  基础的卡亮度
            calculate_positive_dlv: Any | None = None, #+dlv  0.1 加强卡亮度
            calculate_minus_dlv: Any | None = None,    #-dlv   0.1  加强卡亮度
            #只有基础的卡控过了才会进行加强卡控，这样是为了卡得更紧，跑出来的画面更好

            pass_positive_dGamma: Any | None = None,    #+gamma 值越大,亮度越小 能够通过的卡控
            pass_minus_dGamma: Any | None = None,       #-gamma 值越小,亮度越大 能够通过的卡控
            calculate_positive_dGamma: Any | None = None,#+gamma 值越大,亮度越小 自己设置的比较严的卡控
            calculate_minus_dGamma: Any | None = None,   #-gamma 值越小,亮度越大 自己设置的比较严的卡控
            #跟上面同理，为跑出来的画面更好

            gamma_err: Any | None = None,  #是否要和上阶gamma值进行约束,如果需要请设置值,约束值,是上阶的gamma2.2值与此阶gamma2.2的差值

            pass_positive_dxy: Any | None = None,  #+dxy 基础的卡色坐标
            pass_minus_dxy: Any | None = None,     #-dxy 基础的卡色坐标
            calculate_positive_dxy: Any | None = None,#+dxy 加强卡色坐标
            calculate_minus_dxy: Any | None = None,#-dxy  加强卡色坐标

            dEMax: Any | None = None,    #DE 的卡控制
            special_value: Any | None = None   #对于只卡gamma2.2的, 不对色坐标有要求的,调不过时 可以设置这个,设置的值,每次都会GRB减这个值
        )

.. attention:: 
    
    如果对应的阶有进行独立的参数配置则跑独立的参数配置（白色部分），没有则跑默认的参数配置（黄色部分）。

.. note:: 
    
    在调试Gammma前需要将各个参数进行配置。示例如下：

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
    gaDe.ld[255] = GammaLevelDesc(1, 3.34,3.34,   3,   3, None,None,None,None,  None,  0.00135,0.00135,0.00130, 0.00130,0.5,None)
    

    gaDe.ld[127] = GammaLevelDesc(1, None,None,None,None, 0.03,0.03,0.01,0.01,  None,  0.00135,0.00135,0.00130, 0.00130,0.65,None)
    gaDe.ld[111] = GammaLevelDesc(1, None,None,None,None, 0.03,0.03,0.01,0.01,  None,  0.00135,0.00135,0.00130, 0.00130,0.8,None)
    gaDe.ld[95]  = GammaLevelDesc(1, None,None,None,None, 0.03,0.03,0.01,0.01,  None,  0.00135,0.00135,0.00130, 0.00130,0.8,None)
    # gaDe.ld[47]  = GammaLevelDesc(1, None,None,None,None, 0.03,0.03,0.01,0.01,  None,  0.00135,0.00135,0.00130, 0.00130,0.8,None)

    gaDe.ld[23] = GammaLevelDesc(1,None,None,None,None,0.03,0.03,0.01,0.01,None,0.0015,0.0015,0.0012,0.0012,0.5,None)
    gaDe.ld[19] = GammaLevelDesc(1,None,None,None,None,0.03,0.03,0.01,0.01,None,0.0015,0.0015,0.0012,0.0012,0.5,None)


    gaDe.ld[15] = GammaLevelDesc(1,None,None,None,None,0.03,0.03,0.01,0.01,None,0.0018,0.0018,0.0015,0.0015,0.7,None)
    gaDe.ld[11] = GammaLevelDesc(1,None,None,None,None,0.03,0.03,0.01,0.01,None,0.0018,0.0018,0.0015,0.0015,0.7,None)

    gaDe.ld[7] = GammaLevelDesc(1,None,None,None,None,0.03,0.03,0.02,0.01, None, 0.008,0.008,0.005,0.005,None,None)
    gaDe.ld[5] = GammaLevelDesc(1,None,None,None,None,0.09,0.09,0.08,0.09, None, None,None,None,None,None,None)
    gaDe.ld[3] = GammaLevelDesc(1,None,None,None,None,0.09,0.09,0.08,0.09, None, None,None,None,None,None, None)
    gaDe.ld[1] = GammaLevelDesc(1,None,None,None,None,0.09,0.09,0.08,0.09, None, None,None,None,None,None, 1)

.. attention:: 
    
    如果对应的阶有进行独立的参数配置则跑独立的参数配置（白色部分），没有则跑默认的参数配置（黄色部分）。


**2.2. Pid调试：** ::

     - 函数说明: 

        def Gamma2_2_PID(gaDe,P=0.3,startReg=None,GAMMA_LEVEL=None,NumMax=80,setReg=None):
        
        参数：
            gaDe : 默认配置参数
            p  :   每次调试目标与实测的误差的倍数
            startReg :  设置初始RGB的值,可设可不设
            GAMMA_LEVEL :  绑点
            NumMax  :  每阶调试的次数
            setReg  :  写入寄存器的函数接口
        返回 :
            -1 : 调试失败
            outData : 调试成功则返回RGB的值           
        
    - 使用实例:

       outData = Gamma2_2_PID(gaDe,P=0.3,startReg=[846, 734, 919],GAMMA_LEVEL=GAMMA_LEVEL,NumMax=150,setReg = set_255_668nits)
       
.. hint:: 
    
    该函数已经封装到调run_pid的函数，在调试Gamam的过程中不需要外部调用。

.. _my-reference-label:
**2.3. 跑 Pid：** ::

    - 函数说明: 

        def run_pid(modle =0):
        
        参数：
            modle : =0 不跑模型；（默认为不跑模型）
                    =1 跑模型；

    - 使用实例:
       1. run_pid() 或 run_pid(0)  # 不跑模型

       2. run_pid(1)    # 跑模型

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
        gaDe.ld[15] = GammaLevelDesc(1,None,None,None,None,0.03,0.03,0.01,0.01,None,0.0018,0.0018,0.0015,0.0015,0.7,None)
        gaDe.ld[11] = GammaLevelDesc(1,None,None,None,None,0.03,0.03,0.01,0.01,None,0.0018,0.0018,0.0015,0.0015,0.7,None)
        gaDe.ld[7] = GammaLevelDesc(1,None,None,None,None,0.03,0.03,0.02,0.01, None, 0.008,0.008,0.005,0.005,None,None)
        gaDe.ld[5] = GammaLevelDesc(1,None,None,None,None,0.09,0.09,0.08,0.09, None, None,None,None,None,None,None)
        gaDe.ld[3] = GammaLevelDesc(1,None,None,None,None,0.09,0.09,0.08,0.09, None, None,None,None,None,None, None)
        gaDe.ld[1] = GammaLevelDesc(1,None,None,None,None,0.09,0.09,0.08,0.09, None, None,None,None,None,None, 1)

        #函数配置示例：         
        outData = Gamma2_2_PID(gaDe,P=0.3,startReg=[846, 734, 919],GAMMA_LEVEL=GAMMA_LEVEL,NumMax=150,setReg = set_255_668nits)

.. code-block:: python
    :caption: 配置说明：
    :emphasize-lines: 6
    :linenos:
    
    ============  =============== ===========  =============  ============= ============== =============== =========================== =====================  ===================  ===========  ============================  
    当前绑点       独立参数配置     是否要调      基础卡亮度      加强卡亮度     基础gamma卡控   加强gamma卡控    是否要和上阶gamma值进行约束   基础卡色坐标            加强卡色坐标          de卡控       设置的值,每次都会GRB减这个值
    ============  =============== ===========  =============  ============= ============== =============== =========================== =====================  ===================  ===========  ============================    
      255                          1：是 0：否     +     -       +      -      +         -    +          -                              +             -        +          -
    ============  =============== ===========  =============  ============= ============== =============== =========================== =====================  ===================  ===========  ============================
    gaDe.ld[255] = GammaLevelDesc(   1,        3.34, 3.32,     3.1,  3.0,    None,   None,  None,   None,             None,             0.00134,   0.00135,    0.00129, 0.00128,      0.5,               None)
    ============  =============== ===========  =============  ============= ============== =============== =========================== =====================  ====================  ===========  ===========================
                                   这一阶要调   目标lv+3.34,    目标lv+3.1,    目标Gamma +     目标Gamma +       None为否，                 X+0.00134或x-0.00135   X+0.00134或x-0.00135  de = 0.5           None则不减
    说明                                        目标lv-3.32     目标lv-3.0     目标gamma -     目标gamma -      有数值则按该值进行约束       y+0.00134或y-0.00135   y+0.00134或y-0.00135  None或0则不卡    有数值则RGB每次减这个值
                                               None或0则不卡   None或0则不卡   None或0则不卡   None或0则不卡                                None或0则不卡           None或0则不卡
    ============  =============== ===========  =============  ============= ============== =============== =========================== =====================  ====================  ===========  ===========================

.. important:: 
    
    注意在跑Pid期间,请确保屏幕是亮的


**2.4. 使用示例：** ::

    # 初始化镜头
    CA410_Init(1)

    # 1:跑模型, 0:不跑模型
    run_pid(1)



**调试过程如下：**

.. note::
    1.开始跑Pid：
        .. image:: /../picture/Pid_kaishi.png


    2.跑Pid中：
        .. image:: /../picture/Pid_guocheng.png
        

    
    3.跑pid完成：
        - 有跑模型：
        .. image:: /../picture/Pid_wancheng.png
        - 不跑模型：
        .. image:: /../picture/Pid_norun_modle.png

    4.跑模型完成：
        .. image:: /../picture/Pid_run_modle.png


    5.将模型复制到模型库：
        .. image:: /../picture/Pid_copy_modle.png
            
.. hint::

 跑完模型后会在设备上生成模型文件。文件路径：/emmc/modle，
 如果没有复制到全部的模型，也可以用USB打开设备上的模型文件。


    
**2.5. 常见错误及解决方法：** ::





    
    
