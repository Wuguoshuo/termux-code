#!/bin/bash

# iFlow SSH Manager - 通过SSH连接Ubuntu服务器并管理多个Screen窗口中的iflow进程

# 配置变量
SSH_HOST="${SSH_HOST:-}"          # SSH 服务器地址
SSH_USER="${SSH_USER:-}"          # SSH 用户名
SSH_PORT="${SSH_PORT:-22}"        # SSH 端口
PROJECT_DIR="${PROJECT_DIR:-}"    # 项目文件夹路径
SCREEN_NAMES=("iflow1" "iflow2" "iflow3")  # Screen 窗口名称
POLL_INTERVAL=5                   # 轮询间隔（秒）
RESUME_CMD="/resume"              # 恢复会话命令

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 显示使用帮助
show_help() {
    cat << EOF
用法: $(basename "$0") [选项]

通过SSH远程连接Ubuntu服务器并管理多个Screen窗口中的iflow进程

选项:
    -h, --help              显示此帮助信息
    -H, --host <地址>       SSH服务器地址（必填）
    -u, --user <用户名>     SSH用户名（必填）
    -p, --port <端口>       SSH端口（默认: 22）
    -d, --dir <目录>        项目文件夹路径（必填）

环境变量:
    SSH_HOST               SSH服务器地址
    SSH_USER               SSH用户名
    SSH_PORT               SSH端口（默认: 22）
    PROJECT_DIR            项目文件夹路径

示例:
    $(basename "$0") -H 192.168.1.100 -u ubuntu -d /home/ubuntu/iflow-project
    $(basename "$0") --host myserver.com --user admin --dir /var/www/iflow

EOF
}

# 解析命令行参数
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -H|--host)
                SSH_HOST="$2"
                shift 2
                ;;
            -u|--user)
                SSH_USER="$2"
                shift 2
                ;;
            -p|--port)
                SSH_PORT="$2"
                shift 2
                ;;
            -d|--dir)
                PROJECT_DIR="$2"
                shift 2
                ;;
            *)
                print_error "未知参数: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# 验证配置
validate_config() {
    if [[ -z "$SSH_HOST" ]]; then
        print_error "请提供SSH服务器地址（使用 -H 或 --host 参数）"
        exit 1
    fi

    if [[ -z "$SSH_USER" ]]; then
        print_error "请提供SSH用户名（使用 -u 或 --user 参数）"
        exit 1
    fi

    if [[ -z "$PROJECT_DIR" ]]; then
        print_error "请提供项目文件夹路径（使用 -d 或 --dir 参数）"
        exit 1
    fi

    print_success "配置验证通过"
    print_info "主机: $SSH_USER@$SSH_HOST:$SSH_PORT"
    print_info "项目目录: $PROJECT_DIR"
}

# 检查远程服务器上的 screen 是否存在
check_remote_screen() {
    ssh -p "$SSH_PORT" "$SSH_USER@$SSH_HOST" "which screen" 2>/dev/null
    if [[ $? -ne 0 ]]; then
        print_warning "远程服务器上未安装 screen，正在尝试安装..."
        ssh -p "$SSH_PORT" "$SSH_USER@$SSH_HOST" "sudo apt-get update && sudo apt-get install -y screen"
    fi
}

# 获取远程 iflow 命令的完整路径
get_iflow_command() {
    local cmd="command -v iflow || which iflow || echo 'iflow'"
    echo "$cmd"
}

# 启动单个 screen 窗口中的 iflow
start_screen_session() {
    local screen_name="$1"

    ssh -p "$SSH_PORT" -o ServerAliveInterval=60 -o ServerAliveCountMax=3 \
        "$SSH_USER@$SSH_HOST" "cd '$PROJECT_DIR' && screen -dmS $screen_name bash -c 'iflow; sleep 2'"

    if [[ $? -eq 0 ]]; then
        print_success "已启动 screen 窗口: $screen_name"
        return 0
    else
        print_error "启动 screen 窗口失败: $screen_name"
        return 1
    fi
}

# 检查 screen 窗口中是否正在运行 iflow
check_screen_status() {
    local screen_name="$1"
    ssh -p "$SSH_PORT" "$SSH_USER@$SSH_HOST" "screen -ls | grep -q '$screen_name' && echo 'running' || echo 'not_found'"
}

# 获取 screen 窗口中的进程状态
get_screen_process_status() {
    local screen_name="$1"
    ssh -p "$SSH_PORT" "$SSH_USER@$SSH_HOST" "
        if screen -ls | grep -q '$screen_name'; then
            # 检查 iflow 进程是否在运行
            screen -S '$screen_name' -Q echo 'checking' 2>/dev/null
            if pgrep -f 'iflow' > /dev/null 2>&1; then
                echo 'running'
            else
                echo 'stopped'
            fi
        else
            echo 'not_found'
        fi
    "
}

