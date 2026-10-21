# Stage2 Git学习心得
1. 什么是Git：Git是分布式版本管理工具，可以记录代码文件每一次修改，方便回溯版本、多人协作开发。
2. 这次操作流程：
   - git clone：把github上的仓库下载到本地
   - git checkout -b 分支名：新建并切换到自己的开发分支，不在main主分支直接修改
   - git add .：把改动加入暂存区
   - git commit -m "备注"：提交改动，写上说明
   - git push origin 分支名：把本地分支上传到远程GitHub仓库
3. 收获：
   学会了基础的Git工作流，明白了分支的意义——保护主分支，每个人在自己分支上开发，最后通过PR合并。
4. 遇到的问题：
   一开始分不清文件夹和md文件，搞错了文件类型，反复调整才弄对路径和命名规则。
   # Stage2 安装并配置Git、使用分支提交
## 1. Git身份配置
安装Git后，需要配置全局用户名和邮箱，用来标记提交人信息，命令：
```bash
git config --global user.name "杨一升"
git config --global user.email "3582117279@qq.com"