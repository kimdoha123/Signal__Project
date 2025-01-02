FROM ultralytics/ultralytics:latest-jetson-jetpack4

ARG DEBIAN_FRONTEND=noninteractive
ARG USER=vscode


# 1. Install sudo and create the vscode user with root privileges
RUN apt-get update && apt-get install -y --no-install-recommends sudo \
    && useradd -m -d /home/$USER -s /bin/bash $USER \
    && usermod -aG sudo,video,dialout,plugdev,i2c,audio,input $USER \
    && echo "$USER ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# 2. Update dependencies index
RUN apt-get update

# 3. Switch to the vscode user
USER $USER
ARG HOME="/home/$USER"
RUN sudo chown -R $USER:$USER /home/$USER
RUN export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1:/$LD_PRELOAD >> ~/.bashrc

# 4. Set environment variables for pyenv and PATH
ENV PATH="${HOME}/.local/bin:$PATH"

# # 5. Install Python, and poetry
# RUN echo "Installing and poetry" \
#     && mkdir -p /home/$USER/.poetry-cache \
#     && export TMPDIR=/home/$USER/.poetry-cache \
#     && curl -sSL https://install.python-poetry.org | python3 -

# RUN poetry config virtualenvs.in-project true

# 6. Set permissions to ensure the user can access installed tools



# Optional: Expose ports or add entry points if needed
# EXPOSE 8000
