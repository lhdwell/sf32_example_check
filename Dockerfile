# 基础镜像：选择 Ubuntu 22.04（长期支持版，稳定性高）
FROM ubuntu:24.04

# 1. 安装系统依赖（严格遵循官方文档的 Ubuntu/Debian 依赖清单）
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    wget \
    flex \
    bison \
    gperf \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    cmake \
    ninja-build \
    ccache \
    libffi-dev \
    libssl-dev \
    dfu-util \
    libusb-1.0-0 \
    libusb-1.0-0-dev \
    sudo \
    bash-completion \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*  # 清理 apt 缓存，减小镜像体积

# 环境变量配置（仅保留核心路径与分支，不涉及国内镜像或自定义工具路径）
ENV SDK_WORKDIR="/opt/OpenSiFli"
ENV SDK_PATH="${SDK_WORKDIR}/SiFli-SDK"
ENV SDK_BRANCH="v2.4.3"

# 2. 创建 SDK 工作目录并授权（避免后续克隆/编译时的权限问题）
RUN mkdir -p ${SDK_WORKDIR} \
    && chmod 755 ${SDK_WORKDIR}  # 确保当前用户有读写权限

# 3. 从 GitHub 官方仓库克隆 SiFli SDK（必须带 --recursive 拉取子模块，官方强制要求）
# 容错处理：额外执行子模块更新，避免克隆过程中子模块拉取不完整
RUN cd ${SDK_WORKDIR} \
    && git clone --recursive -b ${SDK_BRANCH} https://github.com/OpenSiFli/SiFli-SDK ${SDK_PATH} \
    && cd ${SDK_PATH} \
    && git submodule update --init --recursive

# 4. 安装 SDK 工具链（编译器、调试器等，使用官方默认配置，不修改工具安装路径）
# 工具默认安装到官方指定的 $HOME/.sifli 目录，不自定义路径
RUN cd ${SDK_PATH} \
    && chmod +x install.sh \
    && ./install.sh \
    && rm -rf ~/.cache/pip

# 5. 配置环境变量永久生效（整合官方 export.sh 到 .bashrc，终端启动自动加载）
RUN echo "source ${SDK_PATH}/export.sh" >> ~/.bashrc \
    # 可选：添加 SDK 快速激活别名，方便手动刷新环境
    && echo "alias sf32sdk='source ${SDK_PATH}/export.sh'" >> ~/.bashrc

ADD find.py .
ADD build.py .

# 6. 设置默认工作目录（进入容器后直接定位到 SDK 根目录，方便开发操作）
WORKDIR ${SDK_PATH}

# 7. 默认启动命令（进入交互式 bash 终端，支持后续编译、调试操作）
CMD ["/bin/bash", "-i","-c","python3 /build.py"]