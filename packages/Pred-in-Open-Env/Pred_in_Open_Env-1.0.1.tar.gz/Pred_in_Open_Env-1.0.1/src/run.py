from wrap import predict_model
import numpy as np
import argparse

def task1(currentTime,forecastDuration):
    Model=predict_model(forecastDuration=forecastDuration,step=1,all_data=np.load('./data/flow_after_change.npy'),
                     out_data=np.load('./data/out_week1.npy'),receive_data=np.load('./data/receive_week1.npy'),
                              to_GPU=True,update=False)

    Model.excel2arr("./data/0520-0610.xlsx")
    Model.task_1(currentTime)
    print(Model.output1)

def task2(startTime,endTime,duration):
    Model = predict_model(forecastDuration=duration, step=144, all_data=np.load('./data/flow_after_change.npy'),
                          out_data=np.load('./data/out_week1.npy'), receive_data=np.load('./data/receive_week1.npy'),
                          to_GPU=True, update=False)
    Model.excel2arr("./data/0520-0610.xlsx")
    Model.task_2(startTime,endTime)
    print(Model.output2)

def task3(startTime,endTime,duration,id):
    Model = predict_model(forecastDuration=duration, step=144, all_data=np.load('./data/flow_after_change.npy'),
                          out_data=np.load('./data/out_week1.npy'), receive_data=np.load('./data/receive_week1.npy'),
                          to_GPU=True, update=False)
    Model.excel2arr("./data/0520-0610.xlsx")
    Model.task_3(startTime,endTime,id)
    print(Model.output3)

def main():
    parser = argparse.ArgumentParser(description="多任务执行脚本")
    subparsers = parser.add_subparsers(dest='task', help='选择要执行的任务')


    parser_task1 = subparsers.add_parser('task1', help='全点位未来 10/20/30 分钟人数预测及人数流向接口')
    parser_task1.add_argument('--currentTime', type=str, help='当前时间（yyyy-MM-dd HH:mm:ss）')
    parser_task1.add_argument('--forecastDuration', type=int, help='预测时长（10，20，30），单位：分钟')


    parser_task2 = subparsers.add_parser('task2', help='全点位在指定时间范围内实际人数与预测人数趋势')
    parser_task2.add_argument('--startTime', type=str, help='开始时间（yyyy-MM-dd HH:mm:ss）')
    parser_task2.add_argument('--endTime', type=str, help='结束时间（yyyy-MM-dd HH:mm:ss）')
    parser_task2.add_argument('--duration', type=int, help='指定数据时间间隔，10/20/30，表示返回数据的时间间隔为10/20/30分钟')

    parser_task3 = subparsers.add_parser('task3', help='指定点位指定时间范围内实际人数与预测人数趋势')
    parser_task3.add_argument('--startTime', type=str, help='开始时间（yyyy-MM-dd HH:mm:ss）')
    parser_task3.add_argument('--endTime', type=str, help='结束时间（yyyy-MM-dd HH:mm:ss）')
    parser_task3.add_argument('--duration', type=int, help='指定数据时间间隔，10/20/30，表示返回数据的时间间隔为10/20/30分钟')
    parser_task3.add_argument('--id', type=int,
                              help='指定点位序号，1～10')
    # 解析命令行参数
    args = parser.parse_args()

    # 根据选择的任务执行对应的函数
    if args.task == 'task1':
        task1(args.currentTime,args.forecastDuration)
    elif args.task == 'task2':
        task2(args.startTime,args.endTime,args.duration)
    elif args.task == 'task3':
        task3(args.startTime,args.endTime,args.duration,args.id)
    else:
        print("请指定要执行的任务")

if __name__ == "__main__":
    main()


