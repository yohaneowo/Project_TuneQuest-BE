# task_reject_on_worker_lost作用是当worker进程意外退出时，task会被放回到队列中
task_reject_on_worker_lost = True
# task_acks_late作用是只有当worker完成了这个task时，任务才被标记为ack状态
task_acks_late = True

enable_utc = True
timezone = 'Europe/London'