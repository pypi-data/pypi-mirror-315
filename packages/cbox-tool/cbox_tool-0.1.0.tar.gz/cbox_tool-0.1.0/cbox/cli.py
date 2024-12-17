import click
from .mybox import MyBox

@click.group()
def cli():
    """MyBox - 强大的多仓库管理工具

    MyBox 帮助您轻松管理多个 Git 仓库，支持工作空间管理、批量操作和分支管理等功能。
    
    快速开始:
        $ mybox add workspace1 ~/projects/workspace1  # 添加工作空间
        $ mybox list                                 # 查看工作空间
        $ mybox clone workspace1 <repo-url>          # 克隆仓库
    
    详细文档请访问: https://github.com/yourusername/mybox
    """
    pass

@cli.command()
@click.argument('name')
@click.argument('path')
def add(name, path):
    """添加新的工作空间
    
    参数:
        NAME: 工作空间名称
        PATH: 工作空间路径

    示例:
        $ mybox add dev ~/projects/dev
        $ mybox add work ~/workspace
    """
    MyBox().add_workspace(name, path)

@cli.command()
def list():
    """列出所有工作空间及其状态
    
    显示信息包括:
    - 工作空间名称
    - 路径
    - 状态（活动/未找到）
    
    示例:
        $ mybox list
    """
    MyBox().list_workspaces()

@cli.command()
@click.argument('workspace')
@click.argument('repo_url')
def clone(workspace, repo_url):
    """克隆远程仓库到指定工作空间
    
    参数:
        WORKSPACE: 工作空间名称
        REPO_URL: 远程仓库URL

    示例:
        $ mybox clone dev https://github.com/user/repo.git
    """
    MyBox().clone(workspace, repo_url)

@cli.command()
@click.argument('workspace')
def status(workspace):
    """显示工作空间中所有仓库的状态
    
    显示信息包括:
    - 仓库名称
    - 当前分支
    - 是否有未提交的更改
    - 未跟踪的文件数量
    
    参数:
        WORKSPACE: 工作空间名称

    示例:
        $ mybox status dev
    """
    MyBox().status(workspace)

@cli.command()
@click.argument('workspace')
def pull(workspace):
    """拉取工作空间中所有仓库的更新
    
    参数:
        WORKSPACE: 工作空间名称

    示例:
        $ mybox pull dev
    """
    MyBox().pull(workspace)

@cli.command()
@click.argument('workspace')
def push(workspace):
    """推送工作空间中所有仓库的更改
    
    参数:
        WORKSPACE: 工作空间名称

    示例:
        $ mybox push dev
    """
    MyBox().push(workspace)

@cli.command()
@click.argument('workspace')
@click.argument('message')
def commit(workspace, message):
    """提交工作空间中所有仓库的更改
    
    参数:
        WORKSPACE: 工作空间名称
        MESSAGE: 提交信息

    示例:
        $ mybox commit dev "feat: add new feature"
    """
    MyBox().commit(workspace, message)

@cli.command()
@click.argument('workspace')
def branches(workspace):
    """列出工作空间中所有仓库的分支
    
    显示信息包括:
    - 分支名称
    - 是否是当前分支
    - 跟踪信息
    - 最后一次提交信息
    
    参数:
        WORKSPACE: 工作空间名称

    示例:
        $ mybox branches dev
    """
    MyBox().list_branches(workspace)

@cli.command()
@click.argument('workspace')
@click.argument('branch_name')
@click.option('--start-point', help='新分支的起始点')
def create_branch(workspace, branch_name, start_point):
    """在工作空间中的所有仓库创建新分支
    
    参数:
        WORKSPACE: 工作空间名称
        BRANCH_NAME: 新分支名称
        --start-point: 可选，新分支的起始点

    示例:
        $ mybox create-branch dev feature/new-ui
        $ mybox create-branch dev hotfix/bug-123 --start-point main
    """
    MyBox().create_branch(workspace, branch_name, start_point)

@cli.command()
@click.argument('workspace')
@click.argument('branch_name')
def switch(workspace, branch_name):
    """切换工作空间中所有仓库的分支
    
    参数:
        WORKSPACE: 工作空间名称
        BRANCH_NAME: 目标分支名称

    示例:
        $ mybox switch dev feature/new-ui
    """
    MyBox().switch(workspace, branch_name)

@cli.command()
@click.argument('workspace')
@click.argument('branch_name')
@click.option('--force', '-f', is_flag=True, help='强制删除分支')
def delete_branch(workspace, branch_name, force):
    """删除工作空间中所有仓库的指定分支
    
    参数:
        WORKSPACE: 工作空间名称
        BRANCH_NAME: 要删除的分支名称
        --force, -f: 强制删除（即使未合并）

    示例:
        $ mybox delete-branch dev feature/old-feature
        $ mybox delete-branch dev feature/wip -f
    """
    MyBox().delete_branch(workspace, branch_name, force)

@cli.command()
@click.argument('workspace')
@click.argument('repo_path')
def import_repo(workspace, repo_path):
    """导入现有的本地仓库到工作空间
    
    参数:
        WORKSPACE: 工作空间名称
        REPO_PATH: 本地仓库路径

    示例:
        $ mybox import-repo dev ~/old-projects/my-app
    """
    MyBox().import_repo(workspace, repo_path)

@cli.command()
@click.argument('workspace')
@click.argument('repo_name')
@click.option('--bare', is_flag=True, help='创建裸仓库')
def init(workspace, repo_name, bare):
    """在工作空间中初始化新的git仓库
    
    参数:
        WORKSPACE: 工作空间名称
        REPO_NAME: 新仓库名称
        --bare: 创建裸仓库

    示例:
        $ mybox init dev new-project
        $ mybox init dev central-repo --bare
    """
    MyBox().init(workspace, repo_name, bare)

@cli.command()
@click.argument('workspace')
@click.argument('scan_path')
def scan_import(workspace, scan_path):
    """扫描目录并导入所有找到的git仓库
    
    参数:
        WORKSPACE: 工作空间名称
        SCAN_PATH: 要扫描的目录路径

    示例:
        $ mybox scan-import dev ~/projects
    """
    MyBox().scan_import(workspace, scan_path)

if __name__ == '__main__':
    cli()
