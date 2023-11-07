#!/bin/bash

# 第一步：查找端口为8083的进程
PORT=8083
PROCESS_ID=$(lsof -i :$PORT -t)

if [ -n "$PROCESS_ID" ]; then
  echo "找到端口 $PORT 的进程，进程ID为 $PROCESS_ID"

  # 第二步：关闭进程
  kill $PROCESS_ID
  echo "已关闭进程 $PROCESS_ID"
else
  echo "未找到端口 $PORT 的进程"
fi

echo "开始执行git命令"
# 第三步：执行git pull命令
# 进入您的Git仓库目录
# 注意：在脚本中，请将以下路径替换为您的实际Git仓库路径
GIT_REPO_DIR="/opt/webService"
cd $GIT_REPO_DIR

# 执行git pull命令
git pull
echo "已执行git pull"

# 第四步：执行python命令
# 假设您要运行一个名为your_script.py的Python脚本
# 注意：在脚本中，请将以下命令替换为您要运行的实际Python命令
nohup python3 main.py > output.log 2>&1 &
echo "已执行Python命令"
