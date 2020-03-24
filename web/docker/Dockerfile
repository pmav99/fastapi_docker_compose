# vi: ft=Dockerfile
#
# https://jtreminio.com/blog/running-docker-containers-as-current-host-user/#ok-so-what-actually-works
# https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
#
#-----------------------------------------------------------------------------------------

FROM ubuntu:bionic-20200311@sha256:bec5a2727be7fff3d308193cfde3491f8fba1a2ba392b7546b43a051853a341d AS stage0-base

LABEL org.opencontainers.image.url='https://gitlab.com/pmav99/fastapi_template' \
      org.opencontainers.image.source='https://gitlab.com/pmav99/fastapi_template' \
      org.opencontainers.image.documentation='https://gitlab.com/pmav99/fastapi_template' \
      org.opencontainers.image.licenses='proprietary software' \
      org.opencontainers.image.vendor='klimeto.com' \
      org.opencontainers.image.authors='Tomas Kliment; Panos Mavrogiorgos'

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=off

# Configure apt
RUN set -xeu; \
    echo 'APT::Install-Recommends "false";' | tee -a /etc/apt/apt.conf.d/99-install-suggests-recommends; \
    echo 'APT::Install-Suggests "false";' | tee -a /etc/apt/apt.conf.d/99-install-suggests-recommends; \
    echo 'Configuring apt: OK';

# Setup the locales
ENV LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANGUAGE=en_US:en

#ENV TZ=Europe/Rome
ENV TZ=Etc/UTC

RUN set -xeu; \
    apt update; \
    apt upgrade -yq; \
    # set locales
    apt install -yq locales; \
    sed -i -e "s/# ${LANG} UTF-8/${LANG} UTF-8/" /etc/locale.gen; \
    dpkg-reconfigure --frontend=noninteractive locales; \
    update-locale LANG=${LANG}; \
    echo 'Setting locales: OK'; \
    # setup timezone
    apt install -yq tzdata; \
    ln -snf /usr/share/zoneinfo/"${TZ}" /etc/localtime; \
    echo "${TZ}" | tee /etc/timezone; \
    dpkg-reconfigure tzdata; \
    echo 'Setting up timezone: OK'; \
    # setup ppas
    apt install -yq software-properties-common; \
    add-apt-repository -y ppa:deadsnakes/ppa; \
    echo 'Setting up ppas : OK'; \
    apt install -yq \
        build-essential \
        bsdtar \
        bzip2 \
        ca-certificates \
        curl \
        file \
        git \
        gosu \
        gzip \
        jq \
        moreutils \
        nano \
        netcat \
        procps \
        silversearcher-ag \
        tar \
        tree \
        unzip \
        vim \
        less \
        wget \
        zip \
        # python
        python3.7 \
        python3.7-dev \
        python3.7-venv \
    ; \
    apt purge -yq software-properties-common; \
    apt autoremove -y --purge; \
    find / -xdev -name *.pyc -delete; \
    rm -rf /var/lib/apt/lists/*; \
    echo 'Basic setup: OK';



ENV TINI_VERSION=0.18.0
ENV TINI_DEB_PACKAGE=tini_"${TINI_VERSION}"-amd64.deb

RUN set -xeu; \
    wget https://github.com/krallin/tini/releases/download/v"${TINI_VERSION}"/"${TINI_DEB_PACKAGE}"; \
    dpkg -i "${TINI_DEB_PACKAGE}"; \
    rm -rf "${TINI_DEB_PACKAGE}"; \
    echo 'tini installation: OK'

# Create a normal user
ARG USER_NAME
ARG USER_ID
ARG GROUP_ID

ENV USER_NAME=${USER_NAME}
ENV USER_ID=${USER_ID}
ENV GROUP_ID=${GROUP_ID}
ENV USER_HOME=/home/${USER_NAME}

RUN set -xeu; \
    # Add the user
    groupadd -g ${GROUP_ID} ${USER_NAME}; \
    useradd -u ${USER_ID} -g ${GROUP_ID} -m -s /bin/bash ${USER_NAME}; \
    usermod -a -G users ${USER_NAME}; \
    echo "Creating user ${USER_NAME}: OK";

# Create and activate the virtualenv
# https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV VIRTUAL_ENV=${USER_HOME}/.venv
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"
RUN set -xeu; \
    echo 'Create virtualenv'; \
    gosu "${USER_NAME}" python3.7 -m venv ${VIRTUAL_ENV}; \
    gosu "${USER_NAME}" pip install -U --no-cache --no-compile pip; \
    find ${VIRTUAL_ENV} -name *.pyc -delete; \
    echo 'done'

# Install requirements
COPY requirements/requirements.txt \
     requirements/requirements-dev.txt \
     # destination
     /tmp

ARG DEPLOY_ENV=prod
ENV DEPLOY_ENV=${DEPLOY_ENV}

RUN set -xe; \
    if [ "${DEPLOY_ENV}" = 'dev' ]; then export REQUIREMENTS_FILE=/tmp/requirements-dev.txt; else export REQUIREMENTS_FILE=/tmp/requirements.txt; fi; \
    pip install --no-cache --no-compile -r "${REQUIREMENTS_FILE}"; \
    find ${VIRTUAL_ENV} -name *.pyc -delete; \
    echo 'Install dependencies: OK';


# Install any new requirements
RUN set -xe; \
    echo 'Install dependencies'; \
    pip install --no-cache -r /tmp/requirements.txt; \
    find ${VIRTUAL_ENV} -name *.pyc -delete; \
    echo 'done'

# Copy executable scripts to a directory within the $PATH
COPY ./docker/entrypoint_inject.sh \
     #./docker/start.sh \
     #./docker/start_reload.sh \
     # destination
     /usr/local/bin/

ENV APPDIR=${USER_HOME}/app
COPY ./ ${APPDIR}
WORKDIR ${APPDIR}