# 重新启动指定 screen 中的 iflow
restart_screen_session() {
    local screen_name="$1"
    print_warning "检测到 $screen_name 中的 iflow 已停止，准备重启..."

    # 发送 /resume 命令
    local ssh_cmd="screen -S '$screen_name' -X stuff '$RESUME_CMD\n'"

    ssh -p "$SSH_PORT" "$SSH_USER@$SSH_HOST" "$ssh_cmd"
    sleep 1

    # 等待一下检查是否成功
    sleep 2
    local status=$(get_screen_process_status "$screen_name")

    if [[ "$status" == "running" ]]; then
        print_success "$screen_name 已成功重启并恢复会话"
        return 0
    else
        # 如果 /resume 不起作用，直接启动
        print_info "尝试直接启动 iflow..."
        local start_cmd="screen -S '$screen_name' -X stuff 'iflow\n'"
        ssh -p "$SSH_PORT" "$SSH_USER@$SSH_HOST" "$start_cmd"
        sleep 2

        status=$(get_screen_process_status "$screen_name")
        if [[ "$status" == "running" ]]; then
            print_success "$screen_name 已成功重启"
            return 0
        else
            print_error "$screen_name 重启失败"
            return 1
        fi
    fi
}

# 启动所有 screen 窗口
start_all_screens() {
    print_info "正在启动所有 screen 窗口..."

    for screen_name in "${SCREEN_NAMES[@]}"; do
        start_screen_session "$screen_name"
        sleep 1
    done

    print_success "所有 screen 窗口启动完成"
}

# 轮询检查所有 screen 窗口
poll_screens() {
    print_info "开始轮询检查所有 screen 窗口..."

    while true; do
        local needs_restart=()

        for screen_name in "${SCREEN_NAMES[@]}"; do
            local status=$(get_screen_process_status "$screen_name")

            case "$status" in
                "running")
                    print_info "$screen_name: 运行正常"
                    ;;
                "stopped")
                    print_warning "$screen_name: iflow 已停止"
                    needs_restart+=("$screen_name")
                    ;;
                "not_found")
                    print_error "$screen_name: screen 窗口不存在"
                    needs_restart+=("$screen_name")
                    ;;
                *)
                    print_warning "$screen_name: 未知状态: $status"
                    ;;
            esac
        done

        # 重启需要重启的窗口
        for screen_name in "${needs_restart[@]}"; do
            restart_screen_session "$screen_name"
        done

        print_info "等待 ${POLL_INTERVAL} 秒后再次检查..."
        sleep "$POLL_INTERVAL"
    done
}

# 用户交互模式 - 实时监控并允许用户输入
interactive_mode() {
    print_info "进入交互模式..."
    print_info "按 Ctrl+C 退出"
    echo ""

    # 在后台启动轮询
    poll_screens &
    POLL_PID=$!

    # 用户输入循环
    while true; do
        read -p "输入命令 (help/status/restart <name>/quit): " cmd arg

        case "$cmd" in
            help)
                echo "可用命令:"
                echo "  help           - 显示此帮助信息"
                echo "  status         - 查看所有 screen 状态"
                echo "  restart <name> - 重启指定 screen 窗口"
                echo "  restart all    - 重启所有 screen 窗口"
                echo "  send <name> <msg> - 发送命令到指定 screen"
                echo "  quit           - 退出脚本"
                ;;
            status)
                for screen_name in "${SCREEN_NAMES[@]}"; do
                    local status=$(get_screen_process_status "$screen_name")
                    echo "$screen_name: $status"
                done
                ;;
            restart)
                if [[ "$arg" == "all" ]]; then
                    for screen_name in "${SCREEN_NAMES[@]}"; do
                        restart_screen_session "$screen_name"
                    done
                elif [[ -n "$arg" ]]; then
                    restart_screen_session "$arg"
                else
                    print_error "请指定要重启的窗口名称"
                fi
                ;;
            send)
                local screen_name="$arg"
                shift 2
                local message="$*"
                if [[ -n "$screen_name" && -n "$message" ]]; then
                    ssh -p "$SSH_PORT" "$SSH_USER@$SSH_HOST" \
                        "screen -S '$screen_name' -X stuff '$message'"
                    print_success "消息已发送到 $screen_name"
                else
                    print_error "用法: send <screen_name> <message>"
                fi
                ;;
            quit|exit)
                print_info "正在停止轮询..."
                kill $POLL_PID 2>/dev/null
                print_info "退出交互模式"
                break
                ;;
            *)
                print_error "未知命令: $cmd"
                ;;
        esac
    done
}

# 主函数
main() {
    parse_args "$@"
    validate_config

    echo "=========================================="
    echo "      iFlow SSH Manager"
    echo "=========================================="
    echo ""

    # 检查远程 screen
    check_remote_screen

    # 询问运行模式
    echo "请选择运行模式:"
    echo "1) 交互模式（允许用户输入命令）"
    echo "2) 自动模式（自动轮询和重启）"
    echo ""
    read -p "请选择 [1/2]: " mode

    case "$mode" in
        1)
            echo ""
            print_info "启动交互模式..."
            echo ""
            start_all_screens
            echo ""
            interactive_mode
            ;;
        2)
            echo ""
            print_info "启动自动模式..."
            echo ""
            start_all_screens
            echo ""
            poll_screens
            ;;
        *)
            print_error "无效选择，使用默认自动模式"
            start_all_screens
            poll_screens
            ;;
    esac
}

# 捕获 Ctrl+C
trap 'echo ""; print_info "正在退出..."; exit 0' INT

# 运行主函数
main "$@"
