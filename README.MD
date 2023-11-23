
获取txt中的内容
依次读取每一行的内容
 eg. 读取第一行 user1 request --> 进入user_request的情况
     返回user_request的结果 在terminal中显示， 同时修改terminal中的cpu资源剩余量（此外，terminal中还要显示另外三个值）
     
     读取第二行
     读取第三行
     ...
     读取第n行
     user1 release --> 进入user_release的情况
     返回user_release的结果在terminal中显示，同时修改terminal中cpu的资源剩余量进行释放

     关于三个值及request操作
     1. alarm rate 
        在每次request 都要进行alarm rate监控函数，如果allocated resource + 本次request > alarm rate 开启overbooking mode
        
     2. low-usage rate
        当使用的资源低于low usage rate的时候，系统会退出overbooking mode
        
     3. fraction value
        预先设定好fraction value, 在进行request的时候，若overbooking==TRUE 则allocated cpu = request cpu*fraction value

     关于release的操作
      一旦进入release操作
      1. 要确定该用户确实已经成功的request到同等数量的CPU, 否则release失败
      2. 对CPU剩余资源进行释放, 并通知用户release结果
      

        

     real CPU list
      user1 1 CPU
      user2 1 CPU
      user3 0.8 CPU
      user4 3.2 CPU
      ...



  1. empty --> request(1-1) request request... 达到alarm rate --> overbooking mode 
  2. request(1-0.8) release release ... release request(1-0.8) 低于low-usage rate --> exit overbooking mode
  3. 循环1


  request
  1. 当前有剩余资源
  2. 判断当前的模式 overbooking = true OR false
  3. 返回request 结果（success, err(没有足够的空间)）


  release 
  1. 判断该用户是否符合release条件
  2. 更新 release 后的overbooking
  3. 进行release操作
  4. 返回 release 结果


  **multiple scenarios**
   request(alarm: 70 overbook = flase)
   首先需要满足： request+allocated <= total
   1. 50 下一次 30 50+30 >= 70 --> overbook = true --> real: 50+30*0.8 = 74
   2. 60 下一次 10 60+10 >= 70 但是此时 overbook = true，所以本次为10*0.8 实际使用为68,尽管小于alarm rate， 仍然进入overbooking mode

   request(overbook = false)
   另一种情况（request+allocate < alarm 
   什么都不操作

   request(overbook = true)
   首先需要满足： request+allocated <= total
   request *= fraction rate 


   release(low-usage: 20)(overbook = false)
   1. release && no mode change

   release(overbook = true)
   1. release release release if allocated - release <= 20 exit overbooking mode

   
   内存满了的情况： 
   在后续有release的时候，应该先给哪个用户分配
   eg.
   user1 request 30 CPU
   user2 request 20 CPU
   user3 request 20 CPU
   user2 release 20 CPU
   user3 release 20 CPU
   user4 request 50 CPU
   user5 request 30 CPU 
   user6 request 20 CPU
   user7 request 20 CPU
   user8 release 20 CPU
   user1 release 30 CPU
   user10 request 5 CPU

   user6, user7, user10 在排队 在user1 release 30cpu后, 剩下的cpu怎么分配？
   


   



    **multiple scenarios2**

    scen1: out of resource

   




   关于input
   在运行后，通过命令行的方式与用户交互，是否要自行输入or使用我们的data
   用户自行输入，可以选择直接输入数据，系统执行，直到用户退出/ 同时用户可以选择输入一个txt文件










